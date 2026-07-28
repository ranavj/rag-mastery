import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// dev server 5173 (backend CORS me yahi origin allow hai — Day 20)
export default defineConfig({
  plugins: [react()],
  server: { port: 5173 },
});
