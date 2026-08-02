# -*- coding: utf-8 -*-
"""
Builds index.html for the Mdm Ling Bakery Mid-Autumn 2026 microsite.

Run:  python3 build_site.py
Everything is generated from data.py, so the keepsake cards, the Gift
Concierge and the Build Your Gift tool always agree with each other.

Visual system: MLB brand refresh 2026 (brands/mlb/design-system.css).
Dusty Rose #A97F78 · Champagne Gold #C7A66A · Cocoa #4E3C37 on Cloud #F3F2F1.
Inter throughout, Work Sans for standalone numbers only.
"""
import json
import os
import re
from data import (KEEPSAKES, SETS, BOOTHS, RECIPIENTS, PRIORITIES, TABLES,
                  BUDGETS, WA_CUSTOMER, WA_CORPORATE, EMAIL_CORPORATE,
                  CORPORATE_MIN, FREE_DELIVERY, SITE_URL, GA_ID)

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET_V = 3  # bump when an asset is replaced under the same filename


# --------------------------------------------------------------------------
# CSS
# --------------------------------------------------------------------------
CSS = """
:root{
  --rose:#A97F78; --gold:#C7A66A; --cocoa:#4E3C37; --cloud:#F3F2F1;
  --sage:#A5A58D; --plum:#6E4B4A; --mushroom:#D8CEC3; --brass:#8B7355;
  --taupe:#B6A79C; --paper:#FFFFFF;
  --ink:var(--cocoa); --muted:#8A7A72; --hair:#E2DAD3;
  --f:'Inter',system-ui,-apple-system,sans-serif;
  --fn:'Work Sans','Inter',sans-serif;
  --maxw:1120px; --readw:640px;
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth; scroll-padding-top:74px;}
@media (prefers-reduced-motion:reduce){ html{scroll-behavior:auto;} *{animation:none!important; transition:none!important;} }
body{margin:0; background:var(--cloud); color:var(--ink); font-family:var(--f);
  font-weight:400; font-size:17px; line-height:1.65; -webkit-font-smoothing:antialiased;
  font-feature-settings:"cv11","ss01";}
img{max-width:100%; display:block;}
a{color:inherit;}
.wrap{max-width:var(--maxw); margin:0 auto; padding:0 26px;}
.read{max-width:var(--readw);}

/* ---------- nav ---------- */
nav.jump{position:sticky; top:0; z-index:60; background:rgba(243,242,241,.94);
  backdrop-filter:saturate(150%) blur(12px); border-bottom:1px solid var(--hair);}
nav.jump .in{max-width:var(--maxw); margin:0 auto; padding:0 26px; display:flex; gap:26px;
  overflow-x:auto; scrollbar-width:none; height:56px; align-items:center;}
nav.jump .in::-webkit-scrollbar{display:none;}
nav.jump a{text-decoration:none; white-space:nowrap; font-size:12px; font-weight:500;
  letter-spacing:.14em; text-transform:uppercase; color:var(--muted); padding:4px 0;
  border-bottom:1.5px solid transparent; transition:color .2s,border-color .2s;}
nav.jump a:hover{color:var(--ink);}
nav.jump a.active{color:var(--rose); border-bottom-color:var(--gold);}
.progress{height:1.5px; background:var(--gold); width:0; transition:width .1s linear;}

/* ---------- hero ---------- */
header.hero{background:var(--rose); color:#FBF8F6; padding:78px 0 66px; position:relative; overflow:hidden;}
header.hero::after{content:""; position:absolute; right:-90px; top:-90px; width:340px; height:340px;
  border-radius:50%; border:1px solid rgba(251,248,246,.22);}
header.hero::before{content:""; position:absolute; right:10px; top:30px; width:170px; height:170px;
  border-radius:50%; background:rgba(199,166,106,.26);}
.hero .wrap{position:relative; z-index:2;}
.hgrid{display:block;}
@media(min-width:940px){ .hgrid{display:grid; grid-template-columns:1.1fr .9fr;
  gap:60px; align-items:center;} }
.eyebrow{font-size:11.5px; font-weight:600; letter-spacing:.34em; text-transform:uppercase;
  color:#EBD9AE;}
.hero h1{font-family:var(--f); font-weight:600; letter-spacing:-.028em; line-height:1.02;
  font-size:clamp(40px,7.2vw,68px); margin:18px 0 0; max-width:14ch;}
.hero .cn{font-size:clamp(19px,3vw,25px); font-weight:500; margin:16px 0 0; color:#F0E2C4;}
.hero .cn .han{letter-spacing:.14em;}
.hero .cn .en{letter-spacing:.01em; font-size:.86em; color:#EBD9AE;}
.hero p{max-width:44ch; margin:20px 0 0; font-size:17px; color:#F3E6E2;}
.hero .acts{display:flex; flex-wrap:wrap; gap:12px; margin-top:32px;}
.hshot{margin:40px 0 0; max-width:340px; aspect-ratio:4/5; overflow:hidden;
  border:1px solid rgba(251,248,246,.4); background:rgba(251,248,246,.08);}
@media(min-width:940px){ .hshot{margin:0; max-width:none;} }
.hshot img{width:100%; height:100%; object-fit:cover;}
.hshot figcaption{display:none;}

/* ---------- buttons ---------- */
.btn{display:inline-flex; align-items:center; gap:9px; font-family:var(--f); font-size:14px;
  font-weight:600; letter-spacing:.02em; padding:13px 22px; border:1.5px solid var(--cocoa);
  background:var(--cocoa); color:var(--cloud); text-decoration:none; cursor:pointer;
  border-radius:2px; transition:background .18s,color .18s,border-color .18s;}
.btn:hover{background:#3B2C28; border-color:#3B2C28;}
.btn.gold{background:var(--gold); border-color:var(--gold); color:#3B2C28;}
.btn.gold:hover{background:#B8934F; border-color:#B8934F;}
.btn.ghost{background:transparent; color:inherit; border-color:currentColor;}
.btn.ghost:hover{background:rgba(78,60,55,.08);}
.btn.light{background:#FBF8F6; border-color:#FBF8F6; color:var(--rose);}
.btn.light:hover{background:#fff; border-color:#fff;}
.btn.sm{font-size:13px; padding:10px 17px;}
.btn[disabled]{opacity:.45; pointer-events:none;}

/* ---------- section furniture ---------- */
.part{margin:104px 0 0;}
.part-head{border-top:1.5px solid var(--gold); padding-top:20px; margin-bottom:42px;}
.part-num{font-family:var(--fn); font-size:13px; font-weight:600; letter-spacing:.2em;
  color:var(--gold); text-transform:uppercase;}
.part-head h2{font-weight:600; letter-spacing:-.022em; line-height:1.06;
  font-size:clamp(30px,4.6vw,46px); margin:10px 0 0; color:var(--cocoa); max-width:18ch;}
.part-head .lede{max-width:var(--readw); margin:16px 0 0; font-size:17px; color:#6B5A54;}
.part-head .lede strong{color:var(--rose); font-weight:600;}

/* ---------- ethos ---------- */
.ethos{background:var(--cocoa); color:#EDE6E2; padding:52px 0; margin-top:0;}
.ethos h2{font-size:clamp(22px,3vw,30px); font-weight:600; letter-spacing:-.02em; margin:0 0 14px; color:#fff;}
.ethos p{max-width:58ch; margin:0; color:#D7CCC6; font-size:16.5px;}
.ethos .pillars{display:flex; flex-wrap:wrap; gap:0; margin-top:30px; border-top:1px solid rgba(199,166,106,.4);}
.ethos .pillars span{flex:1 1 200px; padding:16px 20px 16px 0; font-size:13.5px; color:#E7DCD6;
  border-right:1px solid rgba(199,166,106,.22);}
.ethos .pillars span:last-child{border-right:0;}

/* ---------- concierge ---------- */
.tool{background:var(--paper); border:1px solid var(--hair); border-radius:3px; padding:36px 34px;}
.tool-kicker{font-size:11.5px; font-weight:600; letter-spacing:.24em; text-transform:uppercase; color:var(--gold);}
.tool h3{font-size:clamp(24px,3.4vw,33px); font-weight:600; letter-spacing:-.022em; margin:10px 0 8px;}
.tool .sub{color:var(--muted); font-size:15.5px; margin:0 0 26px; max-width:52ch;}
.qsteps{display:flex; gap:6px; margin-bottom:26px;}
.qsteps i{flex:1; height:2px; background:var(--hair);}
.qsteps i.on{background:var(--gold);}
.q{display:none;}
.q.on{display:block;}
.q .qn{font-family:var(--fn); font-size:12px; font-weight:600; letter-spacing:.16em;
  text-transform:uppercase; color:var(--muted);}
.q h4{font-size:22px; font-weight:600; letter-spacing:-.015em; margin:8px 0 20px;}
.opts{display:grid; gap:10px;}
@media(min-width:620px){ .opts{grid-template-columns:1fr 1fr;} }
.opt{text-align:left; font-family:var(--f); font-size:15.5px; font-weight:500; color:var(--ink);
  background:#FCFAF9; border:1.5px solid var(--hair); border-radius:2px; padding:15px 18px;
  cursor:pointer; transition:border-color .16s,background .16s;}
.opt:hover{border-color:var(--rose); background:#fff;}
.qback{margin-top:20px; background:none; border:0; font-family:var(--f); font-size:13.5px;
  color:var(--muted); cursor:pointer; padding:0; text-decoration:underline; text-underline-offset:3px;}
.qback:hover{color:var(--ink);}

.result{display:none;}
.result.on{display:block;}
.res-grid{display:grid; gap:26px;}
@media(min-width:720px){ .res-grid{grid-template-columns:250px 1fr; align-items:start;} }
.res-photo{border:1px solid var(--hair); background:var(--mushroom); aspect-ratio:4/5; overflow:hidden;}
.res-photo img{width:100%; height:100%; object-fit:cover;}
.res-body h4{font-size:29px; font-weight:600; letter-spacing:-.022em; margin:0;}
.res-body .rcn{font-size:18px; color:var(--rose); font-weight:500; letter-spacing:.1em; margin:6px 0 0;}
.res-body .rgloss{font-size:13.5px; color:var(--muted); font-style:italic; margin:3px 0 0;}
.res-why{border-left:2px solid var(--gold); padding:2px 0 2px 16px; margin:20px 0 0; font-size:16.5px;}
.res-meta{display:flex; flex-wrap:wrap; gap:8px; margin:20px 0 0;}
.res-acts{display:flex; flex-wrap:wrap; gap:10px; margin:24px 0 0;}
.res-alt{margin:30px 0 0; padding:20px 0 0; border-top:1px solid var(--hair); font-size:15px; color:var(--muted);}
.res-alt a{color:var(--rose); font-weight:600; text-decoration:none; border-bottom:1px solid var(--gold);}
.res-note{margin:16px 0 0; font-size:13.5px; color:var(--muted);}

/* ---------- tags ---------- */
.tag{display:inline-flex; align-items:center; gap:5px; font-size:11.5px; font-weight:600;
  letter-spacing:.05em; padding:5px 10px; border:1px solid var(--hair); border-radius:2px;
  background:#FCFAF9; color:#6B5A54;}
.tag.gold{border-color:#E4D3AF; background:#FBF6EA; color:#8A6E33;}
.tag.rose{border-color:#E6D2CE; background:#FBF3F1; color:var(--rose);}
.tag.sage{border-color:#D5DAC9; background:#F4F6EF; color:#5F6B4C;}
.tag.chill{border-color:#CDD9DE; background:#F0F5F7; color:#4C6570;}
.price{font-family:var(--fn); font-weight:600; font-size:20px; letter-spacing:-.01em; color:var(--cocoa);}

/* ---------- keepsake cards ---------- */
.packs{display:grid; gap:2px; background:var(--hair); border:1px solid var(--hair);}
@media(min-width:760px){ .packs{grid-template-columns:1fr 1fr;} }
.pack{background:var(--paper); padding:0; display:flex; flex-direction:column;}
.pack-photo{aspect-ratio:4/5; overflow:hidden; background:var(--mushroom); position:relative;}
.pack-photo img{width:100%; height:100%; object-fit:cover; transition:transform .5s ease;}
.pack:hover .pack-photo img{transform:scale(1.03);}
.chan{position:absolute; left:0; top:0; font-size:10.5px; font-weight:600; letter-spacing:.14em;
  text-transform:uppercase; padding:7px 12px; background:var(--cocoa); color:var(--cloud);}
.chan.booth{background:var(--gold); color:#3B2C28;}
.pack-body{padding:26px 26px 28px; display:flex; flex-direction:column; flex:1;}
.pack .fmt{font-size:11.5px; font-weight:600; letter-spacing:.16em; text-transform:uppercase; color:var(--muted);}
.pack h4{font-size:25px; font-weight:600; letter-spacing:-.022em; margin:9px 0 0; line-height:1.15;}
.pack h4 .var{font-weight:400; font-size:16px; color:var(--muted);}
.pack .pcn{font-size:17px; font-weight:500; letter-spacing:.1em; color:var(--rose); margin:7px 0 0;}
.pack .pgloss{font-size:13px; font-style:italic; color:var(--muted); margin:2px 0 0;}
.becomes{margin:20px 0 0; padding:14px 0 0; border-top:1px solid var(--hair);}
.becomes .lbl{display:block; font-size:10.5px; font-weight:700; letter-spacing:.18em;
  text-transform:uppercase; color:var(--gold); margin-bottom:5px;}
.becomes p{margin:0; font-size:15px; color:#5E4F49;}
.pack .desc{margin:18px 0 0; font-size:15.5px; color:#5E4F49;}
.pack .desc p{margin:0 0 11px;}
.pack .desc p:last-child{margin-bottom:0;}
.pack .desc strong{color:var(--plum); font-weight:600;}
.pack .note{margin:14px 0 0; font-size:13px; color:var(--muted); font-style:italic;}
.pack-foot{margin-top:auto; padding-top:22px; display:flex; flex-wrap:wrap; align-items:center; gap:12px;}
.pack-foot .price{margin-right:auto;}
details.more{margin:16px 0 0;}
details.more summary{cursor:pointer; font-size:13.5px; font-weight:600; color:var(--rose);
  list-style:none; padding:2px 0;}
details.more summary::-webkit-details-marker{display:none;}
details.more summary::after{content:" +";}
details.more[open] summary::after{content:" \\2212";}

/* ---------- builder ---------- */
.bpick{display:flex; flex-wrap:wrap; gap:8px; margin:0 0 26px;}
.chip{font-family:var(--f); font-size:13.5px; font-weight:500; padding:9px 15px; cursor:pointer;
  background:#FCFAF9; border:1.5px solid var(--hair); border-radius:2px; color:var(--ink);
  transition:border-color .16s,background .16s;}
.chip:hover{border-color:var(--rose);}
.chip.on{border-color:var(--rose); background:var(--rose); color:#fff;}
.bout{display:none; border-top:1px solid var(--hair); padding-top:26px;}
.bout.on{display:block;}
.bhead{display:flex; flex-wrap:wrap; gap:16px; align-items:flex-start; margin-bottom:22px;}
.bhead img{width:96px; height:120px; object-fit:cover; border:1px solid var(--hair); flex:none;}
.bhead h4{margin:0; font-size:23px; font-weight:600; letter-spacing:-.02em;}
.setlist{display:grid; gap:2px; background:var(--hair); border:1px solid var(--hair);}
.setrow{background:#FCFAF9; padding:15px 18px; display:grid; gap:4px 16px; align-items:start;}
@media(min-width:640px){ .setrow{grid-template-columns:78px 1fr auto;} }
.setrow .sid{font-family:var(--fn); font-size:19px; font-weight:600; color:var(--rose);}
.setrow .sid small{display:block; font-family:var(--f); font-size:11px; font-weight:600;
  letter-spacing:.1em; text-transform:uppercase; color:var(--muted); margin-top:1px;}
.setrow ul{margin:0; padding:0; list-style:none; font-size:14.5px; color:#5E4F49;}
.setrow li{padding:1px 0;}

/* ---------- sets table ---------- */
.settable{border:1px solid var(--hair); background:var(--paper);}
.settable .r{display:grid; gap:4px 18px; padding:17px 20px; border-bottom:1px solid var(--hair);}
@media(min-width:680px){ .settable .r{grid-template-columns:74px 168px 1fr;} }
.settable .r:last-child{border-bottom:0;}
.settable .r.hdr{background:#FAF7F5; font-size:11px; font-weight:600; letter-spacing:.16em;
  text-transform:uppercase; color:var(--muted);}
.settable .g{font-size:13.5px; color:var(--muted);}
.settable ul{margin:0; padding:0; list-style:none; font-size:15px; color:#5E4F49;}

/* ---------- flavours ---------- */
.range{margin:52px 0 0;}
.range-head{display:flex; align-items:baseline; gap:14px; flex-wrap:wrap;
  border-bottom:1.5px solid var(--gold); padding-bottom:13px;}
.range-num{font-family:var(--fn); font-size:34px; font-weight:600; color:var(--gold); line-height:.85;}
.range-head h3{font-size:25px; font-weight:600; letter-spacing:-.02em; margin:0;}
.range-head .tag2{font-size:14px; color:var(--muted);}
.range-intro{margin:20px 0 0; font-size:16px; color:#5E4F49; max-width:var(--readw);}
.range-intro strong{color:var(--plum); font-weight:600;}
.flavours{display:grid; gap:2px; background:var(--hair); border:1px solid var(--hair); margin-top:24px;}
@media(min-width:700px){ .flavours{grid-template-columns:1fr 1fr;} }
.flav{background:var(--paper); padding:22px 24px; display:flex; gap:18px;}
.flav .fp{flex:0 0 96px;}
.flav .fp img{width:96px; height:126px; object-fit:cover; background:var(--mushroom);}
.flav h4{font-size:19px; font-weight:600; letter-spacing:-.015em; margin:0 0 8px; line-height:1.2;}
.flav .badges{display:flex; gap:6px; margin:0 0 10px; flex-wrap:wrap;}
.flav .story{font-size:14.5px; color:#5E4F49; margin:0;}
.flav .story strong{color:var(--plum); font-weight:600;}
.ing{margin-top:13px; padding-top:11px; border-top:1px dashed var(--hair);}
.ing .lbl{display:block; font-size:10px; font-weight:700; letter-spacing:.16em;
  text-transform:uppercase; color:var(--gold); margin:0 0 3px;}
.ing .lbl.mt{margin-top:10px;}
.ing p{margin:0; font-size:12.5px; color:#7A6A64; line-height:1.5;}
.algs{display:flex; flex-wrap:wrap; gap:5px;}
.alg{font-size:11px; font-weight:500; color:#7A4A46; background:#FBF3F1; border:1px solid #EBDCD8;
  padding:2px 7px; border-radius:2px;}
.trace{margin:7px 0 0; font-size:11px; font-style:italic; color:#9C8C86;}

/* ---------- panels ---------- */
.panel{background:var(--paper); border:1px solid var(--hair); border-left:2px solid var(--gold);
  padding:26px 28px; margin:32px 0 0;}
.panel h4{font-size:19px; font-weight:600; letter-spacing:-.015em; margin:0 0 9px;}
.panel p{margin:0 0 10px; font-size:15.5px; color:#5E4F49;}
.panel p:last-child{margin-bottom:0;}
.panel strong{color:var(--plum); font-weight:600;}

.feature{background:var(--paper); border:1px solid var(--hair); display:grid; gap:0;}
@media(min-width:820px){ .feature{grid-template-columns:1fr 1fr;} }
.feature .fimg{background:var(--mushroom); min-height:320px; overflow:hidden;}
.feature .fimg img{width:100%; height:100%; object-fit:cover;}
.feature .ftxt{padding:38px 36px;}
.feature h3{font-size:clamp(24px,3.2vw,32px); font-weight:600; letter-spacing:-.022em; margin:12px 0 16px;}
.feature p{font-size:16px; color:#5E4F49; margin:0 0 13px;}
.feature p:last-of-type{margin-bottom:0;}
.feature strong{color:var(--plum); font-weight:600;}

/* ---------- corporate ---------- */
.corp{background:var(--cocoa); color:#EDE6E2; padding:44px 40px; border-radius:3px;}
.corp h3{color:#fff; font-size:clamp(24px,3.2vw,32px); font-weight:600; letter-spacing:-.022em; margin:10px 0 14px;}
.corp p{color:#D7CCC6; max-width:56ch; margin:0 0 20px; font-size:16px;}
.corp .facts{display:grid; gap:0; border-top:1px solid rgba(199,166,106,.4); margin:26px 0 28px;}
@media(min-width:620px){ .corp .facts{grid-template-columns:repeat(3,1fr);} }
.corp .facts div{padding:16px 20px 16px 0; border-right:1px solid rgba(199,166,106,.22);}
.corp .facts div:last-child{border-right:0;}
.corp .facts .n{font-family:var(--fn); font-size:26px; font-weight:600; color:var(--gold); display:block;}
.corp .facts .l{font-size:13px; color:#C9BDB7;}
.corp .acts{display:flex; flex-wrap:wrap; gap:11px;}

/* ---------- booths ---------- */
.booths{display:grid; gap:2px; background:var(--hair); border:1px solid var(--hair);}
@media(min-width:560px){ .booths{grid-template-columns:1fr 1fr;} }
@media(min-width:900px){ .booths{grid-template-columns:repeat(3,1fr);} }
.booth{background:var(--paper); padding:16px 20px;}
.booth.flag{background:#FBF6EA;}
.booth .bn{font-size:15.5px; font-weight:600; margin:0;}
.booth .bl{font-size:13.5px; color:var(--muted); margin:2px 0 0;}
.booth .bf{display:inline-block; margin-top:6px; font-size:10.5px; font-weight:700;
  letter-spacing:.14em; text-transform:uppercase; color:var(--gold);}

/* ---------- footer ---------- */
footer{margin-top:104px; background:var(--cocoa); color:#C9BDB7; padding:52px 0 44px; font-size:14px;}
footer .fcn{display:block; color:var(--gold); font-size:19px; letter-spacing:.14em; margin:8px 0 22px;}
footer .fb{font-size:19px; font-weight:600; color:#fff; letter-spacing:-.02em;}
footer .fl{max-width:64ch; margin:22px 0 0; color:#A99B95; font-size:13px;}
footer a{color:var(--gold);}

#toTop{position:fixed; right:20px; bottom:20px; z-index:70; width:42px; height:42px;
  border:1px solid var(--hair); background:var(--paper); color:var(--rose); font-size:17px;
  cursor:pointer; opacity:0; pointer-events:none; transition:opacity .2s; border-radius:2px;}
#toTop.show{opacity:1; pointer-events:auto;}
"""


