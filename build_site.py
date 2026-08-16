# -*- coding: utf-8 -*-
"""
Builds index.html for the Mdm Ling Bakery Mid-Autumn 2026 microsite.

Run:  python3 build_site.py
Everything is generated from data.py, so the keepsake cards, the Gift
Concierge and the Build Your Gift tool always agree with each other.

Visual system: MLB brand refresh 2026 (brands/mlb/design-system.css).
Dusty Rose #A97F78 / Champagne Gold #C7A66A / Cocoa #4E3C37 on Cloud #F3F2F1.
Inter throughout (variable, optical sizing for display); Work Sans is used
ONLY for standalone numerals, which is where the big ghosted section marks
come from.

DESIGN NOTE (Aug 2026 rebuild, "The Garden Table")
--------------------------------------------------
The 2026 campaign was shot as a garden picnic: a cream fringed parasol,
white ironwork tables, rattan chairs, rose and bougainvillea hedges, blue
and white teacups. The earlier build ignored that and rendered everything
as identical bordered white cards in a two-column grid, which read as
generic. This build takes its cues from the photography instead:

  * no decorative geometry anywhere (the old ring/circle motifs are gone)
  * no bordered cards on the page ground; hairlines and type do the work
  * full-bleed photographic bands carry the section transitions
  * the keepsakes are laid out editorially, not uniformly: four features,
    one paired band for The Dawn + The Dusk, then a staggered grid
  * the intro is the shoot's own rose hedge, filmed, which parts to enter
  * real defocused rose petals (cut from the shoot) drift over the page

Templating uses {{KEY}} placeholders and str.replace rather than %-format,
because the CSS and JS are full of literal % and the escaping was a
liability at this size.
"""
import json
import os
import re
import seo
from data import (KEEPSAKES, SETS, BOOTHS, CATEGORIES, RECIPIENTS, PRIORITIES,
                  TABLES, BUDGETS, WA_CUSTOMER, FREE_DELIVERY, SITE_URL, GA_ID)

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET_V = 10  # bump when an asset is replaced under the same filename

# Breast Cancer Foundation, Singapore. Verified 6 Aug 2026.
# Kien plans to swap this for the campaign-tagged self-examination page later:
#   https://bcf.org.sg/get-involved/breast_self_examination/
#     ?utm_source=print&utm_medium=qr_code&utm_campaign=mdm_ling_bakery
BCF_URL = "https://www.bcf.org.sg"
ARTIST_IG = "https://www.instagram.com/theworldofying/"
# WooCommerce account page, which carries the newsletter signup. Checked 16 Aug 2026.
NEWSLETTER = "https://www.mdmlingbakery.com/my-account/"


def fill(t, **kw):
    for k, v in kw.items():
        t = t.replace("{{%s}}" % k, str(v))
    return t


def v(path):
    return "assets/%s?v=%d" % (path, ASSET_V)


