# -*- coding: utf-8 -*-
"""
Mdm Ling Bakery · Mid-Autumn 2026 microsite — single source of truth.

Every keepsake, price, channel and mooncake set lives here. The static HTML
cards, the Gift Concierge and the Build-Your-Gift tool are all generated from
this one structure, so a result and a card can never disagree.

Prices and set definitions are taken from the official 2026 e-brochure
(assets/mlb-midautumn-2026-brochure.pdf, page 5). Online availability and
product URLs are taken from the live WooCommerce catalogue on
mdmlingbakery.com, checked 3 Aug 2026.
"""

WA_CUSTOMER = "6584680201"      # general customer service
FREE_DELIVERY = 100

SITE_URL = "https://kiensieng.github.io/mlb-mooncake-2026-9536f369736f98c6/"
GA_ID = "G-MD1H486BMD"

# --------------------------------------------------------------------------
# MOONCAKE SETS — brochure page 5, "Step 2"
# --------------------------------------------------------------------------
SETS = [
    {"id": "A", "group": "Traditional", "halal": True,
     "flavours": ["4 × Lotus with Melon Seeds and Yolk"]},
    {"id": "B", "group": "Traditional", "halal": True,
     "flavours": ["4 × Lotus with Melon Seeds"]},
    {"id": "C", "group": "Traditional", "halal": True,
     "flavours": ["2 × Lotus with Melon Seeds and Yolk", "2 × Lotus with Melon Seeds"]},
    {"id": "D", "group": "Signature", "halal": True,
     "flavours": ["1 × Black Sesame Peanut Butter", "1 × Red Dates Longan",
                  "1 × Belgian Double Chocolate", "1 × Emerald Pandan Golden Yolk"]},
    {"id": "E", "group": "Signature & Traditional", "halal": True,
     "flavours": ["1 × Lotus with Melon Seeds and Yolk", "1 × Lotus with Melon Seeds",
                  "1 × Black Sesame Peanut Butter", "1 × Red Dates Longan"]},
    {"id": "F", "group": "Signature & Traditional", "halal": True,
     "flavours": ["1 × Lotus with Melon Seeds and Yolk", "1 × Lotus with Melon Seeds",
                  "1 × Belgian Double Chocolate", "1 × Emerald Pandan Golden Yolk"]},
    {"id": "G", "group": "Snowskin Truffle", "halal": False,
     "flavours": ["2 × Truffle Popping Candy", "2 × Truffle Pistachio Kunafa",
                  "2 × Truffle Muscat Grape", "2 × Truffle Passionfruit"]},
]

BAKED_SETS = ["A", "B", "C", "D", "E", "F"]