# --------------------------------------------------------------------------
# Static flavour content (prose stays hand written)
# --------------------------------------------------------------------------
def flav(img, alt, name, badges, story, ing, algs, trace):
    b = "".join('<span class="tag %s">%s</span>' % (c, t) for c, t in badges)
    a = "".join('<span class="alg">%s</span>' % x for x in algs)
    return """<div class="flav">
      <div class="fp"><img src="assets/%s?v=%d" alt="%s" width="96" height="126" loading="lazy" decoding="async"></div>
      <div>
        <h4>%s</h4>
        <div class="badges">%s</div>
        <p class="story">%s</p>
        <div class="ing">
          <span class="lbl">Ingredients</span><p>%s</p>
          <span class="lbl mt">Allergen advice · contains</span>
          <div class="algs">%s</div>
          <p class="trace">%s</p>
        </div>
      </div>
    </div>""" % (img, ASSET_V, alt, name, b, story, ing, a, trace)


HALAL = ("sage", "Halal certified")
VEG = ("sage", "Vegetarian")


def w(g):
    return ("", "%s" % g)


RANGES = [
    {
        "n": 1, "id": "traditional", "title": "Premium Traditional Baked",
        "tag": "The classics, baked golden", "intro": None,
        "items": [
            flav("trad-yolk.webp", "Traditional white lotus mooncake with salted egg yolk",
                 "Lotus with Melon Seeds and Yolk",
                 [HALAL, VEG, ("", "160g")],
                 "Smooth <strong>white lotus paste</strong> studded with melon seeds and wrapped around a <strong>golden salted egg yolk</strong>, baked the <strong>time honoured Cantonese way</strong>. <strong>The one everyone reaches for first.</strong>",
                 "White lotus paste, wheat flour, salted egg yolk, golden syrup, blended cooking oil (palm, peanut, sesame), melon seed, egg, milk.",
                 ["🌾 Gluten (wheat)", "🥚 Egg", "🥛 Milk", "Sesame", "🥜 Peanuts"],
                 "May contain traces of soy."),
            flav("trad-no-yolk.webp", "Traditional white lotus mooncake without yolk",
                 "Lotus with Melon Seeds",
                 [HALAL, VEG, ("", "160g")],
                 "Pure <strong>white lotus paste</strong> with melon seeds folded through, in a classic baked skin. Quiet, smooth and traditional, <strong>for those who like it simple</strong>.",
                 "White lotus paste, melon seed, wheat flour, golden syrup, blended cooking oil (palm, peanut, sesame), egg, milk.",
                 ["🌾 Gluten (wheat)", "🥚 Egg", "🥛 Milk", "Sesame", "🥜 Peanuts"],
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
                 ["🌾 Gluten (wheat)", "🥛 Milk", "🌰 Tree nuts", "Sesame", "🥚 Egg", "🥜 Peanuts", "🫘 Soy"],
                 "May contain traces of nuts."),
            flav("momo-sesame.webp", "Momoyama black sesame peanut butter mooncake",
                 "Black Sesame Peanut Butter",
                 [HALAL, VEG, ("", "160g")],
                 "Created for <strong>parents and grandparents with a sweet tooth</strong>. Toasty <strong>black sesame</strong> meets smooth <strong>peanut butter</strong>, a nod to the black sesame and peanut pastes they grew up ordering at Singapore dessert stalls, carried in a soft Momoyama skin.",
                 "Black sesame lotus paste, Maruchi dough, peanut butter, melon seeds, blended cooking oil (palm, peanut, sesame), pumpkin powder.",
                 ["🌾 Gluten (wheat)", "🥚 Egg", "Sesame", "🥜 Peanuts", "🥛 Milk", "🫘 Soy"],
                 "May contain traces of nuts."),
            flav("momo-pandan.webp", "Momoyama emerald pandan mooncake with golden yolk",
                 "Emerald Pandan Golden Yolk",
                 [HALAL, VEG, ("", "160g")],
                 "Created for <strong>every generation</strong>. The sweet <strong>pandan fragrance</strong> everyone knows from kaya, carried in a modern Momoyama skin, with the <strong>golden yolk from the traditional mooncake</strong> at its centre. The <strong>best of both worlds</strong> in one bite.",
                 "Pandan paste, Maruchi dough, custard salted egg yolk paste, melon seed, blended cooking oil (palm, peanut, sesame), purple sweet potato powder.",
                 ["🌾 Gluten (wheat)", "🥛 Milk", "🥚 Egg", "Sesame", "🥜 Peanuts", "🫘 Soy"],
                 "May contain traces of nuts."),
            flav("momo-reddates.webp", "Momoyama red dates longan mooncake",
                 "Red Dates Longan",
                 [HALAL, VEG, ("", "160g")],
                 "Created with our <strong>elders</strong> in mind. <strong>Red dates</strong> and <strong>longan</strong> are flavours they've known all their lives, long treasured in Chinese tradition as nourishing and warming, folded into a rose hued Momoyama skin. Gentle, familiar and easy to love.",
                 "Red date lotus, Maruchi dough, longan bits, melon seeds, blended cooking oil (palm, peanut, sesame), colour (102, 110, 124).",
                 ["🌾 Gluten (wheat)", "🥚 Egg", "Sesame", "🥜 Peanuts", "🥛 Milk", "🫘 Soy"],
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
                 "A pale green snowskin of soft glutinous rice, filled with smooth mungbean and a <strong>muscat grape truffle</strong> at its heart. <strong>Fragrant, delicate and quietly refreshing.</strong>",
                 "Cold water, icing sugar, glutinous rice flour, snowskin powder, shortening, cooking oil, mungbean filling, muscat grape truffle (white couverture, cream, green tea powder, white grape flavour).",
                 ["🥛 Milk"],
                 "May contain traces of gluten, egg, nuts, sesame, peanuts and soy."),
            flav("snow-passionfruit.webp", "Truffle Passionfruit snowskin mooncake with cream and passionfruit truffle centre",
                 "Truffle Passionfruit", [("chill", "Chilled"), ("", "63g")],
                 "A sunny golden snowskin of soft glutinous rice, filled with smooth mungbean paste and a <strong>passionfruit truffle</strong> that lands <strong>bright and tangy</strong>. A little tropical sunshine that wakes the whole box up.",
                 "Cold water, icing sugar, glutinous rice flour, snowskin powder, shortening, cooking oil, mungbean filling, passionfruit truffle (white couverture, Unigra passionfruit, cream).",
                 ["🥛 Milk"],
                 "May contain traces of gluten, egg, nuts, sesame, peanuts and soy."),
            flav("snow-popping.webp", "Truffle Popping Candy snowskin mooncake with dragon fruit paste and popping candy centre",
                 "Truffle Popping Candy", [("chill", "Chilled"), ("", "63g")],
                 "A blush pink snowskin of soft glutinous rice, filled with vivid <strong>dragonfruit paste</strong> and a <strong>popping candy truffle that crackles as you bite</strong>. <strong>The one that makes everyone at the table laugh first</strong> and reach for seconds after.",
                 "Cold water, icing sugar, glutinous rice flour, snowskin powder, shortening, cooking oil, dragon fruit paste (lotus paste, dragon fruit powder), popping candy truffle (white couverture, pink popping candy filling, blue popping candy filling).",
                 ["🥛 Milk"],
                 "May contain traces of gluten, egg, nuts, sesame, peanuts and soy."),
            flav("snow-pistachio.webp", "Truffle Pistachio Kunafa snowskin mooncake with almond filling and pistachio paste centre",
                 "Truffle Pistachio Kunafa", [("chill", "Chilled"), ("", "63g")],
                 "An ivory snowskin of soft glutinous rice, filled with smooth mungbean paste and a rich <strong>pistachio kunafa truffle</strong>. Our nod to the beloved <strong>Middle Eastern dessert</strong>, reimagined for the mooncake table.",
                 "Cold water, icing sugar, glutinous rice flour, snowskin powder, shortening, cooking oil, mungbean filling, pistachio kunafa truffle (milk couverture, almond filling, pistachio paste, pistachio nuts, feuilletine).",
                 ["🌰 Tree nuts (pistachio, almond)", "🥛 Milk"],
                 "May contain traces of gluten, egg, sesame, peanuts and soy."),
        ],
    },
]