# --------------------------------------------------------------------------
# CSS
# --------------------------------------------------------------------------
CSS = """
:root{
  --rose:#A97F78; --gold:#C7A66A; --cocoa:#4E3C37; --cloud:#F3F2F1;
  --sage:#A5A58D; --plum:#6E4B4A; --mushroom:#D8CEC3; --brass:#8B7355;
  --taupe:#B6A79C; --paper:#FBFAF9; --linen:#EFE9E2;
  --ink:var(--cocoa); --muted:#8A7A72; --hair:#DFD6CE; --hair-soft:#E9E2DB;
  --f:'Inter',system-ui,-apple-system,sans-serif;
  --fn:'Work Sans','Inter',sans-serif;
  --maxw:1240px; --readw:60ch;
  --navh:58px;
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth; scroll-padding-top:calc(var(--navh) + 14px);}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto;} *{animation:none!important; transition:none!important;}
}
body{margin:0; background:var(--cloud); color:var(--ink); font-family:var(--f);
  font-weight:400; font-size:17.5px; line-height:1.62; -webkit-font-smoothing:antialiased;
  font-feature-settings:"cv11","ss01"; overflow-x:hidden;}
img{max-width:100%; display:block;}
a{color:inherit;}
.wrap{max-width:var(--maxw); margin:0 auto; padding:0 clamp(20px,5vw,48px);}
.read{max-width:var(--readw);}
.bleed{width:100vw; margin-left:calc(50% - 50vw);}

/* type ------------------------------------------------------------------ */
h1,h2,h3,h4{font-variation-settings:"opsz" 32; text-wrap:balance;}
.eyebrow{display:block; font-size:11px; font-weight:600; letter-spacing:.32em;
  text-transform:uppercase; color:var(--gold);}
.han{letter-spacing:.16em;}
.cnmark{font-size:clamp(17px,2.4vw,22px); font-weight:500; color:var(--rose);
  letter-spacing:.16em;}
.gloss{font-size:13.5px; font-style:italic; color:var(--muted);}

/* decorative script pairing: Great Vibes for the English title, Ma Shan Zheng
   (brush hand) for 花月情长. Both stay legible at the sizes used. */
.cs-en{font-family:'Great Vibes','Inter',cursive; font-weight:400; letter-spacing:.01em;}
.cs-cn{font-family:'Ma Shan Zheng','Inter',cursive; font-weight:400; letter-spacing:.1em;}

/* ---------- into the garden (intro) ---------- */
.intro{position:fixed; inset:0; z-index:220; display:none; cursor:pointer; overflow:hidden;
  background:#2A211E; -webkit-tap-highlight-color:transparent;}
.intro.show{display:block;}
/* Opening the gate now dives INTO the hedge: the filmed foliage scales up past
   the lens and fades, so the page appears as if you stepped through the bushes. */
.intro.open{background:transparent; pointer-events:none;}
.intro:focus{outline:none;}
.intro .gv{position:absolute; inset:0; width:100%; height:100%; object-fit:cover;
  z-index:1; transform-origin:50% 46%; will-change:transform,opacity;
  transition:transform 1350ms cubic-bezier(.6,.02,.35,1), opacity 620ms ease 700ms;}
.intro.open .gv{transform:scale(3.4); opacity:0;}
/* a soft vignette so the seal always reads over the foliage */
.intro .veil{position:absolute; inset:0; z-index:3; pointer-events:none;
  background:radial-gradient(ellipse 70% 55% at 50% 48%, rgba(30,23,20,.62) 0%,
             rgba(30,23,20,.30) 55%, rgba(30,23,20,.44) 100%);
  transition:opacity 500ms ease;}
.intro.open .veil{opacity:0;}
.intro .seal{position:absolute; left:50%; top:50%; z-index:4; text-align:center;
  transform:translate(-50%,-50%); color:#F6ECD8; width:min(88vw,560px);
  transition:opacity 420ms ease, transform 1000ms cubic-bezier(.5,0,.2,1);}
.intro.open .seal{opacity:0; transform:translate(-50%,-50%) scale(1.6);}
.intro .seal .s-logo{display:block; width:min(46vw,190px); height:auto; margin:0 auto;
  filter:drop-shadow(0 2px 14px rgba(24,18,15,.55));}
.intro .seal .s-en{display:block; margin:26px 0 0; font-size:clamp(38px,9.5vw,60px);
  line-height:1.12; color:#FBF3E2; text-shadow:0 2px 22px rgba(24,18,15,.65);}
.intro .seal .s-han{display:block; margin:10px 0 0; font-size:clamp(34px,9vw,56px);
  line-height:1.1; color:#F4E3C2; text-shadow:0 2px 26px rgba(24,18,15,.7);}
.intro .seal .s-season{display:block; margin:20px 0 0; font-size:clamp(11px,2.4vw,13px);
  font-weight:600; letter-spacing:.3em; text-transform:uppercase; color:#E4D6CE;}
.intro .seal .s-rule{display:block; width:54px; height:1px; margin:24px auto 0;
  background:linear-gradient(90deg,transparent,#D9BF86,transparent);}
.intro .prompt{position:absolute; left:0; right:0; bottom:max(7vh,58px); z-index:4;
  text-align:center; color:#E6D9D2; font-size:11.5px; font-weight:600; letter-spacing:.28em;
  text-transform:uppercase; transition:opacity 240ms ease;}
.intro.open .prompt{opacity:0;}
.intro .prompt i{display:block; width:1px; height:26px; background:linear-gradient(#D9BF86,transparent);
  margin:14px auto 0; animation:reach 2.4s ease-in-out infinite;}
@keyframes reach{0%,100%{transform:scaleY(.6); opacity:.5;} 50%{transform:scaleY(1); opacity:1;}}

/* ---------- drifting petals ---------- */
#petals{position:fixed; inset:0; z-index:58; pointer-events:none; opacity:.62;}

/* ---------- nav ---------- */
nav.jump{position:sticky; top:0; z-index:60; background:rgba(243,242,241,.93);
  backdrop-filter:saturate(150%) blur(14px); border-bottom:1px solid var(--hair);}
nav.jump .in{max-width:var(--maxw); margin:0 auto; padding:0 clamp(20px,5vw,48px);
  display:flex; gap:clamp(18px,2.4vw,30px); overflow-x:auto; scrollbar-width:none;
  height:var(--navh); align-items:center; -webkit-overflow-scrolling:touch;
  touch-action:pan-x; overscroll-behavior-x:contain;}
nav.jump .in::-webkit-scrollbar{display:none;}
/* desktop: the bar's links sit centred; phones keep the left-anchored slide */
@media(min-width:760px){ nav.jump .in{justify-content:center;} }
nav.jump a{text-decoration:none; white-space:nowrap; font-size:11.5px; font-weight:600;
  letter-spacing:.16em; text-transform:uppercase; color:var(--muted); padding:5px 0;
  border-bottom:1.5px solid transparent; transition:color .2s,border-color .2s;}
nav.jump a:hover{color:var(--ink);}
nav.jump a.active{color:var(--rose); border-bottom-color:var(--gold);}
.progress{height:1px; background:var(--gold); width:0; transition:width .1s linear;
  position:relative; overflow:visible;}
/* a butterfly rides the leading edge of the reading line */
.progress .pfly{position:absolute; right:-10px; top:50%; width:19px; height:19px;
  transform:translateY(-50%) rotate(90deg); pointer-events:none;}
.progress .pfly svg{width:100%; height:100%; display:block; overflow:visible;
  filter:drop-shadow(0 1px 2px rgba(78,60,55,.35));}
.progress .pfly svg path{fill:var(--gold); stroke:#FBF6F2; stroke-width:1.6; stroke-linejoin:round;}
.progress .pfly svg ellipse{fill:#4E3C37;}
.progress .pfly svg .ant{fill:none; stroke:#4E3C37; stroke-width:1.6; stroke-linecap:round;}
.progress .pfly .wl, .progress .pfly .wr{transform-box:fill-box; animation:flut 1s ease-in-out infinite;}
.progress .pfly .wl{transform-origin:100% 50%;}
.progress .pfly .wr{transform-origin:0% 50%;}
/* the brochure sits apart from the section links, pinned to the bar's edge */
nav.jump a.nbro{position:absolute; right:16px; top:50%; transform:translateY(-50%);
  z-index:3; color:#96762F; border:1px solid var(--gold); padding:7px 13px;
  background:rgba(243,242,241,.9);}
nav.jump a.nbro:hover{color:#FBF6F2; background:var(--gold);}
@media (max-width:759px){
  nav.jump a.nbro{position:static; transform:none; border:1px solid var(--gold);
    padding:6px 11px; background:none;}
}
/* slide affordances: a fading edge plus an animated chevron so the bar
   obviously carries more than it shows */
nav.jump{position:sticky;}
nav.jump .edge{position:absolute; top:0; bottom:0; width:44px; pointer-events:none;
  z-index:2; transition:opacity .25s;}
nav.jump .edge.r{right:0;
  background:linear-gradient(to left, rgba(243,242,241,.96) 25%, rgba(243,242,241,0));}
nav.jump .edge.l{left:0; opacity:0;
  background:linear-gradient(to right, rgba(243,242,241,.96) 25%, rgba(243,242,241,0));}
nav.jump .edge.r::after{content:"\\203A"; position:absolute; right:9px; top:50%;
  transform:translateY(-54%); font-size:22px; line-height:1; color:var(--rose);
  animation:nudge 1.6s ease-in-out infinite;}
nav.jump.at-end .edge.r{opacity:0;}
nav.jump.scrolled .edge.l{opacity:1;}
@keyframes nudge{0%,100%{transform:translate(0,-54%);} 50%{transform:translate(4px,-54%);}}

/* phones: the bar lives at the bottom, where the thumb is — taller, louder,
   and it slides sideways (pan-x is explicit so the page scroll never eats it) */
@media (max-width:759px){
  /* left/right pin the fixed bar to the viewport; without them it
     shrink-wraps its links, grows wider than the screen, and the row
     inside never overflows, which is why it could not slide */
  nav.jump{position:fixed; top:auto; bottom:0; left:0; right:0; width:auto;
    border-bottom:0; border-top:1px solid var(--hair);
    padding-bottom:env(safe-area-inset-bottom);
    box-shadow:0 -8px 26px rgba(78,60,55,.16);}
  nav.jump .in{height:66px; gap:24px;}
  nav.jump a{padding:8px 0; border-bottom:0; border-top:2px solid transparent;
    font-size:12.5px;}
  nav.jump a.active{border-top-color:var(--gold);}
  nav.jump .progress{order:-1;}
  body{padding-bottom:calc(66px + env(safe-area-inset-bottom));}
  html{scroll-padding-top:18px;}
}

/* ---------- hero ----------
   The opening is split rather than overlaid. The hero frame is the whole
   collection staged under the parasol, and its subject sits mid-frame: a
   square photograph offers no horizontal pan on a wide viewport, so any
   headline laid over it collided with the products and every scrim strong
   enough to fix that threw the photograph away. So the photograph runs
   undimmed and the title block sits beneath it on cocoa, overlapping the
   frame slightly the way an opening spread does. */
header.hero{background:var(--cocoa);}
/* the brand strip: centred logo at the very top of the page, season below it */
.hbrand{position:relative; background:var(--cloud); text-align:center;
  padding:clamp(26px,4vw,44px) 20px clamp(22px,3.4vw,36px);}
.hbrand img{display:inline-block; width:min(58vw,240px); height:auto;}
.hbrand .hseason{display:block; margin:14px 0 0; font-size:11.5px; font-weight:600;
  letter-spacing:.32em; text-transform:uppercase; color:var(--gold);}
/* the campaign name writes itself across the strip, bows out, then the logo
   takes its place (once per session, skipped for reduced-motion and deep links) */
.hb-title{position:absolute; inset:0; display:none; flex-direction:column;
  align-items:center; justify-content:center; pointer-events:none;}
.hb-title .cs-en{font-size:clamp(30px,5.4vw,46px); color:#96762F;}
.hb-title .cs-cn{font-size:clamp(20px,3.2vw,28px); color:var(--rose); margin-top:6px;}
.hbrand.anim .hb-title{display:flex; opacity:0; animation:hbT 2.8s ease forwards;}
.hbrand.anim .hb-logo{opacity:0; animation:hbL .9s ease 2.9s forwards;}
@keyframes hbT{0%{opacity:0; transform:translateY(12px);}
  18%{opacity:1; transform:none;} 70%{opacity:1; transform:none;}
  100%{opacity:0; transform:translateY(-10px);}}
@keyframes hbL{from{opacity:0; transform:translateY(8px);} to{opacity:1; transform:none;}}
header.hero .hfig{position:relative; height:min(62svh,640px); overflow:hidden;
  background:var(--mushroom);}
header.hero .hfig picture{position:absolute; inset:0;}
header.hero .hbg{width:100%; height:100%; object-fit:cover; object-position:50% 40%;}
/* Wide screens: the photograph fills the whole screen below the logo strip,
   framed on the band of the image where the products sit. */
@media(min-width:760px){
  header.hero .hfig{height:calc(100svh - var(--navh));}
  header.hero .hbg{object-position:50% 58%;}
}
header.hero .hfig::after{content:""; position:absolute; inset:0; pointer-events:none;
  background:linear-gradient(to top, rgba(42,31,27,.55) 0%, rgba(42,31,27,.10) 22%,
             rgba(42,31,27,0) 44%);}
/* hotspots: pulsing markers over the products in the hero photograph.
   Positioned by JS with object-fit cover maths, so they stay pinned to the
   products whatever the crop. */
.hspots{position:absolute; inset:0; z-index:3;}
/* markers are gilded butterflies that hover over the products, wings beating */
.hspot{position:absolute; width:52px; height:52px; margin:-26px 0 0 -26px; padding:0;
  border:0; background:none; cursor:pointer; -webkit-tap-highlight-color:transparent;
  animation:flyin 3.4s ease-in-out var(--fd,0s) both,
    bob 3.6s ease-in-out calc(var(--fd,0s) + 3.5s) infinite;}
/* each butterfly drifts in on a curved, wandering path: out wide, rising,
   then a slow spiral down onto its product */
@keyframes flyin{
  0%{opacity:0; transform:translate(var(--fx,-220px), var(--fy,220px)) scale(.72);}
  10%{opacity:1;}
  42%{transform:translate(calc(var(--fx,-220px) * .42), calc(var(--fy,220px) * .3 - 52px)) scale(.88);}
  68%{transform:translate(calc(var(--fx,-220px) * .15), calc(var(--fy,220px) * .05 - 34px)) scale(.96);}
  86%{transform:translate(calc(var(--fx,-220px) * .04), -12px);}
  100%{opacity:1; transform:none;}
}
/* in the air the body banks left and right like a real flight line, and
   settles level as it lands */
.hspot svg{animation:bank 3.4s ease-in-out var(--fd,0s) both;}
@keyframes bank{
  0%{transform:rotate(-34deg);}
  20%{transform:rotate(16deg);}
  40%{transform:rotate(-26deg);}
  60%{transform:rotate(12deg);}
  80%{transform:rotate(-16deg);}
  100%{transform:rotate(-8deg);}
}
/* wings beat quickly in flight, then ease to a rest-beat on landing */
.hspot.landed .wl, .hspot.landed .wr{animation-duration:1.9s;}
/* the moment the hero leaves the screen, every wing rests */
.hspots.offstage .hspot, .hspots.offstage .hspot .wl, .hspots.offstage .hspot .wr{
  animation-play-state:paused;}
/* before the garden gate opens, the flock waits in the wings */
.hspots.waiting .hspot, .hspots.waiting .hspot svg,
.hspots.waiting .hspot .wl, .hspots.waiting .hspot .wr{animation-play-state:paused;}
@media(max-width:600px){
  .hspot{width:34px; height:34px; margin:-17px 0 0 -17px;}
  .hpop{width:min(230px,68vw);}
  .hpop img{height:96px;}
  .hpop .hp-x{width:34px; height:34px; font-size:19px;}
  .htip{font-size:12px; padding:9px 14px;}
}
.hspot svg{width:100%; height:100%; display:block; overflow:visible;
  transform:rotate(-8deg);
  filter:drop-shadow(0 4px 9px rgba(30,22,19,.6)); transition:transform .18s;}
.hspot:hover svg, .hspot:focus-visible svg{transform:rotate(-8deg) scale(1.16);}
/* Wings are coloured per butterfly (--bw upper, --bw2 lower) from the palette
   of the collection's own floral artwork; each one is set in JS to contrast
   with the product it lands on. Champagne gold is the fallback and is still
   worn by the hint butterfly and one hero butterfly. */
.hspot svg path{fill:var(--bw,var(--gold)); stroke:#FBF6F2; stroke-width:1.6; stroke-linejoin:round;}
.hspot svg .w2{fill:var(--bw2,var(--bw,var(--gold)));}
.hspot svg ellipse{fill:#4E3C37; stroke:#FBF6F2; stroke-width:1;}
.hspot svg .ant{fill:none; stroke:#FBF6F2; stroke-width:1.4; stroke-linecap:round;}
.hspot .wl, .hspot .wr{transform-box:fill-box; animation:flut .6s ease-in-out infinite;}
/* once landed the banking animation comes off the body so hover works again */
.hspot.landed svg{animation:none;}
.hspot .wl{transform-origin:100% 50%;}
.hspot .wr{transform-origin:0% 50%;}
@keyframes flut{0%,100%{transform:scaleX(1);} 50%{transform:scaleX(.74);}}
@keyframes bob{0%,100%{transform:translateY(0);} 50%{transform:translateY(-7px);}}
/* the product card a butterfly opens */
.hpop{position:absolute; z-index:6; width:min(270px,74vw); background:#FBF6F2; color:#4E3C37;
  border:1px solid var(--gold); box-shadow:0 18px 50px rgba(20,14,12,.5);
  opacity:0; visibility:hidden; transform:translateY(8px);
  transition:opacity .18s, transform .18s, visibility .18s;}
.hpop.on{opacity:1; visibility:visible; transform:none;}
.hpop img{width:100%; height:132px; object-fit:cover; display:block;}
/* the woven bag sits low in its photograph */
.hpop img[src*="weaving-moments"]{object-position:50% 72%;}
.hpop .hp-b{padding:14px 16px 16px; display:flex; flex-direction:column; gap:4px;}
.hpop .hp-n{font-weight:600; font-size:15.5px; color:#2A1F1B; padding-right:20px;}
.hpop .hp-m{font-size:12.5px; color:#6F5F58;}
.hpop .btn{margin-top:10px; justify-content:center;}
.hpop .hp-x{position:absolute; top:6px; right:6px; width:30px; height:30px; border:0;
  background:rgba(42,31,27,.65); color:#FBF6F2; font-size:17px; line-height:1;
  cursor:pointer; display:flex; align-items:center; justify-content:center;}
/* the hint that the butterflies are alive */
.htip{position:absolute; left:50%; bottom:clamp(16px,3.4vw,30px); z-index:4;
  transform:translateX(-50%) translateY(8px); display:flex; align-items:center; gap:11px;
  max-width:86vw; background:rgba(42,31,27,.86); color:#F4E9E2; font-size:13px;
  font-weight:600; letter-spacing:.04em; padding:11px 18px;
  border:1px solid rgba(199,166,106,.65); pointer-events:none;
  opacity:0; visibility:hidden; transition:opacity .3s, transform .3s, visibility .3s;}
.htip.on{opacity:1; visibility:visible; transform:translateX(-50%);}
.htip svg{width:26px; height:26px; flex:none; transform:rotate(-8deg);}
.htip svg path{fill:var(--gold); stroke:#FBF6F2; stroke-width:1.6; stroke-linejoin:round;}
.htip svg ellipse{fill:#2A1F1B; stroke:#FBF6F2; stroke-width:1;}
.htip svg .ant{fill:none; stroke:#FBF6F2; stroke-width:1.4; stroke-linecap:round;}
/* ---------- the tally: how much of the garden you've found ----------
   Takes over the hint pill's slot the moment the first butterfly is opened,
   so the two never share the screen. Numerals are Work Sans (the one place
   the brand allows it: standalone numbers). */
.htally{position:absolute; left:50%; bottom:clamp(16px,3.4vw,30px); z-index:4;
  transform:translateX(-50%) translateY(8px); display:flex; align-items:center; gap:12px;
  max-width:86vw; background:rgba(42,31,27,.86); color:#F4E9E2;
  padding:10px 18px; border:1px solid rgba(199,166,106,.65); pointer-events:none;
  opacity:0; visibility:hidden; transition:opacity .3s, transform .3s, visibility .3s;}
.htally.on{opacity:1; visibility:visible; transform:translateX(-50%);}
.htally .tn{font-family:var(--fn); font-size:19px; font-weight:600; line-height:1;
  color:var(--gold); font-variant-numeric:tabular-nums; white-space:nowrap;}
.htally .tn b{font-weight:600; color:#FBF6F2; font-size:23px;}
.htally .tl{font-size:12px; font-weight:600; letter-spacing:.14em;
  text-transform:uppercase; white-space:nowrap;}
.htally .tbar{display:block; width:clamp(56px,11vw,110px); height:2px;
  background:rgba(244,233,226,.28); flex:none;}
.htally .tbar i{display:block; height:100%; width:0; background:var(--gold);
  transition:width .5s cubic-bezier(.22,1,.36,1);}
/* the whole garden found: the pill grows a way onward */
.htally.done{pointer-events:auto; gap:14px; padding:11px 14px 11px 18px;}
.htally.done .tbar{display:none;}
.htally.done svg{width:26px; height:26px; flex:none; transform:rotate(-8deg);}
.htally.done svg path{fill:var(--gold); stroke:#FBF6F2; stroke-width:1.6; stroke-linejoin:round;}
.htally.done svg ellipse{fill:#2A1F1B; stroke:#FBF6F2; stroke-width:1;}
.htally.done svg .ant{fill:none; stroke:#FBF6F2; stroke-width:1.4; stroke-linecap:round;}
.htally .tgo{font-size:12px; font-weight:700; letter-spacing:.1em; text-transform:uppercase;
  color:#2A1F1B; background:var(--gold); padding:8px 13px; text-decoration:none;
  white-space:nowrap; transition:background .2s;}
.htally .tgo:hover, .htally .tgo:focus-visible{background:#DCC08A;}
.htally .thn{font-size:13px; font-weight:600; letter-spacing:.03em;}
.htally .thn .han{color:var(--gold);}
/* On a phone the frame is the portrait cut and the products stack towards the
   bottom, so a pill anchored there sits on top of the lowest butterflies (The
   Dusk and The Painted Garden Box) and puts them out of reach. Above the
   flock is clear sky: the highest butterfly is at 39.5% of the frame. */
@media(max-width:760px){
  .htip, .htally{top:clamp(12px,3.4vw,22px); bottom:auto;}
}
@media(max-width:600px){
  .htally{gap:9px; padding:9px 13px;}
  .htally .tn{font-size:16px;} .htally .tn b{font-size:19px;}
  .htally .tl{font-size:10.5px; letter-spacing:.1em;}
  .htally.done{flex-wrap:wrap; justify-content:center; max-width:88vw; gap:10px;}
  /* the wording carries it on a small screen; the icon only adds height */
  .htally.done svg{display:none;}
  .htally .thn{font-size:12px;} .htally .tgo{font-size:11px; padding:7px 11px;}
}
/* a butterfly already opened settles: its wings come to rest, and it drops
   behind the ones still to be found so the remaining targets get easier to
   hit as the hunt goes on (several products sit shoulder to shoulder) */
.hspot{z-index:2;}
.hspot.found{z-index:1;}
.hspot.found .wl, .hspot.found .wr{animation:none !important;}
.hspot.found svg{transform:scale(.94);}
.hspot.found:hover svg, .hspot.found:focus-visible svg{transform:rotate(-8deg) scale(1.16);}
@media(prefers-reduced-motion:reduce){
  .hspot, .hspot svg, .hspot .wl, .hspot .wr{animation:none !important;}
}
.hspot .hlabel{position:absolute; left:50%; bottom:calc(100% + 8px); transform:translateX(-50%);
  background:rgba(42,31,27,.92); color:#FBF6F2; font-size:11.5px; font-weight:600;
  letter-spacing:.04em; padding:7px 12px; white-space:nowrap; pointer-events:none;
  opacity:0; transition:opacity .18s;}
.hspot:hover .hlabel, .hspot:focus-visible .hlabel{opacity:1;}
.hspot.edge-l .hlabel{left:0; transform:none;}
.hspot.edge-r .hlabel{left:auto; right:0; transform:none;}
.hero .hcap{position:relative; z-index:2; color:#FBF6F2;
  padding:clamp(30px,4.6vw,58px) 0 clamp(44px,6vw,80px);}
.hero .hcap .wrap{display:grid; gap:clamp(18px,3vw,54px); align-items:end;}
@media(min-width:960px){ .hero .hcap .wrap{grid-template-columns:1.35fr 1fr;} }
.hero .eyebrow{color:#EFDCB4;}
.hero h1{font-weight:600; letter-spacing:-.032em; line-height:.99;
  font-size:clamp(40px,7.2vw,82px); margin:0; max-width:15ch;}
.hero .hcn{margin:24px 0 0; line-height:1.15;}
.hero .hcn .cs-en{display:block; font-size:clamp(30px,5.4vw,46px); color:#F4E3C2;}
.hero .hcn .cs-cn{display:block; margin-top:6px; font-size:clamp(26px,4.6vw,38px); color:#E9D3B7;}
.hero p.lede{max-width:44ch; margin:0; font-size:clamp(15.5px,2vw,17.5px); color:#DCCEC8;}
.hero .acts{display:flex; flex-wrap:wrap; gap:12px; margin-top:clamp(22px,3vw,30px);}

/* ---------- buttons ---------- */
.btn{display:inline-flex; align-items:center; gap:9px; font-family:var(--f); font-size:13.5px;
  font-weight:600; letter-spacing:.04em; padding:14px 24px; border:1.5px solid var(--cocoa);
  background:var(--cocoa); color:var(--cloud); text-decoration:none; cursor:pointer;
  border-radius:0; transition:background .18s,color .18s,border-color .18s,transform .18s;}
.btn:hover{background:#382925; border-color:#382925;}
.btn.gold{background:var(--gold); border-color:var(--gold); color:#3B2C28;}
.btn.gold:hover{background:#B8934F; border-color:#B8934F;}
.btn.ghost{background:transparent; color:inherit; border-color:currentColor;}
.btn.ghost:hover{background:rgba(78,60,55,.07);}
.btn.light{background:#FBF6F2; border-color:#FBF6F2; color:#4E3C37;}
.btn.light:hover{background:#fff; border-color:#fff;}
.btn.sm{font-size:12.5px; padding:11px 18px;}
.btn[disabled]{opacity:.45; pointer-events:none;}
/* a quieter text link, used where a button would be too loud */
.tlink{display:inline-flex; align-items:center; gap:7px; font-size:13.5px; font-weight:600;
  color:var(--rose); text-decoration:none; border-bottom:1px solid var(--gold);
  padding-bottom:2px; transition:color .18s,border-color .18s;}
.tlink:hover{color:var(--cocoa); border-color:var(--cocoa);}

/* ---------- back buttons: previous section, and the top of the page ---------- */
.backer{position:fixed; right:16px; bottom:18px; z-index:58; display:flex;
  flex-direction:column; gap:8px; opacity:0; visibility:hidden; transform:translateY(10px);
  transition:opacity .22s, transform .22s, visibility .22s;}
.backer.on{opacity:1; visibility:visible; transform:none;}
.backer button{width:52px; height:52px; padding:0; border:1.5px solid var(--gold);
  background:rgba(42,31,27,.88); color:#F4E3C2; cursor:pointer; font-family:var(--f);
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:2px;
  transition:background .18s;}
.backer button:hover{background:#4E3C37;}
.backer button svg{width:15px; height:15px; display:block;}
.backer button span{font-size:8.5px; font-weight:700; letter-spacing:.14em;
  text-transform:uppercase;}
@media (max-width:759px){
  .backer{bottom:calc(66px + env(safe-area-inset-bottom) + 14px); right:12px;}
}

/* ---------- section furniture ---------- */
.part{margin:clamp(74px,11vw,140px) 0 0;}
.part-head{position:relative; margin-bottom:clamp(34px,5vw,58px);}
.part-head .mark{position:absolute; right:0; top:-.28em; font-family:var(--fn);
  font-size:clamp(84px,17vw,210px); font-weight:600; line-height:.8; color:#E7DFD7;
  z-index:0; pointer-events:none; user-select:none; letter-spacing:-.04em;}
.part-head .inner{position:relative; z-index:1;}
.part-head h2{font-weight:600; letter-spacing:-.028em; line-height:1.02;
  font-size:clamp(32px,6vw,62px); margin:12px 0 0; color:var(--cocoa); max-width:20ch;}
.part-head .lede{max-width:var(--readw); margin:20px 0 0; font-size:17px; color:#6B5A54;}
.part-head .lede strong{color:var(--rose); font-weight:600;}
.rule{height:1px; background:var(--gold); border:0; margin:0;}

/* ---------- photographic bands ---------- */
.band{position:relative; min-height:min(76svh,660px); display:flex; align-items:flex-end;
  overflow:hidden; background:var(--mushroom); margin:clamp(74px,11vw,140px) 0 0;}
/* A phone crops a 3:2 band to roughly its middle third, so each band also
   ships a portrait cut rather than upscaling the centre of the landscape one. */
.band picture{position:absolute; inset:0; z-index:0;}
.band img{width:100%; height:100%; object-fit:cover;}
.band::after{content:""; position:absolute; inset:0; z-index:1; pointer-events:none;
  background:linear-gradient(to top, rgba(44,33,29,.80) 0%, rgba(44,33,29,.34) 38%,
             rgba(44,33,29,0) 72%);}
.band .bt{position:relative; z-index:2; color:#FBF6F2; max-width:var(--maxw); margin:0 auto;
  width:100%; padding:0 clamp(20px,5vw,48px) clamp(38px,6vw,64px);}
.band .bt p{margin:14px 0 0; font-size:clamp(20px,3.4vw,34px); font-weight:500;
  letter-spacing:-.02em; line-height:1.24; max-width:26ch;
  text-shadow:0 2px 22px rgba(30,22,19,.45);}
.band .bt .eyebrow{color:#EFDCB4;}
.band.short{min-height:min(52svh,440px);}

/* ---------- manifesto ----------
   Sits directly under the hero caption on the same cocoa ground, so it reads
   as one closing thought rather than a second stranded block. */
.manifesto{background:var(--cocoa); color:#EFE7E2;
  padding:clamp(10px,2vw,20px) 0 clamp(56px,9vw,104px);}
.manifesto .mtext{border-top:1px solid rgba(199,166,106,.35);
  padding-top:clamp(26px,4vw,44px);}
.manifesto p strong{color:#fff; font-weight:600;}
/* one thought, read top to bottom: the why, the principle, three keepsakes
   shown rather than described, then the practical note as a gilded aside */
.manifesto .m-lede{font-size:clamp(19px,2.6vw,26px); color:#F0E7E2; line-height:1.55;
  max-width:40ch; margin:0 0 clamp(22px,3.2vw,34px);}
.manifesto .m-sub{font-size:clamp(17px,2.2vw,21px); color:#E3D8D3; line-height:1.6;
  margin:0 0 clamp(20px,3vw,30px);}
.manifesto .m-cards{display:grid; gap:clamp(14px,2.4vw,28px);
  grid-template-columns:repeat(auto-fit, minmax(210px,1fr));
  margin:0 0 clamp(26px,4vw,40px);}
.manifesto .m-cards figure{margin:0;}
.manifesto .m-cards img{width:100%; height:auto; aspect-ratio:4/3; object-fit:cover;
  display:block; background:#3A2C27;}
.manifesto .m-cards figcaption{margin-top:11px; font-size:14.5px; color:#D8CBC5;
  line-height:1.55;}
.manifesto .m-cards figcaption strong{color:#fff;}
.manifesto .m-note{font-size:15.5px; color:#CDBFB9; line-height:1.6; max-width:64ch;
  margin:0 0 clamp(18px,2.6vw,26px);}
.manifesto .m-halal{border-left:2px solid var(--gold);
  padding:6px 0 6px clamp(18px,2.4vw,26px); color:#EFE3DC;
  font-size:clamp(16px,2vw,18px); line-height:1.6; margin:0;}

/* ---------- tools (matcher + builder) ---------- */
.tool{background:var(--linen); padding:clamp(30px,5vw,60px) clamp(22px,4vw,56px);}
/* the tool name is the headline act, not a form label: large, gilded and
   flanked by a rule so it can't be mistaken for a survey heading */
.tool-kicker{display:flex; align-items:center; gap:18px; font-size:clamp(14px,1.9vw,18px);
  font-weight:700; letter-spacing:.3em; text-transform:uppercase; color:#96762F;
  white-space:nowrap;}
.tool-kicker::before{content:"\\273F"; font-size:.9em; color:var(--gold); letter-spacing:0;}
.tool-kicker::after{content:""; height:1.5px; flex:1; max-width:220px;
  background:linear-gradient(90deg,var(--gold),transparent);}
.tool h3{font-size:clamp(28px,4.6vw,46px); font-weight:600; letter-spacing:-.026em;
  margin:14px 0 10px; line-height:1.06;}
.tool .sub{color:#6F5F58; font-size:16px; margin:0 0 30px; max-width:56ch;}
.qsteps{display:flex; gap:5px; margin-bottom:30px; max-width:280px;}
.qsteps i{flex:1; height:2px; background:#D6CBC2;}
.qsteps i.on{background:var(--gold);}
.q{display:none;}
.q.on{display:block;}
.q .qn{font-family:var(--fn); font-size:11.5px; font-weight:600; letter-spacing:.18em;
  text-transform:uppercase; color:var(--muted);}
.q h4{font-size:clamp(20px,3vw,27px); font-weight:600; letter-spacing:-.02em; margin:10px 0 22px;}
.opts{display:grid; gap:0; border-top:1px solid var(--hair);}
.opt{text-align:left; font-family:var(--f); font-size:16px; font-weight:500; color:var(--ink);
  background:none; border:0; border-bottom:1px solid var(--hair); padding:17px 40px 17px 2px;
  cursor:pointer; position:relative; transition:background .16s,padding-left .16s,color .16s;}
.opt::after{content:"\\2192"; position:absolute; right:10px; top:50%; transform:translateY(-50%);
  color:var(--gold); opacity:0; transition:opacity .16s,right .16s;}
.opt:hover, .opt:focus-visible{background:#FBFAF9; padding-left:14px; color:var(--rose); outline:none;}
.opt:hover::after, .opt:focus-visible::after{opacity:1; right:16px;}
.qback{margin-top:22px; background:none; border:0; font-family:var(--f); font-size:13.5px;
  color:var(--muted); cursor:pointer; padding:0; text-decoration:underline; text-underline-offset:3px;}
.qback:hover{color:var(--ink);}

.result{display:none;}
.result.on{display:block;}
.res-grid{display:grid; gap:clamp(22px,3.5vw,40px);}
@media(min-width:760px){ .res-grid{grid-template-columns:290px 1fr; align-items:start;} }
.res-photo{background:var(--mushroom); aspect-ratio:4/5; overflow:hidden;}
.res-photo img{width:100%; height:100%; object-fit:cover;}
.res-body h4{font-size:clamp(26px,3.6vw,34px); font-weight:600; letter-spacing:-.026em; margin:8px 0 0;}
.res-body .rcn{font-size:19px; color:var(--rose); font-weight:500; letter-spacing:.13em; margin:8px 0 0;}
.res-body .rgloss{font-size:13.5px; color:var(--muted); font-style:italic; margin:3px 0 0;}
.res-why{border-left:2px solid var(--gold); padding:3px 0 3px 18px; margin:22px 0 0; font-size:17px;}
.res-meta{display:flex; flex-wrap:wrap; gap:8px; margin:22px 0 0;}
.res-acts{display:flex; flex-wrap:wrap; gap:11px; align-items:center; margin:26px 0 0;}
.res-alt{margin:30px 0 0; padding:20px 0 0; border-top:1px solid var(--hair); font-size:15px; color:var(--muted);}
.res-alt a{color:var(--rose); font-weight:600; text-decoration:none; border-bottom:1px solid var(--gold);}
.res-note{margin:16px 0 0; font-size:14px; color:#7A6A64;}
/* the travel veto explanation: quiet, but it has to be read */
.res-note.flag{border-left:2px solid var(--gold); padding:2px 0 2px 14px; color:#5E4F49;}
.res-note.flag strong{color:var(--cocoa);}

/* ---------- tags ---------- */
.tag{display:inline-flex; align-items:center; gap:5px; font-size:11px; font-weight:600;
  letter-spacing:.08em; text-transform:uppercase; padding:5px 10px; border:1px solid var(--hair);
  background:transparent; color:#6B5A54;}
.tag.gold{border-color:#DDC796; color:#8A6E33;}
/* the $1 pledge reads as a filled badge, not another quiet chip */
.tag.charity{background:var(--gold); border-color:var(--gold); color:#33241F;
  font-weight:700; box-shadow:0 2px 8px rgba(199,166,106,.35);}
/* and on the giving pieces it sits as a ribbon pinned over the photo's edge */
.feat .fimg{position:relative;}
.feat .fbadge{position:absolute; top:20px; left:-12px; z-index:2;
  display:inline-flex; align-items:center; gap:8px;
  background:var(--cocoa); color:#FBF6F2; font-size:13px; font-weight:700;
  letter-spacing:.09em; text-transform:uppercase; padding:10px 16px;
  border:1.5px solid var(--gold); box-shadow:0 8px 22px rgba(30,22,19,.4);}
.feat .fbadge svg{width:16px; height:16px; fill:var(--gold); flex:none;}
.feat.rev .fbadge{left:auto; right:-12px;}
@media(max-width:600px){ .feat .fbadge{left:12px; top:12px;} .feat.rev .fbadge{right:12px; left:auto;} }
.tag.rose{border-color:#E0CBC6; color:var(--rose);}
.tag.sage{border-color:#CFD6C4; color:#5F6B4C;}
.tag.chill{border-color:#C6D4DA; color:#4C6570;}

/* ---------- keepsakes: features ---------- */
.feat{display:grid; gap:0; margin:clamp(56px,8vw,108px) 0 0; align-items:center;}
@media(min-width:900px){
  .feat{grid-template-columns:1fr 1fr; gap:clamp(34px,4.5vw,72px);}
  .feat.rev .fimg{order:2;}
}
.feat .fimg{position:relative; background:var(--mushroom); aspect-ratio:4/5; overflow:hidden;}
.feat .fimg img{width:100%; height:100%; object-fit:cover; transition:transform 900ms cubic-bezier(.2,.6,.2,1);}
.feat:hover .fimg img{transform:scale(1.028);}
.feat .ftxt{padding:clamp(26px,3.5vw,10px) 0 0;}
@media(min-width:900px){ .feat .ftxt{padding:0;} }
.feat .chan{display:block; font-size:10.5px; font-weight:700; letter-spacing:.2em;
  text-transform:uppercase; color:var(--brass); margin-bottom:14px;}
.feat .chan.booth{color:#96762F;}
.feat .fmt{display:block; font-size:11px; font-weight:600; letter-spacing:.2em;
  text-transform:uppercase; color:var(--muted);}
.feat h3{font-size:clamp(28px,4.6vw,50px); font-weight:600; letter-spacing:-.03em;
  line-height:1.02; margin:10px 0 0;}
.feat h3 .var{display:block; font-weight:400; font-size:.42em; color:var(--muted);
  letter-spacing:0; margin-top:8px;}
.feat .fcn{margin:14px 0 0;}
.feat .desc{margin:22px 0 0; font-size:16.5px; color:#5E4F49; max-width:52ch;}
.feat .desc p{margin:0 0 13px;}
.feat .desc p:last-child{margin-bottom:0;}
.feat .desc strong{color:var(--plum); font-weight:600;}
.feat .becomes{margin:24px 0 0; padding:16px 0 0; border-top:1px solid var(--hair); max-width:52ch;}
.feat .becomes .lbl{display:block; font-size:10px; font-weight:700; letter-spacing:.2em;
  text-transform:uppercase; color:var(--gold); margin-bottom:6px;}
.feat .becomes p{margin:0; font-size:16px; color:#5E4F49;}
.feat .note{margin:14px 0 0; font-size:13.5px; color:var(--muted); font-style:italic; max-width:52ch;}
.feat .disc{margin:20px 0 4px; max-width:52ch; border:1.5px solid var(--gold);
  background:#FBF6EC; padding:14px 18px;}
.feat .disc .lbl{display:block; font-size:10px; font-weight:700; letter-spacing:.2em;
  text-transform:uppercase; color:#8A6E33; margin-bottom:5px;}
.feat .disc p{margin:0; font-size:14.5px; color:#5E4F49;}
.feat .foot{display:flex; flex-wrap:wrap; align-items:center; gap:12px; margin:26px 0 0;}
.feat .meta{margin-top:18px;}

/* ---------- keepsakes: category carousels ----------
   Each family opens with a row of small thumbnails (the overview), then one
   product on stage. Tap a thumbnail, or the arrows, to switch products. */
.cat{margin:clamp(64px,9vw,120px) 0 0; scroll-margin-top:calc(var(--navh) + 14px);}
.cat-rule{height:1.5px; background:linear-gradient(90deg,var(--gold),transparent); border:0; margin:0 0 26px;}
.cat-head h3{font-size:clamp(26px,4.4vw,44px); font-weight:600; letter-spacing:-.028em;
  line-height:1.04; margin:10px 0 0;}
.cat-head .cat-blurb{margin:12px 0 0; font-size:16px; color:#6B5A54; max-width:58ch;}
.cat-head .cat-blurb a{color:var(--rose); font-weight:600; text-decoration:none;
  border-bottom:1px solid var(--gold);}
/* head on the left, arrows + thumbnails filling the right, so the row above
   each product reads as one balanced band instead of a half-empty one */
.cat-top{display:grid; gap:20px clamp(28px,4vw,56px); align-items:end;}
@media(min-width:900px){
  .cat-top{grid-template-columns:minmax(0,1fr) auto;}
  .cat-side{justify-self:end; text-align:right;}
  .cat-side .cat-arrows{justify-content:flex-end;}
}
.cat-arrows{display:flex; align-items:center; gap:8px; margin:0 0 16px;}
.cat-arrows .cnt{font-family:var(--fn); font-size:13px; font-weight:600; color:var(--muted);
  min-width:44px; text-align:center; letter-spacing:.06em;}
.cnav{width:44px; height:44px; border:1.5px solid var(--cocoa); background:none; cursor:pointer;
  color:var(--cocoa); font-size:18px; line-height:1; display:flex; align-items:center;
  justify-content:center; transition:background .16s,color .16s;}
.cnav:hover{background:var(--cocoa); color:var(--cloud);}
.cat-thumbs{display:flex; align-items:flex-start; gap:clamp(10px,1.6vw,16px); margin:0;
  overflow-x:auto; scrollbar-width:none; -webkit-overflow-scrolling:touch; padding-bottom:4px;}
.cat-thumbs::-webkit-scrollbar{display:none;}
.cthumb{flex:0 0 auto; width:clamp(88px,11vw,148px); font-family:var(--f); padding:0;
  cursor:pointer; text-align:left; background:none; border:0; color:var(--ink);}
.cthumb img{width:100%; aspect-ratio:1/1; object-fit:cover; display:block;
  background:var(--mushroom); outline:1.5px solid var(--hair); outline-offset:-1.5px;
  transition:outline-color .16s;}
.cthumb span{display:block; font-size:11px; font-weight:600; line-height:1.3; padding:8px 0 0;}
.cthumb:hover img{outline-color:var(--rose);}
.cthumb.on img{outline:2.5px solid var(--rose); outline-offset:-2.5px;}
.cthumb.on span{color:var(--rose);}
.cpanels{margin:6px 0 0;}
.cpanel{display:none;}
.cpanel.on{display:block; animation:fadein .4s ease;}
@keyframes fadein{from{opacity:0; transform:translateY(8px);} to{opacity:1; transform:none;}}

/* ---------- builder ---------- */
.bpick{margin:0 0 34px;}
.bgroup{display:block; font-size:11px; font-weight:700; letter-spacing:.2em;
  text-transform:uppercase; color:var(--brass); margin:28px 0 12px;
  padding-top:18px; border-top:1px solid var(--hair);}
.bpick .bgroup:first-child{margin-top:0; padding-top:0; border-top:0;}
.brow{display:grid; grid-template-columns:repeat(3,1fr); gap:clamp(10px,1.6vw,18px);}
@media(min-width:620px){ .brow{grid-template-columns:repeat(5,1fr);} }
@media(min-width:980px){ .brow{grid-template-columns:repeat(6,1fr);} }
.chip{font-family:var(--f); padding:0; cursor:pointer; text-align:left; background:none;
  border:0; color:var(--ink); transition:opacity .16s;}
/* the frame is a fixed 4:5 window (padding trick, not aspect-ratio, so every
   browser crops identically and the rows always line up) */
.chip .cw{display:block; position:relative; padding-top:125%; overflow:hidden;
  background:var(--mushroom); outline:1.5px solid transparent; outline-offset:-1.5px;
  transition:outline-color .16s;}
.chip .cw img{position:absolute; inset:0; width:100%; height:100%; object-fit:cover; display:block;}
.chip span.cn2{display:block; font-size:11.5px; font-weight:600; line-height:1.3; padding:9px 0 0;
  letter-spacing:.01em;}
.chip:hover .cw{outline-color:var(--rose);}
.chip.on .cw{outline-color:var(--rose); outline-width:2.5px;}
.chip.on span{color:var(--rose);}
.bout{display:none; border-top:1px solid var(--hair); padding-top:30px;}
.bout.on{display:block;}
.bhead{display:flex; flex-wrap:wrap; gap:20px; align-items:flex-start; margin-bottom:26px;}
.bhead img{width:104px; height:130px; object-fit:cover; flex:none; background:var(--mushroom);}
.bhead h4{margin:0; font-size:clamp(21px,3vw,26px); font-weight:600; letter-spacing:-.022em;}
.setlist{border-top:1px solid var(--hair);}
.setrow{padding:16px 2px; display:grid; gap:5px 18px; align-items:start;
  border-bottom:1px solid var(--hair);}
@media(min-width:640px){ .setrow{grid-template-columns:84px 1fr auto;} }
.setrow .sid{font-family:var(--fn); font-size:21px; font-weight:600; color:var(--rose);}
.setrow .sid small{display:block; font-family:var(--f); font-size:10.5px; font-weight:600;
  letter-spacing:.12em; text-transform:uppercase; color:var(--muted); margin-top:2px;}
.setrow ul{margin:0; padding:0; list-style:none; font-size:14.5px; color:#5E4F49;}
.setrow li{padding:1px 0;}

/* ---------- sets table ---------- */
.settable{border-top:1.5px solid var(--gold);}
.settable .r{display:grid; gap:5px 20px; padding:18px 2px; border-bottom:1px solid var(--hair);}
@media(min-width:700px){ .settable .r{grid-template-columns:70px 190px 1fr;} }
.settable .r.hdr{font-size:10.5px; font-weight:700; letter-spacing:.2em;
  text-transform:uppercase; color:var(--muted); padding:12px 2px;}
.settable .sid{font-family:var(--fn); font-size:23px; font-weight:600; color:var(--rose); line-height:1;}
.settable .g{font-size:13.5px; color:var(--muted);}
.settable ul{margin:0; padding:0; list-style:none; font-size:15px; color:#5E4F49;}

/* ---------- flavour overview (one glance, grouped by range) ---------- */
.fov-group{margin:clamp(30px,4.5vw,48px) 0 0;}
.fov-h{display:block; font-size:12px; font-weight:700; letter-spacing:.22em;
  text-transform:uppercase; color:var(--brass); text-decoration:none;
  border-bottom:1px solid var(--hair); padding-bottom:10px;}
.fov-h:hover{color:var(--rose);}
.fov{display:grid; grid-template-columns:repeat(2,1fr); gap:clamp(14px,2.4vw,24px);
  margin:18px 0 0;}
@media(min-width:560px){ .fov{grid-template-columns:repeat(4,1fr);} }
@media(min-width:900px){ .fov{grid-template-columns:repeat(4,1fr);} }
.fov a{display:block; text-decoration:none; color:var(--ink);}
/* the frame crops in tight on the mooncake itself: the full scene shots put
   the cake small and low, so the thumb zooms to the plate */
.fov .fw{display:block; aspect-ratio:1/1; overflow:hidden; background:var(--mushroom);
  outline:1.5px solid var(--hair); outline-offset:-1.5px; transition:outline-color .16s;}
.fov img{width:100%; aspect-ratio:1/1; object-fit:cover; display:block;
  transform:scale(1.55); transform-origin:50% 96%;}
/* the single yolk shot is already a close-up: shown unzoomed, its plate sits
   at the same size as the zoomed wide shots beside it */
.fov img[src*="trad-yolk"]{transform:none;}
.fov a:hover .fw{outline-color:var(--rose);}
.fov .fname{display:block; font-size:12.5px; font-weight:600; line-height:1.3; margin:9px 0 0;}
.fov a:hover .fname{color:var(--rose);}

/* ---------- callouts (the lines that must not be missed) ---------- */
.callout{border:1.5px solid var(--gold); background:#FBF6EC; padding:18px 22px;
  margin:26px 0 0; max-width:70ch; font-size:15.5px; color:#4E3C37;}
/* the newsletter offer under a match: sits below the order button so it never
   competes with it, but is the next thing read once they have their answer */
.res-news{margin:22px 0 0; padding:16px 0 0; border-top:1px solid var(--hair);
  display:flex; flex-wrap:wrap; align-items:center; gap:12px 16px;}
.res-news p{margin:0; font-size:14.5px; color:#5E4F49; flex:1 1 15ch;}
.res-news strong{color:var(--plum);}
.res-news .tc{display:block; margin-top:3px; font-size:11.5px; color:var(--muted);
  letter-spacing:.04em;}
.callout strong{color:var(--plum);}
.callout a{color:var(--rose); font-weight:600;}

/* ---------- flavours ---------- */
.range{margin:clamp(46px,7vw,86px) 0 0; scroll-margin-top:calc(var(--navh) + 14px);}
.flav{scroll-margin-top:calc(var(--navh) + 20px);}
.range-head{display:flex; align-items:baseline; gap:16px; flex-wrap:wrap;
  border-bottom:1.5px solid var(--gold); padding-bottom:14px;}
.range-num{font-family:var(--fn); font-size:clamp(30px,5vw,46px); font-weight:600;
  color:var(--gold); line-height:.82; letter-spacing:-.03em;}
.range-head h3{font-size:clamp(21px,3.2vw,29px); font-weight:600; letter-spacing:-.024em; margin:0;}
.range-head .tag2{font-size:14px; color:var(--muted);}
.range-intro{margin:22px 0 0; font-size:16.5px; color:#5E4F49; max-width:var(--readw);}
.range-intro strong{color:var(--plum); font-weight:600;}
.flavours{display:grid; gap:clamp(24px,3.5vw,44px); margin-top:30px;}
@media(min-width:640px){ .flavours{grid-template-columns:1fr 1fr;} }
@media(min-width:1040px){ .flavours{grid-template-columns:repeat(4,1fr);} }
.flav{display:flex; flex-direction:column;}
.flav .fp{padding:0; border:0; background:none; cursor:pointer; display:block; position:relative;
  width:100%;}
.flav .fp img{width:100%; height:auto; aspect-ratio:1/1; object-fit:cover; background:var(--mushroom); display:block;}
.flav .fp::after{content:""; position:absolute; inset:0; background:rgba(20,16,15,.24);
  opacity:0; transition:opacity .16s;}
.flav .fp::before{content:""; position:absolute; top:50%; left:50%; width:24px; height:24px;
  transform:translate(-50%,-50%); z-index:1; opacity:0; transition:opacity .16s;
  background-repeat:no-repeat; background-position:center;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round'%3E%3Ccircle cx='10' cy='10' r='7'/%3E%3Cline x1='20.5' y1='20.5' x2='15.2' y2='15.2'/%3E%3C/svg%3E");}
.flav .fp:hover::after, .flav .fp:focus-visible::after,
.flav .fp:hover::before, .flav .fp:focus-visible::before{opacity:1;}
.flav h4{font-size:18px; font-weight:600; letter-spacing:-.018em; margin:16px 0 8px; line-height:1.22;}
.flav .badges{display:flex; gap:6px; margin:0 0 11px; flex-wrap:wrap;}
.flav .story{font-size:14.5px; color:#5E4F49; margin:0;}
.flav .story strong{color:var(--plum); font-weight:600;}
.ing{margin-top:14px; padding-top:12px; border-top:1px dashed var(--hair);}
.ing summary{cursor:pointer; font-size:10px; font-weight:700; letter-spacing:.18em;
  text-transform:uppercase; color:var(--gold); list-style:none; padding:1px 0;}
.ing summary::-webkit-details-marker{display:none;}
.ing summary::after{content:" +"; color:var(--muted); font-weight:600;}
.ing[open] summary::after{content:" \\2212";}
.ing .ing-body{margin-top:11px;}
.ing .lbl{display:block; font-size:9.5px; font-weight:700; letter-spacing:.18em;
  text-transform:uppercase; color:var(--gold); margin:0 0 3px;}
.ing .lbl.mt{margin-top:10px;}
.ing p{margin:0; font-size:12.5px; color:#7A6A64; line-height:1.5;}
.algs{display:flex; flex-wrap:wrap; gap:5px;}
.alg{font-size:11px; font-weight:500; color:#7A4A46; border:1px solid #E5D6D2; padding:2px 7px;}
.trace{margin:7px 0 0; font-size:11px; font-style:italic; color:#9C8C86;}

/* ---------- panels ---------- */
.panel{border-left:2px solid var(--gold); padding:4px 0 4px 24px; margin:clamp(34px,5vw,56px) 0 0;
  max-width:var(--readw);}
.panel h4{font-size:19px; font-weight:600; letter-spacing:-.018em; margin:0 0 10px;}
.panel p{margin:0 0 11px; font-size:15.5px; color:#5E4F49;}
.panel p:last-child{margin-bottom:0;}
.panel strong{color:var(--plum); font-weight:600;}

/* ---------- the artist / BCF feature ---------- */
.artist{position:relative; overflow:hidden; background:var(--cocoa);
  margin:clamp(74px,11vw,140px) 0 0;}
/* padding-block only: a padding SHORTHAND here would zero out the .wrap
   side gutters and flush the text to the screen edge */
.artist .ainner{position:relative; z-index:2;
  padding-top:clamp(48px,8vw,100px); padding-bottom:clamp(48px,8vw,100px);}
.artist .collab{display:block; text-align:center; color:#E4D6CE; font-size:12px;
  font-weight:600; letter-spacing:.24em; text-transform:uppercase; line-height:2;
  margin:0 auto 22px; position:relative; padding-bottom:20px;}
.artist .collab::after{content:""; position:absolute; left:50%; bottom:0; width:54px; height:1px;
  transform:translateX(-50%); background:linear-gradient(90deg,transparent,#D9BF86,transparent);}
/* the three partner marks, side by side under the collaboration line */
.collab-logos{display:flex; align-items:center; justify-content:center; flex-wrap:wrap;
  gap:clamp(16px,3vw,32px); margin:0 auto clamp(38px,5.5vw,58px);}
.collab-logos img{height:28px; width:auto; display:block; opacity:.94;}
.collab-logos img.ying{height:46px;}
.collab-logos img.mlb{height:34px;}
.collab-logos span{color:#C7A66A; font-size:13px; opacity:.8;}
/* phones: the marks stack, house brand first */
@media(max-width:600px){
  .collab-logos{flex-direction:column; gap:22px;}
  .collab-logos span{display:none;}
  .collab-logos img.mlb{order:1;}
  .collab-logos img.ying{order:2;}
  .collab-logos img.bcf{order:3;}
}
.agrid{display:grid; gap:clamp(30px,4.5vw,64px); align-items:start;}
@media(min-width:900px){ .agrid{grid-template-columns:1fr 1.05fr;} }
/* the artwork is the hero of this section: one large, uncropped plate */
.amedia figure{margin:0;}
.amedia img{width:100%; height:auto; display:block; background:var(--mushroom);
  box-shadow:0 18px 60px rgba(20,14,12,.45);}
.amedia figcaption{font-size:11.5px; letter-spacing:.12em; text-transform:uppercase;
  color:#BBA89F; margin-top:12px; line-height:1.6;}
/* phones read the story as one column: collab line, logos, eyebrow, the
   artwork, the message, the artist, the pledge, then the box */
@media(max-width:899px){
  .agrid{display:flex; flex-direction:column; gap:20px;}
  .agrid .acol, .agrid .amedia{display:contents;}
  .acol .eyebrow{order:1;}
  .amedia .aart{order:2;}
  .artist .acol h3{order:3; margin-top:0;}
  .artist .acol p{order:4; margin-top:0;}
  .ablurb{order:5; margin-top:0;}
  .artist .bcfnote{order:6; margin-top:0;}
  .amedia .amact{order:7; margin:0;}
  .amedia .agroup{order:8; margin-top:6px;}
}
/* the artist appears as a compact byline blurb: portrait, attribution and her link */
.ablurb{display:flex; gap:16px; align-items:center; flex-wrap:wrap; margin:26px 0 0;
  padding:16px 18px; border:1px solid rgba(199,166,106,.35);
  background:rgba(251,246,242,.05);}
.ablurb img{width:72px; height:72px; border-radius:50%; object-fit:cover;
  object-position:50% 18%; flex:none; display:block;
  border:1.5px solid var(--gold); box-shadow:0 4px 16px rgba(20,14,12,.4);}
.ablurb .apre{display:block; font-size:11px; font-weight:600; letter-spacing:.18em;
  text-transform:uppercase; color:#C7A66A; margin-bottom:4px;}
.ablurb .an{display:block; font-size:16.5px; font-weight:600; color:#FBF6F2;}
.ablurb .as{display:block; font-size:13px; color:#CDBBB2; margin-top:3px;}
.ablurb .awb{margin-top:12px;}
.artist .acol{max-width:56ch; color:#EFE4DE;}
.artist .eyebrow{color:#EFDCB4;}
.artist h3{font-size:clamp(28px,4.8vw,52px); font-weight:600; letter-spacing:-.03em;
  line-height:1.02; margin:14px 0 0; color:#FBF6F2;}
.artist p{margin:18px 0 0; font-size:16.5px; color:#E0D3CD;}
.artist p strong{color:#fff; font-weight:600;}
.artist .acts{display:flex; flex-wrap:wrap; gap:12px; align-items:center; margin:30px 0 0;}
/* the giving note: boxed and gilded so the $1 pledge reads as the heart of the section */
.artist .bcfnote{margin-top:34px; padding:clamp(22px,3.4vw,30px) clamp(20px,3vw,28px);
  border:1.5px solid rgba(199,166,106,.6); background:rgba(199,166,106,.10);
  box-shadow:0 10px 34px rgba(20,14,12,.3);}
.artist .bcfnote .btn{margin-top:20px;}
/* the dollar that carries further: scripted, gilded, flanked by fine rules */
.artist .amt{display:flex; align-items:center; gap:18px; color:var(--gold);}
.artist .amt .d{font-family:'Great Vibes',cursive; font-size:clamp(52px,8vw,72px);
  line-height:.9; text-shadow:0 2px 18px rgba(199,166,106,.35);}
.artist .amt::before, .artist .amt::after{content:""; height:1px; flex:1; max-width:88px;
  background:linear-gradient(90deg,transparent,#D9BF86);}
.artist .amt::after{background:linear-gradient(90deg,#D9BF86,transparent);}
.artist .amt .dsub{font-size:10.5px; font-weight:700; letter-spacing:.26em;
  text-transform:uppercase; color:#EBD9AE;}
.artist .bcfnote p{margin:14px 0 0; font-size:15.5px;}
/* under the artwork: its call to action, then the collaborators together */
.amedia .amact{display:flex; justify-content:flex-end; margin:18px 0 0;}
.amedia .agroup{margin-top:clamp(28px,4.5vw,46px);}
.amedia .agroup figcaption.credit{text-transform:none; letter-spacing:0; font-size:13px;
  color:#CDBBB2; line-height:1.65; margin-top:12px;}

/* ---------- booth map ---------- */
/* ---------- nearest booth finder ---------- */
.nearest{margin:22px 0 0; max-width:560px;}
.nearest form{display:flex; gap:10px; flex-wrap:wrap;}
.nearest input{flex:1 1 200px; min-width:0; font-family:var(--f); font-size:15px;
  padding:12px 14px; border:1.5px solid var(--hair); background:#fff; color:var(--ink);
  border-radius:0; -webkit-appearance:none;}
.nearest input:focus{outline:none; border-color:var(--gold);}
.near-out{margin-top:14px;}
.near-note{font-size:13.5px; color:var(--muted); margin:0 0 8px;}
.near-item{display:grid; grid-template-columns:1fr auto; gap:2px 14px; width:100%;
  text-align:left; font-family:var(--f); padding:12px 14px; margin:0 0 8px;
  border:1.5px solid var(--hair); background:#fff; cursor:pointer;
  transition:border-color .16s;}
.near-item:hover{border-color:var(--gold);}
.near-item .ni-n{font-size:14.5px; font-weight:600; color:var(--ink);}
.near-item .ni-d{font-size:13px; font-weight:600; color:#96762F; text-align:right;}
.near-item .ni-m{grid-column:1 / -1; font-size:12.5px; color:var(--muted);}

.booth-map{height:min(56svh,440px); margin:0 0 18px; background:var(--mushroom);}
.booth-map .leaflet-popup-content-wrapper{border-radius:0; box-shadow:0 6px 22px rgba(78,60,55,.2);}
.booth-map .leaflet-popup-tip{box-shadow:none;}
.booth-map .leaflet-popup-content{margin:14px 16px; font-family:var(--f);}
.bpop .bn{font-size:15px; font-weight:600; margin:0 0 2px; color:var(--ink);}
.bpop .bl{font-size:12.5px; color:var(--muted); margin:0;}
.bpop .bd{font-size:12px; font-weight:600; color:#96762F; margin:3px 0 0;}
.bpop .bf{display:inline-block; margin-top:6px; font-size:10px; font-weight:700;
  letter-spacing:.14em; text-transform:uppercase; color:#96762F;}
.bpop a{display:inline-block; margin-top:9px; font-size:12.5px; font-weight:600; color:var(--rose);}
.pin{display:block; filter:drop-shadow(0 2px 3px rgba(78,60,55,.35));}
.map-tools{display:flex; justify-content:flex-end; margin:-6px 0 20px;}

/* ---------- booths ---------- */
.booths{display:grid; border-top:1px solid var(--hair); grid-template-columns:1fr 1fr;
  column-gap:14px;}
@media(min-width:920px){ .booths{grid-template-columns:repeat(3,1fr);} }
.booth{background:none; padding:14px 12px 14px 2px; border:0; border-bottom:1px solid var(--hair);
  width:100%; text-align:left; font-family:var(--f); cursor:pointer; display:block;
  transition:background .14s,padding-left .14s;}
.booth:hover{background:#EFE9E2; padding-left:12px;}
.booth.on{background:#EFE9E2; box-shadow:inset 2px 0 0 var(--rose); padding-left:12px;}
.booth .bn{font-size:14.5px; font-weight:600; margin:0; color:var(--ink);}
.booth .bl{font-size:12.5px; color:var(--muted); margin:2px 0 0;}
.booth .bd{font-size:12px; font-weight:600; color:#96762F; margin:4px 0 0;}
.booth .bf{display:inline-block; margin-top:5px; font-size:9.5px; font-weight:700;
  letter-spacing:.14em; text-transform:uppercase; color:#96762F;}

/* ---------- lightbox ---------- */
.lightbox{position:fixed; inset:0; background:rgba(24,18,16,.93); display:none;
  align-items:center; justify-content:center; padding:clamp(20px,5vw,44px); z-index:240;}
.lightbox.on{display:flex;}
.lightbox img{max-width:min(560px,92vw); max-height:82vh; width:auto; height:auto;
  object-fit:contain; background:var(--mushroom);}
.lightbox .lb-close{position:absolute; top:14px; right:16px; background:none; border:0;
  color:#fff; font-size:32px; line-height:1; cursor:pointer; padding:8px; font-family:var(--f);}
.lightbox .lb-cap{position:absolute; bottom:24px; left:0; right:0; text-align:center;
  color:#EDE6E2; font-size:13px; padding:0 20px;}

/* ---------- footer ---------- */
footer{margin-top:clamp(74px,11vw,140px); background:var(--cocoa); color:#C9BDB7;
  padding:clamp(46px,7vw,80px) 0 clamp(40px,6vw,60px); font-size:14px;}
footer .flogo{width:min(48vw,200px); height:auto; display:block;}
footer .fnav .fig{padding:11px 13px;}
footer .fnav .fig svg{width:18px; height:18px; display:block;}
footer .fnav .fig:hover{color:var(--gold) !important; border-color:var(--gold);}
footer .fcn{display:block; margin:20px 0 30px; line-height:1.2;}
footer .fcn .cs-cn{font-size:30px; color:var(--gold);}
footer .fcn .cs-en{font-size:27px; color:#EBD9AE; margin-left:12px;}
@media(max-width:600px){
  footer .fcn .cs-en{display:block; margin:8px 0 0;}
}
footer .fl{max-width:66ch; margin:30px 0 0; color:#A3948E; font-size:12.5px; line-height:1.6;}
footer a{color:var(--gold);}
footer .fnav{display:flex; flex-wrap:wrap; gap:12px; margin:0 0 26px;}
footer .fbadges{display:flex; gap:26px; align-items:center; margin:34px 0 0;}
footer .fbadges img{height:62px; width:auto;}
"""


