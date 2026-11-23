"use strict";
const defaults=[{name:"GitHub",url:"https://github.com/"},{name:"Mozilla",url:"https://www.mozilla.org/"},{name:"Wikipedia",url:"https://www.wikipedia.org/"},{name:"YouTube",url:"https://www.youtube.com/"}];
const tilesNode=document.getElementById("tiles");
const editor=document.getElementById("editor");
let editing=false;
function validUrl(value){try{const u=new URL(value);return u.protocol==="https:"||u.protocol==="http:"?u.href:null}catch{return null}}
function read(){try{const value=JSON.parse(localStorage.getItem("geekser-shortcuts"));return Array.isArray(value)?value.filter(v=>v&&typeof v.name==="string"&&validUrl(v.url)):defaults.slice()}catch{return defaults.slice()}}
let tiles=read();
function save(){try{localStorage.setItem("geekser-shortcuts",JSON.stringify(tiles))}catch(e){console.warn("Unable to persist shortcuts",e)}}
function render(){
  tilesNode.replaceChildren();
  tiles.forEach((tile,index)=>{
    const card=document.createElement("div");card.className="tile";
    const link=document.createElement("a");link.href=tile.url;
    const initial=document.createElement("span");initial.className="initial";initial.textContent=(tile.name[0]||"?").toUpperCase();
    const details=document.createElement("div"),name=document.createElement("strong"),domain=document.createElement("small");
    name.textContent=tile.name;domain.textContent=new URL(tile.url).hostname;details.append(name,domain);link.append(initial,details);card.append(link);
    if(editing){const remove=document.createElement("button");remove.className="remove";remove.textContent="×";remove.setAttribute("aria-label","Remove "+tile.name);remove.addEventListener("click",()=>{tiles.splice(index,1);save();render()});card.append(remove)}
    tilesNode.append(card);
  });
}
document.getElementById("edit").addEventListener("click",()=>{editing=!editing;editor.hidden=!editing;document.getElementById("edit").textContent=editing?"Done":"Edit shortcuts";render()});
document.getElementById("add").addEventListener("submit",event=>{event.preventDefault();const name=document.getElementById("name").value.trim();const url=validUrl(document.getElementById("url").value.trim());if(!name||!url)return;tiles.push({name,url});save();event.target.reset();render()});
document.getElementById("search").addEventListener("submit",event=>{event.preventDefault();const q=document.getElementById("query").value.trim();if(!q)return;const host=/^(localhost|[^\s/]+\.[^\s/]+)(:\d+)?(\/.*)?$/i.test(q);const url=host?validUrl("https://"+q):null;location.assign(url||"https://www.google.com/search?q="+encodeURIComponent(q))});
render();