# --------------------------------------------------------------------------
# Builders
# --------------------------------------------------------------------------
def wa(number, text):
    from urllib.parse import quote
    return "https://wa.me/%s?text=%s" % (number, quote(text))


def keepsake_card(k):
    chan_cls = "chan" if k["channel"] == "online" else "chan booth"
    chan_lbl = "Order online" if k["channel"] == "online" else "At our booths"
    var = ' <span class="var">(%s)</span>' % k["variant"] if k.get("variant") else ""

    tags = ['<span class="tag">%s</span>' % k["pcs"]]
    if "G" in k["sets"]:
        tags.append('<span class="tag chill">Snowskin · chilled</span>')
    else:
        tags.append('<span class="tag sage">Halal certified</span>')
    if k.get("artist"):
        tags.append('<span class="tag rose">Artist edition</span>')
    if k.get("bcf"):
        tags.append('<span class="tag gold">$1 to charity</span>')

    if k["channel"] == "online":
        cta = ('<a class="btn sm" href="%s" target="_blank" rel="noopener" '
               'data-order="%s" data-name="%s">Order online</a>'
               % (k["url"], k["id"], k["name"]))
    else:
        msg = ("Hello! I'd like to ask about the %s Mid-Autumn gift set (S$%d). "
               "Which booths have it in stock?" % (k["name"], k["price"]))
        cta = ('<a class="btn sm gold" href="%s" target="_blank" rel="noopener" '
               'data-booth="%s" data-name="%s">Check booth stock</a>'
               '<a class="btn sm ghost" href="#where">See booths</a>'
               % (wa(WA_CUSTOMER, msg), k["id"], k["name"]))

    note = '<p class="note">%s</p>' % k["note"] if k.get("note") else ""
    body = "".join("<p>%s</p>" % p for p in k["body"])

    return """<article class="pack" id="k-%s">
  <div class="pack-photo"><span class="%s">%s</span>
    <img src="assets/%s?v=%d" alt="%s" width="700" height="875" loading="lazy" decoding="async"></div>
  <div class="pack-body">
    <span class="fmt">%s</span>
    <h4>%s%s</h4>
    <p class="pcn">%s</p>
    <p class="pgloss">%s · %s</p>
    <div class="becomes"><span class="lbl">After Mid-Autumn it becomes</span><p>%s</p></div>
    <details class="more"><summary>The full story</summary><div class="desc">%s</div>%s</details>
    <div class="pack-foot"><span class="price">S$%d</span>%s</div>
    <div class="res-meta" style="margin-top:14px">%s</div>
  </div>
</article>""" % (k["id"], chan_cls, chan_lbl, k["img"], ASSET_V, k["alt"],
                 k["format"], k["name"], var, k["cn"], k["pinyin"], k["gloss"],
                 k["becomes"], body, note, k["price"], cta, "".join(tags))