# --------------------------------------------------------------------------
# Static flavour content (prose stays hand written)
# --------------------------------------------------------------------------
def slugify(name):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-")


# Every flav() call registers itself here, in page order, so the one-glance
# flavour overview can never disagree with the cards below it.
FLAV_INDEX = []


def flav(img, alt, name, badges, story, ing, algs, trace):
    b = "".join('<span class="tag %s">%s</span>' % (c, t) for c, t in badges)
    a = "".join('<span class="alg">%s</span>' % x for x in algs)
    src = v(img)
    slug = "f-" + slugify(name)
    # seo.py reads this to build the flavour schema, so it carries the whole
    # flavour, not just what the one-glance overview needs.
    FLAV_INDEX.append({"img": img, "name": name, "slug": slug, "story": story,
                       "ing": ing, "algs": list(algs), "trace": trace,
                       "badges": list(badges), "range": ""})
    return """<div class="flav" id="%s">
      <button type="button" class="fp" data-lightbox="%s" data-lightbox-alt="%s" aria-label="View a larger photo of %s">
        <img src="%s" alt="%s" width="420" height="420" loading="lazy" decoding="async">
      </button>
      <h4>%s</h4>
      <div class="badges">%s</div>
      <p class="story">%s</p>
      <details class="ing">
        <summary>Ingredients &amp; allergen advice</summary>
        <div class="ing-body">
          <span class="lbl">Ingredients</span><p>%s</p>
          <span class="lbl mt">Allergen advice &middot; contains</span>
          <div class="algs">%s</div>
          <p class="trace">%s</p>
        </div>
      </details>
    </div>""" % (slug, src, alt, name, src, alt, name, b, story, ing, a, trace)


