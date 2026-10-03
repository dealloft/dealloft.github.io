
const SHOW_SAMPLES = true;   // set to false before you publish, after adding real deals below
const CATS = [{"id": "fashion", "name": "Fashion & Beauty", "color": "#C4552D"}, {"id": "home", "name": "Home & Living", "color": "#2F4A3A"}, {"id": "wellness", "name": "Health & Wellness", "color": "#8A5A44"}, {"id": "tech", "name": "Tech & Gadgets", "color": "#3C4F76"}, {"id": "family", "name": "Baby & Family", "color": "#B9852E"}, {"id": "fitness", "name": "Fitness & Outdoors", "color": "#5B6B3A"}];
// ===== DEALS =====  Add REAL deals only: brand, offer text from the brand's program, code (or ''), your affiliate link.
const DEALS = [
  {sample:true, cat:'wellness', brand:'Brand name', offer:'Describe the real offer here', code:'YOURCODE', url:'#'},
  {sample:true, cat:'fashion',  brand:'Brand name', offer:'Describe the real offer here', code:'',         url:'#'},
  {sample:true, cat:'home',     brand:'Brand name', offer:'Describe the real offer here', code:'YOURCODE', url:'#'},
  {sample:true, cat:'tech',     brand:'Brand name', offer:'Describe the real offer here', code:'',         url:'#'},
  {sample:true, cat:'fitness',  brand:'Brand name', offer:'Describe the real offer here', code:'YOURCODE', url:'#'},
  {sample:true, cat:'family',   brand:'Brand name', offer:'Describe the real offer here', code:'',         url:'#'},
];
const SITE_NAME = "Dealloft";
// ===== BLOG POSTS =====  Add a new post by copying one block. Newest date shows first.
// body: blank line = new paragraph, "## " = heading, "- " = bullet list, [text](https://link) = link
const POSTS = [
  {sample:true, slug:'sample-post-one', cat:'wellness', date:'2026-10-01', read:'5 min read', title:'Your first blog post title', excerpt:'One or two sentences that make someone want to read this post.',
   body:`Write your intro here. Say what problem the reader has and what the post will help them decide.

## What to look for

Write only what you can support. Say when you have not tried a product yourself.

- First point
- Second point

## Our picks

For each pick: what it is, who it suits, the price range and your affiliate link, like [this link](https://example.com).`},
  {sample:true, slug:'sample-post-two', cat:'home', date:'2026-09-28', read:'4 min read', title:'Your second blog post title', excerpt:'A short summary of what the post covers.', body:`Replace this with your post.`},
  {sample:true, slug:'sample-post-three', cat:'tech', date:'2026-09-25', read:'6 min read', title:'Your third blog post title', excerpt:'A short summary of what the post covers.', body:`Replace this with your post.`},
  {sample:true, slug:'sample-post-four', cat:'fashion', date:'2026-09-20', read:'3 min read', title:'Your fourth blog post title', excerpt:'A short summary of what the post covers.', body:`Replace this with your post.`},
];