def sets_table():
    rows = ['<div class="r hdr"><div>Set</div><div>Range</div><div>What\'s inside</div></div>']
    for s in SETS:
        fl = "".join("<li>%s</li>" % f for f in s["flavours"])
        halal = " · Halal certified, vegetarian" if s["halal"] else " · not Halal certified"
        rows.append(
            '<div class="r"><div class="price">%s</div>'
            '<div class="g">%s%s</div><ul>%s</ul></div>'
            % (s["id"], s["group"], halal, fl))
    return '<div class="settable">%s</div>' % "".join(rows)


def booths_html():
    out = []
    for name, level, flag in BOOTHS:
        f = '<span class="bf">Flagship store</span>' if flag else ""
        out.append('<div class="booth%s"><p class="bn">%s</p><p class="bl">%s</p>%s</div>'
                   % (" flag" if flag else "", name, level, f))
    return '<div class="booths">%s</div>' % "".join(out)


def js_data():
    """Trim the keepsake data down to what the browser tools need."""
    out = []
    for k in KEEPSAKES:
        out.append({
            "id": k["id"], "name": k["name"], "cn": k["cn"], "pinyin": k["pinyin"],
            "gloss": k["gloss"], "format": k["format"], "pcs": k["pcs"],
            "price": k["price"], "img": k["img"], "alt": k["alt"],
            "channel": k["channel"], "url": k.get("url", ""),
            "sets": k["sets"], "duoNote": k.get("duo_note", ""),
            "becomes": k["becomes"], "why": k["why"], "note": k.get("note", ""),
            "variant": k.get("variant", ""), "bcf": bool(k.get("bcf")),
            "artist": bool(k.get("artist")), "score": k["score"],
            "halalSafe": "G" not in k["sets"],
        })
    return out


