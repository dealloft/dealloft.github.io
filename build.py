#!/usr/bin/env python3
"""Builds the Dealloft static site.

Edit content in:
  content/posts/*.md   one file per blog post (front matter, '---', then body)
  content/brands.json  brand names, public URLs and your affiliate links
  content/deals.json   deal cards for the homepage and Deals page
Then run:  python3 build.py
It regenerates data.js, posts/*.html, the other pages, sitemap.xml and robots.txt.
"""
import json, os, re, html, glob, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
NAME = "Dealloft"
TAG = "Shop smarter. Pay less."
SITE_URL = "https://dealloft.github.io"            # e.g. "https://yourorg.github.io" (no trailing slash). Needed for sitemap and canonical tags.
EMAIL = "thomas.s15786@gmail.com"   # shown on the Contact page
AUTHOR = "Dealloft Editorial"
SHOW_SAMPLES = False

CATS = [("fashion","Fashion & Beauty","#C4552D"),("home","Home & Living","#2F4A3A"),("wellness","Health & Wellness","#8A5A44"),
        ("tech","Tech & Gadgets","#3C4F76"),("family","Baby, Kids & Pets","#B9852E"),("fitness","Fitness & Outdoors","#5B6B3A")]
CATMAP = {a: (b, c) for a, b, c in CATS}

def esc(s): return html.escape(s, quote=True)

# ---------- markdown-lite ----------
def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    def link(m):
        t, u = m.group(1), html.unescape(m.group(2))
        if u.startswith("go:"):
            return f'<a href="../go.html?b={u[3:]}" rel="sponsored nofollow noopener" target="_blank">{t}</a>'
        return f'<a href="{esc(u)}" rel="noopener" target="_blank">{t}</a>'
    return re.sub(r"\[(.+?)\]\((.+?)\)", link, s)

