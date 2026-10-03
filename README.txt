Dealloft site
=============
Everything you edit lives in /content. Then run:  python3 build.py   (Claude Code can do this for you)

content/posts/*.md   one file per blog post (front matter, a line with ---, then the body)
content/brands.json  brand names, public URLs and YOUR UpPromote affiliate links ("aff")
content/deals.json   deal cards (brand, category, offer text, code, date checked)

Before publishing:
1. Paste your UpPromote link for each brand into content/brands.json ("aff"). Until you do,
   the /go page sends visitors to the brand's normal site and you earn nothing.
2. Set EMAIL (and SITE_URL, e.g. https://yourorg.github.io) at the top of build.py, then run build.py.
   SITE_URL turns on canonical tags and sitemap.xml.
3. Keep unpublished drafts OUT of the repo: anything you push is public.