JS = """
(function(){
  var K = %(keepsakes)s;
  var S = %(sets)s;
  var TABLE_SET = %(tableset)s;
  var BUDGET = %(budget)s;
  var RECIP = %(recip)s;
  var WA_CUSTOMER = "%(wacust)s";
  var SITE = "%(site)s";

  function ga(name, params){ if(window.gtag){ window.gtag('event', name, params||{}); } }
  function byId(id){ return document.getElementById(id); }
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function find(id){ for(var i=0;i<K.length;i++){ if(K[i].id===id) return K[i]; } return null; }
  function setById(id){ for(var i=0;i<S.length;i++){ if(S[i].id===id) return S[i]; } return null; }

  /* ---------------- jump nav ---------------- */
  var links = [].slice.call(document.querySelectorAll('.jump a[href^="#"]'));
  var secs  = links.map(function(a){ return byId(a.getAttribute('href').slice(1)); });
  var bar = byId('navProgress'), toTop = byId('toTop');
  function onScroll(){
    var h = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + '%%';
    toTop.classList.toggle('show', window.scrollY > 700);
    var idx = -1;
    for (var i=0;i<secs.length;i++){
      if (secs[i] && secs[i].getBoundingClientRect().top <= 100) idx = i;
    }
    links.forEach(function(a,i){ a.classList.toggle('active', i===idx); });
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  window.addEventListener('resize', onScroll, {passive:true});
  onScroll();
  toTop.addEventListener('click', function(){
    var r = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({top:0, behavior: r ? 'auto' : 'smooth'});
  });

  /* ---------------- outbound click tracking ---------------- */
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a');
    if(!a) return;
    if(a.dataset.order) ga('order_click', {item_id:a.dataset.order, item_name:a.dataset.name});
    if(a.dataset.booth) ga('booth_click', {item_id:a.dataset.booth, item_name:a.dataset.name});
    if(a.dataset.corp)  ga('corporate_click', {method:a.dataset.corp});
    if(a.dataset.brochure) ga('brochure_download', {});
  });

  /* ---------------- gift concierge ---------------- */
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

  function pool(){
    var b = BUDGET[ans.budget];
    var hard = K.filter(function(k){
      if (ans.table === 'halal'   && !k.halalSafe) return false;
      if (ans.table === 'chilled' && k.sets.indexOf('G') < 0) return false;
      if (ans.budget !== 'b4'){ if (k.price <= b.min || k.price > b.max) return false; }
      return true;
    });
    if (hard.length) return {list:hard, relaxed:false};
    /* Nothing survived. Drop the budget rail last, and say so. */
    var soft = K.filter(function(k){
      if (ans.table === 'halal'   && !k.halalSafe) return false;
      if (ans.table === 'chilled' && k.sets.indexOf('G') < 0) return false;
      return true;
    });
    return {list:soft.length ? soft : K.slice(), relaxed:true};
  }

  function scoreOf(k){
    var s = (k.score[ans.recipient]||0) * 2 + (k.score[ans.priority]||0) * 3;
    var want = TABLE_SET[ans.table];
    if (k.sets.length && k.sets.indexOf(want) < 0) s -= 3;   /* wrong mooncake family */
    if (ans.budget === 'b4' && k.price >= 78) s += 1;        /* corporate leans premium */
    if (k.channel === 'online') s += 0.5;                    /* tiebreak: buyable now */
    return s;
  }

  function recSet(k){
    if (!k.sets.length) return null;
    var want = TABLE_SET[ans.table];
    return k.sets.indexOf(want) >= 0 ? want : k.sets[0];
  }

  function finish(){
    var p = pool();
    var ranked = p.list.slice().sort(function(a,b){ return scoreOf(b) - scoreOf(a); });
    var top = ranked[0], alt = ranked[1];
    render(top, alt, p.relaxed);
    ga('concierge_complete', {
      recipient: ans.recipient, priority: ans.priority,
      table: ans.table, budget: ans.budget, match: top.id
    });
  }

  function render(k, alt, relaxed){
    var st = recSet(k);
    var s = st ? setById(st) : null;
    var recipLabel = RECIP[ans.recipient] || 'them';

    var meta = ['<span class="tag">' + esc(k.format) + ' · ' + esc(k.pcs) + '</span>'];
    if (k.sets.indexOf('G') >= 0) meta.push('<span class="tag chill">Snowskin · chilled</span>');
    else meta.push('<span class="tag sage">Halal certified</span>');
    if (k.bcf) meta.push('<span class="tag gold">$1 to charity</span>');
    if (k.channel === 'booth') meta.push('<span class="tag">At our booths</span>');

    var setLine = s
      ? '<p class="res-note"><strong>Recommended mooncake set ' + s.id + '</strong> · ' +
        esc(s.flavours.join(', ')) + '</p>'
      : (k.duoNote ? '<p class="res-note">' + esc(k.duoNote) + '</p>' : '');

    var cta;
    if (k.channel === 'online'){
      cta = '<a class="btn" href="' + k.url + '" target="_blank" rel="noopener" ' +
            'data-order="' + k.id + '" data-name="' + esc(k.name) + '">Order online · S$' + k.price + '</a>';
    } else {
      var msg = "Hello! The gift matcher on your Mid-Autumn page suggested the " + k.name +
                " (S$" + k.price + "). Which booths have it in stock?";
      cta = '<a class="btn gold" href="https://wa.me/' + WA_CUSTOMER + '?text=' +
            encodeURIComponent(msg) + '" target="_blank" rel="noopener" data-booth="' + k.id +
            '" data-name="' + esc(k.name) + '">Check booth stock · S$' + k.price + '</a>';
    }

    var shareMsg = "For " + recipLabel + " this Mid-Autumn: " + k.name + " " + k.cn +
                   " from Mdm Ling Bakery, S$" + k.price + ". " + k.becomes + " " + SITE;

    var html =
      '<div class="res-grid">' +
        '<div class="res-photo"><img src="assets/' + k.img + '?v=%(v)d" alt="' + esc(k.alt) + '"></div>' +
        '<div class="res-body">' +
          '<span class="tool-kicker">Your match</span>' +
          '<h4>' + esc(k.name) + (k.variant ? ' <span style="font-weight:400;font-size:18px;color:var(--muted)">(' + esc(k.variant) + ')</span>' : '') + '</h4>' +
          '<p class="rcn">' + esc(k.cn) + '</p>' +
          '<p class="rgloss">' + esc(k.pinyin) + ' · ' + esc(k.gloss) + '</p>' +
          '<p class="res-why">For ' + esc(recipLabel) + ', ' + esc(k.why) + '</p>' +
          '<div class="res-meta">' + meta.join('') + '</div>' +
          setLine +
          (relaxed ? '<p class="res-note">Nothing in the collection sits inside that budget with those requirements, so this is the closest fit.</p>' : '') +
          (k.note ? '<p class="res-note">' + esc(k.note) + '</p>' : '') +
          '<div class="res-acts">' + cta +
            '<a class="btn ghost" href="https://wa.me/?text=' + encodeURIComponent(shareMsg) +
              '" target="_blank" rel="noopener" id="cShare">Send to someone</a>' +
            '<button class="btn ghost" id="cAgain" type="button">Start again</button>' +
          '</div>' +
          (alt ? '<p class="res-alt">Also worth a look: <a href="#k-' + alt.id + '">' + esc(alt.name) +
                 '</a> at S$' + alt.price + ', ' + esc(alt.becomes.charAt(0).toLowerCase() + alt.becomes.slice(1)) + '</p>' : '') +
        '</div>' +
      '</div>';

    var box = byId('cResult');
    box.innerHTML = html;
    box.classList.add('on');
    byId('cQuiz').style.display = 'none';
    pips.forEach(function(p){ p.classList.add('on'); });
    byId('cAgain').addEventListener('click', function(){ ans = {}; show(0); });
    byId('cShare').addEventListener('click', function(){ ga('concierge_share', {match:k.id}); });
    box.scrollIntoView({behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto':'smooth', block:'start'});
  }

  /* ---------------- build your gift ---------------- */
  var bpick = byId('bPick'), bout = byId('bOut');
  K.forEach(function(k){
    var c = document.createElement('button');
    c.type = 'button'; c.className = 'chip'; c.textContent = k.name +
      (k.variant ? ' (' + k.variant + ')' : '');
    c.addEventListener('click', function(){
      [].slice.call(bpick.children).forEach(function(x){ x.classList.remove('on'); });
      c.classList.add('on');
      buildOut(k);
      ga('builder_select', {item_id:k.id, item_name:k.name});
    });
    bpick.appendChild(c);
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
      var msg = "Hello! I'd like to ask about the " + k.name + " Mid-Autumn gift set (S$" +
                k.price + "). Which booths have it in stock?";
      cta = '<a class="btn sm gold" href="https://wa.me/' + WA_CUSTOMER + '?text=' +
            encodeURIComponent(msg) + '" target="_blank" rel="noopener" data-booth="' + k.id +
            '" data-name="' + esc(k.name) + '">Check booth stock</a>';
    }

    bout.innerHTML =
      '<div class="bhead">' +
        '<img src="assets/' + k.img + '?v=%(v)d" alt="' + esc(k.alt) + '">' +
        '<div><h4>' + esc(k.name) + '</h4>' +
          '<p class="rgloss" style="margin:4px 0 0">' + esc(k.cn) + ' · ' + esc(k.pinyin) + '</p>' +
          '<div class="res-meta" style="margin-top:12px"><span class="price">S$' + k.price + '</span>' +
          '<span class="tag">' + esc(k.format) + ' · ' + esc(k.pcs) + '</span>' +
          '<span class="tag' + (k.channel === 'booth' ? ' gold' : '') + '">' +
            (k.channel === 'booth' ? 'At our booths' : 'Order online') + '</span></div>' +
          '<div class="res-acts" style="margin-top:16px">' + cta +
            '<a class="btn sm ghost" href="#k-' + k.id + '">Read its story</a></div>' +
        '</div>' +
      '</div>' +
      '<p class="rgloss" style="margin:0 0 12px">Choose one mooncake set to go inside</p>' +
      '<div class="setlist">' + rows + '</div>' +
      (k.note ? '<p class="res-note">' + esc(k.note) + '</p>' : '');
    bout.classList.add('on');
  }
})();
"""