HALAL = ("sage", "Halal certified")
VEG = ("sage", "Vegetarian")

RANGES = [
    {
        "n": 1, "id": "traditional", "title": "Premium Traditional Baked",
        "tag": "The classics, baked golden", "intro": None,
        "items": [
            flav("trad-yolk.webp", "Traditional white lotus mooncake with salted egg yolk",
                 "Lotus with Melon Seeds and Yolk",
                 [HALAL, VEG, ("", "160g")],
                 "Smooth <strong>white lotus paste</strong> studded with melon seeds and wrapped around a <strong>golden salted egg yolk</strong>, baked the <strong>time honoured Cantonese way</strong>. <strong>The one everyone reaches for first.</strong>",
                 "White lotus paste, wheat flour, salted egg yolk \U0001F315, golden syrup, blended cooking oil (palm, peanut, sesame), melon seed, egg, milk.",
                 ["Gluten (wheat)", "Egg", "Milk", "Sesame", "Peanuts"],
                 "May contain traces of soy."),
            flav("trad-no-yolk.webp", "Traditional white lotus mooncake without yolk",
                 "Lotus with Melon Seeds",
                 [HALAL, VEG, ("", "160g")],
                 "Pure <strong>white lotus paste</strong> with melon seeds folded through, in a classic baked skin. Quiet, smooth and traditional, <strong>for those who like it simple</strong>.",
                 "White lotus paste, melon seed, wheat flour, golden syrup, blended cooking oil (palm, peanut, sesame), egg, milk.",
                 ["Gluten (wheat)", "Egg", "Milk", "Sesame", "Peanuts"],
                 "May contain traces of soy."),
        ],
    },
    {
        "n": 2, "id": "assorted", "title": "Signature Assorted Baked",
        "tag": "A flavour for every generation",
        "intro": "Our signature assorted range carries the modern side of Mdm Ling Bakery. Each flavour gets its own <strong>low sugar Momoyama skin</strong> and a softer bite, and each was created with a <strong>different generation at the table</strong> in mind. From the littlest ones to the grandparents, everyone finds a mooncake made for them.",
        "items": [
            flav("momo-choc.webp", "Momoyama Belgian double chocolate mooncake",
                 "Belgian Double Chocolate",
                 [HALAL, VEG, ("", "160g")],
                 "Created for the <strong>youngest at the table</strong>. Chocolate is a flavour children already know and love, so this is their first step into mooncakes: a <strong>double hit of chocolate in both the skin and the paste</strong>, finished with a pinch of <strong>Himalayan salt</strong> that sharpens the cocoa from the first bite to the last.",
                 "Chocolate lotus paste, Maruchi dough, chocolate paste (Master Martini), melon seeds, blended cooking oil (palm, peanut, sesame), cocoa powder, Himalayan salt.",
                 ["Gluten (wheat)", "Milk", "Tree nuts", "Sesame", "Egg", "Peanuts", "Soy"],
                 "May contain traces of nuts."),
            flav("momo-sesame.webp", "Momoyama black sesame peanut butter mooncake",
                 "Black Sesame Peanut Butter",
                 [HALAL, VEG, ("", "160g")],
                 "Created for <strong>parents and grandparents with a sweet tooth</strong>. Toasty <strong>black sesame</strong> meets smooth <strong>peanut butter</strong>, a nod to the black sesame and peanut pastes they grew up ordering at Singapore dessert stalls, carried in a soft Momoyama skin.",
                 "Black sesame lotus paste, Maruchi dough, peanut butter, melon seeds, blended cooking oil (palm, peanut, sesame), pumpkin powder.",
                 ["Gluten (wheat)", "Egg", "Sesame", "Peanuts", "Milk", "Soy"],
                 "May contain traces of nuts."),
            flav("momo-pandan.webp", "Momoyama emerald pandan mooncake with golden yolk",
                 "Emerald Pandan Golden Yolk",
                 [HALAL, VEG, ("", "160g")],
                 "Created for <strong>every generation</strong>. The sweet <strong>pandan fragrance</strong> everyone knows from kaya, carried in a modern Momoyama skin, with the <strong>golden yolk from the traditional mooncake</strong> at its centre. The <strong>best of both worlds</strong> in one bite.",
                 "Pandan paste, Maruchi dough, custard salted egg yolk paste \U0001F315, melon seed, blended cooking oil (palm, peanut, sesame), purple sweet potato powder.",
                 ["Gluten (wheat)", "Milk", "Egg", "Sesame", "Peanuts", "Soy"],
                 "May contain traces of nuts."),
            flav("momo-reddates.webp", "Momoyama red dates longan mooncake",
                 "Red Dates Longan",
                 [HALAL, VEG, ("", "160g")],
                 "Created with our <strong>elders</strong> in mind. <strong>Red dates</strong> and <strong>longan</strong> are flavours they've known all their lives, long treasured in Chinese tradition as nourishing and warming, folded into a rose hued Momoyama skin. Gentle, familiar and easy to love.",
                 "Red date lotus, Maruchi dough, longan bits, melon seeds, blended cooking oil (palm, peanut, sesame), colour (102, 110, 124).",
                 ["Gluten (wheat)", "Egg", "Sesame", "Peanuts", "Milk", "Soy"],
                 "May contain traces of nuts."),
        ],
    },
    {
        "n": 3, "id": "snowskin", "title": "Premium Truffle Snowskin",
        "tag": "Chilled, with a truffle centre",
        "intro": "The playful side of the collection. Each snowskin mooncake hides a <strong>truffle centre</strong> beneath its soft, delicate skin, best enjoyed chilled. Elegant enough for the table, fun enough that the last one never lasts. <strong>This range isn't Halal certified.</strong>",
        "items": [
            flav("snow-muscat.webp", "Truffle Muscat Grape snowskin mooncake with white grape truffle centre",
                 "Truffle Muscat Grape", [("chill", "Chilled"), ("", "63g")],
                 "A pale green snowskin of soft glutinous rice, filled with smooth lotus paste and a <strong>muscat grape truffle</strong> at its heart. <strong>Fragrant, delicate and quietly refreshing.</strong>",
                 "Cold water, icing sugar, glutinous rice flour, snowskin powder, shortening, cooking oil, lotus paste, muscat grape truffle (white couverture, cream, green tea powder, white grape flavour).",
                 ["Milk"],
                 "May contain traces of gluten, egg, nuts, sesame, peanuts and soy."),
            flav("snow-passionfruit.webp", "Truffle Passionfruit snowskin mooncake with cream and passionfruit truffle centre",
                 "Truffle Passionfruit", [("chill", "Chilled"), ("", "63g")],
                 "A sunny golden snowskin of soft glutinous rice, filled with smooth lotus paste and a <strong>passionfruit truffle</strong> that lands <strong>bright and tangy</strong>. A little tropical sunshine that wakes the whole box up.",
                 "Cold water, icing sugar, glutinous rice flour, snowskin powder, shortening, cooking oil, lotus paste, passionfruit truffle (white couverture, Unigra passionfruit, cream).",
                 ["Milk"],
                 "May contain traces of gluten, egg, nuts, sesame, peanuts and soy."),
            flav("snow-popping.webp", "Truffle Popping Candy snowskin mooncake with dragon fruit paste and popping candy centre",
                 "Truffle Popping Candy", [("chill", "Chilled"), ("", "63g")],
                 "A blush pink snowskin of soft glutinous rice, filled with vivid <strong>dragonfruit paste</strong> and a <strong>popping candy truffle that crackles as you bite</strong>. <strong>The one that makes everyone at the table laugh first</strong> and reach for seconds after.",
                 "Cold water, icing sugar, glutinous rice flour, snowskin powder, shortening, cooking oil, dragon fruit paste (lotus paste, dragon fruit powder), popping candy truffle (white couverture, pink popping candy filling, blue popping candy filling).",
                 ["Milk"],
                 "May contain traces of gluten, egg, nuts, sesame, peanuts and soy."),
            flav("snow-pistachio.webp", "Truffle Pistachio Kunafa snowskin mooncake with almond filling and pistachio paste centre",
                 "Truffle Pistachio Kunafa", [("chill", "Chilled"), ("", "63g")],
                 "An ivory snowskin of soft glutinous rice, filled with smooth lotus paste and a rich <strong>pistachio kunafa truffle</strong>. Our nod to the beloved <strong>Middle Eastern dessert</strong>, reimagined for the mooncake table.",
                 "Cold water, icing sugar, glutinous rice flour, snowskin powder, shortening, cooking oil, lotus paste, pistachio kunafa truffle (milk couverture, almond filling, pistachio paste, pistachio nuts, feuilletine).",
                 ["Tree nuts (pistachio, almond)", "Milk"],
                 "May contain traces of gluten, egg, sesame, peanuts and soy."),
        ],
    },
]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def wa(number, text):
    from urllib.parse import quote
    return "https://wa.me/%s?text=%s" % (number, quote(text))


def by_id(kid):
    for k in KEEPSAKES:
        if k["id"] == kid:
            return k
    raise KeyError(kid)


def chan_label(k):
    return "Order online" if k["channel"] == "online" else "At our booths"


def tags_for(k):
    tags = ['<span class="tag">%s</span>' % k["pcs"]]
    if "G" in k["sets"]:
        tags.append('<span class="tag chill">Snowskin &middot; chilled</span>')
    elif k["sets"]:
        tags.append('<span class="tag">Traditional / Assorted</span>')
        tags.append('<span class="tag sage">Halal certified</span>')
    else:
        tags.append('<span class="tag">Traditional</span>')
        tags.append('<span class="tag sage">Halal certified</span>')
    if k.get("artist"):
        tags.append('<span class="tag rose">Artist edition</span>')
    if k.get("bcf"):
        tags.append('<span class="tag charity">$1 to charity</span>')
    return "".join(tags)


def cta_for(k, small=True):
    sm = " sm" if small else ""
    if k["channel"] == "online":
        return ('<a class="btn%s" href="%s" target="_blank" rel="noopener" '
                'data-order="%s" data-name="%s">Order online</a>'
                % (sm, k["url"], k["id"], k["name"]))
    return ('<a class="btn%s gold" href="#where" '
            'data-booth="%s" data-name="%s">Find a booth near you</a>'
            % (sm, k["id"], k["name"]))


# --------------------------------------------------------------------------
# Keepsake layouts
# --------------------------------------------------------------------------
def feature(kid, reverse=False):
    """A hero keepsake: big photo one side, the full story the other."""
    k = by_id(kid)
    var = '<span class="var">%s</span>' % k["variant"] if k.get("variant") else ""
    body = "".join("<p>%s</p>" % p for p in k["body"])
    note = '<p class="note">%s</p>' % k["note"] if k.get("note") else ""
    disc = ""
    if k.get("disclaimer"):
        disc = ('<div class="disc"><span class="lbl">Please note</span><p>%s</p></div>'
                % k["disclaimer"])
    extra = ""
    if k.get("bcf"):
        extra += ('<a class="tlink" href="%s" target="_blank" rel="noopener" '
                  'data-bcf="card">About the Breast Cancer Foundation</a>' % BCF_URL)
    if k.get("artist"):
        extra += ('<a class="tlink" href="%s" target="_blank" rel="noopener">'
                  'About World of Ying</a>' % ARTIST_IG)
    fb = ""
    if k.get("bcf"):
        fb = ('<span class="fbadge"><svg viewBox="0 0 24 24" aria-hidden="true">'
              '<path d="M12 2c-2.8 3.4-3.4 6.9-1.7 10L5.4 20h3.7l2.9-4.4L14.9 20h3.7'
              'l-4.9-8c1.7-3.1 1.1-6.6-1.7-10z"/></svg>$1 to charity</span>')
    return """<article class="feat%s" id="k-%s">
  <div class="fimg">%s<img src="%s" alt="%s" width="900" height="1125" loading="lazy" decoding="async"></div>
  <div class="ftxt">
    <span class="chan%s">%s</span>
    <span class="fmt">%s</span>
    <h3>%s%s</h3>
    <p class="fcn"><span class="cnmark han">%s</span> <span class="gloss">%s &middot; %s</span></p>
    %s
    <div class="desc">%s</div>
    <div class="becomes"><span class="lbl">After Mid-Autumn it becomes</span><p>%s</p></div>
    %s
    <div class="foot">%s%s</div>
    <div class="res-meta meta">%s</div>
  </div>
</article>""" % (" rev" if reverse else "", k["id"], fb, v(k["img"]), k["alt"],
                 "" if k["channel"] == "online" else " booth", chan_label(k),
                 k["format"], k["name"], var, k["cn"], k["pinyin"], k["gloss"],
                 disc, body, k["becomes"], note, cta_for(k, small=False), extra, tags_for(k))


