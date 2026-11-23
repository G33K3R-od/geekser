"use strict";
const defaults=[{name:"GitHub",url:"https://github.com/"},{name:"Mozilla",url:"https://www.mozilla.org/"},{name:"Wikipedia",url:"https://www.wikipedia.org/"},{name:"YouTube",url:"https://www.youtube.com/"}];
const tilesNode=document.getElementById("tiles");
const settings=document.body.classList.contains("settings");
let dragIndex=null;
function validUrl(value){try{const u=new URL(value);return ["https:","http:"].includes(u.protocol)?u.href:null}catch{return null}}
function read(){try{const value=JSON.parse(localStorage.getItem("geekser-shortcuts"));return Array.isArray(value)?value.filter(v=>v&&typeof v.name==="string"&&v.name.trim()&&typeof v.url==="string"&&validUrl(v.url)).slice(0,48):defaults.slice()}catch{return defaults.slice()}}
let tiles=read();
function save(){try{localStorage.setItem("geekser-shortcuts",JSON.stringify(tiles))}catch(e){console.warn("Unable to persist shortcuts",e)}}
function move(from,to){if(from===to||from<0||to<0||from>=tiles.length||to>=tiles.length)return;const [item]=tiles.splice(from,1);tiles.splice(to,0,item);save();render()}
function siteColor(host){let hash=0;for(const c of host)hash=(hash*31+c.charCodeAt(0))>>>0;return ["#5b426e","#3b5573","#755141","#326264","#694263","#42614c"][hash%6]}
function faviconCandidates(url){
  const parsed=new URL(url);
  // Browser's normal image cache is used. No third-party favicon proxy.
  return [parsed.origin+"/favicon.ico"];
}
function render(){
  tilesNode.replaceChildren();
  document.getElementById("empty").hidden=tiles.length!==0;
  document.getElementById("count").textContent=String(tiles.length).padStart(2,"0")+" SAVED";
  tiles.forEach((tile,index)=>{
    const host=new URL(tile.url).hostname;
    const card=document.createElement("article");card.className="tile"+(settings?" is-editing":"");card.draggable=settings;
    const link=document.createElement("a");link.className="tile-link";link.href=tile.url;
    const icon=document.createElement("span");icon.className="site-icon";icon.style.setProperty("--icon-bg",siteColor(host));
    const fallback=document.createElement("span");fallback.className="site-initial";fallback.textContent=(tile.name[0]||"?").toUpperCase();icon.append(fallback);
    const favicon=document.createElement("img");favicon.className="favicon";favicon.alt="";favicon.width=26;favicon.height=26;favicon.referrerPolicy="no-referrer";
    favicon.addEventListener("load",()=>{fallback.hidden=true;favicon.classList.add("loaded")});
    favicon.addEventListener("error",()=>{favicon.remove();fallback.hidden=false});
    favicon.src=faviconCandidates(tile.url)[0];icon.append(favicon);
    const details=document.createElement("div");details.className="site-details";
    const name=document.createElement("strong");name.textContent=tile.name;
    const domain=document.createElement("small");domain.textContent=host;
    details.append(name,domain);link.append(icon,details);card.append(link);
    if(settings){
      const remove=document.createElement("button");remove.type="button";remove.className="remove-shortcut";remove.setAttribute("aria-label","Remove "+tile.name);remove.title="Remove shortcut";remove.textContent="×";remove.addEventListener("click",()=>{tiles.splice(index,1);save();render()});card.append(remove);
      card.addEventListener("dragstart",event=>{dragIndex=index;card.classList.add("dragging");event.dataTransfer.effectAllowed="move";event.dataTransfer.setData("text/plain",String(index))});
      card.addEventListener("dragover",event=>{event.preventDefault();event.dataTransfer.dropEffect="move";card.classList.add("drop-target")});
      card.addEventListener("dragleave",()=>card.classList.remove("drop-target"));
      card.addEventListener("drop",event=>{event.preventDefault();if(dragIndex!==null)move(dragIndex,index);dragIndex=null});
      card.addEventListener("dragend",()=>{dragIndex=null;render()});
      card.addEventListener("keydown",event=>{if(!event.altKey||!["ArrowLeft","ArrowRight"].includes(event.key))return;event.preventDefault();move(index,index+(event.key==="ArrowLeft"?-1:1))});
      card.tabIndex=0;card.setAttribute("aria-label","Reorder "+tile.name+" with Alt and arrow keys");
    }
    tilesNode.append(card);
  });
}
if(settings){
  document.getElementById("add").addEventListener("submit",event=>{
    event.preventDefault();
    const name=document.getElementById("name").value.trim();
    const url=validUrl(document.getElementById("url").value.trim());
    if(!name||!url||tiles.length>=48)return;
    tiles.push({name,url});save();event.target.reset();render();
  });
}
render();
