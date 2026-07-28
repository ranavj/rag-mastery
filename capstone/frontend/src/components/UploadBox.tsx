import { useState } from "react";

import { api } from "../api/client";

// PDF upload flow — file chuno → POST /api/upload → status (doc_id + chunks).
export default function UploadBox({ companyId }: { companyId: string }) {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function upload() {
    if (!file || busy) return;
    setBusy(true);
    setStatus("⏳ uploading…");
    try {
      const res = await api.upload(file, companyId);
      setStatus(
        res.status === "ok"
          ? `✅ ${res.chunks} chunks stored (doc ${res.doc_id})`
          : "❌ upload error"
      );
    } catch {
      setStatus("❌ upload failed — backend server chal raha hai?");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="card upload">
      <h2 className="card__title">📤 Docs upload</h2>
      <div className="upload__row">
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
        <button onClick={upload} disabled={!file || busy}>
          Upload
        </button>
      </div>
      {status && <div className="upload__status">{status}</div>}
    </section>
  );
}
