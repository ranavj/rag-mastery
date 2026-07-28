// ApiClient — fetch wrapper. Ek hi jagah se backend ko call karo (service layer).
//
// SKELETON (Day 19). Day 23 me bharega (Vite + React setup ke baad).
// Types: ./types.ts (backend schemas ka mirror).

import type { ChatRequest, ChatResponse, UploadResponse } from "./types";

const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api";

export const api = {
  // async chat(req: ChatRequest): Promise<ChatResponse> { ... }
  // async upload(file: File, companyId: string): Promise<UploadResponse> { ... }
  // async health(): Promise<boolean> { ... }
};

export type { ChatRequest, ChatResponse, UploadResponse };