# --------------------------------------------------------------------------
# KEEPSAKES — the heart of the collection, packaging first
#
# channel : "online" = live on mdmlingbakery.com  ·  "booth" = at our booths
# sets    : which lettered mooncake sets this keepsake takes ([] = fixed 2 pc)
# score   : Gift Concierge weights, 0-3, across recipient and priority axes
# --------------------------------------------------------------------------
KEEPSAKES = [
    {
        "id": "the-dawn", "name": "The Dawn", "cn": "花晨",
        "pinyin": "huā chén", "gloss": "flower morning",
        "format": "Leather Gift Bag", "pcs": "4 pcs", "price": 92,
        "img": "the-dawn.webp",
        "alt": "The Dawn cream leather Mid-Autumn gift bag by Mdm Ling Bakery",
        "channel": "online",
        "url": "https://www.mdmlingbakery.com/products/the-dawn-bag-traditional-assorted-mooncakes/",
        "sets": BAKED_SETS,
        "becomes": "A cream leather bag carried on ordinary days, long after the season.",
        "why": "it's a bag someone actually wears, not a box they feel guilty throwing out.",
        "body": [
            "Soft as first light, The Dawn is a <strong>cream leather bag</strong> made to be <strong>carried long after the celebration ends</strong>.",
            "Its gentle, neutral tone and supple finish move easily from a festive visit to <strong>everyday wear</strong>, a quiet kind of luxury that never asks for attention.",
            "Its name comes from the old idiom <strong>花晨月夕</strong>, flower mornings and moonlit evenings, the two loveliest hours of any day. We split it across a pair of bags: The Dawn is <strong>花晨</strong>, the morning the flowers open, in cream like first light.",
            "Designed as a <strong>keepsake rather than a wrapper</strong>, The Dawn turns a Mid-Autumn gift into something kept, used and remembered for years to come. <strong>Pair it with The Dusk</strong>, its warmer companion, for two halves of the same day.",
        ],
        "score": {"family": 2, "friend": 3, "colleagues": 2, "clients": 2, "traveller": 3,
                  "keep": 3, "story": 2, "favourite": 1, "impress": 2},
    },
    {
        "id": "the-dusk", "name": "The Dusk", "cn": "月夕",
        "pinyin": "yuè xī", "gloss": "moonlit evening",
        "format": "Leather Gift Bag", "pcs": "4 pcs", "price": 92,
        "img": "the-dusk.webp",
        "alt": "The Dusk terracotta leather Mid-Autumn gift bag by Mdm Ling Bakery",
        "channel": "online",
        "url": "https://www.mdmlingbakery.com/products/the-dusk-bag-traditional-assorted-mooncakes/",
        "sets": BAKED_SETS,
        "becomes": "A terracotta bag that carries a weekend as easily as a celebration.",
        "why": "the colour has enough warmth for the occasion and enough restraint for a Tuesday.",
        "body": [
            "Warm as the last hour of daylight, The Dusk is a <strong>terracotta leather bag</strong> with a richer, deeper character than its cream counterpart.",
            "Its earthy, sunset tone carries a sense of occasion while staying <strong>wearable well beyond the season</strong>, as at home with a weekend coat as with a celebration.",
            "The Dusk is <strong>月夕</strong>, the moonlit evening from the idiom <strong>花晨月夕</strong>, the other of the day's two loveliest hours. Where The Dawn wears first light, The Dusk wears the last of it, and together the pair <strong>bookend the day the way family bookends a life</strong>.",
            "<strong>More heirloom than packaging</strong>, The Dusk lets your Mid-Autumn gift live on as a bag that's reached for again and again. <strong>The natural other half to The Dawn.</strong>",
        ],
        "score": {"family": 2, "friend": 3, "colleagues": 2, "clients": 2, "traveller": 3,
                  "keep": 3, "story": 2, "favourite": 1, "impress": 2},
    },
    {
        "id": "the-painted-garden", "name": "The Painted Garden", "cn": "百花迎月",
        "pinyin": "bǎi huā yíng yuè", "gloss": "a hundred flowers rising to greet the moon",
        "format": "Heritage Tin", "pcs": "4 pcs", "price": 78,
        "img": "painted-garden-tin.webp",
        "alt": "The Painted Garden 4 piece watercolour floral keepsake mooncake tin",
        "channel": "online",
        "url": "https://www.mdmlingbakery.com/products/the-painted-garden-traditional-assorted-mooncakes/",
        "sets": BAKED_SETS,
        "becomes": "A tin for keepsakes, trinkets and the small things worth saving.",
        "why": "there's a real artist and a real story behind the artwork, which gives you something to say when you hand it over.",
        "artist": True,
        "body": [
            "The Painted Garden is a <strong>metal keepsake tin</strong> dressed in soft watercolour blooms by <strong>Singaporean artist Phuay Li Ying</strong>, the kind of pastel garden that feels like spring held still.",
            "Ying painted the garden as a <strong>quiet portrait of Mdm Ling herself</strong>. The central bloom is her, and the smaller flowers are the people she gathers around her, <strong>wildflowers of many colours and origins rising together to greet the festival moon</strong>.",
            "Every petal is washed in gentle pinks, lilacs and gold, a celebration of nature at its most tender, finished with a quiet glow of <strong>foil</strong>.",
            "<strong>Sustainably designed to be kept and reused</strong> long after Mid-Autumn, the tin finds a second life holding keepsakes, trinkets and the small things worth saving. A Mid-Autumn gift set for <strong>family, friends and clients</strong> that stays on the shelf.",
        ],
        "score": {"family": 3, "friend": 3, "colleagues": 3, "clients": 3, "traveller": 2,
                  "keep": 2, "story": 3, "favourite": 2, "impress": 2},
    },
    {
        "id": "the-painted-garden-duo", "name": "The Painted Garden Duo", "cn": "百花迎月",
        "pinyin": "bǎi huā yíng yuè", "gloss": "a hundred flowers rising to greet the moon",
        "format": "Duo Tin", "pcs": "2 pcs", "price": 48,
        "img": "painted-garden-duo.webp",
        "alt": "The Painted Garden 2 piece duo watercolour floral mooncake tin",
        "channel": "online",
        "url": "https://www.mdmlingbakery.com/products/the-painted-garden-duo-2pc-traditional-mooncakes/",
        "sets": [], "duo_note": "Traditional mooncakes, two pieces.",
        "becomes": "A slim tin that finds a home on a desk or a dressing table.",
        "why": "a smaller gesture that still arrives looking considered, which is the hard part.",
        "artist": True,
        "body": [
            "The Painted Garden in a <strong>slimmer form</strong>, carrying the same soft watercolour blooms by <strong>Singaporean artist Phuay Li Ying</strong> in a size made for <strong>lighter, thoughtful gifting</strong>.",
            "Look closely and you'll find Ying's story in miniature: the central bloom is <strong>Mdm Ling herself</strong>, ringed by the people she gathers around her.",
            "Ideal for a <strong>smaller gesture that still feels considered</strong>, it's an easy way to wish someone well this Mid-Autumn.",
            "Like its larger companion, the tin is made to be <strong>kept and reused</strong> long after the season passes. \U0001F315",
        ],
        "score": {"family": 1, "friend": 3, "colleagues": 3, "clients": 2, "traveller": 2,
                  "keep": 2, "story": 3, "favourite": 1, "impress": 1},
    },
    {
        "id": "the-painted-garden-box", "name": "The Painted Garden Box", "cn": "百花迎月",
        "pinyin": "bǎi huā yíng yuè", "gloss": "a hundred flowers rising to greet the moon",
        "format": "Gift Box", "pcs": "4 pcs", "price": 88,
        "img": "painted-garden-box.webp",
        "alt": "The Painted Garden Box watercolour floral Mid-Autumn gift box by Mdm Ling Bakery",
        "channel": "online",
        "url": "https://www.mdmlingbakery.com/products/the-painted-garden-box-traditional-assorted-mooncakes/",
        "sets": BAKED_SETS,
        "becomes": "A silk-paper box that keeps letters and photographs safe.",
        "why": "every one bought sends $1 to the Breast Cancer Foundation, so the gesture reaches past the table.",
        "artist": True, "bcf": True,
        "body": [
            "The Painted Garden features artwork by <strong>Singaporean artist Phuay Li Ying</strong> and arrives in a beautifully designed box, dressed in soft watercolour blooms printed on <strong>silk paper</strong> for an <strong>elegant, artisanal finish</strong>, the kind of pastel garden that feels like spring held still.",
            "Every petal is washed in gentle pinks, lilacs and gold, a celebration of nature at its most tender, finished with a quiet glow of <strong>foil</strong>.",
            "<strong>Thoughtfully designed for sustainable keeping and reuse</strong> long after Mid-Autumn, the box finds a second life storing keepsakes, trinkets and the small things worth saving. A Mid-Autumn gift set for <strong>family, friends and clients</strong> that stays on the shelf.",
            "This Mid-Autumn Festival, let your celebration carry further. With every purchase of The Painted Garden Box, <strong>we'll donate $1 to the Breast Cancer Foundation</strong>, supporting breast cancer awareness, screening and survivor care in Singapore. Each garden you give helps look after someone else's: <strong>care, passed along twice in one gift</strong>.",
        ],
        "score": {"family": 2, "friend": 2, "colleagues": 3, "clients": 3, "traveller": 3,
                  "keep": 2, "story": 3, "favourite": 2, "impress": 2},
    },
    {
        "id": "a-court-of-peonies", "name": "A Court of Peonies", "cn": "花好月圆",
        "pinyin": "huā hǎo yuè yuán", "gloss": "flowers in bloom beneath a full moon",
        "format": "Heritage Tin", "pcs": "4 pcs", "price": 78,
        "img": "court-peonies-tin.webp",
        "alt": "A Court of Peonies 4 piece navy floral keepsake mooncake tin",
        "channel": "online",
        "url": "https://www.mdmlingbakery.com/products/a-court-of-peonies-traditional-assorted-mooncakes/",
        "sets": BAKED_SETS,
        "becomes": "A navy tin that holds tea, biscuits or letters just as well.",
        "why": "花好月圆 is the blessing spoken at every reunion table, so the name does half the talking for you.",
        "body": [
            "Named for the classic wish of <strong>reunion and togetherness</strong>, A Court of Peonies is a <strong>metal keepsake tin</strong> set against <strong>deep navy</strong>, where bold, painterly peonies bloom in jewel tones of coral, magenta and teal.",
            "The peony has long stood for <strong>honour, grace and prosperity</strong>, making this a gift that carries good meaning as much as good looks. <strong>Where The Painted Garden whispers, A Court of Peonies sings.</strong> 花好月圆 is the blessing spoken at every reunion table; <strong>give this tin and you're saying it out loud</strong>.",
            "<strong>Sustainably designed to be reused</strong> long after Mid-Autumn, it's a striking gift set for family, friends and <strong>corporate gifting</strong> alike.",
        ],
        "score": {"family": 3, "friend": 2, "colleagues": 3, "clients": 3, "traveller": 2,
                  "keep": 2, "story": 3, "favourite": 2, "impress": 3},
    },
    {
        "id": "a-court-of-peonies-duo", "name": "A Court of Peonies Duo", "cn": "花好月圆",
        "pinyin": "huā hǎo yuè yuán", "gloss": "flowers in bloom beneath a full moon",
        "format": "Duo Tin", "pcs": "2 pcs", "price": 48,
        "img": "court-peonies-duo.webp",
        "alt": "A Court of Peonies 2 piece duo sage floral mooncake tin",
        "channel": "online",
        "url": "https://www.mdmlingbakery.com/products/court-of-peonies-duo-2pc-traditional-mooncakes/",
        "sets": [], "duo_note": "Traditional mooncakes, two pieces.",
        "becomes": "A sage tin small enough for a shelf, sturdy enough to keep.",
        "why": "it carries the same good wishes as its bigger sister at a size you can give widely.",
        "body": [
            "The same bold peonies in a <strong>slimmer keepsake tin</strong>, made for <strong>lighter Mid-Autumn gifting</strong> without losing any of their presence.",
            "Set against a <strong>soft sage</strong> ground with the collection's signature blooms, it's a smaller gesture that still speaks of <strong>honour and good wishes</strong>.",
            "Built to be <strong>kept and reused</strong>, it carries the season well beyond the festival.",
        ],
        "score": {"family": 1, "friend": 3, "colleagues": 3, "clients": 2, "traveller": 2,
                  "keep": 2, "story": 2, "favourite": 1, "impress": 1},
    },
    {
        "id": "blossom-drawer-chest", "name": "Blossom Drawer Chest", "cn": "花间藏月",
        "pinyin": "huā jiān cáng yuè", "gloss": "a moon treasured among the flowers",
        "format": "Keepsake Chest", "pcs": "4 pcs", "price": 118,
        "img": "blossom-drawer.webp",
        "alt": "Blossom Drawer Chest pink keepsake box with working drawer",
        "channel": "online",
        "url": "https://www.mdmlingbakery.com/products/blossom-drawer-chest-traditional-assorted-mooncakes/",
        "sets": BAKED_SETS,
        "becomes": "A drawer for jewellery and the little treasures that deserve a home.",
        "why": "it's furniture, not packaging, so it stays on the dressing table for years.",
        "body": [
            "<strong>More furniture than packaging</strong>, the Blossom Drawer Chest is a keepsake box with a <strong>working drawer</strong>, finished in soft blush pink with an <strong>embossed floral motif</strong>.",
            "The name tells you how it gives: <strong>花间藏月, a moon hidden among the flowers</strong>. Pull the drawer and there they are, four mooncakes resting inside like a secret, <strong>kept tucked away for the moment you choose to reveal it</strong>.",
            "Then keep the chest for everything after. The drawer is made for <strong>jewellery, keepsakes and the little treasures</strong> that deserve a home.",
            "A Mid-Autumn gift set that doubles as a <strong>lasting piece for the dressing table</strong>, thoughtful enough for <strong>someone you'd really like to impress</strong>.",
        ],
        "score": {"family": 3, "friend": 2, "colleagues": 2, "clients": 3, "traveller": 1,
                  "keep": 3, "story": 2, "favourite": 2, "impress": 3},
    },
    {
        "id": "orchid-reverie", "name": "Orchid Reverie", "cn": "幽兰伴月",
        "pinyin": "yōu lán bàn yuè", "gloss": "a quiet orchid keeping the moon company",
        "format": "Snowskin Keepsake Tin", "pcs": "8 pcs", "price": 88,
        "img": "orchid-reverie.webp",
        "alt": "Orchid Reverie keepsake tin with snowskin mooncakes cut open to show their truffle centres",
        "channel": "online",
        "url": "https://www.mdmlingbakery.com/products/orchid-reverie-tin-8pcs-snow-skin-mooncakes/",
        "sets": ["G"],
        "becomes": "A tin that keeps biscuits, tea or letters as happily as mooncakes.",
        "why": "eight pieces, two of each flavour, so nobody at the table has to settle.",
        "note": "Not Halal certified. Vegetarian, with no pork and no lard.",
        "body": [
            "Orchid Reverie is a <strong>square metal keepsake tin</strong> painted with orchids in full bloom, in watercolour pinks, corals and gold.",
            "Inside sit <strong>eight snowskin mooncakes, two of each of our four truffle flavours</strong>, so nobody at the table has to settle for one. Serve them chilled and let everyone find their favourite.",
            "The orchid earns its place here. Singapore's <strong>national flower</strong> is an orchid, and it's a bloom that opens slowly and <strong>holds its flower for months</strong>, which is exactly what we hope a Mid-Autumn gift does for the people who receive it.",
            "Its name, <strong>幽兰伴月</strong>, sets that quiet orchid beside the moon and leaves the two to keep each other company. <strong>伴 means to accompany</strong>, and that's the whole point of a gift like this, <strong>company that outlasts the evening</strong>.",
            "Designed to be <strong>refilled and reused long after the season</strong>, the tin keeps biscuits, tea or letters just as happily as it keeps mooncakes. <strong>Our most asked for snowskin range, in the tin made for it.</strong>",
        ],
        "score": {"family": 3, "friend": 2, "colleagues": 2, "clients": 1, "traveller": 0,
                  "keep": 2, "story": 2, "favourite": 3, "impress": 2},
    },
    {
        "id": "weaving-moments", "name": "Weaving Moments", "cn": "丝丝情长",
        "pinyin": "sī sī qíng cháng", "gloss": "every thread, a lasting bond",
        "format": "Woven Bag", "pcs": "4 pcs", "price": 92,
        "img": "weaving-moments.webp",
        "alt": "Weaving Moments woven leather Mid-Autumn gift bag",
        "channel": "booth", "sets": BAKED_SETS,
        "becomes": "A woven bag that goes to market, to work and to dinner.",
        "why": "the weave is the message, every strand holding another, which is a rare thing to be able to point at.",
        "body": [
            "Look closely at the <strong>woven texture</strong>: every strand crosses another, holds it, and is held in return. That's how the bonds we treasure are made too, <strong>moment over moment, year over year</strong>.",
            "Its name, <strong>丝丝情长</strong>, borrows 情长 straight from the collection itself, because this bag is the collection's idea made touchable: <strong>affection, woven to last</strong>.",
            "<strong>Sustainably designed as a thoughtful keepsake</strong>, this stylish bag is an invitation to cherish meaningful moments and carry them with you.",
        ],
        "score": {"family": 2, "friend": 3, "colleagues": 2, "clients": 2, "traveller": 3,
                  "keep": 3, "story": 3, "favourite": 1, "impress": 2},
    },
    {
        "id": "tote-of-good-health", "name": "Tote of Good Health", "cn": "月满安康",
        "pinyin": "yuè mǎn ān kāng", "gloss": "a full moon, lasting wellness",
        "variant": "Fuchsia",
        "format": "Leather Tote", "pcs": "4 pcs", "price": 88,
        "img": "tote-fuchsia.webp",
        "alt": "Tote of Good Health fuchsia leather tote Mid-Autumn gift bag",
        "channel": "booth", "sets": BAKED_SETS,
        "becomes": "A structured fuchsia tote worn well past the festival.",
        "why": "of everything we wish the people we love, health comes first, and the name says exactly that.",
        "body": [
            "Bold, bright and impossible to ignore, the Tote of Good Health arrives in a <strong>vivid fuchsia</strong>, finished with a <strong>printed scarf</strong> tied at the handle.",
            "Its structured silhouette and confident colour make it a <strong>leather tote built to be worn long after Mid-Autumn</strong>, a daily reminder of the care behind the gift.",
            "Of all the things we wish the people we love, <strong>health comes first</strong>, and the name says it in four characters: <strong>月满安康, when the moon is full, may you be well</strong>. For parents, grandparents and the people whose wellbeing you think about daily.",
            "<strong>Sustainably designed as a keepsake</strong>, this gift set turns a simple visit into something that stays, and carries that wish into the year ahead.",
        ],
        "score": {"family": 3, "friend": 2, "colleagues": 1, "clients": 1, "traveller": 2,
                  "keep": 3, "story": 3, "favourite": 1, "impress": 2},
    },
    {
        "id": "tote-of-bliss", "name": "Tote of Bliss", "cn": "花开喜乐",
        "pinyin": "huā kāi xǐ lè", "gloss": "blooms open, joy follows",
        "variant": "Green",
        "format": "Leather Tote", "pcs": "4 pcs", "price": 88,
        "img": "tote-green.webp",
        "alt": "Tote of Bliss green leather tote Mid-Autumn gift bag",
        "channel": "booth", "sets": BAKED_SETS,
        "becomes": "A jade green tote that dresses up or down without trying.",
        "why": "it unfolds in stages, bag then scarf then mooncakes, so the giving lasts longer than the handover.",
        "body": [
            "Cool, composed and effortlessly chic, the Tote of Bliss arrives in a <strong>fresh jade green</strong>, finished with a <strong>printed scarf</strong> knotted at the handle.",
            "Its clean, structured silhouette makes it a <strong>leather tote you'll reach for long after the season</strong>, dressed up or down with ease.",
            "The name promises that <strong>when flowers open, joy follows</strong>, and that's exactly how this tote gives: first the bag, then the scarf, then the mooncakes, <strong>one happiness unfolding after another</strong>.",
            "<strong>Sustainably designed as a keepsake</strong>, this Mid-Autumn gift set lets a little of the celebration's calm travel with you wherever you go.",
        ],
        "score": {"family": 2, "friend": 3, "colleagues": 2, "clients": 1, "traveller": 3,
                  "keep": 3, "story": 2, "favourite": 1, "impress": 2},
    },
    {
        "id": "treasure-scroll", "name": "Treasure Scroll", "cn": "花月长卷",
        "pinyin": "huā yuè cháng juǎn", "gloss": "an unrolling scroll of flowers and moonlight",
        "variant": "Rose Pink",
        "format": "Scroll Box", "pcs": "4 pcs", "price": 88,
        "img": "treasure-scroll.webp",
        "alt": "Treasure Scroll Rose Pink long gift box by Mdm Ling Bakery",
        "channel": "booth", "sets": BAKED_SETS,
        "becomes": "A long box for prints, papers and things too precious to fold.",
        "why": "it opens scene by scene rather than all at once, which turns the handover into a moment.",
        "body": [
            "Scrolls once carried the things <strong>too precious to fold</strong>: paintings, letters, promises. The Treasure Scroll opens the same way, unrolling to reveal its mooncakes <strong>scene by scene</strong>.",
            "Adorned in a <strong>luminous rose pink</strong> with <strong>sage green accents</strong>, its name echoes the collection itself: 花月情长 says affection lasts long, and <strong>花月长卷 gives that affection a shape, a long scroll that keeps unrolling</strong>.",
            "Whether for <strong>family, friends or clients</strong>, it leaves a <strong>lasting impression</strong> long after the treats are enjoyed. <strong>Some gifts are opened. This one is unveiled.</strong> \U0001F315",
        ],
        "score": {"family": 2, "friend": 2, "colleagues": 3, "clients": 3, "traveller": 1,
                  "keep": 2, "story": 3, "favourite": 1, "impress": 3},
    },
    {
        "id": "elegance-reunion-turntable", "name": "Elegance Reunion Turntable", "cn": "花月同席",
        "pinyin": "huā yuè tóng xí", "gloss": "flowers and moon at the same table",
        "format": "Serving Turntable", "pcs": "4 pcs", "price": 118,
        "img": "elegance-turntable.webp",
        "alt": "Elegance Reunion Turntable, a round floral serving turntable by Mdm Ling Bakery",
        "channel": "booth", "sets": BAKED_SETS,
        "becomes": "A serving turntable that comes back out at every reunion dinner.",
        "why": "it's the one keepsake that earns a place at the table itself, not just on a shelf.",
        "note": "Available in several designs. Ask at any of our booths for what's in stock.",
        "disclaimer": "Images are for illustration purposes only. The turntable comes in several designs, so please check with our retail points for the designs currently available. \U0001F315",
        "body": [
            "A <strong>round serving turntable</strong> printed with a painted garden of peonies, roses and trailing greens, rimmed in gold.",
            "Set it at the centre of the table and everything comes round to everyone. That's the whole idea: <strong>nobody reaches, nobody misses out</strong>, which is what a reunion dinner is supposed to feel like.",
            "Its name, <strong>花月同席</strong>, puts the flowers and the moon at the <strong>same table</strong>. 席 is the banquet seat, the place kept for you, and that's the wish this one carries.",
            "Long after Mid-Autumn it <strong>stays in service</strong>, carrying tea, fruit and whatever the next gathering needs. <strong>The gift that keeps getting used in front of you.</strong>",
        ],
        "score": {"family": 3, "friend": 1, "colleagues": 1, "clients": 2, "traveller": 0,
                  "keep": 3, "story": 2, "favourite": 3, "impress": 3},
    },
]