def build():
    ks = json.dumps(js_data(), ensure_ascii=False, separators=(",", ":"))
    st = json.dumps(SETS, ensure_ascii=False, separators=(",", ":"))
    tableset = json.dumps({t[0]: t[2] for t in TABLES}, ensure_ascii=False)
    budget = json.dumps({b[0]: {"min": b[2], "max": b[3]} for b in BUDGETS}, ensure_ascii=False)
    recip = json.dumps({r[0]: r[2] for r in RECIPIENTS}, ensure_ascii=False)

    js = JS % {"keepsakes": ks, "sets": st, "tableset": tableset, "budget": budget,
               "recip": recip, "wacust": WA_CUSTOMER, "site": SITE_URL, "v": ASSET_V}

    # ---- concierge questions ----
    def optset(key, opts, n, total, title):
        o = "".join('<button type="button" class="opt" data-val="%s">%s</button>' % (v, l)
                    for v, l in opts)
        back = '<button type="button" class="qback">Back</button>' if n > 1 else ""
        return ('<div class="q%s" data-key="%s"><span class="qn">Question %d of %d</span>'
                '<h4>%s</h4><div class="opts">%s</div>%s</div>'
                % (" on" if n == 1 else "", key, n, total, title, o, back))

    qs = "".join([
        optset("recipient", [(r[0], r[1]) for r in RECIPIENTS], 1, 4, "Who are you gifting?"),
        optset("priority", [(p[0], p[1]) for p in PRIORITIES], 2, 4, "What matters most to you here?"),
        optset("table", [(t[0], t[1]) for t in TABLES], 3, 4, "And their table?"),
        optset("budget", [(b[0], b[1]) for b in BUDGETS], 4, 4, "Roughly what per gift?"),
    ])

    ranges = ""
    for r in RANGES:
        intro = '<p class="range-intro">%s</p>' % r["intro"] if r["intro"] else ""
        ranges += ('<section class="range" id="%s"><div class="range-head">'
                   '<span class="range-num">%d</span><h3>%s</h3><span class="tag2">%s</span></div>'
                   '%s<div class="flavours">%s</div></section>'
                   % (r["id"], r["n"], r["title"], r["tag"], intro, "".join(r["items"])))

    online = sum(1 for k in KEEPSAKES if k["channel"] == "online")
    corp_msg = ("Hello! I'd like to enquire about Mid-Autumn 2026 corporate gifting "
                "and bulk orders.")

    html = TEMPLATE % {
        "css": CSS, "js": js, "qs": qs,
        "packs": "".join(keepsake_card(k) for k in KEEPSAKES),
        "sets_table": sets_table(),
        "ranges": ranges,
        "booths": booths_html(),
        "ga": GA_ID, "site": SITE_URL, "v": ASSET_V,
        "n_keepsakes": len(KEEPSAKES), "n_online": online,
        "n_booths": len(BOOTHS),
        "wa_corp": wa(WA_CORPORATE, corp_msg),
        "wa_cust": wa(WA_CUSTOMER, "Hello! I have a question about your Mid-Autumn 2026 mooncakes."),
        "email_corp": EMAIL_CORPORATE, "corp_min": "{:,}".format(CORPORATE_MIN),
        "free_del": FREE_DELIVERY,
        "tel_corp": "+65 8428 6006", "tel_cust": "+65 8468 0201",
    }
    out = os.path.join(HERE, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote %s  (%.1f KB)" % (out, len(html) / 1024.0))
    print("keepsakes: %d  ·  online: %d  ·  booth: %d"
          % (len(KEEPSAKES), online, len(KEEPSAKES) - online))


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mdm Ling Bakery · Mid-Autumn 2026</title>
<meta name="description" content="Mdm Ling Bakery Mid-Autumn 2026. Fourteen keepsake gift sets and three mooncake ranges, with a gift matcher to help you choose. 花月情长, A Bond in Lasting Bloom. Halal certified, made in Singapore.">
<link rel="canonical" href="%(site)s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Mdm Ling Bakery">
<meta property="og:title" content="Mdm Ling Bakery · Mid-Autumn 2026">
<meta property="og:description" content="Fourteen keepsake gift sets built to outlive the season. 花月情长 · A Bond in Lasting Bloom.">
<meta property="og:url" content="%(site)s">
<meta property="og:image" content="%(site)sassets/og-midautumn-2026.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Mdm Ling Bakery Mid-Autumn 2026 keepsake gift set collection">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Mdm Ling Bakery · Mid-Autumn 2026">
<meta name="twitter:description" content="Fourteen keepsake gift sets built to outlive the season. 花月情长 · A Bond in Lasting Bloom.">
<meta name="twitter:image" content="%(site)sassets/og-midautumn-2026.jpg">
<meta name="theme-color" content="#A97F78">
<link rel="icon" href="data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%%3E%%3Crect width='64' height='64' fill='%%23A97F78'/%%3E%%3Ccircle cx='32' cy='31' r='15' fill='none' stroke='%%23C7A66A' stroke-width='3'/%%3E%%3C/svg%%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Work+Sans:wght@500;600&display=swap" rel="stylesheet">
<script async src="https://www.googletagmanager.com/gtag/js?id=%(ga)s"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '%(ga)s');
</script>
<style>%(css)s</style>
</head>
<body>

