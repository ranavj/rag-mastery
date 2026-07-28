# Day 23 — React frontend ⚛️ (Phase 5 🟠, learner ka ghar 🏠)

> Build-day. Backend Day 20-22 me ready ho gaya — aaj sirf UI. React tumhare liye naya nahi,
> isliye focus = INTEGRATION (contract ka payoff + tool_used differentiator ko visible banana).

## Scaffold (Vite + React + TS)
`npm create vite` ki jagah hand-scaffold: `package.json` (react 18 + vite 5 + ts), `vite.config.ts`
(port 5173 — backend CORS me yahi origin), `tsconfig*.json`, `index.html`, `src/main.tsx`, `vite-env.d.ts`.
Run: `npm install` → `npm run dev`.
- 🐛 npm ne esbuild postinstall block kiya (security warning) — par binary aa gaya, vite chala. Warning ignore.

## 🔑 Contract ka PAYOFF (Day 19 ka fruit)
`src/api/types.ts` **Day 19 me hi likha tha** (backend Pydantic ka mirror). Aaj bas import kiya —
`ChatResponse`, `Source`, `UploadResponse` fully typed. `client.ts` me `fetch` ke responses pe
ZERO guessing: `res.json()` ka type pehle se pata. Yahi "single source of truth" ka fayda —
backend `tool_used` bhejta hai to TS ko already maloom.

## Files
- `api/client.ts` — `api.chat()` / `api.upload()` (FormData) / `api.health()`. BASE = `VITE_API_URL ?? localhost:8000/api`.
- `components/ToolBadge.tsx` — `tool_used` → colored pill (policy=green, account=amber, none=red).
  **Differentiator VISIBLE** — user ko dikhta agent ne kaunsa tool chuna.
- `components/Citation.tsx` — page chip, hover pe poora snippet (title attr).
- `components/UploadBox.tsx` — file input → `/api/upload` → status (doc_id + chunks).
- `components/ChatWindow.tsx` — Msg[] state (user | assistant=ChatResponse), send(), loading/error/empty,
  sample chips, auto-scroll (useRef + scrollIntoView).
- `App.tsx` — layout + health-dot (backend online/offline) + fixed company_id="bajaj" (single-tenant).
- `index.css` — clean light theme, bubbles, badges.

## ✅ Test LIVE (browser, 5173 + backend 8000)
- App load → "backend online" green dot (health check).
- "EMI bounce charge?" → 🟢 policy_search badge + ₹1000+GST + citations page 2,7.
- "VJ-200 ka status?" → 🟡 account_api badge + CLOSED/₹0 (mock), no citations.
- Poora chain: React fetch → FastAPI → agent → tool → Claude → typed response → badge+citations render.

## Day 24 polish TODO (noted)
- **Markdown render:** answer me `**bold**` + `| table |` raw dikh raha → `react-markdown` add.
- Dedup (backend, 92 chunks). Mobile responsive. RAGAS eval dashboard (Day 24 ka main kaam).

## Next (Day 24) — Eval + Polish
RAGAS (Day 12) pipeline pe (faithfulness/relevancy) → mini dashboard. Markdown render, error/empty polish,
README + screenshots. Phir Day 25 deploy (Render + Vercel).