def render_body(md):
    lines = md.strip().split("\n")
    out, faq, i, section = [], [], 0, ""
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1; continue
        if ln.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].startswith("> "):
                buf.append(lines[i][2:]); i += 1
            out.append(f'<div class="answer"><b class="lbl">Short answer</b><p>{inline(" ".join(buf))}</p></div>')
            continue
        if ln.startswith("## "):
            section = ln[3:].strip()
            out.append(f"<h2 id=\"{re.sub(r'[^a-z0-9]+','-',section.lower()).strip('-')}\">{inline(section)}</h2>"); i += 1; continue
        if ln.startswith("### "):
            q = ln[4:].strip()
            ans = []
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith("#"):
                ans.append(lines[i].strip()); i += 1
            a = " ".join(ans)
            if section == "FAQ":
                faq.append((q, a))
            out.append(f"<h3>{inline(q)}</h3><p>{inline(a)}</p>")
            continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            rows = [r for r in rows if not all(re.fullmatch(r"-+", c) for c in r)]
            t = "<div class=\"tbl\"><table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr></thead><tbody>"
            for r in rows[1:]:
                t += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
            out.append(t + "</tbody></table></div>"); continue
        if ln.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:]); i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>"); continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r"(> |## |### |\||- )", lines[i]):
            buf.append(lines[i].strip()); i += 1
        txt = " ".join(buf)
        if section.startswith("How we researched"):
            out.append(f'<p class="method">{inline(txt)}</p>')
        else:
            out.append(f"<p>{inline(txt)}</p>")
    return "\n".join(out), faq

def parse_post(path):
    raw = open(path, encoding="utf-8").read()
    head, body = raw.split("\n---\n", 1)
    meta = {}
    for ln in head.splitlines():
        if ":" in ln:
            k, v = ln.split(":", 1); meta[k.strip()] = v.strip()
    meta["body"] = body
    return meta

# ---------- shared layout ----------
def head(title, desc, on="", root="", canonical="", extra_head=""):
    can = f'<link rel="canonical" href="{esc(canonical)}">' if canonical else ""
    og = f'<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="article">' if canonical else ""
    nav = lambda k, label, href: f'<a href="{root}{href}" class="{"on" if on==k else ""}">{label}</a>'
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">{can}{og}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}style.css">{extra_head}</head><body>
<div class="disc">Some links on this site are affiliate links. We may earn a commission at no extra cost to you. <a href="{root}disclosure.html">Learn more</a></div>
<header class="top"><div class="wrap"><a class="logo" href="{root}index.html"><i></i>{NAME}</a>
<nav>{nav("deals","Deals","deals.html")}{nav("blog","Blog","blog.html")}{nav("about","About","about.html")}{nav("contact","Contact","contact.html")}</nav>
<a class="btn" href="{root}deals.html">Browse deals</a></div></header>"""

def foot(root=""):
    return f"""<footer><div class="wrap"><div class="cols"><div><a class="logo" style="color:#fff" href="{root}index.html"><i></i>{NAME}</a><p style="max-width:28em;margin-top:12px">Guides and deals for everyday shopping. Clear terms, sources cited, no pressure.</p></div>
<div><h4>Explore</h4><a href="{root}deals.html">Deals</a><a href="{root}blog.html">Blog</a><a href="{root}about.html">About</a></div>
<div><h4>Legal</h4><a href="{root}disclosure.html">Affiliate disclosure</a><a href="{root}privacy.html">Privacy</a><a href="{root}contact.html">Contact</a></div></div>
<small>&copy; 2026 {NAME}. We earn commissions from some links. Prices and offers can change; always check the retailer's page.</small></div></footer>
<script src="{root}data.js"></script><script src="{root}app.js"></script>"""

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)

# ---------- load content ----------
brands = {k: v for k, v in json.load(open(f"{ROOT}/content/brands.json")).items() if not k.startswith("_")}
deals = json.load(open(f"{ROOT}/content/deals.json"))
posts = [parse_post(p) for p in sorted(glob.glob(f"{ROOT}/content/posts/*.md"))]
posts.sort(key=lambda p: p["date"], reverse=True)

# ---------- data.js ----------
data = {
    "SITE_NAME": NAME, "SHOW_SAMPLES": SHOW_SAMPLES,
    "CATS": [{"id": a, "name": b, "color": c} for a, b, c in CATS],
    "BRANDS": {k: {"name": v["name"], "url": v["url"], "aff": v.get("aff", ""), "aff2": v.get("aff_backup", "")} for k, v in brands.items()},
    "DEALS": deals,
    "POSTS": [{"slug": p["slug"], "title": p["title"], "excerpt": p["excerpt"], "cat": p["category"], "date": p["date"],
               "read": p.get("read", "5 min read"), "href": f"posts/{p['slug']}.html"} for p in posts],
}
write("data.js", "// Generated by build.py. Edit content/ and re-run build.py instead of editing this file.\n" +
      "\n".join(f"const {k} = {json.dumps(v, indent=1)};" for k, v in data.items()) + "\n")

# ---------- post pages ----------
for p in posts:
    body_html, faq = render_body(p["body"])
    cat_name = CATMAP[p["category"]][0]
    url = f"{SITE_URL}/posts/{p['slug']}.html" if SITE_URL else ""
    ld = [{
        "@context": "https://schema.org", "@type": "Article", "headline": p["title"], "description": p["description"],
        "datePublished": p["date"], "dateModified": p.get("updated", p["date"]),
        "author": {"@type": "Organization", "name": AUTHOR}, "publisher": {"@type": "Organization", "name": NAME},
        **({"mainEntityOfPage": url} if url else {}),
    }]
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage",
                   "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\[(.+?)\]\(.+?\)", r"\1", a)}} for q, a in faq]})
    ld_tag = '<script type="application/ld+json">' + json.dumps(ld) + "</script>"
    brand = brands[p["brand"]]
    cta = f'<div class="cta-box"><p><b>Ready to look?</b> See {esc(brand["name"])} on its own store and check the current price and stock.</p><a class="btn" href="../go.html?b={p["brand"]}" rel="sponsored nofollow noopener" target="_blank">Visit {esc(brand["name"])}</a></div>'
    # insert the CTA before the FAQ section
    body_html = body_html.replace('<h2 id="faq">', cta + '<h2 id="faq">', 1)
    page = (head(p.get("seo_title", p["title"]), p["description"], "blog", "../", url, ld_tag) +
        f"""<main><article class="article">
<div class="crumbs"><a href="../index.html">Home</a> / <a href="../blog.html">Blog</a> / {esc(cat_name)}</div>
<h1>{esc(p["title"])}</h1>
<div class="byline"><span>By {esc(AUTHOR)}</span><span>&middot;</span><span>Published {p["date"]}</span><span>&middot;</span><span>{esc(p.get("read","5 min read"))}</span></div>
<div class="disclose"><b>Disclosure:</b> this page contains affiliate links. If you buy through them we may earn a commission at no extra cost to you. It does not change what we write.</div>
{body_html}
</article></main>""" + foot("../"))
    write(f"posts/{p['slug']}.html", page)

def post_cards(items, feature=True):
    """Server-rendered post list, so crawlers that do not run JavaScript still see every link."""
    def fmt(d): return datetime.date.fromisoformat(d).strftime("%b %d, %Y").replace(" 0", " ")
    def grad(c): return f"linear-gradient(135deg,{c},{c}99)"
    out = ""
    rest = items
    if feature and items:
        p = items[0]; name, col = CATMAP[p["category"]]; rest = items[1:]
        out += (f'<a class="feat" href="posts/{p["slug"]}.html"><div class="thumb" style="background:{grad(col)}"><em>{esc(name)}</em></div>'
                f'<div class="body"><span class="meta">{fmt(p["date"])} &middot; {esc(p.get("read","5 min read"))}</span><h2>{esc(p["title"])}</h2>'
                f'<p>{esc(p["excerpt"])}</p><span style="color:var(--acc);font-weight:600">Read the guide &rarr;</span></div></a>')
    out += '<div class="grid">'
    for p in rest:
        name, col = CATMAP[p["category"]]
        out += (f'<a class="card" style="text-decoration:none" href="posts/{p["slug"]}.html"><div class="thumb" style="height:140px;background:{grad(col)}"><em>{esc(name)}</em></div>'
                f'<div class="body"><span class="meta">{fmt(p["date"])} &middot; {esc(p.get("read","5 min read"))}</span><h3>{esc(p["title"])}</h3><p>{esc(p["excerpt"])}</p></div></a>')
    return out + "</div>"

# ---------- pages ----------
def page(fn, title, desc, body, on="", extra=""):
    write(fn, head(title, desc, on) + body + foot() + extra)

cat_tiles = "".join(f'<a class="cat" href="deals.html#{a}"><span style="background:{c}"></span><b>{b}</b></a>' for a, b, c in CATS)

page("index.html", f"{NAME}: {TAG}", "Plain-English product guides and deals with sources, prices and clear affiliate disclosure.", f"""
<main><section style="padding-top:44px"><div class="wrap"><div class="head"><div><span class="eyebrow">The blog</span><h1 style="font-size:clamp(2rem,4.2vw,3.2rem);margin:0">Smart shopping, explained.</h1></div><a href="blog.html">All posts &rarr;</a></div>{post_cards(posts[:5])}</div></section>
<section style="background:var(--soft);margin-top:20px"><div class="wrap"><div class="head"><div><span class="eyebrow">Hottest deals</span><h2 style="margin:0">Store offers worth a look right now</h2></div><a href="deals.html">All deals &rarr;</a></div><div class="grid" id="deals"></div></div></section>
<section><div class="wrap"><div class="head"><h2>Browse by topic</h2></div><div class="cats">{cat_tiles}</div></div></section>
<section><div class="wrap"><div class="band"><div><h2>How we keep it honest</h2></div><p>We show the offer, the terms and where it applies, and we say when we have not tested a product. When you buy through some of our links, we earn a small commission from the retailer. It never changes your price.</p></div></div></section></main>""",
     extra="<script>renderDeals(document.getElementById('deals'),4)</script>")

page("deals.html", f"Deals: {NAME}", "Current store offers, with the date we last checked each one.", """<main><section><div class="wrap"><span class="eyebrow">Deals</span><h1 style="font-size:clamp(2rem,4vw,3rem)">Current offers</h1>
<p style="color:var(--mute);max-width:40em">Offers are set by the retailers. We show the date we last checked each one. Terms and expiry can change, so confirm at checkout.</p>
<div class="filters" id="filters" style="margin-top:22px"></div><div class="grid" id="deals"></div></div></section></main>""", "deals",
     "<script>const t=document.getElementById('deals');initFilters(document.getElementById('filters'),t);const h=location.hash.slice(1);if(h&&CATS.some(c=>c.id===h)){state.cat=h;[...document.getElementById('filters').children].forEach(b=>b.classList.toggle('on',b.dataset.c===h))}renderDeals(t)</script>")

page("blog.html", f"Blog: {NAME}", "Buying guides with specs, prices, safety notes and sources.", f"""<main><section><div class="wrap"><span class="eyebrow">Blog</span><h1 style="font-size:clamp(2rem,4vw,3rem)">All guides</h1>{post_cards(posts)}</div></section></main>""", "blog")

page("about.html", f"About: {NAME}", f"About {NAME} and how we make money.", f"""<main><div class="wrap page"><span class="eyebrow">About</span><h1>About {NAME}</h1>
<p>{NAME} publishes buying guides and a deals page. Each guide is built from the brand's own store pages and independent sources, which we link at the bottom.</p>
<h2>How we make money</h2><p>Many links here are affiliate links. If you buy after clicking, the retailer may pay us a commission. It costs you nothing extra and does not change the price you see.</p>
<h2>What we promise</h2><p>We describe offers as the retailer states them, we say when we have not tested a product, we mark what is a brand claim, and we update or remove information that is out of date. If you spot something wrong, <a href="contact.html">tell us</a>.</p></div></main>""", "about")

page("contact.html", f"Contact: {NAME}", f"Contact {NAME}.", f"""<main><div class="wrap page"><span class="eyebrow">Contact</span><h1>Get in touch</h1>
<p>Questions, corrections or an expired offer to report? Email <a href="mailto:{EMAIL}"><b>{EMAIL}</b></a> and we will reply as soon as we can.</p></div></main>""", "contact")

page("disclosure.html", f"Affiliate disclosure: {NAME}", "How affiliate links work on this site.", f"""<main><div class="wrap page"><span class="eyebrow">Disclosure</span><h1>Affiliate disclosure</h1>
<p>{NAME} participates in affiliate programs. When you click some links and make a purchase, we may receive a commission from the retailer. This comes at no additional cost to you.</p>
<p>Commissions help us run the site. They do not change the price you pay, and we describe offers using the information the retailer provides. Offers, prices and codes can change at any time, so always confirm at checkout.</p></div></main>""")

page("privacy.html", f"Privacy: {NAME}", "Privacy policy.", f"""<main><div class="wrap page"><span class="eyebrow">Privacy</span><h1>Privacy policy</h1>
<p>This is a static website. We do not ask you to create an account or submit personal information. If you email us, we use your message only to reply.</p>
<p>When you click an affiliate link, the retailer or affiliate network may set cookies to credit our referral. Their privacy policies apply on their sites. Fonts are loaded from Google Fonts, which may receive your IP address.</p>
<p>If we add analytics or advertising tags later, we will update this page to describe them.</p></div></main>""")

# go.html: redirect page (noindex)
write("go.html", head(f"Taking you to the store: {NAME}", "Redirecting to the retailer.", "", "", "", '<meta name="robots" content="noindex,nofollow">') + f"""
<main class="go"><div class="box"><h1 style="font-size:2rem" id="t">Taking you to the store&hellip;</h1>
<p id="m" style="color:var(--mute)">This link may be an affiliate link. We may earn a commission if you buy, at no extra cost to you.</p>
<p><a class="btn" id="b" href="index.html" rel="sponsored nofollow noopener">Continue</a></p>
<p id="bk" style="display:none;font-size:.9rem"><a id="bka" href="#" rel="sponsored nofollow noopener">Link not working? Try the backup link</a></p></div></main>""" + foot() + """
<script>(function(){var id=new URLSearchParams(location.search).get('b');var b=BRANDS[id];
if(!b){document.getElementById('t').textContent='Link not found';document.getElementById('b').textContent='Back to home';return}
var u=b.aff||b.url;document.getElementById('t').textContent='Taking you to '+b.name+'\\u2026';
var a=document.getElementById('b');a.href=u;a.textContent='Continue to '+b.name;if(b.aff2){document.getElementById('bk').style.display='block';document.getElementById('bka').href=b.aff2}
setTimeout(function(){location.replace(u)},1200)})()</script>""")

# llms.txt (optional hint file for AI tools; not an official standard)
write("llms.txt", f"# {NAME}\n\n> Plain-English product guides and store offers, with sources and affiliate disclosure.\n\n## Guides\n" +
      "".join(f"- [{p['title']}]({SITE_URL + '/' if SITE_URL else ''}posts/{p['slug']}.html): {p['excerpt']}\n" for p in posts))
# robots + sitemap
BOTS = ["Googlebot", "Bingbot", "OAI-SearchBot", "ChatGPT-User", "GPTBot", "Claude-SearchBot", "Claude-User", "ClaudeBot",
        "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended", "DuckDuckBot", "CCBot"]
robots = "# Search and AI answer-engine crawlers are welcome. Only the affiliate redirect page is excluded.\n"
for b in BOTS:
    robots += f"User-agent: {b}\nAllow: /\nDisallow: /go.html\n\n"
robots += "User-agent: *\nAllow: /\nDisallow: /go.html\n" + (f"\nSitemap: {SITE_URL}/sitemap.xml\n" if SITE_URL else "")
write("robots.txt", robots)
if SITE_URL:
    urls = ["", "blog.html", "deals.html", "about.html", "contact.html", "disclosure.html", "privacy.html"] + [f"posts/{p['slug']}.html" for p in posts]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
          "".join(f"<url><loc>{SITE_URL}/{u}</loc></url>" for u in urls) + "</urlset>")
print(f"Built {len(posts)} posts, {len(deals)} deals.", "(set SITE_URL for canonical tags + sitemap)" if not SITE_URL else "")