def category_block(cat):
    """One keepsake family: thumbnail overview on top, one product on stage."""
    items = cat["items"]
    panels = ""
    for i, kid in enumerate(items):
        panels += '<div class="cpanel%s" data-kid="%s">%s</div>' % (
            " on" if i == 0 else "", kid, feature(kid, reverse=bool(i % 2)))
    thumbs = ""
    if len(items) > 1:
        for i, kid in enumerate(items):
            k = by_id(kid)
            label = k["name"] + (" (%s)" % k["variant"] if k.get("variant") else "")
            thumbs += ('<button type="button" class="cthumb%s" data-idx="%d" '
                       'aria-label="Show %s"><img src="%s" alt="%s" loading="lazy" '
                       'decoding="async"><span>%s</span></button>'
                       % (" on" if i == 0 else "", i, label, v(k["img"]), k["alt"], label))
        thumbs = '<div class="cat-thumbs">%s</div>' % thumbs
    arrows = ""
    if len(items) > 1:
        arrows = ('<div class="cat-arrows">'
                  '<button type="button" class="cnav prev" aria-label="Previous piece">&#8592;</button>'
                  '<span class="cnt">1 / %d</span>'
                  '<button type="button" class="cnav next" aria-label="Next piece">&#8594;</button>'
                  '</div>' % len(items))
    side = ""
    if thumbs or arrows:
        side = '<div class="cat-side">%s%s</div>' % (arrows, thumbs)
    return """<section class="cat" id="cat-%s" data-cat="%s">
  <hr class="cat-rule">
  <div class="cat-top">
    <div class="cat-head">
      <span class="eyebrow">%s</span>
      <h3>%s</h3>
      <p class="cat-blurb">%s</p>
    </div>
    %s
  </div>
  <div class="cpanels">%s</div>
</section>""" % (cat["id"], cat["id"], cat["sub"], cat["name"], cat["blurb"],
                 side, panels)


def keepsakes_html():
    return "".join(category_block(c) for c in CATEGORIES)


def check_layout_covers_data():
    laid = set(kid for c in CATEGORIES for kid in c["items"])
    have = {k["id"] for k in KEEPSAKES}
    missing, extra = have - laid, laid - have
    if missing or extra:
        raise SystemExit("Keepsake categories out of sync with data.py.\n"
                         "  not laid out: %s\n  unknown ids: %s" % (sorted(missing), sorted(extra)))


def flavour_overview():
    """The one-glance flavour map, grouped by range, tap any to jump."""
    groups = [("traditional", "Premium Traditional Baked", 2),
              ("assorted", "Signature Assorted Baked", 4),
              ("snowskin", "Premium Truffle Snowskin", 4)]
    if len(FLAV_INDEX) != sum(g[2] for g in groups):
        raise SystemExit("Flavour overview out of sync: %d cards" % len(FLAV_INDEX))
    out, i = [], 0
    for rid, title, n in groups:
        items = ""
        for f in FLAV_INDEX[i:i + n]:
            items += ('<a href="#%s"><span class="fw"><img src="%s" alt="%s" loading="lazy" decoding="async"></span>'
                      '<span class="fname">%s</span></a>'
                      % (f["slug"], v(f["img"]), f["name"], f["name"]))
        i += n
        out.append('<div class="fov-group"><a class="fov-h" href="#%s">%s</a>'
                   '<div class="fov">%s</div></div>' % (rid, title, items))
    return "".join(out)


def booths_html():
    out = []
    for name, level, flag, lat, lng, dates in BOOTHS:
        f = '<span class="bf">Flagship store</span>' if flag else ""
        out.append('<button type="button" class="booth" data-loc="%s">'
                   '<p class="bn">%s</p><p class="bl">%s</p>'
                   '<p class="bd">%s</p>%s</button>'
                   % (slugify(name), name, level, dates, f))
    return '<div class="booths">%s</div>' % "".join(out)


def booths_json():
    return [{"id": slugify(n), "name": n, "level": lv, "flag": fg, "lat": la, "lng": lo,
             "dates": dt,
             "maps": "https://www.google.com/maps/search/?api=1&query=%s,%s" % (la, lo)}
            for n, lv, fg, la, lo, dt in BOOTHS]


def js_data():
    out = []
    for k in KEEPSAKES:
        out.append({
            "id": k["id"], "name": k["name"], "cn": k["cn"], "pinyin": k["pinyin"],
            "gloss": k["gloss"], "format": k["format"], "pcs": k["pcs"],
            "price": k["price"], "img": k["img"], "alt": k["alt"],
            "channel": k["channel"], "url": k.get("url", ""),
            "sets": k["sets"], "duoNote": k.get("duo_note", ""),
            "becomes": k["becomes"], "why": k["why"], "note": k.get("note", ""),
            "disclaimer": k.get("disclaimer", ""),
            "variant": k.get("variant", ""), "bcf": bool(k.get("bcf")),
            "artist": bool(k.get("artist")), "score": k["score"],
            "halalSafe": "G" not in k["sets"],
        })
    return out