<nav class="jump">
  <div class="in">
    <a href="#concierge">Gift matcher</a>
    <a href="#keepsakes">Keepsakes</a>
    <a href="#builder">Build your gift</a>
    <a href="#sets">Mooncake sets</a>
    <a href="#mooncakes">Mooncakes</a>
    <a href="#garden">The Painted Garden</a>
    <a href="#corporate">Corporate</a>
    <a href="#where">Where to buy</a>
  </div>
  <div class="progress" id="navProgress"></div>
</nav>

<header class="hero">
  <div class="wrap hgrid">
    <div>
      <span class="eyebrow">Mdm Ling Bakery · Mid-Autumn 2026</span>
      <h1>Gifts that outlive the season</h1>
      <p class="cn"><span class="han">花月情长</span> <span class="en">· A Bond in Lasting Bloom</span></p>
      <p>Fourteen keepsakes and three mooncake ranges. Every piece is made to be kept, used and remembered long after the last mooncake is gone.</p>
      <div class="acts">
        <a class="btn light" href="#concierge">Find the right gift</a>
        <a class="btn ghost" href="#keepsakes" style="color:#FBF8F6">See the keepsakes</a>
      </div>
    </div>
    <figure class="hshot">
      <img src="assets/painted-garden-tin.webp?v=%(v)d" alt="The Painted Garden keepsake tin, this year's artist edition, painted by Phuay Li Ying" width="700" height="875" fetchpriority="high" decoding="async">
    </figure>
  </div>
</header>

<section class="ethos">
  <div class="wrap">
    <h2>What we stand for</h2>
    <p>At Mdm Ling Bakery, gifting is the whole point. We design gift sets that are sustainable, heartfelt and genuinely useful, the kind kept and reused long after the mooncakes are gone. Every piece carries a little of Singapore's heritage with a modern spirit, made for the simple, universal act of bringing something to share.</p>
    <div class="pillars">
      <span>Sustainably designed keepsakes</span>
      <span>Heartfelt, functional, meaningful</span>
      <span>Singapore heritage, modern spirit</span>
      <span>Made to be shared</span>
    </div>
  </div>
</section>

