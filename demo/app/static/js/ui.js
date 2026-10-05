// Eklavya UI helpers (ES module, no deps): icon(), el(), toast(), modal(), sheet(), ring(), conf(), etc.
import { ICONS } from "../vendor/lucide-icons.js";

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
export { esc };

/** icon("mic", {size:"sm"|"xs"|"lg"|"xl"|number, cls:"extra", label:"aria text", stroke:2}) -> inline SVG string */
export function icon(name, opts = {}) {
  const inner = ICONS[name];
  if (!inner) { console.warn("[ui] unknown icon:", name); return ""; }
  const { size, cls = "", label, stroke } = opts;
  const sz = typeof size === "number" ? ` style="width:${size}px;height:${size}px"` : "";
  const sc = ["sm", "xs", "lg", "xl"].includes(size) ? ` icon-${size}` : "";
  const aria = label ? `role="img" aria-label="${esc(label)}"` : `aria-hidden="true"`;
  const sw = stroke ? ` stroke-width="${stroke}"` : "";
  return `<svg class="icon${sc} ${cls}"${sz}${sw} viewBox="0 0 24 24" ${aria}>${inner}</svg>`;
}
export const hasIcon = (n) => n in ICONS;

/** el("div.card#id", {class, onclick, dataset:{}, html, style:{}}, ...children) -> HTMLElement */
export function el(tag, attrs = {}, ...kids) {
  const m = /^([a-z0-9-]*)((?:[.#][\w-]+)*)$/i.exec(tag) || [];
  const node = document.createElement(m[1] || "div");
  (m[2] || "").replace(/([.#])([\w-]+)/g, (_, k, v) => (k === "." ? node.classList.add(v) : (node.id = v)));
  if (attrs && (typeof attrs !== "object" || attrs instanceof Node || Array.isArray(attrs) || typeof attrs === "string")) { kids.unshift(attrs); attrs = {}; }
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v == null || v === false) continue;
    if (k === "class") node.className += (node.className ? " " : "") + v;
    else if (k === "html") node.innerHTML = v;
    else if (k === "text") node.textContent = v;
    else if (k === "style" && typeof v === "object") Object.assign(node.style, v);
    else if (k === "dataset") Object.assign(node.dataset, v);
    else if (k.startsWith("on") && typeof v === "function") node.addEventListener(k.slice(2).toLowerCase(), v);
    else node.setAttribute(k, v === true ? "" : v);
  }
  const add = (c) => {
    if (c == null || c === false) return;
    if (Array.isArray(c)) return c.forEach(add);
    node.append(c instanceof Node ? c : document.createTextNode(String(c)));
  };
  kids.forEach(add);
  return node;
}
/** Build DOM from an HTML string (single root or fragment). */
export function html(str) { const t = document.createElement("template"); t.innerHTML = str.trim(); return t.content.childElementCount === 1 ? t.content.firstElementChild : t.content; }

/* ---------- Toasts ---------- */
const TOAST_ICON = { ok: "circle-check", warn: "triangle-alert", danger: "circle-x", info: "info" };
function toastHost() {
  // inside the phone screen when present so toasts live in the device
  const host = document.querySelector(".phone-screen") || document.body;
  let t = host.querySelector(":scope > .toasts");
  if (!t) { t = el("div.toasts", { "aria-live": "polite" }); host.append(t); }
  return t;
}
/** toast("Saved", {type:"ok"|"warn"|"danger"|"info", msg:"detail", ms:3200}) */
export function toast(title, opts = {}) {
  const { type = "info", msg, ms = 3200 } = typeof opts === "string" ? { msg: opts } : opts;
  const node = el(`div.toast.toast-${type}`, { role: "status" },
    html(icon(TOAST_ICON[type] || "info")),
    el("div.grow", {}, el("div.toast-title", { text: title }), msg ? el("div.toast-msg", { text: msg }) : null));
  toastHost().prepend(node);
  const close = () => { node.classList.add("is-leaving"); setTimeout(() => node.remove(), 220); };
  if (ms) setTimeout(close, ms);
  node.addEventListener("click", close);
  return close;
}

/* ---------- Modal / sheet ---------- */
/**
 * modal({title, body: string|Node, actions:[{label, cls:"btn-primary", value, keepOpen, onClick}], sheet:false, dismissable:true})
 * -> Promise resolving to the clicked action's value (or undefined on dismiss). Result promise has .close().
 */
export function modal({ title, body, actions, sheet: asSheet = false, dismissable = true, icon: ic, size } = {}) {
  let resolve;
  const p = new Promise((r) => (resolve = r));
  const host = document.querySelector(".phone-screen") || document.body;
  const prevFocus = document.activeElement;
  const close = (v) => {
    document.removeEventListener("keydown", onKey);
    back.style.opacity = 0; setTimeout(() => back.remove(), 150);
    prevFocus?.focus?.(); resolve(v);
  };
  const onKey = (e) => { if (e.key === "Escape" && dismissable) close(undefined); };
  const bodyNode = typeof body === "string" ? html(`<div class="soft">${body}</div>`) : body;
  const acts = (actions ?? [{ label: "OK", cls: "btn-primary", value: true }]).map((a) =>
    el(`button.btn.${(a.cls || "btn-ghost").split(" ").join(".")}`, {
      type: "button",
      onclick: async () => { if (a.onClick) await a.onClick(close); if (!a.keepOpen) close(a.value); },
    }, a.icon ? html(icon(a.icon, { size: "sm" })) : null, a.label));
  const box = el(asSheet ? "div.sheet" : "div.modal", { role: "dialog", "aria-modal": "true", style: size ? { width: size } : null },
    title ? el("div.modal-head", {}, el("div.row", {}, ic ? el("span.icon-tile", { html: icon(ic) }) : null, el("h2.h2", { text: title })),
      dismissable ? el("button.btn.btn-ghost.btn-icon.btn-sm", { "aria-label": "Close", onclick: () => close(undefined), html: icon("x") }) : null) : null,
    bodyNode, acts.length ? el("div.modal-actions", {}, acts) : null);
  const back = el(`div.modal-backdrop${asSheet ? ".sheet-backdrop" : ""}`, { onclick: (e) => { if (e.target === back && dismissable) close(undefined); } }, box);
  host.append(back);
  document.addEventListener("keydown", onKey);
  (box.querySelector("[autofocus],input,textarea,.btn-primary,.btn") || box).focus?.();
  p.close = close; p.el = box;
  return p;
}
export const sheet = (o) => modal({ ...o, sheet: true });
export async function confirmDialog(title, message, { confirm = "Confirm", cancel = "Cancel", danger = false } = {}) {
  return !!(await modal({ title, body: message, actions: [{ label: cancel, cls: "btn-ghost", value: false }, { label: confirm, cls: danger ? "btn-danger" : "btn-primary", value: true }] }));
}

/* ---------- Small component factories (return HTML strings) ---------- */
export const initials = (name = "") => name.split(/\s+/).filter(Boolean).slice(0, 2).map((s) => s[0]).join("").toUpperCase() || "?";
export const avatar = (name, { size = "", accent = false } = {}) => `<span class="avatar ${size} ${accent ? "accent" : ""}" title="${esc(name)}">${esc(initials(name))}</span>`;
export const chip = (label, { tone = "", icon: ic, sm = false } = {}) => `<span class="chip ${tone ? "chip-" + tone : ""} ${sm ? "chip-sm" : ""}">${ic ? icon(ic) : ""}${esc(label)}</span>`;

/** ring(72, {label:"72%", sub:"progress", tone:"accent|ok", size:"sm|lg"}) -> HTML */
export function ring(pct, { label, sub, tone = "", size = "" } = {}) {
  const p = Math.max(0, Math.min(100, pct));
  return `<div class="ring ${tone} ${size ? "ring-" + size : ""}" style="--pct:${p}" role="progressbar" aria-valuenow="${Math.round(p)}" aria-valuemin="0" aria-valuemax="100">
    <svg viewBox="0 0 40 40"><circle class="ring-track" cx="20" cy="20" r="15.915" pathLength="100"/><circle class="ring-bar" cx="20" cy="20" r="15.915" pathLength="100"/></svg>
    <div class="ring-label"><span>${esc(label ?? Math.round(p) + "%")}${sub ? `<small>${esc(sub)}</small>` : ""}</span></div></div>`;
}
/** conf(0.82) -> 5-bar confidence meter with % */
export function conf(v, { showPct = true } = {}) {
  const level = Math.max(1, Math.min(5, Math.ceil(v * 5)));
  return `<span class="conf" data-level="${level}" title="AI confidence ${Math.round(v * 100)}%"><span class="conf-bars"><i></i><i></i><i></i><i></i><i></i></span>${showPct ? Math.round(v * 100) + "%" : ""}</span>`;
}
/** scoreBar("Safety", 78, {passMark:60}) -> HTML (tone auto from score vs pass mark) */
export function scoreBar(name, pct, { passMark, tone, value } = {}) {
  const t = tone ?? (passMark != null ? (pct >= passMark ? "ok" : pct >= passMark - 15 ? "warn" : "danger") : "");
  return `<div class="score"><span class="score-name" title="${esc(name)}">${esc(name)}</span><div class="score-track"><i class="${t}" style="--w:${pct}%"></i>${passMark != null ? `<b class="pass-mark" style="--at:${passMark}%"></b>` : ""}</div><span class="score-val">${esc(value ?? Math.round(pct))}</span></div>`;
}
/** syncChip("saved"|"waiting"|"synced") */
export function syncChip(state) {
  const m = { saved: ["Saved", "hard-drive"], waiting: ["Waiting", "refresh-cw"], synced: ["Synced", "check"] }[state] || ["", "check"];
  return `<span class="sync sync-${state}">${icon(m[1] === "hard-drive" ? "database" : m[1], { size: "xs" })}${m[0]}</span>`;
}
export const aiTag = (t = "AI suggestion") => `<span class="ai-tag">${icon("sparkles", { size: "xs" })}${esc(t)}</span>`;
export const humanTag = (t = "Assessor decision") => `<span class="human-tag">${icon("pen-line", { size: "xs" })}${esc(t)}</span>`;

/* ---------- Theme ---------- */
export function setTheme(t) { // "light" | "dark" | "auto"
  try { t === "auto" ? (document.documentElement.removeAttribute("data-theme"), localStorage.removeItem("ek-theme")) : (document.documentElement.dataset.theme = t, localStorage.setItem("ek-theme", t)); } catch { }
}
export function initTheme() { try { const t = localStorage.getItem("ek-theme"); if (t) document.documentElement.dataset.theme = t; } catch { } }

export const fmt = {
  pct: (v) => Math.round(v * 100) + "%",
  date: (d) => new Date(d).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" }),
  time: (d) => new Date(d).toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" }),
  short: (h, n = 8) => (h ? h.slice(0, n) + "…" + h.slice(-4) : ""),
};
