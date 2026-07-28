// API contract — FRONTEND side (TypeScript).
//
// Yeh file backend ke `backend/app/models/schemas.py` ka MIRROR hai.
// Dono ko hamesha match rakho = single source of truth.
// Day 19 pe finalize (Day 23 me ApiClient + components inhe use karenge).

// ---------- POST /api/upload  (multipart: file + company_id) ----------
export interface UploadResponse {
  doc_id: string;
  chunks: number;
  status: "ok" | "error";
}

// ---------- POST /api/chat ----------
export interface ChatRequest {
  company_id: string;
  question: string;
}

export interface Source {
  text: string;
  page?: number; // optional — har source me page na ho (Day 6 metadata)
  doc_id: string;
}

export interface ChatResponse {
  answer: string;
  sources: Source[]; // citations (agar RAG tool chala)
  tool_used: "policy_search" | "account_api" | "none"; // agent ne kya chuna
}

// ---------- GET /api/health ----------
export interface HealthResponse {
  status: "ok";
}