# --------------------------------------------------------------------------
# JS
# --------------------------------------------------------------------------
JS = """
(function(){
  var K = {{KEEPSAKES}};
  var S = {{SETS}};
  var B = {{BOOTHS}};
  var CATS = {{CATS}};
  var TABLE_SET = {{TABLESET}};
  var BUDGET = {{BUDGET}};
  var RECIP = {{RECIP}};
  var WA_CUSTOMER = "{{WACUST}}";
  var SITE = "{{SITE}}";
  var AV = "{{AV}}";
  var BCF = "{{BCF}}";
  var NEWSLETTER = "{{NEWSLETTER}}";

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function ga(name, params){ if(window.gtag){ window.gtag('event', name, params||{}); } }
  function byId(id){ return document.getElementById(id); }
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function asset(f){ return 'assets/' + f + '?v=' + AV; }
  function setById(id){ for(var i=0;i<S.length;i++){ if(S[i].id===id) return S[i]; } return null; }

  /* ---------------- into the garden ----------------
     The shoot's own rose hedge, filmed, which parts to let you in. Shows once
     per session. Any tap, scroll or key opens it. Skipped entirely for
     reduced-motion, for a repeat visit, and for anyone arriving on a deep link
     (an EDM pointing at #where should land on #where, not on a gate). */
  /* Everything choreographed to the moment of entry (title animation, the
     butterflies' arrival) waits for the garden gate to open. When there is
     no gate this session, entry is immediate. */
  var gardenEntered = false, enterCbs = [];
  function onGardenEnter(cb){
    if (gardenEntered){ cb(); return; }
    enterCbs.push(cb);
  }
  function fireGardenEnter(){
    if (gardenEntered) return;
    gardenEntered = true;
    for (var i = 0; i < enterCbs.length; i++){ try { enterCbs[i](); } catch(e){} }
    enterCbs = [];
  }

  /* the campaign title writes itself across the brand strip, bows out, and
     the logo takes its place. Once per session; never for reduced-motion or
     a deep link; after the garden gate when the gate is showing. */
  function startBrandAnim(){
    if (reduced || window.location.hash) return;
    var hb = byId('hbrand');
    if (!hb) return;
    var seen = null;
    try { seen = window.sessionStorage.getItem('mlbTitle26'); } catch(e){}
    if (seen) return;
    try { window.sessionStorage.setItem('mlbTitle26','1'); } catch(e){}
    hb.classList.add('anim');
  }

  (function(){
    var intro = byId('intro');
    if (!intro){ startBrandAnim(); fireGardenEnter(); return; }
    var seen;
    try { seen = window.sessionStorage.getItem('mlbIntro'); } catch(e){ seen = null; }
    if (reduced || seen || window.location.hash){
      if (intro.parentNode) intro.parentNode.removeChild(intro);
      startBrandAnim();
      fireGardenEnter();
      return;
    }

    if (!window.matchMedia('(pointer: coarse)').matches){
      var verb = byId('introVerb');
      if (verb) verb.textContent = 'Click';
    }
    intro.classList.add('show');

    /* Start whichever clip matches this viewport. Phones get the portrait cut
       so we are not upscaling a 16:9 frame across a tall screen. Opening the
       gate scales the foliage up past the lens: a dive into the bushes. */
    var portrait = window.matchMedia('(max-aspect-ratio: 1/1)').matches;
    var poster = portrait ? 'intro-garden-p.jpg' : 'intro-garden.jpg';
    var vid = byId('introVid');
    if (vid){
      var src = portrait ? 'intro-garden-p.mp4' : 'intro-garden.mp4';
      vid.setAttribute('poster', asset(poster));
      vid.src = asset(src);
      var p = vid.play();
      if (p && p.catch) p.catch(function(){ /* poster carries it */ });
    }

    var prevOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    var opened = false;

    function open(){
      if (opened) return;
      opened = true;
      try { window.sessionStorage.setItem('mlbIntro','1'); } catch(e){}
      intro.classList.add('open');
      document.body.style.overflow = prevOverflow;
      ga('intro_open', {});
      window.setTimeout(startBrandAnim, 500);
      window.setTimeout(fireGardenEnter, 450);
      window.setTimeout(function(){
        if (vid){ try { vid.pause(); vid.removeAttribute('src'); vid.load(); } catch(e){} }
        if (intro.parentNode) intro.parentNode.removeChild(intro);
      }, 1600);
    }

    intro.addEventListener('click', open);
    intro.addEventListener('keydown', function(e){
      if (e.key === 'Enter' || e.key === ' ' || e.key === 'Escape'){ e.preventDefault(); open(); }
    });
    window.addEventListener('wheel', open, {passive:true, once:true});
    window.addEventListener('touchmove', open, {passive:true, once:true});
    window.addEventListener('keydown', open, {once:true});
    /* Never trap anyone: it opens on its own after a few seconds of no input. */
    window.setTimeout(open, 7000);
    intro.focus({preventScroll:true});
  })();

  /* ---------------- drifting petals ----------------
     Real defocused rose petals cut from the campaign shoot, so they read as
     petals passing the lens rather than CSS confetti. Off for reduced-motion,
     paused when the tab is hidden, and thinned right out on small screens. */
  (function(){
    var cv = byId('petals');
    if (!cv || reduced) { if (cv) cv.style.display = 'none'; return; }
    var ctx = cv.getContext('2d');
    var imgs = [], loaded = 0, N = 4;
    for (var i=0;i<N;i++){
      var im = new Image();
      im.onload = function(){ loaded++; };
      im.src = asset('petal' + i + '.png');
      imgs.push(im);
    }
    /* 1.5x is indistinguishable for soft defocused petals and halves the
       pixels pushed per frame on a 3x phone screen */
    var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    var coarse = window.matchMedia('(pointer: coarse)').matches;
    var tick = 0;
    var W = 0, H = 0, petals = [], raf = null;

    function count(){
      var a = window.innerWidth * window.innerHeight;
      return Math.max(7, Math.min(20, Math.round(a / 78000)));
    }
    function mk(seedTop){
      return {
        img: imgs[(Math.random()*N)|0],
        x: Math.random()*W,
        y: seedTop ? -80 - Math.random()*H : Math.random()*H,
        s: 0.20 + Math.random()*0.42,
        vy: 12 + Math.random()*24,
        vx: -9 + Math.random()*18,
        rot: Math.random()*Math.PI*2,
        vr: (-0.5 + Math.random())*0.35,
        sw: 0.3 + Math.random()*0.9,
        ph: Math.random()*Math.PI*2,
        op: 0.34 + Math.random()*0.46
      };
    }
    function resize(){
      W = window.innerWidth; H = window.innerHeight;
      cv.width = Math.floor(W*dpr); cv.height = Math.floor(H*dpr);
      cv.style.width = W+'px'; cv.style.height = H+'px';
      ctx.setTransform(dpr,0,0,dpr,0,0);
      var want = count();
      while (petals.length < want) petals.push(mk(false));
      if (petals.length > want) petals.length = want;
    }
    var last = 0;
    function frame(t){
      raf = window.requestAnimationFrame(frame);
      /* phones draw every other frame: 30fps is plenty for drifting petals */
      if (coarse && (tick++ & 1)) return;
      if (!last) last = t;
      var dt = Math.min((t-last)/1000, 0.07); last = t;
      ctx.clearRect(0,0,W,H);
      if (loaded === 0) return;
      for (var i=0;i<petals.length;i++){
        var p = petals[i];
        p.ph += dt*p.sw;
        p.y += p.vy*dt;
        p.x += (p.vx + Math.sin(p.ph)*14)*dt;
        p.rot += p.vr*dt;
        if (p.y - 120 > H) { petals[i] = mk(true); continue; }
        if (p.x < -140) p.x = W + 120; else if (p.x > W + 140) p.x = -120;
        if (!p.img || !p.img.width) continue;
        ctx.save();
        ctx.globalAlpha = p.op;
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rot);
        ctx.drawImage(p.img, -p.img.width*p.s/2, -p.img.height*p.s/2,
                      p.img.width*p.s, p.img.height*p.s);
        ctx.restore();
      }
    }
    function start(){ if (raf === null){ last = 0; raf = window.requestAnimationFrame(frame); } }
    function stop(){ if (raf !== null){ window.cancelAnimationFrame(raf); raf = null; } }
    resize();
    window.addEventListener('resize', resize, {passive:true});
    document.addEventListener('visibilitychange', function(){
      if (document.hidden) stop(); else start();
    });
    start();
  })();

  /* ---------------- jump nav ---------------- */
  var links = [].slice.call(document.querySelectorAll('.jump a[href^="#"]'));
  var secs  = links.map(function(a){ return byId(a.getAttribute('href').slice(1)); });
  var bar = byId('navProgress');
  var navEl = document.querySelector('nav.jump');
  var navIn = navEl ? navEl.querySelector('.in') : null;
  function onScroll(){
    var h = document.documentElement.scrollHeight - window.innerHeight;
    if (bar) bar.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + '%';
    var idx = -1;
    for (var i=0;i<secs.length;i++){
      if (secs[i] && secs[i].getBoundingClientRect().top <= 120) idx = i;
    }
    links.forEach(function(a,i){
      var on = i===idx;
      if (on && !a.classList.contains('active') && navIn){
        /* keep the active section's tab in view as you read down the page */
        var r = a.getBoundingClientRect(), n = navIn.getBoundingClientRect();
        if (r.left < n.left + 10 || r.right > n.right - 10){
          navIn.scrollTo({left: a.offsetLeft - 24, behavior:'smooth'});
        }
      }
      a.classList.toggle('active', on);
    });
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  window.addEventListener('resize', onScroll, {passive:true});
  onScroll();
  /* edge fades: show only where there is more bar to slide to */
  if (navIn && navEl){
    var navEdges = function(){
      var max = navIn.scrollWidth - navIn.clientWidth;
      navEl.classList.toggle('at-end', navIn.scrollLeft >= max - 4);
      navEl.classList.toggle('scrolled', navIn.scrollLeft > 4);
    };
    navIn.addEventListener('scroll', navEdges, {passive:true});
    window.addEventListener('resize', navEdges, {passive:true});
    navEdges();
  }

  /* ---------------- keepsake category carousels ---------------- */
  var catState = {};
  [].slice.call(document.querySelectorAll('.cat')).forEach(function(sec){
    var panels = [].slice.call(sec.querySelectorAll('.cpanel'));
    if (!panels.length) return;
    var thumbs = [].slice.call(sec.querySelectorAll('.cthumb'));
    var cnt = sec.querySelector('.cat-arrows .cnt');
    var st = {sec:sec, panels:panels, thumbs:thumbs, cnt:cnt, idx:0};
    catState[sec.dataset.cat] = st;
    function go(n){
      st.idx = (n + panels.length) % panels.length;
      panels.forEach(function(p,i){ p.classList.toggle('on', i===st.idx); });
      thumbs.forEach(function(t,i){ t.classList.toggle('on', i===st.idx); });
      if (cnt) cnt.textContent = (st.idx+1) + ' / ' + panels.length;
      ga('keepsake_switch', {category: sec.dataset.cat, item_id: panels[st.idx].dataset.kid});
    }
    st.go = go;
    thumbs.forEach(function(t){
      t.addEventListener('click', function(){ go(parseInt(t.dataset.idx, 10)); });
    });
    var prev = sec.querySelector('.cnav.prev'), next = sec.querySelector('.cnav.next');
    if (prev) prev.addEventListener('click', function(){ go(st.idx - 1); });
    if (next) next.addEventListener('click', function(){ go(st.idx + 1); });
  });

  /* Any link to #k-<id> (hero hotspots, gift matcher, builder, artist feature)
     first flips the right category to that product, then scrolls to it. */
  function revealKeepsake(id, scroll){
    for (var c in catState){
      var st = catState[c];
      for (var i=0;i<st.panels.length;i++){
        if (st.panels[i].dataset.kid === id){
          st.go(i);
          if (scroll !== false){
            st.sec.scrollIntoView({behavior: reduced ? 'auto' : 'smooth', block:'start'});
          }
          return true;
        }
      }
    }
    return false;
  }
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a[href^="#k-"]');
    if (!a) return;
    var id = a.getAttribute('href').slice(3);
    if (revealKeepsake(id)) e.preventDefault();
  });
  if (window.location.hash && window.location.hash.indexOf('#k-') === 0){
    revealKeepsake(window.location.hash.slice(3));
  }

  /* ---------------- hero hotspots ----------------
     Markers pinned to the products inside the hero photograph. The photo is
     object-fit:cover, so each marker's percentage position (in image space)
     is mapped through the same cover maths on every resize. */
  (function(){
    var fig = byId('heroFig'), layer = byId('hspots'), img = byId('heroImg');
    if (!fig || !layer || !img) return;
    /* [x%, y%, keepsake id] measured on the master frames */
    var LAND = [
      [56, 70.5, 'the-painted-garden-box'],
      [46, 41, 'tote-of-bliss'],
      [29, 50, 'blossom-drawer-chest'],
      [51, 52, 'tote-of-good-health'],
      [52.5, 60, 'a-court-of-peonies'],
      [48, 57.5, 'treasure-scroll'],
      [41, 55, 'a-court-of-peonies-duo'],
      [41, 59.5, 'the-painted-garden-duo'],
      [45.5, 62, 'the-dawn'],
      [58, 64, 'the-painted-garden'],
      [70, 60, 'elegance-reunion-turntable'],
      [43, 69, 'the-dusk'],
      [68, 68, 'weaving-moments']
    ];
    var PORT = [
      [57, 71.5, 'the-painted-garden-box'],
      [46.5, 39.5, 'tote-of-bliss'],
      [21, 52, 'blossom-drawer-chest'],
      [55, 54, 'tote-of-good-health'],
      [52, 62, 'a-court-of-peonies'],
      [45, 59, 'treasure-scroll'],
      [36, 58.5, 'a-court-of-peonies-duo'],
      [35, 63.5, 'the-painted-garden-duo'],
      [42, 65, 'the-dawn'],
      [60, 66, 'the-painted-garden'],
      [72, 60, 'elegance-reunion-turntable'],
      [40, 72, 'the-dusk'],
      [74, 68, 'weaving-moments']
    ];
    function kOf(id){
      for (var i=0;i<K.length;i++){ if (K[i].id===id) return K[i]; }
      return null;
    }
    function nameOf(id){ var k = kOf(id); return k ? k.name : ''; }
    /* ---- butterfly colours ----------------------------------------------
       Every hue below already appears in the collection's floral artwork, so
       the flock reads as part of the photograph rather than as UI dropped on
       top of it. Each pair is [upper wing, lower wing]; the cream outline and
       cocoa body are shared, which is what holds them together as one set. */
    var WING = {
      gold:       ['#C7A66A', '#A8874B'],
      jade:       ['#2F8A72', '#216450'],
      coral:      ['#E2673F', '#BE4B2A'],
      raspberry:  ['#C63F6D', '#9E2C55'],
      cornflower: ['#5C7CC4', '#42599E'],
      marigold:   ['#E3A63C', '#BE8322'],
      plum:       ['#7E4E7C', '#5E3760']
    };
    /* Assigned against the surface each butterfly lands on, sampled off the
       hero frame, so no butterfly wears its own product's colour: teal tote
       gets coral, fuchsia tote gets jade, terracotta bag gets jade, mint bag
       gets coral, and the pale tins get the deeper hues. Neighbouring spots
       never share a colour. */
    var SPOT_WING = {
      'the-painted-garden-box':     'raspberry',
      'tote-of-bliss':              'coral',
      'blossom-drawer-chest':       'cornflower',
      'tote-of-good-health':        'jade',
      'a-court-of-peonies':         'gold',
      'treasure-scroll':            'cornflower',
      'a-court-of-peonies-duo':     'raspberry',
      'the-painted-garden-duo':     'marigold',
      'the-dawn':                   'plum',
      'the-painted-garden':         'jade',
      'elegance-reunion-turntable': 'cornflower',
      'the-dusk':                   'jade',
      'weaving-moments':            'coral'
    };
    var BFLY = '<svg viewBox="0 0 48 48" aria-hidden="true">' +
      '<g class="wl">' +
        '<path class="w1" d="M21.5 22.5 C16 10 4 6 3.5 14.5 C3.2 20 10 24.5 21.5 25.5 Z"/>' +
        '<path class="w2" d="M21.5 27 C13 27.5 7 33 9.5 38.5 C11.8 43 19 39.5 22 30.5 Z"/>' +
      '</g>' +
      '<g class="wr">' +
        '<path class="w1" d="M26.5 22.5 C32 10 44 6 44.5 14.5 C44.8 20 38 24.5 26.5 25.5 Z"/>' +
        '<path class="w2" d="M26.5 27 C35 27.5 41 33 38.5 38.5 C36.2 43 29 39.5 26 30.5 Z"/>' +
      '</g>' +
      '<ellipse cx="24" cy="26" rx="2.1" ry="8.2"/>' +
      '<path class="ant" d="M23 19 C21.5 14.5 18.5 11.5 15.5 10.5 M25 19 C26.5 14.5 29.5 11.5 32.5 10.5"/>' +
      '</svg>';
    /* the card a butterfly opens: product photo, name, and a button through */
    var pop = document.createElement('div');
    pop.className = 'hpop';
    layer.appendChild(pop);
    var popFor = null;
    function closePop(){ pop.classList.remove('on'); popFor = null; }
    function openPop(id, b){
      if (popFor === id && pop.classList.contains('on')){ closePop(); return; }
      var k = kOf(id); if (!k) return;
      popFor = id;
      pop.innerHTML =
        '<img src="assets/' + k.img + '?v={{AV}}" alt="">' +
        '<button type="button" class="hp-x" aria-label="Close">&times;</button>' +
        '<div class="hp-b">' +
          '<span class="hp-n">' + esc(k.name) + '</span>' +
          '<span class="hp-m">' + esc(k.cn) + ' &middot; ' + esc(k.format) + '</span>' +
          '<a class="btn gold sm" href="#k-' + k.id + '">See the product</a>' +
        '</div>';
      pop.classList.add('on');
      var cw = fig.clientWidth, ch = fig.clientHeight;
      var x = parseFloat(b.style.left) || 0, y = parseFloat(b.style.top) || 0;
      var pw = pop.offsetWidth || 260, ph = pop.offsetHeight || 240;
      var left = Math.max(10, Math.min(x - pw/2, cw - pw - 10));
      /* the card sits above the butterfly so it never covers the product;
         it only drops below when there is no room overhead */
      var top = (y - ph - 40 < 10) ? (y + 36) : (y - ph - 40);
      if (top + ph > ch - 10) top = Math.max(10, ch - ph - 10);
      pop.style.left = left + 'px'; pop.style.top = top + 'px';
    }
    pop.addEventListener('click', function(e){
      if (e.target.closest && e.target.closest('.hp-x')){ closePop(); return; }
      if (e.target.closest && e.target.closest('a')) closePop();
    });
    /* a tap anywhere that isn't the card or a butterfly puts the card away */
    document.addEventListener('click', function(e){
      if (!pop.classList.contains('on')) return;
      var t = e.target;
      if (t.closest && (t.closest('.hpop') || t.closest('.hspot'))) return;
      closePop();
    });
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape') closePop();
    });
    /* one quiet hint that the butterflies open the collection */
    var tip = document.createElement('div');
    tip.className = 'htip';
    var tipVerb = window.matchMedia('(hover: hover)').matches ? 'Hover over' : 'Tap';
    tip.innerHTML = BFLY + '<span>' + tipVerb + ' a butterfly to discover the collection</span>';
    layer.appendChild(tip);
    var tipSeen = null;
    try { tipSeen = window.sessionStorage.getItem('mlbHtip'); } catch(e){}
    function hideTip(){ tip.classList.remove('on'); }
    /* the flock (and its hint) hold until the visitor steps through the gate */
    layer.classList.add('waiting');
    onGardenEnter(function(){
      layer.classList.remove('waiting');
      if (!tipSeen){
        window.setTimeout(function(){
          /* checked here, not above: this callback can run before the tally
             below has read its saved count, and a hint drawn over a tally
             that is already on screen is what a returning visitor saw */
          if (foundN) return;
          tip.classList.add('on');
          try { window.sessionStorage.setItem('mlbHtip','1'); } catch(e){}
          window.setTimeout(hideTip, 9000);
        }, 2600);
      }
    });
    /* ---- the tally -------------------------------------------------------
       Thirteen butterflies mark thirteen keepsakes, and the risk is that
       someone opens the two nearest their thumb and scrolls on. So every
       butterfly opened is counted, and finding the whole garden hands them
       on to the Gift Matcher. Session-scoped, like the intro gate, so a
       return visit is a fresh garden. Verified reachable at every viewport
       from 320px up: no butterfly is ever cropped out of the frame. */
    var TOTAL = LAND.length;
    var found = {}, foundN = 0, doneShown = false;
    try {
      var saved = window.sessionStorage.getItem('mlbFound26');
      if (saved){
        saved.split(',').forEach(function(id){ if (id){ found[id] = 1; foundN++; } });
      }
    } catch(e){}
    var tally = document.createElement('div');
    tally.className = 'htally';
    tally.setAttribute('aria-live', 'polite');
    layer.appendChild(tally);

    function drawTally(){
      hideTip();
      if (foundN >= TOTAL){
        tally.classList.add('done');
        tally.innerHTML = BFLY +
          '<span class="thn">You\\'ve found the whole garden. ' +
          '<span class="han">\\u82B1\\u6708\\u60C5\\u957F</span></span>' +
          '<a class="tgo" href="#concierge" data-tally-go="1">Try our gift matcher</a>';
      } else {
        tally.innerHTML =
          '<span class="tn"><b>' + foundN + '</b> / ' + TOTAL + '</span>' +
          '<span class="tl">found</span>' +
          '<span class="tbar"><i style="width:' +
            Math.round(foundN / TOTAL * 100) + '%"></i></span>';
      }
      tally.classList.add('on');
    }
    tally.addEventListener('click', function(e){
      if (e.target.closest && e.target.closest('[data-tally-go]')) ga('garden_complete_go', {});
    });

    function markFound(id){
      if (found[id]) return;
      found[id] = 1; foundN++;
      try {
        window.sessionStorage.setItem('mlbFound26', Object.keys(found).join(','));
      } catch(e){}
      var b = spotFor(id);
      if (b) b.classList.add('found');
      drawTally();
      if (foundN >= TOTAL && !doneShown){
        doneShown = true;
        ga('garden_complete', {});
      }
    }
    /* a returning visitor keeps the count they had */
    if (foundN) onGardenEnter(function(){ window.setTimeout(drawTally, 900); });

    var spots = LAND.map(function(s, i){
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'hspot';
      /* flight start point: spread around the compass so the flock arrives
         from every direction, each a beat behind the one before */
      var ang = (i * 137.5) % 360 * Math.PI / 180;
      var dist = 300 + (i % 3) * 140;
      b.style.setProperty('--fx', Math.round(Math.cos(ang) * dist) + 'px');
      b.style.setProperty('--fy', Math.round(Math.sin(ang) * dist * 0.7 - 70) + 'px');
      b.style.setProperty('--fd', (0.25 + i * 0.2).toFixed(2) + 's');
      var w = WING[SPOT_WING[s[2]]] || WING.gold;
      b.style.setProperty('--bw', w[0]);
      b.style.setProperty('--bw2', w[1]);
      b.addEventListener('animationend', function(e){
        if (e.animationName === 'flyin') b.classList.add('landed');
      });
      b.setAttribute('aria-label', 'See ' + nameOf(s[2]));
      b.innerHTML = BFLY + '<span class="hlabel">' + esc(nameOf(s[2])) + '</span>';
      if (found[s[2]]) b.classList.add('found');
      b.addEventListener('click', function(){
        hideTip();
        ga('hotspot_click', {item_id: s[2]});
        openPop(s[2], b);
        markFound(s[2]);
      });
      b.addEventListener('mouseenter', hideTip);
      layer.appendChild(b);
      return b;
    });
    function spotFor(id){
      for (var i=0;i<LAND.length;i++){ if (LAND[i][2] === id) return spots[i]; }
      return null;
    }
    function place(){
      closePop();
      var cw = fig.clientWidth, ch = fig.clientHeight;
      var portrait = (img.currentSrc || img.src).indexOf('-p.webp') >= 0;
      var iw = portrait ? 900 : 1500, ih = portrait ? 1200 : 1500;
      var data = portrait ? PORT : LAND;
      var sc = Math.max(cw/iw, ch/ih);
      var dw = iw*sc, dh = ih*sc;
      /* matches the CSS object-position: 50% 40% on the portrait cut,
         50% 58% on the wide full-screen crop */
      var yp = (portrait || cw < 760) ? 0.4 : 0.58;
      var ox = (cw - dw) * 0.5, oy = (ch - dh) * yp;
      var pos = spots.map(function(b, i){
        return {x: ox + data[i][0]/100*dw, y: oy + data[i][1]/100*dh};
      });
      /* Keep every butterfly tappable. Several products sit shoulder to
         shoulder in the frame, and at phone width their markers overlapped by
         more than half a marker, which put one of them physically underneath
         another and out of reach. Butterflies hover rather than sit, so a few
         pixels of drift costs nothing: push any overlapping pair apart until
         each has its own target, capped so none strays off its product. */
      var size = spots[0] ? (spots[0].offsetWidth || 52) : 52;
      var minGap = size * 1.06, cap = size * 0.85;
      for (var pass = 0; pass < 4; pass++){
        var moved = false;
        for (var a = 0; a < pos.length; a++){
          for (var c = a + 1; c < pos.length; c++){
            var dx = pos[c].x - pos[a].x, dy = pos[c].y - pos[a].y;
            var d = Math.sqrt(dx*dx + dy*dy);
            if (d >= minGap) continue;
            if (d < 0.01){ dx = (a % 2 ? 1 : -1); dy = 1; d = 1; }
            var push = (minGap - d) / 2, ux = dx/d, uy = dy/d;
            pos[a].x -= ux*push; pos[a].y -= uy*push;
            pos[c].x += ux*push; pos[c].y += uy*push;
            moved = true;
          }
        }
        if (!moved) break;
      }
      spots.forEach(function(b, i){
        var hx = ox + data[i][0]/100*dw, hy = oy + data[i][1]/100*dh;
        /* never let the relaxation walk a butterfly off its own product */
        var ddx = pos[i].x - hx, ddy = pos[i].y - hy;
        var dd = Math.sqrt(ddx*ddx + ddy*ddy);
        if (dd > cap){ pos[i].x = hx + ddx/dd*cap; pos[i].y = hy + ddy/dd*cap; }
        var x = pos[i].x, y = pos[i].y;
        var vis = x > 26 && x < cw-26 && y > 26 && y < ch-26;
        b.style.display = vis ? '' : 'none';
        b.style.left = x + 'px'; b.style.top = y + 'px';
        b.classList.toggle('edge-l', x < 90);
        b.classList.toggle('edge-r', x > cw-90);
      });
    }
    if (img.complete) place(); else img.addEventListener('load', place);
    window.addEventListener('resize', place, {passive:true});
    /* rest the wings while the hero is off screen: 12 looping animations are
       cheap on screen and pure waste off it */
    if ('IntersectionObserver' in window){
      var io = new IntersectionObserver(function(en){
        layer.classList.toggle('offstage', !en[0].isIntersecting);
      }, {rootMargin: '100px'});
      io.observe(fig);
    }
  })();

  /* ---------------- back to previous section / top ----------------
     Two fixed buttons that appear once the reader is into the page: one walks
     back up section by section, the other returns straight to the top. */
  (function(){
    var bk = byId('backer'), prev = byId('bkPrev'), top = byId('bkTop');
    if (!bk || !prev || !top) return;
    var ids = ['concierge','keepsakes','builder','mooncakes','garden','where'];
    function go(target){
      /* self-animated ease-out. The page sets scroll-behavior:smooth, which
         turns every plain scrollTo into a competing smooth scroll, so CSS
         smoothness is suspended for the duration and restored after. */
      target = Math.max(0, target);
      var html = document.documentElement, prevSB = html.style.scrollBehavior;
      html.style.scrollBehavior = 'auto';
      function done(){ html.style.scrollBehavior = prevSB; }
      if (reduced){ window.scrollTo(0, target); done(); return; }
      var start = window.scrollY, d = target - start, t0 = null, fired = false;
      var dur = Math.min(900, 320 + Math.abs(d) * 0.05);
      function step(ts){
        fired = true;
        if (t0 === null) t0 = ts;
        var p = Math.min(1, (ts - t0) / dur);
        var e = 1 - Math.pow(1 - p, 3);
        window.scrollTo(0, start + d * e);
        if (p < 1) requestAnimationFrame(step); else done();
      }
      requestAnimationFrame(step);
      /* frames can be suspended (background webviews, some embeds): jump instead */
      setTimeout(function(){ if (!fired){ window.scrollTo(0, target); done(); } }, 180);
    }
    prev.addEventListener('click', function(){
      var y = window.scrollY, navh = 58, cur = -1;
      var tops = [];
      for (var i=0;i<ids.length;i++){
        var el = byId(ids[i]);
        if (el) tops.push(el.getBoundingClientRect().top + y - navh - 14);
      }
      for (var j=0;j<tops.length;j++){ if (tops[j] <= y + 8) cur = j; }
      /* deep inside a section: first return to its start; already at a
         section's start: step up to the one before it */
      if (cur >= 0 && y > tops[cur] + 40) go(tops[cur]);
      else if (cur >= 1) go(tops[cur - 1]);
      else go(0);
    });
    top.addEventListener('click', function(){ go(0); });
    var shown = null;
    function vis(){
      var on = window.scrollY > 600;
      if (on !== shown){ shown = on; bk.classList.toggle('on', on); }
    }
    window.addEventListener('scroll', vis, {passive:true});
    window.addEventListener('resize', vis, {passive:true});
    vis();
  })();

  /* ---------------- nearest booth finder ----------------
     A postal code (or any address text) goes to OneMap, Singapore's national
     geocoder, and the three closest booths come back with their dates. */
  (function(){
    var form = byId('nearForm'), inp = byId('nearIn'), out = byId('nearOut');
    if (!form || !inp || !out) return;
    function distKm(a1, o1, a2, o2){
      var rad = Math.PI / 180, R = 6371;
      var dLa = (a2 - a1) * rad, dLo = (o2 - o1) * rad;
      var s = Math.sin(dLa/2) * Math.sin(dLa/2) +
              Math.cos(a1 * rad) * Math.cos(a2 * rad) * Math.sin(dLo/2) * Math.sin(dLo/2);
      return 2 * R * Math.asin(Math.sqrt(s));
    }
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var q = (inp.value || '').replace(/\\D/g, '');
      if (q.length !== 6){
        out.hidden = false;
        out.innerHTML = '<p class="near-note">Please enter your 6 digit postal code.</p>';
        inp.focus();
        return;
      }
      out.hidden = false;
      out.innerHTML = '<p class="near-note">Finding booths near ' + esc(q) + '\\u2026</p>';
      ga('booth_search', {});
      fetch('https://www.onemap.gov.sg/api/common/elastic/search?searchVal=' +
            encodeURIComponent(q) + '&returnGeom=Y&getAddrDetails=N&pageNum=1')
        .then(function(r){ return r.json(); })
        .then(function(d){
          var r0 = d && d.results && d.results[0];
          if (!r0 || !r0.LATITUDE){
            out.innerHTML = '<p class="near-note">We couldn\\u2019t place that postal code. ' +
              'Please check the 6 digits and try again.</p>';
            return;
          }
          var la = parseFloat(r0.LATITUDE), lo = parseFloat(r0.LONGITUDE);
          var ranked = B.map(function(b){ return { b: b, d: distKm(la, lo, b.lat, b.lng) }; })
            .sort(function(x, y){ return x.d - y.d; }).slice(0, 3);
          out.innerHTML = '<p class="near-note">Closest to you \\u00B7 tap one to see it on the map</p>' +
            ranked.map(function(r){
              return '<button type="button" class="near-item" data-near="' + r.b.id + '">' +
                '<span class="ni-n">' + esc(r.b.name) + '</span>' +
                '<span class="ni-d">' + (r.d < 1 ? Math.round(r.d * 1000) + ' m' : r.d.toFixed(1) + ' km') + '</span>' +
                '<span class="ni-m">' + esc(r.b.level) + ' \\u00B7 ' + esc(r.b.dates) + '</span>' +
                '</button>';
            }).join('');
        })
        .catch(function(){
          out.innerHTML = '<p class="near-note">The lookup didn\\u2019t respond. Please try again in a moment.</p>';
        });
    });
    out.addEventListener('click', function(e){
      var it = e.target.closest && e.target.closest('.near-item');
      if (!it) return;
      var booth = document.querySelector('.booth[data-loc="' + it.dataset.near + '"]');
      if (booth) booth.click();
    });
  })();

  /* ---------------- outbound click tracking ---------------- */
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a');
    if(!a) return;
    if(a.dataset.order) ga('order_click', {item_id:a.dataset.order, item_name:a.dataset.name});
    if(a.dataset.booth) ga('booth_click', {item_id:a.dataset.booth, item_name:a.dataset.name});
    if(a.dataset.brochure) ga('brochure_download', {});
    if(a.dataset.bcf) ga('bcf_click', {placement:a.dataset.bcf});
    if(a.dataset.news) ga('newsletter_click', {placement:a.dataset.news});
  });

  /* ---------------- gift matcher ---------------- */
  var ans = {}, step = 0;
  var qs = [].slice.call(document.querySelectorAll('.q'));
  var pips = [].slice.call(document.querySelectorAll('.qsteps i'));

  function show(n){
    step = n;
    qs.forEach(function(q,i){ q.classList.toggle('on', i===n); });
    pips.forEach(function(p,i){ p.classList.toggle('on', i<=n); });
    byId('cResult').classList.remove('on');
    byId('cQuiz').style.display = '';
  }

  qs.forEach(function(q, qi){
    q.querySelectorAll('.opt').forEach(function(btn){
      btn.addEventListener('click', function(){
        ans[q.dataset.key] = btn.dataset.val;
        if (qi < qs.length - 1) { show(qi + 1); }
        else { finish(); }
      });
    });
  });
  [].slice.call(document.querySelectorAll('.qback')).forEach(function(b){
    b.addEventListener('click', function(){ if(step>0) show(step-1); });
  });

  /* Snowskin has to be kept chilled, so it cannot go on a plane. Someone
     heading overseas is therefore a HARD veto on set G, and it outranks the
     chilled answer: pick "heading overseas" + "happy with chilled snowskin"
     and you get a baked match with an on-screen explanation, never snowskin. */
  function travelling(){ return ans.recipient === 'traveller'; }
  function wantsChilled(){ return ans.table === 'chilled' && !travelling(); }
  function snowskinOnly(k){
    return k.sets.length > 0 && k.sets.indexOf('G') >= 0 &&
           k.sets.join('').replace(/G/g, '') === '';
  }
  /* Set the customer's table answer points at, after the travel veto. The
     adventurous answer falls back to the Signature baked set, its closest
     room-temperature equivalent. */
  function wantSet(){
    if (travelling() && ans.table === 'chilled') return 'D';
    return TABLE_SET[ans.table];
  }
  function suppressedSnowskin(){ return travelling() && ans.table === 'chilled'; }

  function pool(){
    var b = BUDGET[ans.budget];
    var hard = K.filter(function(k){
      if (ans.table === 'halal' && !k.halalSafe) return false;
      if (travelling()   && snowskinOnly(k)) return false;
      if (wantsChilled() && k.sets.indexOf('G') < 0) return false;
      if (ans.budget !== 'b4'){ if (k.price <= b.min || k.price > b.max) return false; }
      return true;
    });
    if (hard.length) return {list:hard, relaxed:false};
    /* Nothing survived. Drop the budget rail last, and say so on screen. */
    var soft = K.filter(function(k){
      if (ans.table === 'halal' && !k.halalSafe) return false;
      if (travelling()   && snowskinOnly(k)) return false;
      if (wantsChilled() && k.sets.indexOf('G') < 0) return false;
      return true;
    });
    if (!soft.length){
      /* Last resort still respects the travel veto. */
      soft = K.filter(function(k){ return !(travelling() && snowskinOnly(k)); });
    }
    return {list:soft.length ? soft : K.slice(), relaxed:true};
  }

  function scoreOf(k){
    var s = (k.score[ans.recipient]||0) * 2 + (k.score[ans.priority]||0) * 3;
    var want = wantSet();
    if (k.sets.length && k.sets.indexOf(want) < 0) s -= 3;   /* wrong mooncake family */
    if (ans.budget === 'b4' && k.price >= 78) s += 1;        /* corporate leans premium */
    if (k.channel === 'online') s += 0.5;                    /* tiebreak: buyable now */
    return s;
  }

  function recSet(k){
    if (!k.sets.length) return null;
    var want = wantSet();
    if (k.sets.indexOf(want) >= 0) return want;
    /* Never hand a traveller the snowskin set as a fallback. */
    var ok = travelling() ? k.sets.filter(function(x){ return x !== 'G'; }) : k.sets;
    return ok.length ? ok[0] : null;
  }

  function finish(){
    var p = pool();
    var ranked = p.list.slice().sort(function(a,b){ return scoreOf(b) - scoreOf(a); });
    render(ranked[0], ranked[1], p.relaxed);
    ga('concierge_complete', {
      recipient: ans.recipient, priority: ans.priority,
      table: ans.table, budget: ans.budget, match: ranked[0].id
    });
  }

  function render(k, alt, relaxed){
    var st = recSet(k);
    var s = st ? setById(st) : null;
    var recipLabel = RECIP[ans.recipient] || 'them';

    var meta = ['<span class="tag">' + esc(k.format) + ' &middot; ' + esc(k.pcs) + '</span>'];
    if (k.sets.indexOf('G') >= 0) meta.push('<span class="tag chill">Snowskin &middot; chilled</span>');
    else meta.push('<span class="tag sage">Halal certified</span>');
    if (k.bcf) meta.push('<span class="tag charity">$1 to charity</span>');
    if (k.channel === 'booth') meta.push('<span class="tag">At our booths</span>');

    var setLine = s
      ? '<p class="res-note"><strong>Recommended mooncake set ' + s.id + '</strong> &middot; ' +
        esc(s.flavours.join(', ')) + '</p>'
      : (k.duoNote ? '<p class="res-note">' + esc(k.duoNote) + '</p>' : '');

    var cta;
    if (k.channel === 'online'){
      cta = '<a class="btn" href="' + k.url + '" target="_blank" rel="noopener" ' +
            'data-order="' + k.id + '" data-name="' + esc(k.name) + '">Order online</a>';
    } else {
      cta = '<a class="btn gold" href="#where" data-booth="' + k.id +
            '" data-name="' + esc(k.name) + '">Find a booth near you</a>';
    }

    var shareMsg = "For " + recipLabel + " this Mid-Autumn: " + k.name + " " + k.cn +
                   " from Mdm Ling Bakery. " + k.becomes + " " + SITE;

    var html =
      '<div class="res-grid">' +
        '<div class="res-photo"><img src="' + asset(k.img) + '" alt="' + esc(k.alt) + '"></div>' +
        '<div class="res-body">' +
          '<span class="tool-kicker">Your match</span>' +
          '<h4>' + esc(k.name) + (k.variant ? ' <span style="font-weight:400;font-size:.6em;color:var(--muted)">(' + esc(k.variant) + ')</span>' : '') + '</h4>' +
          '<p class="rcn han">' + esc(k.cn) + '</p>' +
          '<p class="rgloss">' + esc(k.pinyin) + ' &middot; ' + esc(k.gloss) + '</p>' +
          '<p class="res-why">For ' + esc(recipLabel) + ', ' + esc(k.why) + '</p>' +
          '<div class="res-meta">' + meta.join('') + '</div>' +
          setLine +
          (suppressedSnowskin()
            ? '<p class="res-note flag"><strong>We\\'ve left snowskin out of this one.</strong> ' +
              'Snowskin mooncakes are kept chilled and they don\\'t survive a journey, ' +
              'so we\\'ve matched something baked instead. It keeps at room temperature ' +
              'and travels in hand luggage without a worry.</p>'
            : '') +
          (relaxed ? '<p class="res-note">Nothing in the collection sits inside that budget with those requirements, so this is the closest fit.</p>' : '') +
          (k.note ? '<p class="res-note">' + esc(k.note) + '</p>' : '') +
          (k.bcf ? '<p class="res-note">Every one of these sends <strong>$1 to the Breast Cancer Foundation</strong>. <a class="tlink" href="' + BCF + '" target="_blank" rel="noopener" data-bcf="match">Read about their work</a></p>' : '') +
          '<div class="res-acts">' + cta +
            '<a class="btn ghost" href="https://wa.me/?text=' + encodeURIComponent(shareMsg) +
              '" target="_blank" rel="noopener" id="cShare">Send to someone</a>' +
            '<button class="qback" id="cAgain" type="button" style="margin:0">Start again</button>' +
          '</div>' +
          '<div class="res-news">' +
            '<p>Sign up to our newsletter and take <strong>$5 off your first order</strong>.' +
              '<span class="tc">T&amp;Cs apply</span></p>' +
            '<a class="btn gold sm" href="' + NEWSLETTER + '" target="_blank" rel="noopener" ' +
              'data-news="match">Sign up and claim your $5</a>' +
          '</div>' +
          (alt ? '<p class="res-alt">Also worth a look: <a href="#k-' + alt.id + '">' + esc(alt.name) +
                 '</a>, ' + esc(alt.becomes.charAt(0).toLowerCase() + alt.becomes.slice(1)) + '</p>' : '') +
        '</div>' +
      '</div>';

    var box = byId('cResult');
    box.innerHTML = html;
    box.classList.add('on');
    byId('cQuiz').style.display = 'none';
    pips.forEach(function(p){ p.classList.add('on'); });
    /* The result is a tall card and it scrolled itself into view, so resetting
       in place left the reader stranded below a quiz that had quietly gone
       back to question one. Take them back up to it, the same way finishing
       took them down to the result. */
    byId('cAgain').addEventListener('click', function(){
      ans = {};
      show(0);
      var sec = byId('concierge');
      (sec || byId('cQuiz')).scrollIntoView({behavior: reduced ? 'auto':'smooth', block:'start'});
    });
    byId('cShare').addEventListener('click', function(){ ga('concierge_share', {match:k.id}); });
    box.scrollIntoView({behavior: reduced ? 'auto':'smooth', block:'start'});
  }

  /* ---------------- build your gift ---------------- */
  var bpick = byId('bPick'), bout = byId('bOut');
  function kById(id){ for (var i=0;i<K.length;i++){ if (K[i].id===id) return K[i]; } return null; }
  CATS.forEach(function(cat){
    var head = document.createElement('span');
    head.className = 'bgroup';
    head.textContent = cat.name;
    bpick.appendChild(head);
    var row = document.createElement('div');
    row.className = 'brow';
    cat.items.forEach(function(id){
      var k = kById(id);
      if (!k) return;
      var c = document.createElement('button');
      c.type = 'button'; c.className = 'chip';
      c.innerHTML = '<span class="cw"><img src="' + asset(k.img) + '" alt="' + esc(k.alt) + '" loading="lazy" decoding="async"></span>' +
        '<span class="cn2">' + esc(k.name) + (k.variant ? ' (' + esc(k.variant) + ')' : '') + '</span>';
      c.addEventListener('click', function(){
        [].slice.call(bpick.querySelectorAll('.chip')).forEach(function(x){ x.classList.remove('on'); });
        c.classList.add('on');
        buildOut(k);
        /* bring the result into view: on a phone the output sits below the
           fold, so a tap otherwise looks like it did nothing */
        window.setTimeout(function(){
          bout.scrollIntoView({behavior: reduced ? 'auto' : 'smooth', block:'start'});
        }, 60);
        ga('builder_select', {item_id:k.id, item_name:k.name});
      });
      row.appendChild(c);
    });
    bpick.appendChild(row);
  });

  function buildOut(k){
    var rows = '';
    if (k.sets.length){
      k.sets.forEach(function(id){
        var s = setById(id);
        rows += '<div class="setrow"><div class="sid">' + s.id + '<small>' + esc(s.group) + '</small></div>' +
                '<ul>' + s.flavours.map(function(f){ return '<li>' + esc(f) + '</li>'; }).join('') + '</ul>' +
                '<div>' + (s.halal ? '<span class="tag sage">Halal certified</span>'
                                   : '<span class="tag chill">Not Halal certified</span>') + '</div></div>';
      });
    } else {
      rows = '<div class="setrow"><div class="sid">Duo</div><ul><li>' + esc(k.duoNote) +
             '</li></ul><div><span class="tag sage">Halal certified</span></div></div>';
    }

    var cta;
    if (k.channel === 'online'){
      cta = '<a class="btn sm" href="' + k.url + '" target="_blank" rel="noopener" data-order="' +
            k.id + '" data-name="' + esc(k.name) + '">Order online</a>';
    } else {
      cta = '<a class="btn sm gold" href="#where" data-booth="' + k.id +
            '" data-name="' + esc(k.name) + '">Find a booth near you</a>';
    }

    bout.innerHTML =
      '<div class="bhead">' +
        '<img src="' + asset(k.img) + '" alt="' + esc(k.alt) + '">' +
        '<div><h4>' + esc(k.name) + '</h4>' +
          '<p class="igloss" style="margin:6px 0 0">' + esc(k.cn) + ' &middot; ' + esc(k.pinyin) + '</p>' +
          '<div class="res-meta" style="margin-top:12px">' +
          '<span class="tag">' + esc(k.format) + ' &middot; ' + esc(k.pcs) + '</span>' +
          '<span class="tag' + (k.channel === 'booth' ? ' gold' : '') + '">' +
            (k.channel === 'booth' ? 'At our booths' : 'Order online') + '</span></div>' +
          '<div class="res-acts" style="margin-top:16px">' + cta +
            '<a class="tlink" href="#k-' + k.id + '">Read its story</a></div>' +
        '</div>' +
      '</div>' +
      (k.sets.length ?
        '<div class="callout" style="margin:0 0 22px">\\uD83C\\uDF15 <strong>No need to overthink it.</strong> ' +
        'We\\u2019ve curated the most popular mooncake set combinations below, so you can order online in one go, ' +
        'pick your preferred delivery date, and let us do the carrying.</div>' : '') +
      '<p class="igloss" style="margin:0 0 14px">Choose one mooncake set to go inside</p>' +
      '<div class="setlist">' + rows + '</div>' +
      '<div class="callout"><strong>Prefer your own mix?</strong> You can customise your preferred ' +
      'flavours at any of our retail points across Singapore. <a href="#where">See where to find us</a></div>' +
      (k.note ? '<p class="res-note">' + esc(k.note) + '</p>' : '') +
      (k.disclaimer ? '<p class="res-note">' + esc(k.disclaimer) + '</p>' : '');
    bout.classList.add('on');
  }

  /* ---------------- photo lightbox ---------------- */
  (function(){
    var lb = byId('lightbox'), lbImg = byId('lbImg'), lbCap = byId('lbCap'), lbClose = byId('lbClose');
    if (!lb) return;
    var prevOverflow, lastFocus;
    function open(src, alt){
      lbImg.src = src; lbImg.alt = alt || '';
      lbCap.textContent = alt || '';
      lastFocus = document.activeElement;
      lb.classList.add('on');
      prevOverflow = document.body.style.overflow;
      document.body.style.overflow = 'hidden';
      lbClose.focus();
    }
    function close(){
      lb.classList.remove('on');
      document.body.style.overflow = prevOverflow;
      lbImg.src = '';
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }
    document.addEventListener('click', function(e){
      var t = e.target.closest && e.target.closest('[data-lightbox]');
      if (t){ open(t.dataset.lightbox, t.dataset.lightboxAlt); return; }
      if (e.target === lb) close();
    });
    lbClose.addEventListener('click', close);
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape' && lb.classList.contains('on')) close();
    });
  })();

  /* ---------------- booth map ---------------- */
  (function(){
    var mapEl = byId('boothMap');
    if (!mapEl || typeof L === 'undefined') return;

    function pinIcon(flag){
      var fill = flag ? '#C7A66A' : '#A97F78';
      var h = flag ? 40 : 34, w = flag ? 30 : 26;
      var svg = '<svg width="' + w + '" height="' + h + '" viewBox="0 0 26 34" xmlns="http://www.w3.org/2000/svg">' +
        '<path d="M13 0C5.8 0 0 5.8 0 13c0 9.4 11 20 12.2 21.1a1.1 1.1 0 0 0 1.6 0C15 33 26 22.4 26 13 26 5.8 20.2 0 13 0z" fill="' + fill + '"/>' +
        '<circle cx="13" cy="13" r="5.4" fill="#FBF8F6"/></svg>';
      return L.divIcon({
        className: 'pin', html: svg, iconSize: [w, h], iconAnchor: [w/2, h], popupAnchor: [0, -h+6]
      });
    }

    var DEFAULT_CENTER = [1.345, 103.82], DEFAULT_ZOOM = 11;
    var map = L.map('boothMap', { scrollWheelZoom: false, attributionControl: true })
      .setView(DEFAULT_CENTER, DEFAULT_ZOOM);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap contributors &copy; CARTO', maxZoom: 18
    }).addTo(map);

    var markers = {};
    B.forEach(function(b){
      var m = L.marker([b.lat, b.lng], { icon: pinIcon(b.flag) }).addTo(map);
      m.bindPopup(
        '<div class="bpop"><p class="bn">' + esc(b.name) + '</p><p class="bl">' + esc(b.level) + '</p>' +
        (b.dates ? '<p class="bd">' + esc(b.dates) + '</p>' : '') +
        (b.flag ? '<span class="bf">Flagship store</span>' : '') +
        '<br><a href="' + b.maps + '" target="_blank" rel="noopener">View on Google Maps &#8599;</a></div>',
        { autoPan: false }
      );
      markers[b.id] = m;
    });

    var boothBtns = [].slice.call(document.querySelectorAll('.booth[data-loc]'));
    boothBtns.forEach(function(btn){
      btn.addEventListener('click', function(){
        var m = markers[btn.dataset.loc];
        if (!m) return;
        boothBtns.forEach(function(x){ x.classList.remove('on'); });
        btn.classList.add('on');
        mapEl.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });
        map.setView(m.getLatLng(), 15, { animate: false });
        m.openPopup();
        ga('booth_map_open', { location: btn.dataset.loc });
      });
    });

    var resetBtn = byId('boothMapReset');
    if (resetBtn) resetBtn.addEventListener('click', function(){
      boothBtns.forEach(function(x){ x.classList.remove('on'); });
      map.closePopup();
      map.setView(DEFAULT_CENTER, DEFAULT_ZOOM, { animate: true });
    });
  })();
})();
"""


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------
def check_anchors(html):
    """Every in-page link must land on something.

    The 'find the whole garden' button shipped pointing at #gift when the Gift
    Matcher's anchor is #concierge, so it silently did nothing. Nothing caught
    it, because a bad hash is not an error in a browser: it just fails to
    scroll. This turns that class of bug into a failed build.
    """
    ids = set(re.findall(r'\sid="([^"]+)"', html))
    # only plain literal anchors; the JS builds some hrefs by concatenation
    # ('#k-' + k.id) and those resolve at runtime, not here
    links = set(re.findall(r'href="#([A-Za-z0-9_-]+)"', html))
    dead = sorted(l for l in links if l not in ids)
    if dead:
        raise SystemExit("Links point at anchors that do not exist: %s" % dead)


