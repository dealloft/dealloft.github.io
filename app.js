
const state={cat:'all'};
const catMap=Object.fromEntries(CATS.map(c=>[c.id,c]));
function dealCard(d){const c=catMap[d.cat]||{name:'',color:'#777'};
return `<article class="card">${d.sample?'<span class="tag">Sample</span>':''}
<div class="thumb" style="background:linear-gradient(135deg,${c.color},${c.color}aa)"><em>${c.name}</em></div>
<div class="body"><h3>${d.brand}</h3><p>${d.offer}</p>
<div class="code">${d.code?`<code>${d.code}</code><button onclick="navigator.clipboard&&navigator.clipboard.writeText('${d.code}');this.textContent='Copied';window.open('${d.url}','_blank','noopener')">Copy &amp; shop</button>`:`<a style="flex:1;text-align:center" href="${d.url}" target="_blank" rel="sponsored noopener">Get deal</a>`}</div></div></article>`}
function visibleDeals(){return DEALS.filter(d=>SHOW_SAMPLES||!d.sample)}
function renderDeals(el,limit){const list=visibleDeals().filter(d=>state.cat==='all'||d.cat===state.cat).slice(0,limit||999);
el.innerHTML=list.length?list.map(dealCard).join(''):'<div class="empty">New deals are added here soon.</div>'}
function renderGuides(el,limit){const list=GUIDES.filter(g=>SHOW_SAMPLES||!g.sample).slice(0,limit||999);
el.innerHTML=list.length?list.map(g=>{const c=catMap[g.cat];return `<a class="card" style="text-decoration:none" href="${g.href}"><div class="thumb" style="height:150px;background:linear-gradient(135deg,${c.color},${c.color}88)"><em>${c.name}</em></div><div class="body"><h3>${g.title}</h3><p>${g.summary}</p></div></a>`}).join(''):'<div class="empty">New guides are on the way.</div>'}

function postsList(){return POSTS.filter(p=>SHOW_SAMPLES||!p.sample).sort((a,b)=>b.date.localeCompare(a.date))}
function fmt(d){return new Date(d+'T00:00:00').toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})}
function postHref(p){return 'post.html?p='+encodeURIComponent(p.slug)}
function grad(c){return 'linear-gradient(135deg,'+c.color+','+c.color+'99)'}
function renderPosts(el,limit,withFeature){const list=postsList().slice(0,limit||999);if(!list.length){el.innerHTML='<div class="empty">New posts are on the way.</div>';return}
let html='';let rest=list;
if(withFeature){const p=list[0],c=catMap[p.cat];rest=list.slice(1);
html+=`<a class="feat" href="${postHref(p)}"><div class="thumb" style="background:${grad(c)}"><em>${c.name}</em></div><div class="body"><span class="meta">${fmt(p.date)} · ${p.read||'5 min read'}</span><h2>${p.title}</h2><p>${p.excerpt}</p><span style="color:var(--acc);font-weight:600">Read the post →</span></div></a>`}
html+='<div class="grid">'+rest.map(p=>{const c=catMap[p.cat];return `<a class="card" style="text-decoration:none" href="${postHref(p)}"><div class="thumb" style="height:140px;background:${grad(c)}"><em>${c.name}</em></div><div class="body"><span class="meta">${fmt(p.date)} · ${p.read||'5 min read'}</span><h3>${p.title}</h3><p>${p.excerpt}</p></div></a>`}).join('')+'</div>';
el.innerHTML=html}
function md(t){const esc=x=>x.replace(/&/g,'&amp;').replace(/</g,'&lt;');
const inl=x=>esc(x).replace(/\*\*(.+?)\*\*/g,'<b>$1</b>').replace(/\[(.+?)\]\((.+?)\)/g,(m,a,u)=>`<a href="${u}" ${/^https?:/.test(u)?'target="_blank" rel="sponsored noopener"':''}>${a}</a>`);
return t.trim().split(/\n\s*\n/).map(b=>{b=b.trim();if(b.startsWith('## '))return '<h2>'+inl(b.slice(3))+'</h2>';
if(/^- /.test(b))return '<ul>'+b.split('\n').map(l=>'<li>'+inl(l.replace(/^- /,''))+'</li>').join('')+'</ul>';return '<p>'+inl(b).replace(/\n/g,'<br>')+'</p>'}).join('')}
function renderPost(el){const slug=new URLSearchParams(location.search).get('p');const p=POSTS.find(x=>x.slug===slug);
if(!p){el.innerHTML='<h1>Post not found</h1><p><a href="blog.html">Back to the blog</a></p>';return}
const c=catMap[p.cat];document.title=p.title+' — '+SITE_NAME;
el.innerHTML=`<span class="eyebrow">${c.name}</span><h1>${p.title}</h1><div class="meta">${fmt(p.date)} · ${p.read||'5 min read'} · By ${p.author||'the editorial team'}</div><div class="hd" style="background:${grad(c)}"></div>
<div class="notice">This post may contain affiliate links. If you buy through them we may earn a commission at no extra cost to you. <a href="disclosure.html">Details</a></div>${md(p.body)}`}
function initFilters(el,target){el.innerHTML='<button class="on" data-c="all">All</button>'+CATS.map(c=>`<button data-c="${c.id}">${c.name}</button>`).join('');
el.onclick=e=>{const b=e.target.closest('button');if(!b)return;state.cat=b.dataset.c;[...el.children].forEach(x=>x.classList.toggle('on',x===b));renderDeals(target)}}
