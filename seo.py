# -*- coding: utf-8 -*-
"""
Mdm Ling Bakery · Mid-Autumn 2026 — the machine-readable layer.

Search engines and AI answer engines don't read the page the way a person does.
They read structured data. This module turns `data.py` into that structured
data, so the site tells a crawler exactly what a person sees: every keepsake,
every mooncake set, every flavour with its ingredients and allergens, every
booth with its dates, and the answers to the questions people actually ask.

Built from `data.py` on purpose. Same rule as the rest of the site: a card and
a schema entry can never disagree, because they come from one source.

Generates:
  · robots.txt   search + AI crawlers welcome, points at the sitemap
  · sitemap.xml  the page and the brochure
  · llms.txt     a plain-text summary of the whole collection
  · JSON-LD      injected into <head> by build_site.py

TWO RULES THIS FILE MUST KEEP
  1. No product prices. Brochure prices are retail, before whatever promo is
     running the week someone orders, so the site deliberately shows no dollar
     figure tied to a product. Offers here carry a URL and availability only.
     Store-wide policy numbers (free delivery threshold) are fine.
  2. Halal is per product, not blanket. The baked sets are Halal certified,
     the Snowskin Truffle set is not. `halal_of()` derives it from SETS so it
     can never drift from what the Gift Concierge filters on.
"""

import datetime
import json
import re

from data import (BOOTHS, CATEGORIES, FREE_DELIVERY, KEEPSAKES, SETS,
                  SITE_URL, WA_CUSTOMER)

SITE = SITE_URL.rstrip("/")
STORE = "https://www.mdmlingbakery.com"
IG = "https://www.instagram.com/mdmlingbakery/"
FB = "https://www.facebook.com/mdmlingbakery/"
TT = "https://www.tiktok.com/@mdmlingbakery"
ARTIST_IG = "https://www.instagram.com/theworldofying/"

ORG_ID = STORE + "/#organization"
SITE_ID = SITE + "/#website"
PAGE_ID = SITE + "/#webpage"

CAMPAIGN_EN = "A Bond in Lasting Bloom"
CAMPAIGN_CN = "花月情长"

BROCHURE = SITE + "/assets/mlb-midautumn-2026-brochure.pdf"

SET_HALAL = {s["id"]: s["halal"] for s in SETS}

MONTHS = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
          "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
YEAR = 2026


# ---------------------------------------------------------------- helpers
def plain(s):
    """Strip the inline markup out of a data.py body line."""
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).replace("&amp;", "&").strip()


def describe(k):
    """A keepsake's schema description: its first two body paragraphs."""
    return " ".join(plain(p) for p in k["body"][:2])


def halal_of(k):
    """Derived from the sets a keepsake takes, never hardcoded."""
    ss = k.get("sets") or []
    if not ss:
        return True                      # duo tins are traditional mooncakes
    return all(SET_HALAL[s] for s in ss)


def set_label(s):
    return "Set %s · %s" % (s["id"], s["group"])


def parse_dates(text):
    """'7 Sep - 25 Sep · weekdays only' -> ('2026-09-07', '2026-09-25', note)."""
    note = ""
    if "·" in text:
        text, note = [p.strip() for p in text.split("·", 1)]
    m = re.match(r"(\d{1,2})\s+(\w{3})\s*[–-]\s*(\d{1,2})\s+(\w{3})", text.strip())
    if not m:
        return None, None, (note or text.strip())
    d1, m1, d2, m2 = m.groups()
    if m1 not in MONTHS or m2 not in MONTHS:
        return None, None, (note or text.strip())
    start = datetime.date(YEAR, MONTHS[m1], int(d1)).isoformat()
    end = datetime.date(YEAR, MONTHS[m2], int(d2)).isoformat()
    return start, end, note