def build():
    check_layout_covers_data()

    js = fill(
        JS,
        KEEPSAKES=json.dumps(js_data(), ensure_ascii=False, separators=(",", ":")),
        SETS=json.dumps(SETS, ensure_ascii=False, separators=(",", ":")),
        CATS=json.dumps([{"id": c["id"], "name": c["name"], "items": c["items"]}
                         for c in CATEGORIES], ensure_ascii=False, separators=(",", ":")),
        BOOTHS=json.dumps(booths_json(), ensure_ascii=False, separators=(",", ":")),
        TABLESET=json.dumps({t[0]: t[2] for t in TABLES}, ensure_ascii=False),
        BUDGET=json.dumps({b[0]: {"min": b[2], "max": b[3]} for b in BUDGETS}, ensure_ascii=False),
        RECIP=json.dumps({r[0]: r[2] for r in RECIPIENTS}, ensure_ascii=False),
        WACUST=WA_CUSTOMER, SITE=SITE_URL, AV=ASSET_V, BCF=BCF_URL,
        NEWSLETTER=NEWSLETTER,
    )

    def optset(key, opts, n, total, title):
        o = "".join('<button type="button" class="opt" data-val="%s">%s</button>' % (val, lab)
                    for val, lab in opts)
        back = '<button type="button" class="qback">Back</button>' if n > 1 else ""
        return ('<div class="q%s" data-key="%s"><span class="qn">Question %d of %d</span>'
                '<h4>%s</h4><div class="opts">%s</div>%s</div>'
                % (" on" if n == 1 else "", key, n, total, title, o, back))

    qs = "".join([
        optset("recipient", [(r[0], r[1]) for r in RECIPIENTS], 1, 4, "Who are you gifting?"),
        optset("priority", [(p[0], p[1]) for p in PRIORITIES], 2, 4, "What matters most to you here?"),
        optset("table", [(t[0], t[1]) for t in TABLES], 3, 4, "And their table?"),
        optset("budget", [(b[0], b[1]) for b in BUDGETS], 4, 4, "And how much of a moment should it be?"),
    ])

    ranges = ""
    for r in RANGES:
        intro = '<p class="range-intro">%s</p>' % r["intro"] if r["intro"] else ""
        ranges += ('<section class="range" id="%s"><div class="range-head">'
                   '<span class="range-num">%d</span><h3>%s</h3><span class="tag2">%s</span></div>'
                   '%s<div class="flavours">%s</div></section>'
                   % (r["id"], r["n"], r["title"], r["tag"], intro, "".join(r["items"])))

    online = sum(1 for k in KEEPSAKES if k["channel"] == "online")

    # Tag each flavour with the range it sits in. flav() runs in page order as
    # the RANGES literal is built, so walking them in parallel lines up.
    _i = 0
    for r in RANGES:
        for _ in r["items"]:
            if _i < len(FLAV_INDEX):
                FLAV_INDEX[_i]["range"] = r["title"]
            _i += 1

    html = fill(
        TEMPLATE,
        CSS=CSS, JS=js, QS=qs,
        JSONLD=seo.jsonld_block(FLAV_INDEX),
        KEEPSAKES=keepsakes_html(),
        FLAV_OVERVIEW=flavour_overview(),
        RANGES=ranges,
        BOOTHS=booths_html(),
        GA=GA_ID, SITE=SITE_URL, AV=ASSET_V,
        N_KEEPSAKES=len(KEEPSAKES), N_ONLINE=online, N_BOOTHS=len(BOOTHS),
        WA_CUST=wa(WA_CUSTOMER, "Hello! I have a question about your Mid-Autumn 2026 mooncakes."),
        FREE_DEL=FREE_DELIVERY, TEL_CUST="+65 8468 0201",
        BCF=BCF_URL, ARTIST_IG=ARTIST_IG, NEWSLETTER=NEWSLETTER,
    )

    out = os.path.join(HERE, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    left = re.findall(r"\{\{[A-Z_]+\}\}", html)
    if left:
        raise SystemExit("Unfilled placeholders remain: %s" % sorted(set(left)))
    check_anchors(html)
    print("wrote %s  (%.1f KB)" % (out, len(html) / 1024.0))
    print("keepsakes: %d  ·  online: %d  ·  booth: %d"
          % (len(KEEPSAKES), online, len(KEEPSAKES) - online))

    written = seo.write_files(HERE, FLAV_INDEX)
    graph = seo.build_graph(FLAV_INDEX)["@graph"]
    print("seo: %s  ·  %d schema nodes (%d products, %d booth events)"
          % (", ".join(written), len(graph),
             sum(1 for n in graph if n.get("@type") == "Product"),
             sum(1 for n in graph if n.get("@type") == "SaleEvent")))


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mdm Ling Bakery · Mid-Autumn 2026</title>
<meta name="description" content="Mdm Ling Bakery Mid-Autumn 2026. Keepsake gift sets and three mooncake ranges, with a gift matcher to help you choose. 花月情长, A Bond in Lasting Bloom. Halal certified, made in Singapore.">
<link rel="canonical" href="{{SITE}}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Mdm Ling Bakery">
<meta property="og:title" content="Mdm Ling Bakery · Mid-Autumn 2026">
<meta property="og:description" content="Keepsake gift sets built to outlive the season. 花月情长 · A Bond in Lasting Bloom.">
<meta property="og:url" content="{{SITE}}">
<meta property="og:image" content="{{SITE}}assets/og-midautumn-2026-v3.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Mdm Ling Bakery Mid-Autumn 2026 keepsake gift set collection">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Mdm Ling Bakery · Mid-Autumn 2026">
<meta name="twitter:description" content="Keepsake gift sets built to outlive the season. 花月情长 · A Bond in Lasting Bloom.">
<meta name="twitter:image" content="{{SITE}}assets/og-midautumn-2026-v3.jpg">
<meta name="theme-color" content="#4E3C37">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23A97F78'/%3E%3Ctext x='32' y='45' font-size='38' text-anchor='middle' fill='%23F0E2C4' font-family='sans-serif'%3E花%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&family=Work+Sans:wght@500;600&family=Great+Vibes&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&text=%E8%8A%B1%E6%9C%88%E6%83%85%E9%95%BF&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="assets/band-hero.webp?v={{AV}}" imagesrcset="assets/band-hero-p.webp?v={{AV}} 900w, assets/band-hero.webp?v={{AV}} 1500w" imagesizes="100vw">
<script async src="https://www.googletagmanager.com/gtag/js?id={{GA}}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '{{GA}}');
</script>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="author" content="Mdm Ling Bakery">
<!-- Bing Webmaster Tools site verification. Lives here, not in index.html,
     so a rebuild can't delete it and silently un-verify the site. -->
<meta name="msvalidate.01" content="3F11EDA668E40319822CBEE209A010BE" />
<meta name="geo.region" content="SG">
<meta name="geo.placename" content="Singapore">
<link rel="alternate" type="text/plain" href="/llms.txt" title="Plain-text summary for AI answer engines">
{{JSONLD}}
<style>{{CSS}}</style>
</head>
<body>

<!-- Into the garden. Hidden by default so a no-JS visitor never meets a locked door. -->
<div class="intro" id="intro" role="button" tabindex="0" aria-label="Enter the Mid-Autumn 2026 collection">
  <video class="gv" id="introVid" muted playsinline autoplay loop preload="none" aria-hidden="true"></video>
  <div class="veil" aria-hidden="true"></div>
  <div class="seal">
    <img class="s-logo" src="assets/mlb-logo-white.png?v={{AV}}" alt="Mdm Ling Bakery" width="900" height="304">
    <span class="s-en cs-en">A Bond in Lasting Bloom</span>
    <span class="s-han cs-cn">花月情长</span>
    <span class="s-season">Mid-Autumn 2026</span>
    <span class="s-rule"></span>
  </div>
  <div class="prompt"><span id="introVerb">Tap</span> to enter the garden &#127765;<i></i></div>
</div>

<canvas id="petals" aria-hidden="true"></canvas>

<div class="backer" id="backer">
  <button type="button" id="bkPrev" aria-label="Back to the previous section">
    <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 10.5 8 5.5 13 10.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <span>Prev</span>
  </button>
  <button type="button" id="bkTop" aria-label="Back to the top of the page">
    <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8 8 3 13 8 M3 13 8 8 13 13" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <span>Top</span>
  </button>
</div>

<nav class="jump">
  <div class="in">
    <a href="#concierge">Gift matcher</a>
    <a href="#keepsakes">Keepsakes</a>
    <a href="#builder">Build your gift</a>
    <a href="#mooncakes">Mooncakes</a>
    <a href="#garden">The Painted Garden</a>
    <a href="#where">Where to buy</a>
    <a class="nbro" href="assets/mlb-midautumn-2026-brochure.pdf" target="_blank" rel="noopener" data-brochure="nav">E&#8209;Brochure</a>
  </div>
  <span class="edge l" aria-hidden="true"></span>
  <span class="edge r" aria-hidden="true"></span>
  <div class="progress" id="navProgress"><span class="pfly" aria-hidden="true"><svg viewBox="0 0 48 48"><g class="wl"><path d="M21.5 22.5 C16 10 4 6 3.5 14.5 C3.2 20 10 24.5 21.5 25.5 Z"/><path d="M21.5 27 C13 27.5 7 33 9.5 38.5 C11.8 43 19 39.5 22 30.5 Z"/></g><g class="wr"><path d="M26.5 22.5 C32 10 44 6 44.5 14.5 C44.8 20 38 24.5 26.5 25.5 Z"/><path d="M26.5 27 C35 27.5 41 33 38.5 38.5 C36.2 43 29 39.5 26 30.5 Z"/></g><ellipse cx="24" cy="26" rx="2.1" ry="8.2"/><path class="ant" d="M23 19 C21.5 14.5 18.5 11.5 15.5 10.5 M25 19 C26.5 14.5 29.5 11.5 32.5 10.5"/></svg></span></div>
</nav>

<header class="hero">
  <div class="hbrand" id="hbrand">
    <span class="hb-title" aria-hidden="true"><span class="cs-en">A Bond in Lasting Bloom</span><span class="cs-cn">花月情长</span></span>
    <div class="hb-logo">
      <img src="assets/mlb-logo-color.png?v={{AV}}" alt="Mdm Ling Bakery" width="900" height="308" fetchpriority="high">
      <span class="hseason">Mid-Autumn 2026</span>
    </div>
  </div>
  <div class="hfig" id="heroFig">
    <picture>
      <source media="(max-aspect-ratio: 1/1)" srcset="assets/band-hero-p.webp?v={{AV}}">
      <img class="hbg" id="heroImg" src="assets/band-hero.webp?v={{AV}}" alt="The Mdm Ling Bakery Mid-Autumn 2026 collection laid out on a white garden table under a fringed parasol, surrounded by roses" width="1500" height="1500" fetchpriority="high" decoding="async">
    </picture>
    <div class="hspots" id="hspots" aria-label="Tap a marker to jump to that gift set"></div>
  </div>
  <div class="hcap">
    <div class="wrap">
      <div>
        <h1>Gifts that outlive the season</h1>
        <p class="hcn"><span class="cs-en">A Bond in Lasting Bloom</span><span class="cs-cn">花月情长</span></p>
      </div>
      <div>
        <p class="lede">Keepsakes and three mooncake ranges, photographed in the garden they were made for. Every piece is built to be kept, used and remembered long after the last mooncake is gone. &#127765;</p>
        <div class="acts">
          <a class="btn light" href="#concierge">Try our gift matcher</a>
        </div>
      </div>
    </div>
  </div>
</header>

<section class="manifesto">
  <div class="wrap">
    <div class="mtext">
      <p class="m-lede">In Singapore you don't visit someone empty-handed. You bring something to share. That single gesture is the whole reason this collection exists.</p>
      <p class="m-sub">So we design the <strong>keepsake first</strong> and the season second.</p>
      <div class="m-cards">
        <figure>
          <img src="assets/painted-garden-tin.webp?v={{AV}}" alt="The Painted Garden keepsake tin on the garden table" width="800" height="600" loading="lazy" decoding="async">
          <figcaption><strong>A tin</strong> that holds trinkets for years.</figcaption>
        </figure>
        <figure>
          <img src="assets/the-dusk.webp?v={{AV}}" alt="The Dusk leather gift bag among the flowers" width="800" height="600" loading="lazy" decoding="async">
          <figcaption><strong>A bag</strong> someone actually wears.</figcaption>
        </figure>
        <figure>
          <img src="assets/elegance-turntable.webp?v={{AV}}" alt="The Elegance Reunion Turntable set for the table" width="800" height="600" loading="lazy" decoding="async">
          <figcaption><strong>A turntable</strong> that comes back out at every reunion dinner.</figcaption>
        </figure>
      </div>
      <p class="m-note"><strong>Sustainably made, genuinely useful, and Singaporean in spirit</strong>, with a four character name apiece the way heirlooms in a Chinese household always have.</p>
      <p class="m-halal">The mooncakes are yours to choose. <strong>All our baked sets are Halal certified and vegetarian.</strong> &#127765;</p>
    </div>
  </div>
</section>

<div class="wrap">

  <!-- ================= GIFT MATCHER ================= -->
  <section class="part" id="concierge">
    <div class="tool">
      <span class="tool-kicker">The gift matcher</span>
      <h3>Tell us who it's for</h3>
      <p class="sub">Four quick questions and we'll narrow the whole collection to one keepsake, with the mooncake set that suits their table.</p>
      <div class="qsteps"><i class="on"></i><i></i><i></i><i></i></div>
      <div id="cQuiz">{{QS}}</div>
      <div class="result" id="cResult"></div>
    </div>
  </section>
</div>

<!-- ================= BAND: the garden table ================= -->
<section class="band">
  <picture>
    <source media="(max-aspect-ratio: 4/5)" srcset="assets/band-tea-p.webp?v={{AV}}">
    <img src="assets/band-tea.webp?v={{AV}}" alt="Three friends at a white garden table with Mdm Ling Bakery mooncake tins, in front of a flowering rose hedge" width="1700" height="1133" loading="lazy" decoding="async">
  </picture>
  <div class="bt">
    <span class="eyebrow">Part one</span>
    <p>Everything here was made to still be in the house next year.</p>
  </div>
</section>

<div class="wrap">
  <!-- ================= KEEPSAKES ================= -->
  <section class="part" id="keepsakes">
    <div class="part-head">
      <span class="mark">01</span>
      <div class="inner">
        <span class="eyebrow">The keepsakes</span>
        <h2>Something worth sharing, something worth keeping</h2>
        <p class="lede">Every keepsake belongs to one family, <strong>花月情长 &middot; A Bond in Lasting Bloom</strong>. Pick the piece that suits them, then fill it with the mooncakes of your choice.</p>
        <p class="lede" style="margin-top:12px">Order online with <strong>free delivery above ${{FREE_DEL}}</strong>, choose the delivery date that suits you, and let us do the carrying. Or come see us at one of our <a href="#where" style="color:var(--rose); font-weight:600">{{N_BOOTHS}} booths around Singapore</a>. &#127765;</p>
      </div>
    </div>
  </section>
</div>

<div class="wrap">{{KEEPSAKES}}</div>

<div class="wrap">
  <!-- ================= BUILDER ================= -->
  <section class="part" id="builder">
    <div class="tool">
      <span class="tool-kicker">Build your gift</span>
      <h3>Pick a keepsake, then what goes inside</h3>
      <p class="sub">Every gift is chosen in two steps. Tap a keepsake to see the mooncake sets it takes, what's in each one, and where to get it.</p>
      <div class="bpick" id="bPick"></div>
      <div class="bout" id="bOut"></div>
    </div>
  </section>
</div>

<!-- ================= BAND: at the table ================= -->
<section class="band short">
  <picture>
    <source media="(max-aspect-ratio: 4/5)" srcset="assets/band-mooncake-p.webp?v={{AV}}">
    <img src="assets/band-mooncake.webp?v={{AV}}" alt="Two friends sharing mooncakes at a garden table beneath a fringed parasol" width="1800" height="1200" loading="lazy" decoding="async">
  </picture>
  <div class="bt">
    <span class="eyebrow">Part two</span>
    <p>Three ranges, and a flavour for every generation at the table.</p>
  </div>
</section>

<div class="wrap">
  <!-- ================= MOONCAKES ================= -->
  <section class="part" id="mooncakes">
    <div class="part-head">
      <span class="mark">02</span>
      <div class="inner">
        <span class="eyebrow">The mooncakes</span>
        <h2>What goes inside</h2>
        <p class="lede">Ten flavours across three ranges: our <strong>traditional baked classics</strong>, our <strong>signature assorted range</strong> with a low sugar Momoyama skin, and our <strong>truffle snowskin range</strong> served chilled. Here they are at one glance. Tap any flavour to read its story.</p>
      </div>
    </div>
    {{FLAV_OVERVIEW}}
    {{RANGES}}

    <div class="panel" id="storage">
      <h4>Storage and freshness</h4>
      <p>Our baked mooncakes keep for <strong>2 months from production</strong>, with the <strong>best before date printed on the packaging</strong>. Store them in a <strong>cool, dry place</strong> away from direct sunlight, and enjoy them soon after opening.</p>
      <p>Snowskin mooncakes are <strong>best served chilled</strong>. Keep them away from direct heat and sunlight, and never leave them in the car boot. Within <strong>2 hours of purchase</strong>, place them in the freezer at <strong>&minus;12&deg;C or below</strong>, where they'll keep for <strong>up to 8 weeks</strong>. Once thawed, <strong>do not refreeze</strong>. &#127765;</p>
    </div>
  </section>
</div>

<!-- ================= THE PAINTED GARDEN / YING / BCF ================= -->
<section class="artist" id="garden">
  <div class="ainner wrap">
    <span class="collab">A Mdm Ling Bakery collaboration with<br>World of Ying and Breast Cancer Foundation</span>
    <div class="collab-logos">
      <img class="ying" src="assets/logo-ying.png?v={{AV}}" alt="World of Ying" width="592" height="260" loading="lazy" decoding="async">
      <span aria-hidden="true">&times;</span>
      <img class="mlb" src="assets/mlb-logo-white.png?v={{AV}}" alt="Mdm Ling Bakery" width="900" height="304" loading="lazy" decoding="async">
      <span aria-hidden="true">&times;</span>
      <img class="bcf" src="assets/logo-bcf.png?v={{AV}}" alt="Breast Cancer Foundation" width="359" height="64" loading="lazy" decoding="async">
    </div>
    <div class="agrid">
      <div class="acol">
        <span class="eyebrow">百花迎月 &middot; The Painted Garden</span>
        <h3>The people we love are worth caring for</h3>
        <p>A garden only grows because someone tends it. As you pass this box on, we hope it's also a nudge for the women in your life to look after their breast health.</p>
        <div class="ablurb">
          <img src="assets/ying-portrait.webp?v={{AV}}" alt="Phuay Li Ying, the artist behind The Painted Garden" width="466" height="700" loading="lazy" decoding="async">
          <div>
            <span class="apre">Painted for Mdm Ling Bakery by</span>
            <span class="an">Phuay Li Ying</span>
            <span class="as">@theworldofying &middot; Singapore print artist</span>
            <a class="btn ghost sm awb" href="{{ARTIST_IG}}" target="_blank" rel="noopener">Visit World of Ying &#8599;</a>
          </div>
        </div>
        <div class="bcfnote">
          <span class="amt"><span class="d">$1</span><span class="dsub">with every box,<br>given onward</span></span>
          <p>From every <strong>Painted Garden Box</strong>, this dollar goes to the <strong>Breast Cancer Foundation</strong>, supporting awareness, screening and survivor care here in Singapore. Each garden you give helps look after someone else's.</p>
          <a class="btn gold sm" href="{{BCF}}" target="_blank" rel="noopener" data-bcf="feature">Visit Breast Cancer Foundation &#8599;</a>
        </div>
      </div>
      <div class="amedia">
        <figure class="aart">
          <img src="assets/ying-artwork.webp?v={{AV}}" alt="The Painted Garden, the original watercolour artwork by Phuay Li Ying" width="1400" height="1400" loading="lazy" decoding="async">
          <figcaption>The Painted Garden &middot; original artwork by Phuay Li Ying</figcaption>
        </figure>
        <div class="acts amact">
          <a class="btn light" href="#k-the-painted-garden-box">See The Painted Garden Box</a>
        </div>
        <figure class="agroup">
          <img src="assets/group-collab.webp?v={{AV}}" alt="Phuay Li Ying, Jacob Soo and Evelyn Lim at the table with The Painted Garden artwork and box" width="1400" height="1090" loading="lazy" decoding="async">
          <figcaption class="credit">From left: Phuay Li Ying, founder of World of Ying; Jacob Soo, CEO of Breast Cancer Foundation; and Evelyn Lim, co&#8209;founder of Mdm Ling Bakery.</figcaption>
        </figure>
      </div>
    </div>
  </div>
</section>

<div class="wrap">
  <!-- ================= WHERE TO BUY ================= -->
  <section class="part" id="where">
    <div class="part-head">
      <span class="mark">03</span>
      <div class="inner">
        <span class="eyebrow">Where to buy</span>
        <h2>Find us across Singapore</h2>
        <p class="lede">Every keepsake in this collection is at our booths, and most can also be ordered online with <strong>free delivery above ${{FREE_DEL}}</strong>. If you're after one of the booth only pieces, <strong>drop by any booth</strong> and see what's available on the day. &#127765;</p>
        <div class="res-acts" style="margin-bottom:8px">
          <a class="btn" href="https://www.mdmlingbakery.com" target="_blank" rel="noopener" data-order="store" data-name="Online store">Shop online</a>
          <a class="btn ghost" href="{{WA_CUST}}" target="_blank" rel="noopener" data-booth="general" data-name="General enquiry">Customer experience team &middot; {{TEL_CUST}}</a>
          <a class="tlink" href="assets/mlb-midautumn-2026-brochure.pdf" target="_blank" rel="noopener" data-brochure="1">Download the brochure</a>
        </div>
        <div class="nearest">
          <form id="nearForm" novalidate>
            <input id="nearIn" type="text" inputmode="numeric" autocomplete="postal-code" maxlength="6" pattern="[0-9]{6}" placeholder="Your 6 digit postal code" aria-label="Your 6 digit postal code">
            <button class="btn sm" type="submit">Find my nearest booth</button>
          </form>
          <div id="nearOut" class="near-out" hidden></div>
        </div>
      </div>
    </div>
    <div class="booth-map" id="boothMap" role="img" aria-label="Map of Mdm Ling Bakery Mid-Autumn booths across Singapore"></div>
    <div class="map-tools">
      <button type="button" class="btn ghost sm" id="boothMapReset">View full map</button>
    </div>
    {{BOOTHS}}
  </section>
</div>

<footer>
  <div class="wrap">
    <img class="flogo" src="assets/mlb-logo-white.png?v={{AV}}" alt="Mdm Ling Bakery" width="900" height="304" loading="lazy" decoding="async">
    <span class="fcn"><span class="cs-cn">花月情长</span><span class="cs-en">A Bond in Lasting Bloom</span></span>
    <div class="fnav">
      <a class="btn ghost sm" href="https://www.mdmlingbakery.com" target="_blank" rel="noopener" data-order="store-footer" data-name="Online store" style="color:#C9BDB7">Shop online</a>
      <a class="btn ghost sm" href="{{WA_CUST}}" target="_blank" rel="noopener" style="color:#C9BDB7">Customer experience team</a>
      <a class="btn ghost sm" href="assets/mlb-midautumn-2026-brochure.pdf" target="_blank" rel="noopener" data-brochure="footer" style="color:#C9BDB7">E&#8209;Brochure</a>
      <a class="btn ghost sm fig" href="https://www.instagram.com/mdmlingbakery/" target="_blank" rel="noopener" aria-label="Mdm Ling Bakery on Instagram" style="color:#C9BDB7"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.2" cy="6.8" r="1.2" fill="currentColor" stroke="none"/></svg></a>
    </div>
    <div class="fbadges">
      <img src="assets/badge-mwp.png?v={{AV}}" alt="Made With Passion, Singapore" width="700" height="462" loading="lazy" decoding="async">
      <img src="assets/badge-pos.png?v={{AV}}" alt="Product of Singapore" width="619" height="700" loading="lazy" decoding="async">
    </div>
    <p class="fl">Ingredients and allergen advice on this page follow the printed product labels. If you're gifting to someone with a food allergy, do check the label on the box as well. Halal certification covers our baked mooncakes; the truffle snowskin range isn't Halal certified. &#127765;</p>
  </div>
</footer>

<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Enlarged mooncake photo">
  <button type="button" class="lb-close" id="lbClose" aria-label="Close">&times;</button>
  <img id="lbImg" src="" alt="">
  <p class="lb-cap" id="lbCap"></p>
</div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>{{JS}}</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
