const state={cat:'all'};
const catMap=Object.fromEntries(CATS.map(c=>[c.id,c]));
function brandName(id){return (BRANDS[id]&&BRANDS[id].name)||id}
function goHref(d){return 'go.html?b='+encodeURIComponent(d.brand)}
function fmt(d){return new Date(d+'T00:00:00').toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})}
function grad(c){return 'linear-gradient(135deg,'+c.color+','+c.color+'99)'}
function dealCard(d){const c=catMap[d.cat]||{name:'',color:'#777'};
return `<article class="card">${d.sample?'<span class="tag">Sample</span>':''}
<div class="thumb" style="background:${grad(c)}"><em>${c.name}</em></div>
<div class="body"><h3>${brandName(d.brand)}</h3><p>${d.offer}</p>${d.checked?`<span class="meta">Checked ${fmt(d.checked)}</span>`:''}
<div class="code">${d.code?`<code>${d.code}</code><a href="${goHref(d)}" target="_blank" rel="sponsored noopener" onclick="try{navigator.clipboard.writeText('${d.code}')}catch(e){}">Copy &amp; shop</a>`:`<a style="flex:1;text-align:center" href="${goHref(d)}" target="_blank" rel="sponsored noopener">Shop ${brandName(d.brand)}</a>`}</div></div></article>`}
function visibleDeals(){return DEALS.filter(d=>SHOW_SAMPLES||!d.sample)}
function renderDeals(el,limit){const list=visibleDeals().filter(d=>state.cat==='all'||d.cat===state.cat).slice(0,limit||999);
el.innerHTML=list.length?list.map(dealCard).join(''):'<div class="empty">New deals are added here soon.</div>'}
function postsList(){return POSTS.filter(p=>SHOW_SAMPLES||!p.sample).sort((a,b)=>b.date.localeCompare(a.date))}
function renderPosts(el,limit,withFeature){const list=postsList().slice(0,limit||999);if(!list.length){el.innerHTML='<div class="empty">New posts are on the way.</div>';return}
let html='';let rest=list;
if(withFeature){const p=list[0],c=catMap[p.cat];rest=list.slice(1);
html+=`<a class="feat" href="${p.href}"><div class="thumb" style="background:${grad(c)}"><em>${c.name}</em></div><div class="body"><span class="meta">${fmt(p.date)} · ${p.read}</span><h2>${p.title}</h2><p>${p.excerpt}</p><span style="color:var(--acc);font-weight:600">Read the guide →</span></div></a>`}
html+='<div class="grid">'+rest.map(p=>{const c=catMap[p.cat];return `<a class="card" style="text-decoration:none" href="${p.href}"><div class="thumb" style="height:140px;background:${grad(c)}"><em>${c.name}</em></div><div class="body"><span class="meta">${fmt(p.date)} · ${p.read}</span><h3>${p.title}</h3><p>${p.excerpt}</p></div></a>`}).join('')+'</div>';
el.innerHTML=html}
function initFilters(el,target){el.innerHTML='<button class="on" data-c="all">All</button>'+CATS.map(c=>`<button data-c="${c.id}">${c.name}</button>`).join('');
el.onclick=e=>{const b=e.target.closest('button');if(!b)return;state.cat=b.dataset.c;[...el.children].forEach(x=>x.classList.toggle('on',x===b));renderDeals(target)}}
