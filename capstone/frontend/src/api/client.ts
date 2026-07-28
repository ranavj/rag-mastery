// ApiClient — ek hi jagah se backend ko call. Types = ./types.ts (backend schemas ka mirror).
// Contract Day 19 me fix hua — isliye yahan responses fully typed, zero guessing.

import type { ChatRequest, ChatResponse, UploadResponse } from "./types";

const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api";

export const api = {
  async chat(req: ChatRequest): Promise<ChatResponse> {
    const res = await fetch(`${BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req),
    });
    if (!res.ok) throw new Error(`chat failed: ${res.status}`);
    return res.json();
  },

  async upload(file: File, companyId: string): Promise<UploadResponse> {
    const form = new FormData();
    form.append("file", file); // FastAPI: UploadFile
    form.append("company_id", companyId); // FastAPI: Form(...)
    const res = await fetch(`${BASE}/upload`, { method: "POST", body: form });
    if (!res.ok) throw new Error(`upload failed: ${res.status}`);
    return res.json();
  },

  async health(): Promise<boolean> {
    try {
      const res = await fetch(`${BASE}/health`);
      return res.ok;
    } catch {
      return false;
    }
  },
};

export type { ChatRequest, ChatResponse, UploadResponse };