# --------------------------------------------------------------------------
# CATEGORIES — the keepsakes are browsed as six families. Each category
# renders as a thumbnail overview plus one product on stage at a time,
# switched by tapping a thumbnail or the prev/next arrows.
# --------------------------------------------------------------------------
CATEGORIES = [
    {"id": "painted-garden", "name": "The Painted Garden",
     "sub": "Artist edition",
     "blurb": "Soft watercolour blooms by Singaporean artist <a href=\"#garden\">Phuay Li Ying</a>, across a silk paper gift box, a heritage tin and a slim duo tin.",
     "items": ["the-painted-garden-box", "the-painted-garden", "the-painted-garden-duo"]},
    {"id": "court-of-peonies", "name": "A Court of Peonies",
     "sub": "Heritage tins",
     "blurb": "Bold painterly peonies in jewel tones, on a deep navy heritage tin and a soft sage duo tin.",
     "items": ["a-court-of-peonies", "a-court-of-peonies-duo"]},
    {"id": "dusk-and-dawn", "name": "The Dusk and The Dawn",
     "sub": "A pair of leather bags",
     "blurb": "One old idiom, 花晨月夕, split across two leather bags. Give one, or give both and bookend the day.",
     "items": ["the-dusk", "the-dawn"]},
    {"id": "keepsake-bags", "name": "The Keepsake Bags",
     "sub": "Woven and leather totes",
     "blurb": "Bags made to be worn long after the season, each carrying its own four character wish.",
     "items": ["weaving-moments", "tote-of-bliss", "tote-of-good-health"]},
    {"id": "reunion-pieces", "name": "The Reunion Pieces",
     "sub": "For the table and the dressing table",
     "blurb": "A drawer chest, a serving turntable and a scroll box, the pieces that come back out at every gathering.",
     "items": ["blossom-drawer-chest", "elegance-reunion-turntable", "treasure-scroll"]},
    {"id": "snowskin-edition", "name": "Snowskin Edition",
     "sub": "Chilled, with truffle centres",
     "blurb": "One keepsake tin, eight snowskin mooncakes, our four truffle flavours twice over.",
     "items": ["orchid-reverie"]},
]

