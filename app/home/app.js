"use strict";
const defaults=[{name:"GitHub",url:"https://github.com/"},{name:"Mozilla",url:"https://www.mozilla.org/"},{name:"Wikipedia",url:"https://www.wikipedia.org/"},{name:"YouTube",url:"https://www.youtube.com/"}];
const tilesNode=document.getElementById("tiles");
const editor=document.getElementById("editor");
const editButton=document.getElementById("edit");
let editing=false;
let dragIndex=null;
function validUrl(value){try{const u=new URL(value);return ["https:","http:"].includes(u.protocol)?u.href:null}catch{return null}}
function read(){try{const value=JSON.parse(localStorage.getItem("geekser-shortcuts"));return Array.isArray(value)?value.filter(v=>v&&typeof v.name==="string"&&v.name.trim()&&typeof v.url==="string"&&validUrl(v.url)).slice(0,48):defaults.slice()}catch{return defaults.slice()}}
let tiles=read();
function save(){try{localStorage.setItem("geekser-shortcuts",JSON.stringify(tiles))}catch(e){console.warn("Unable to persist shortcuts",e)}}
function move(from,to){if(from===to||from<0||to<0||from>=tiles.length||to>=tiles.length)return;const [item]=tiles.splice(from,1);tiles.splice(to,0,item);save();render()}
function siteColor(host){let hash=0;for(const c of host)hash=(hash*31+c.charCodeAt(0))>>>0;return ["#59416d","#414c76","#675044","#385c60","#60415c","#435d4b"][hash%6]}
function render(){
  tilesNode.replaceChildren();
  document.getElementById("empty").hidden=tiles.length!==0;
  tiles.forEach((tile,index)=>{
    const host=new URL(tile.url).hostname;
    const card=document.createElement("article");card.className="tile"+(editing?" is-editing":"");card.draggable=editing;
    const link=document.createElement("a");link.className="tile-link";link.href=tile.url;
    const icon=document.createElement("span");icon.className="site-icon";icon.textContent=(tile.name[0]||"?").toUpperCase();icon.style.setProperty("--icon-bg",siteColor(host));
    const details=document.createElement("div");details.className="site-details";
    const name=document.createElement("strong");name.textContent=tile.name;
    const domain=document.createElement("small");domain.textContent=host;
    details.append(name,domain);link.append(icon,details);card.append(link);
    if(editing){
      const controls=document.createElement("div");controls.className="tile-controls";
      for(const [label,delta] of [["Move left",-1],["Move right",1]]){
        const button=document.createElement("button");button.type="button";button.textContent=delta<0?"←":"→";button.setAttribute("aria-label",label+": "+tile.name);button.disabled=index+delta<0||index+delta>=tiles.length;button.addEventListener("click",()=>move(index,index+delta));controls.append(button);
      }
      const remove=document.createElement("button");remove.type="button";remove.textContent="×";remove.setAttribute("aria-label","Remove "+tile.name);remove.addEventListener("click",()=>{tiles.splice(index,1);save();render()});controls.append(remove);card.append(controls);
      card.addEventListener("dragstart",event=>{dragIndex=index;card.classList.add("dragging");event.dataTransfer.effectAllowed="move";event.dataTransfer.setData("text/plain",String(index))});
      card.addEventListener("dragover",event=>{event.preventDefault();event.dataTransfer.dropEffect="move";card.classList.add("drop-target")});
      card.addEventListener("dragleave",()=>card.classList.remove("drop-target"));
      card.addEventListener("drop",event=>{event.preventDefault();if(dragIndex!==null)move(dragIndex,index);dragIndex=null});
      card.addEventListener("dragend",()=>{dragIndex=null;render()});
    }
    tilesNode.append(card);
  });
}
editButton.addEventListener("click",()=>{editing=!editing;editor.hidden=!editing;document.getElementById("drag-hint").hidden=!editing;editButton.textContent=editing?"Done":"Customize";editButton.setAttribute("aria-expanded",String(editing));render()});
document.getElementById("add").addEventListener("submit",event=>{event.preventDefault();const name=document.getElementById("name").value.trim();const url=validUrl(document.getElementById("url").value.trim());if(!name||!url||tiles.length>=48)return;tiles.push({name,url});save();event.target.reset();render()});
function searchURL(query){if(/^https?:\/\//i.test(query))return validUrl(query);if(/^[a-z][a-z\d+.-]*:/i.test(query))return null;const host=/^(localhost|[^\s/]+\.[^\s/]+)(:\d+)?(\/.*)?$/i.test(query);return host?validUrl("https://"+query):"https://www.google.com/search?q="+encodeURIComponent(query)}
document.getElementById("search").addEventListener("submit",event=>{event.preventDefault();const q=document.getElementById("query").value.trim();if(!q)return;const url=searchURL(q);if(url)location.assign(url)});
function updateClock(){document.getElementById("clock").textContent=new Intl.DateTimeFormat(undefined,{hour:"2-digit",minute:"2-digit"}).format(new Date())}
updateClock();setInterval(updateClock,30000);
render();