# ---------------------------------------------------------------- the graph
def build_graph(flav_index):
    g = []

    g.append({
        "@type": ["Organization", "Bakery"],
        "@id": ORG_ID,
        "name": "Mdm Ling Bakery",
        "url": STORE + "/",
        "image": SITE + "/assets/og-midautumn-2026-v3.jpg",
        "description": ("A Singapore bakery known for handcrafted cookies, mooncakes and "
                        "keepsake gift sets. Halal certified, with the exception of the "
                        "chilled snowskin range."),
        "telephone": "+65 8468 0201",
        "areaServed": {"@type": "Country", "name": "Singapore"},
        "sameAs": [STORE + "/", IG, FB, TT],
        "location": {
            "@type": "Place",
            "name": "Mdm Ling Bakery, Jewel Changi Airport",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "78 Airport Boulevard, #01-231, Level 1, Lobby H, Jewel Changi Airport",
                "addressLocality": "Singapore",
                "addressCountry": "SG",
            },
            "geo": {"@type": "GeoCoordinates", "latitude": 1.3602243, "longitude": 103.9896749},
        },
    })

    g.append({
        "@type": "WebSite", "@id": SITE_ID, "url": SITE + "/",
        "name": "Mdm Ling Bakery Mid-Autumn 2026",
        "inLanguage": "en-SG", "publisher": {"@id": ORG_ID},
    })

    g.append({
        "@type": ["WebPage", "CollectionPage"], "@id": PAGE_ID, "url": SITE + "/",
        "name": "Mdm Ling Bakery Mid-Autumn 2026 · %s %s" % (CAMPAIGN_CN, CAMPAIGN_EN),
        "isPartOf": {"@id": SITE_ID}, "about": {"@id": ORG_ID}, "inLanguage": "en-SG",
        "primaryImageOfPage": SITE + "/assets/og-midautumn-2026-v3.jpg",
        "description": ("The full Mdm Ling Bakery Mid-Autumn 2026 collection: %d keepsake gift "
                        "sets, %d mooncake set combinations and %d flavours, with a gift matcher "
                        "and every booth location." % (len(KEEPSAKES), len(SETS), len(flav_index))),
    })

    # --- the keepsakes, the heart of the collection
    kept = []
    for k in KEEPSAKES:
        kid = "%s/#%s" % (SITE, k["id"])
        kept.append((kid, k["name"]))
        halal = halal_of(k)
        props = [
            {"@type": "PropertyValue", "name": "Format", "value": k["format"]},
            {"@type": "PropertyValue", "name": "Mooncakes included", "value": k["pcs"]},
            {"@type": "PropertyValue", "name": "Chinese name",
             "value": "%s (%s) — %s" % (k["cn"], k["pinyin"], k["gloss"])},
            {"@type": "PropertyValue", "name": "Halal certification",
             "value": "Halal certified" if halal
                      else "Not Halal certified. Vegetarian, with no pork and no lard."},
            {"@type": "PropertyValue", "name": "Where to buy",
             "value": ("Order online at mdmlingbakery.com" if k["channel"] == "online"
                       else "Available at our Mid-Autumn booths, not sold online")},
            {"@type": "PropertyValue", "name": "After the season", "value": k["becomes"]},
        ]
        if k.get("variant"):
            props.append({"@type": "PropertyValue", "name": "Colour", "value": k["variant"]})
        if k.get("bcf"):
            props.append({"@type": "PropertyValue", "name": "Supports",
                          "value": "$1 from every purchase goes to the Breast Cancer Foundation"})
        if k.get("artist"):
            props.append({"@type": "PropertyValue", "name": "Artwork",
                          "value": "Painted by Singaporean artist Phuay Li Ying"})
        if k.get("sets"):
            props.append({"@type": "PropertyValue", "name": "Mooncake sets available",
                          "value": ", ".join(k["sets"])})
        if k.get("disclaimer"):
            props.append({"@type": "PropertyValue", "name": "Please note",
                          "value": plain(k["disclaimer"])})

        node = {
            "@type": "Product", "@id": kid,
            "name": k["name"], "alternateName": k["cn"],
            "description": describe(k),
            "image": "%s/assets/%s" % (SITE, k["img"]),
            "url": kid,
            "category": "Mid-Autumn mooncake gift set",
            "brand": {"@id": ORG_ID},
            "additionalProperty": props,
        }
        # Deliberately no price. See the module docstring.
        if k["channel"] == "online" and k.get("url"):
            node["offers"] = {
                "@type": "Offer", "url": k["url"],
                "availability": "https://schema.org/InStock",
                "seller": {"@id": ORG_ID},
                "areaServed": {"@type": "Country", "name": "Singapore"},
            }
        g.append(node)

    g.append({
        "@type": "ItemList", "@id": SITE + "/#keepsakes",
        "name": "Mdm Ling Bakery Mid-Autumn 2026 keepsake gift sets",
        "numberOfItems": len(kept),
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": {"@id": u}}
                            for i, (u, n) in enumerate(kept)],
    })

    # --- the mooncake flavours, with ingredients and allergens
    for f in flav_index:
        fid = "%s/#%s" % (SITE, f["slug"])
        props = [
            {"@type": "PropertyValue", "name": "Range", "value": f.get("range", "")},
            {"@type": "PropertyValue", "name": "Ingredients", "value": plain(f.get("ing", ""))},
        ]
        if f.get("algs"):
            props.append({"@type": "PropertyValue", "name": "Allergen advice, contains",
                          "value": ", ".join(f["algs"])})
        if f.get("trace"):
            props.append({"@type": "PropertyValue", "name": "Allergen advice, may contain",
                          "value": plain(f["trace"])})
        for cls, label in f.get("badges", []):
            props.append({"@type": "PropertyValue", "name": "Badge", "value": label})
        g.append({
            "@type": "Product", "@id": fid,
            "name": f["name"], "description": plain(f.get("story", "")),
            "image": "%s/assets/%s" % (SITE, f["img"]),
            "url": fid, "category": "Mooncake",
            "brand": {"@id": ORG_ID},
            "additionalProperty": [p for p in props if p["value"]],
        })

    # --- the seven lettered sets, choices within a keepsake rather than
    #     products you can buy on their own
    g.append({
        "@type": "ItemList", "@id": SITE + "/#mooncake-sets",
        "name": "Mooncake set combinations",
        "description": ("Every keepsake takes a lettered mooncake set. Sets A to F are baked and "
                        "Halal certified; Set G is the chilled Snowskin Truffle set and is not "
                        "Halal certified."),
        "numberOfItems": len(SETS),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": set_label(s),
             "description": "%s. %s" % (
                 "; ".join(s["flavours"]),
                 "Halal certified." if s["halal"] else "Not Halal certified.")}
            for i, s in enumerate(SETS)],
    })

    # --- where to buy: the dated fairs are sale events, the flagship is a shop
    for name, level, flagship, lat, lng, dates in BOOTHS:
        place = {
            "@type": "Place", "name": "%s, %s" % (name, level),
            "address": {"@type": "PostalAddress", "addressLocality": "Singapore",
                        "addressCountry": "SG", "streetAddress": "%s, %s" % (name, level)},
            "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng},
        }
        start, end, note = parse_dates(dates)
        if not start:
            continue                     # the flagship shop, already on the Organization
        ev = {
            "@type": "SaleEvent",
            "@id": "%s/#booth-%s" % (SITE, re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")),
            "name": "Mdm Ling Bakery Mid-Autumn mooncake fair · %s" % name,
            "description": ("Mdm Ling Bakery Mid-Autumn 2026 mooncakes and keepsake gift sets, "
                            "at our booth in %s%s." % (name, ", " + note if note else "")),
            "startDate": start, "endDate": end,
            "eventStatus": "https://schema.org/EventScheduled",
            "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "location": place,
            "organizer": {"@id": ORG_ID},
            "image": SITE + "/assets/og-midautumn-2026-v3.jpg",
            "url": SITE + "/#where",
        }
        g.append(ev)

    # --- the questions people actually ask
    online = [k["name"] for k in KEEPSAKES if k["channel"] == "online"]
    booth = [k["name"] for k in KEEPSAKES if k["channel"] == "booth"]
    dated = [(n, d) for n, _l, _f, _a, _g, d in BOOTHS]
    faqs = [
        ("What is in the Mdm Ling Bakery Mid-Autumn 2026 collection?",
         "%d keepsake gift sets across %d families, each pairing packaging made to be kept with a "
         "choice of mooncake set. The collection is called %s, %s. Packaging ranges from leather "
         "bags and totes to heritage tins, a drawer chest, a scroll box and a serving turntable."
         % (len(KEEPSAKES), len(CATEGORIES), CAMPAIGN_CN, CAMPAIGN_EN)),
        ("Are Mdm Ling Bakery mooncakes Halal certified?",
         "The baked mooncakes are Halal certified. The Premium Truffle Snowskin range, Set G, is "
         "not Halal certified; it is vegetarian and made with no pork and no lard. Orchid Reverie "
         "is the keepsake that carries the snowskin set, so it is the one exception in the "
         "collection."),
        ("Which gift sets can I order online and which are only at the booths?",
         "Order online at mdmlingbakery.com: %s. Available only at our Mid-Autumn booths: %s."
         % ("; ".join(online), "; ".join(booth))),
        ("Where can I buy Mdm Ling Bakery mooncakes in Singapore?",
         "At %d Mid-Autumn booths across the island, plus our shop at Jewel Changi Airport which "
         "is open daily. Booth dates: %s. Everything sold online is at mdmlingbakery.com."
         % (len(BOOTHS), "; ".join("%s, %s" % (n, d) for n, d in dated))),
        ("What mooncake flavours does Mdm Ling Bakery have for 2026?",
         "%d flavours across three ranges. %s" % (
             len(flav_index), "; ".join(f["name"] for f in flav_index))),
        ("Is there free delivery?",
         "Yes, on orders above $%d within Singapore, from mdmlingbakery.com." % FREE_DELIVERY),
        ("Who painted The Painted Garden artwork?",
         "Singaporean artist Phuay Li Ying, who goes by The World of Ying. She painted it from her "
         "own childhood Mid-Autumn family gatherings. There is no single big flower in it, only "
         "wildflowers in full open bloom, many small flowers coming together into one picture, the "
         "way people from all walks of life do when they gather."),
        ("Does any of the collection support a charity?",
         "Yes. $1 from every Painted Garden Box goes to the Breast Cancer Foundation, supporting "
         "breast cancer awareness, screening and survivor care in Singapore."),
        ("What does 花月情长 mean?",
         "花月情长, huā yuè qíng cháng, is the name of the 2026 collection. In English we render it "
         "as %s. Flowers and moon pass, affection lasts, which is the idea behind packaging built "
         "to outlive the season." % CAMPAIGN_EN),
        ("How do I choose a Mid-Autumn gift?",
         "The site has a Gift Matcher. Four questions about who you are gifting, what matters most, "
         "what their table is like and how much of a moment it should be, and it returns one match "
         "and a runner-up with a recommended mooncake set. Halal certification and budget act as "
         "hard filters, so a match will never contradict what you asked for."),
    ]
    g.append({
        "@type": "FAQPage", "@id": SITE + "/#faq", "isPartOf": {"@id": PAGE_ID},
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    })

    return {"@context": "https://schema.org", "@graph": g}


def jsonld_block(flav_index):
    """The <script> tag build_site.py drops into <head>."""
    graph = build_graph(flav_index)
    return ('<script type="application/ld+json">\n%s\n</script>'
            % json.dumps(graph, ensure_ascii=False, indent=1))


# ------------------------------------------------------------- flat files
ROBOTS = """# midautumn2026.mdmlingbakery.com — Mdm Ling Bakery Mid-Autumn 2026
# A public product catalogue. Search and AI crawlers welcome.

User-agent: *
Allow: /

# Search engines
User-agent: Googlebot
Allow: /
User-agent: Googlebot-Image
Allow: /
User-agent: Bingbot
Allow: /
User-agent: DuckDuckBot
Allow: /

# AI answer engines
User-agent: Google-Extended
Allow: /
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Perplexity-User
Allow: /
User-agent: Applebot
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: Amazonbot
Allow: /
User-agent: meta-externalagent
Allow: /
User-agent: FacebookBot
Allow: /
User-agent: Bytespider
Allow: /
User-agent: cohere-ai
Allow: /
User-agent: DuckAssistBot
Allow: /
User-agent: YouBot
Allow: /

Sitemap: {site}/sitemap.xml
""".format(site=SITE)


def sitemap_xml(lastmod):
    rows = [(SITE + "/", "1.0", "weekly"), (BROCHURE, "0.5", "monthly")]
    body = "\n".join(
        "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
        "    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>"
        % (u, lastmod, cf, pr) for u, pr, cf in rows)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + body + "\n</urlset>\n")


