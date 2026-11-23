"use strict";

const defaults = [
  { name: "GitHub", url: "https://github.com/" },
  { name: "Mozilla", url: "https://www.mozilla.org/" },
  { name: "Wikipedia", url: "https://www.wikipedia.org/" },
  { name: "YouTube", url: "https://www.youtube.com/" }
];
const tilesEl = document.getElementById("tiles");
const editor = document.getElementById("editor");
let tiles = [];
let editing = false;

function validWebUrl(value) {
  try {
    const parsed = new URL(value);
    return ["https:", "http:"].includes(parsed.protocol) ? parsed.href : null;
  } catch { return null; }
}

function hostname(value) {
  try { return new URL(value).hostname; } catch { return ""; }
}

async function persist() {
  await browser.storage.local.set({ shortcuts: tiles });
}

function render() {
  tilesEl.replaceChildren();
  for (const [index, item] of tiles.entries()) {
    const url = validWebUrl(item.url);
    if (!url || typeof item.name !== "string") continue;
    const card = document.createElement("article");
    card.className = "tile";
    const link = document.createElement("a");
    link.href = url;
    const avatar = document.createElement("span");
    avatar.className = "avatar";
    avatar.textContent = (item.name.trim().charAt(0) || "?").toUpperCase();
    const details = document.createElement("div");
    const title = document.createElement("strong");
    title.textContent = item.name;
    const domain = document.createElement("small");
    domain.textContent = hostname(url);
    details.append(title, domain);
    link.append(avatar, details);
    card.append(link);
    if (editing) {
      const remove = document.createElement("button");
      remove.className = "remove";
      remove.type = "button";
      remove.textContent = "×";
      remove.setAttribute("aria-label", "Remove " + item.name);
      remove.addEventListener("click", async () => {
        tiles.splice(index, 1);
        await persist();
        render();
      });
      card.append(remove);
    }
    tilesEl.append(card);
  }
}

document.getElementById("today").textContent = new Intl.DateTimeFormat(undefined, {
  weekday: "long", month: "short", day: "numeric"
}).format(new Date());

document.getElementById("settings").addEventListener("click", () => {
  editing = !editing;
  editor.hidden = !editing;
  document.getElementById("settings").textContent = editing ? "Done" : "Customize";
  render();
});

document.getElementById("add-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const name = document.getElementById("tile-name").value.trim();
  const url = validWebUrl(document.getElementById("tile-url").value.trim());
  if (!name || !url) return;
  tiles.push({ name, url });
  await persist();
  event.target.reset();
  render();
});

document.getElementById("search-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const query = document.getElementById("query").value.trim();
  if (!query) return;
  const direct = validWebUrl(query) || validWebUrl("https://" + query);
  const looksLikeHost = /^(localhost|[^\s/]+\.[^\s/]+)(:\d+)?(\/.*)?$/i.test(query);
  window.location.assign(looksLikeHost && direct
    ? direct
    : "https://www.google.com/search?q=" + encodeURIComponent(query));
});

(async () => {
  try {
    const result = await browser.storage.local.get("shortcuts");
    tiles = Array.isArray(result.shortcuts) ? result.shortcuts.filter(
      item => item && typeof item.name === "string" && validWebUrl(item.url)
    ) : defaults.slice();
  } catch (error) {
    console.error("Geekser storage unavailable:", error);
    tiles = defaults.slice();
  }
  render();
  document.getElementById("query").focus();
})();