# --------------------------------------------------------------------------
# GIFT CONCIERGE — questions. Budget and halal act as HARD FILTERS, not
# weights: the top-tier chest must never surface on a "simple gesture"
# answer, and snowskin must never surface when Halal certification is
# required.
#
# Prices are RETAIL, before whatever promo is running the week someone
# orders — so nothing in this collection is shown to a customer as a
# dollar figure. The min/max on each BUDGETS tier below are internal
# tiering only, used to keep the Concierge's match honest; the label the
# customer sees is a scenario, not a number.
# --------------------------------------------------------------------------
RECIPIENTS = [
    ("family",     "Family",                  "family"),
    ("friend",     "A friend or neighbour",   "a friend"),
    ("colleagues", "Colleagues or a boss",    "colleagues"),
    ("clients",    "Clients, in volume",      "clients"),
    ("traveller",  "Someone heading overseas", "someone heading home"),
]

PRIORITIES = [
    ("keep",      "Something they'll keep and use"),
    ("story",     "A name and a story worth telling"),
    ("favourite", "A favourite for everyone at the table"),
    ("impress",   "Something that lands the moment it's seen"),
]

TABLES = [
    ("traditional", "Traditionalists, lotus and yolk", "C"),
    ("mixed",       "Mixed generations, children included", "F"),
    ("chilled",     "Adventurous, happy with chilled snowskin", "G"),
    ("halal",       "Halal certification matters for everyone", "E"),
]

