# Eklavya design system

Files: `app/static/css/eklavya.css` (all styles), `js/ui.js` (helpers), `vendor/lucide-icons.js` (131 Lucide icons, ISC), `vendor/alpine.min.js` (Alpine 3.17), `fonts/inter-*.woff2` (Inter variable, latin + latin-ext; Devanagari falls back to Noto/Nirmala/system). Living guide: `/static/design-system.html`.

## Rules
1. Use tokens (`var(--primary)`, `var(--surface)`...) never raw hex. Dark mode is automatic (`prefers-color-scheme`) and forceable with `data-theme="dark|light"` on `<html>` or any container (`setTheme()` in ui.js).
2. **AI vs human**: machine output = `.ai-suggestion` (dashed teal border, sparkle `.ai-tag`, `.cite` chips, `.conf` meter). Human decision = `.human-decision` (solid saffron, thick left rule, pen `.human-tag`, `.signature-line`). Never style an AI output as a decision. Show `.banner-cannot-certify` on assessor review.
3. One primary action per view (`btn-primary`); saffron `btn-accent` only for the single commitment (sign / start).
4. Color is never the only signal: pair chips/bars with an icon or text.
5. Icons: `icon("name")` only; add new ones by extending `vendor/lucide-icons.js` (inner SVG of the lucide-static icon).
6. Candidate app lives in `.stage > .phone > .phone-screen`; under 520px the frame dissolves to full-bleed. Assessor/admin use `.app-shell`.
7. Hindi text: add `.hi` (taller line-height). Use `.seg` for the EN/हिं toggle.

## Tokens (CSS vars)
Brand: `--teal-50..950`, `--saffron-50..700`. Semantic: `--bg --surface --surface-2 --surface-3 --border --border-strong --ink --ink-2 --ink-3`, `--primary(-hover/-press/-soft/-soft-2/-ink) --on-primary`, `--accent(-hover/-soft/-soft-2/-text/-ink)`, `--ok/--warn/--danger/--info` each with `-soft` and `-ink`, `--ai(-soft/-border/-ink)`, `--human(-soft/-border/-ink/-solid)`. Shape: `--r-xs 8 / sm 10 / md 14 / lg 18 / xl 24 / pill`, `--shadow-xs/sm/md/lg`, `--sp-1..12`, `--font --mono --ease --dur --focus`.

## Class cheat sheet
- **Type**: `display h1 h2 h3 h4 lead body small xs muted soft eyebrow mono num strong center truncate hi`
- **Layout**: `row col wrap grow between end start gap-1/2/4/5/6 stack grid grid-2/3/4/auto mt-1..8 mb-2/4 ml-auto w-full divider sr-only`
- **Icons**: `icon icon-xs/sm/lg/xl`, `icon-tile [accent|ok|warn|danger|lg]`
- **Buttons**: `btn` + `btn-primary|accent|soft|ghost|danger`, `btn-sm|lg|block|icon`, `is-loading`, `btn-group`, `mic-btn[.is-listening]`, `waveform>i`, `seg>button[aria-pressed]`
- **Forms**: `field label hint input select textarea input-wrap(>icon+input) is-invalid otp check radio switch option(.key .is-selected .is-correct .is-wrong)`
- **Cards**: `card card-flat card-sunken card-pad-0|sm card-interactive card-hero card-head card-foot stat(.stat-label .stat-value .stat-delta.up|down) empty list list-item kv nos-row`
- **Chips**: `chip` + `chip-primary|accent|ok|warn|danger|info|outline|sm|sel|suggest`, `badge`, `dot[.ok .warn .danger .live]`, `sync sync-saved|waiting|synced`, `crit`
- **AI/human**: `ai-suggestion ai-tag ai-rationale cite human-decision human-tag signature-line banner-cannot-certify`
- **Banners**: `banner` + `banner-ok|warn|danger|ink`, `offline-banner[.is-online]`
- **Progress**: `ring[.accent|.ok .ring-sm|.ring-lg](--pct)`, `progress[.accent|.ok]>i(--w)`, `conf[data-level=1-5]`, `conf-track[.low|.high]>i`, `score(.score-name .score-track>i[.ok|.warn|.danger] .pass-mark .score-val)`, `chart>.bar>i[.ai|.accent](--h)` + `chart-labels`, `legend`, `hist`
- **Tabs/Tables**: `tabs>.tab[aria-selected|.is-active]`, `table-wrap>table.table` (`.num`, `.is-clickable`, `table-compact`)
- **Shells**: console `app-shell > aside.sidebar(.brand .brand-mark .nav-section .nav-link.is-active .sidebar-foot) + .main(.topbar .page .page-head .crumbs)`, `menu-toggle`, sidebar `.is-open` on mobile. Phone `stage > .phone > .phone-screen(.statusbar .phone-header .offline-banner .phone-body .bottom-nav(a.is-active|.is-done) .home-bar)`
- **Overlays**: `toasts>.toast.toast-ok|warn|danger|info`, `modal-backdrop>.modal(.modal-head .modal-actions)`, `.sheet-backdrop>.sheet`
- **Flow**: `stepper>.step(.is-active|.is-done)(.step-dot)+.step-line`, `timeline>.tl-item[.ok|.warn|.ai|.human](.tl-time .tl-title)`, `hash`, `chain-link`
- **Loading**: `skeleton[.line|.title|.circle|.block]`, `spinner`, `typing>i*3`
- **Evidence/credential**: `evidence-grid>.evidence-tile(.ph .kind .tags>.chip.ai .flag)`, `evidence-add`, `dropzone[.is-over]`, `qr`, `qr-caption`, `credential(.seal)`, `verify-row.ok|bad`, `avatar[.sm|.lg|.xl|.accent]`, `avatar-stack`
- **Motion**: `fade-in`, `rise-in` (staggered children)

## ui.js API (ES module)
`icon(name,{size:"xs|sm|lg|xl"|px, cls, label})` -> SVG string · `el("div.card#id",{class,html,text,onclick,dataset,style},...kids)` · `html(str)` -> node · `toast(title,{type,msg,ms})` · `modal({title,body,actions:[{label,cls,value,icon,keepOpen,onClick}],icon,size,dismissable})` -> Promise · `sheet(...)` · `confirmDialog(title,msg,{confirm,cancel,danger})` · `ring(pct,{label,sub,tone,size})` · `conf(0..1)` · `scoreBar(name,pct,{passMark,tone,value})` · `syncChip(state)` · `aiTag() humanTag() chip() avatar() initials() esc()` · `setTheme("auto|light|dark") initTheme()` · `fmt.{pct,date,time,short}`. Toasts/modals render inside `.phone-screen` when present.

Font note: Inter is self-hosted (`@font-face` in eklavya.css). Include Alpine with `<script defer src="/static/vendor/alpine.min.js">`; use `x-cloak` to avoid flashes.