<div class="wrap">

  <!-- ================= GIFT CONCIERGE ================= -->
  <section class="part" id="concierge">
    <div class="tool">
      <span class="tool-kicker">The gift matcher</span>
      <h3>Tell us who it's for</h3>
      <p class="sub">Fourteen keepsakes, seven mooncake sets. Four quick questions and we'll narrow it to one, with the mooncake set that suits their table.</p>
      <div class="qsteps"><i class="on"></i><i></i><i></i><i></i></div>
      <div id="cQuiz">%(qs)s</div>
      <div class="result" id="cResult"></div>
    </div>
  </section>

  <!-- ================= KEEPSAKES ================= -->
  <section class="part" id="keepsakes">
    <div class="part-head">
      <span class="part-num">Part One</span>
      <h2>The Keepsakes</h2>
      <p class="lede">The heart of this year's collection. Every keepsake belongs to one family, <strong>花月情长 · A Bond in Lasting Bloom</strong>, and carries its own four character name the way heirlooms in a Chinese household always have. Fill any of them with the mooncake set of your choice.</p>
      <p class="lede" style="margin-top:12px"><strong>%(n_online)d of the %(n_keepsakes)d</strong> can be ordered online right now. The rest are at our %(n_booths)d booths across the island, and we'll help you find one.</p>
    </div>
    <img src="assets/group-packaging.webp?v=%(v)d" alt="The full Mdm Ling Bakery Mid-Autumn 2026 gift set collection, tins, leather bags and gift boxes" width="1120" height="745" loading="lazy" decoding="async" style="border:1px solid var(--hair); margin-bottom:2px;">
    <div class="packs">%(packs)s</div>
  </section>

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

  <!-- ================= MOONCAKE SETS ================= -->
  <section class="part" id="sets">
    <div class="part-head">
      <span class="part-num">Part Two</span>
      <h2>The Mooncake Sets</h2>
      <p class="lede">Choose your keepsake, then choose what fills it. <strong>All baked sets, A to F, are Halal certified and vegetarian.</strong> The snowskin set G is <strong>not Halal certified</strong> and comes only in the Orchid Reverie tin. Our duo tins carry two traditional mooncakes rather than a lettered set.</p>
    </div>
    %(sets_table)s
  </section>

  <!-- ================= MOONCAKES ================= -->
  <section class="part" id="mooncakes">
    <div class="part-head">
      <span class="part-num">Part Three</span>
      <h2>The Mooncakes</h2>
      <p class="lede">Three ranges this year. Our premium traditional baked classics, our signature assorted range with a low sugar skin for each flavour, and our premium truffle snowskin range served chilled.</p>
    </div>
    <img src="assets/group-mooncakes.webp?v=%(v)d" alt="The Mdm Ling Bakery Mid-Autumn 2026 mooncake range, traditional and Momoyama Cantonese" width="1120" height="1680" loading="lazy" decoding="async" style="border:1px solid var(--hair); max-height:520px; object-fit:cover;">
    %(ranges)s

    <div class="panel" id="storage">
      <h4>Storage and freshness</h4>
      <p>Our baked mooncakes keep for <strong>2 months from production</strong>, with the <strong>best before date printed on the packaging</strong>. Store them in a <strong>cool, dry place</strong> away from direct sunlight, and enjoy them soon after opening.</p>
      <p>Snowskin mooncakes are <strong>best served chilled</strong>. Keep them away from direct heat and sunlight, and never leave them in the car boot. Within <strong>2 hours of purchase</strong>, place them in the freezer at <strong>&minus;12&deg;C or below</strong>, where they'll keep for <strong>up to 8 weeks</strong>. Once thawed, <strong>do not refreeze</strong>.</p>
    </div>
  </section>

  <!-- ================= THE PAINTED GARDEN ================= -->
  <section class="part" id="garden">
    <div class="part-head">
      <span class="part-num">The artist</span>
      <h2>A garden painted for Mdm Ling</h2>
    </div>
    <div class="feature">
      <div class="fimg"><img src="assets/painted-garden-tin.webp?v=%(v)d" alt="The Painted Garden keepsake tin, watercolour florals by Singaporean artist Phuay Li Ying" width="700" height="875" loading="lazy" decoding="async"></div>
      <div class="ftxt">
        <span class="tool-kicker">百花迎月 · The Painted Garden</span>
        <h3>The flowers she painted</h3>
        <p>Singaporean artist <strong>Phuay Li Ying</strong> painted this year's garden as a quiet portrait of Mdm Ling herself. The central bloom is her. The smaller flowers are the people she gathers around her, <strong>wildflowers of many colours and origins rising together to greet the festival moon</strong>.</p>
        <p>Her artwork runs across three pieces in the collection: the <strong>heritage tin</strong>, the <strong>duo tin</strong> and the <strong>silk paper gift box</strong>, each washed in gentle pinks, lilacs and gold with a quiet glow of foil.</p>
        <p>And the giving reaches further than the table. For every <strong>Painted Garden Box</strong> bought, <strong>we donate $1 to the Breast Cancer Foundation</strong>, supporting awareness, screening and survivor care here in Singapore. Each garden you give helps look after someone else's.</p>
        <div class="res-acts">
          <a class="btn" href="#k-the-painted-garden-box" >See The Painted Garden Box</a>
          <a class="btn ghost" href="https://www.instagram.com/theworldofying/" target="_blank" rel="noopener">Ying's work</a>
        </div>
      </div>
    </div>
  </section>

  <!-- ================= CORPORATE ================= -->
  <section class="part" id="corporate">
    <div class="corp">
      <span class="tool-kicker">Corporate gifting</span>
      <h3>When the list runs to a hundred names</h3>
      <p>Client gifts, staff appreciation, festive hampers for the whole office. We handle bulk Mid-Autumn orders across the full collection, and we'll help you land on something that looks considered at any volume.</p>
      <div class="facts">
        <div><span class="n">$%(corp_min)s</span><span class="l">Minimum spend for corporate and bulk orders</span></div>
        <div><span class="n">%(n_keepsakes)d</span><span class="l">Keepsakes to choose from, tins to leather</span></div>
        <div><span class="n">$%(free_del)d</span><span class="l">Free delivery on standard orders above this</span></div>
      </div>
      <div class="acts">
        <a class="btn gold" href="%(wa_corp)s" target="_blank" rel="noopener" data-corp="whatsapp">WhatsApp the corporate team</a>
        <a class="btn ghost" href="mailto:%(email_corp)s?subject=Mid-Autumn%%202026%%20corporate%%20gifting" data-corp="email" style="color:#EDE6E2">%(email_corp)s</a>
        <a class="btn ghost" href="tel:+6584286006" data-corp="phone" style="color:#EDE6E2">%(tel_corp)s</a>
      </div>
    </div>
  </section>

  <!-- ================= WHERE TO BUY ================= -->
  <section class="part" id="where">
    <div class="part-head">
      <span class="part-num">Where to buy</span>
      <h2>Find us across Singapore</h2>
      <p class="lede">Every keepsake in this collection is at our booths. <strong>%(n_online)d of the %(n_keepsakes)d</strong> can also be ordered online, with <strong>free delivery above $%(free_del)d</strong>. If you're after one of the booth only pieces, message us and we'll check stock for you.</p>
      <div class="res-acts" style="margin-bottom:26px">
        <a class="btn" href="https://www.mdmlingbakery.com" target="_blank" rel="noopener" data-order="store" data-name="Online store">Shop online</a>
        <a class="btn ghost" href="%(wa_cust)s" target="_blank" rel="noopener" data-booth="general" data-name="General enquiry">WhatsApp us · %(tel_cust)s</a>
        <a class="btn ghost" href="assets/mlb-midautumn-2026-brochure.pdf" target="_blank" rel="noopener" data-brochure="1">Download the brochure</a>
      </div>
    </div>
    %(booths)s
  </section>

</div>

<footer>
  <div class="wrap">
    <span class="fb">Mdm Ling Bakery</span>
    <span class="fcn">花月情长 · A Bond in Lasting Bloom</span>
    <div class="res-acts" style="margin:0 0 24px">
      <a class="btn ghost sm" href="https://www.mdmlingbakery.com" target="_blank" rel="noopener" style="color:#C9BDB7">mdmlingbakery.com</a>
      <a class="btn ghost sm" href="%(wa_cust)s" target="_blank" rel="noopener" style="color:#C9BDB7">%(tel_cust)s</a>
      <a class="btn ghost sm" href="%(wa_corp)s" target="_blank" rel="noopener" style="color:#C9BDB7" data-corp="footer">Corporate %(tel_corp)s</a>
    </div>
    <p class="fl">Ingredients and allergen advice on this page follow the printed product labels. If you're gifting to someone with a food allergy, do check the label on the box as well. Prices shown are retail prices in Singapore dollars. Halal certification covers our baked mooncakes; the truffle snowskin range isn't Halal certified.</p>
  </div>
</footer>

<button id="toTop" aria-label="Back to top">&uarr;</button>
<script>%(js)s</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