BUDGETS = [
    ("b1", "A simple gesture",              0,   50),
    ("b2", "A proper gift, well presented", 50,  90),
    ("b3", "The one that really lands",     90,  120),
    ("b4", "Corporate or bulk gifting",     0, 9999),
]

# --------------------------------------------------------------------------
# WHERE TO BUY — brochure page 3
# Coordinates geocoded via OpenStreetMap Nominatim, 5 Aug 2026.
# --------------------------------------------------------------------------
BOOTHS = [
    ("Jewel Changi Airport",     "#01-231, L1, Lobby H", True,  1.3602243, 103.9896749),
    ("CIMB Plaza",               "L1",          False, 1.2842625, 103.8522209),
    ("Compass One",              "L2",          False, 1.3920337, 103.8949526),
    ("Junction 8",               "L2",          False, 1.3505893, 103.8487447),
    ("Jurong Point",             "L1",          False, 1.3394964, 103.7052540),
    ("Lot One",                  "L1",          False, 1.3850739, 103.7450166),
    ("NEX",                      "L1",          False, 1.3504943, 103.8722727),
    ("Raffles Xchange",          "B1",          False, 1.2937426, 103.8538363),
    ("Takashimaya Square",       "B2",          False, 1.3025211, 103.8353202),
    ("Tampines Mall",            "L1",          False, 1.3525218, 103.9447221),
    ("TANGS at Tang Plaza",      "B1-25",       False, 1.3047546, 103.8330692),
    ("The Clementi Mall",        "L3",          False, 1.3149814, 103.7644695),
    ("Velocity @ Novena Square", "L1",          False, 1.3197981, 103.8440434),
    ("VivoCity",                 "L1",          False, 1.2643707, 103.8229537),
    ("Westgate",                 "L2",          False, 1.3341940, 103.7428671),
]