def llms_txt(flav_index):
    L = [
        "# Mdm Ling Bakery — Mid-Autumn 2026",
        "",
        "> %s · %s. The complete Mid-Autumn 2026 collection from Mdm Ling Bakery, Singapore:"
        % (CAMPAIGN_CN, CAMPAIGN_EN),
        "> %d keepsake gift sets, %d mooncake set combinations and %d flavours."
        % (len(KEEPSAKES), len(SETS), len(flav_index)),
        "> The packaging is the point: every piece is made to be kept and used long after the season.",
        "",
        "## Key facts",
        "",
        "- The baked mooncakes are Halal certified. The Premium Truffle Snowskin range (Set G) is",
        "  NOT Halal certified; it is vegetarian, with no pork and no lard.",
        "- %d of the %d keepsakes can be ordered online at %s. The rest are sold only at our"
        % (sum(1 for k in KEEPSAKES if k["channel"] == "online"), len(KEEPSAKES), STORE),
        "  Mid-Autumn booths.",
        "- Free delivery within Singapore on orders above $%d." % FREE_DELIVERY,
        "- $1 from every Painted Garden Box goes to the Breast Cancer Foundation.",
        "- The Painted Garden artwork is by Singaporean artist Phuay Li Ying (@theworldofying).",
        "- Customer enquiries: +65 %s %s (WhatsApp)." % (WA_CUSTOMER[2:6], WA_CUSTOMER[6:]),
        "",
        "## Keepsake gift sets",
        "",
    ]
    for k in KEEPSAKES:
        where = ("order online at " + k["url"]) if k["channel"] == "online" \
            else "available at our Mid-Autumn booths only"
        L.append("- [%s](%s/#%s) — %s (%s), %s, %s. Halal: %s. After the season: %s. %s."
                 % (k["name"], SITE, k["id"], k["cn"], k["pinyin"], k["format"],
                    k["pcs"], "certified" if halal_of(k) else "not certified",
                    k["becomes"].rstrip("."), where))
    L += ["", "## Mooncake sets", ""]
    for s in SETS:
        L.append("- %s: %s. %s" % (set_label(s), "; ".join(s["flavours"]),
                                   "Halal certified." if s["halal"] else "Not Halal certified."))
    L += ["", "## Mooncake flavours", ""]
    for f in flav_index:
        L.append("- [%s](%s/#%s) — %s. Ingredients: %s"
                 % (f["name"], SITE, f["slug"], plain(f.get("story", "")), plain(f.get("ing", ""))))
    L += ["", "## Where to buy", ""]
    for name, level, flagship, _lat, _lng, dates in BOOTHS:
        L.append("- %s, %s — %s%s" % (name, level, dates, " (flagship shop)" if flagship else ""))
    L += [
        "",
        "## Elsewhere",
        "",
        "- [Mdm Ling Bakery online store](%s/)" % STORE,
        "- [E-brochure (PDF)](%s)" % BROCHURE,
        "- [Instagram](%s)" % IG,
        "",
    ]
    return "\n".join(L)


def write_files(here, flav_index):
    import os
    lastmod = datetime.date.today().isoformat()
    files = {
        "robots.txt": ROBOTS,
        "sitemap.xml": sitemap_xml(lastmod),
        "llms.txt": llms_txt(flav_index),
    }
    for name, body in files.items():
        with open(os.path.join(here, name), "w", encoding="utf-8") as f:
            f.write(body)
    return list(files)
