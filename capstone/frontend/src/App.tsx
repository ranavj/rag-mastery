import { useEffect, useState } from "react";

import { api } from "./api/client";
import ChatWindow from "./components/ChatWindow";
import UploadBox from "./components/UploadBox";

export default function App() {
  // single-tenant demo — company_id fixed. (Multi-tenant auth = post-course.)
  const [companyId] = useState("bajaj");
  const [online, setOnline] = useState<boolean | null>(null);

  useEffect(() => {
    api.health().then(setOnline);
  }, []);

  return (
    <div className="app">
      <header className="app__header">
        <h1>🛟 SmartSupport</h1>
        <div className="app__meta">
          <span className="app__tenant">tenant: {companyId}</span>
          <span className={`dot ${online ? "dot--on" : online === false ? "dot--off" : ""}`}>
            {online == null ? "…" : online ? "backend online" : "backend offline"}
          </span>
        </div>
      </header>

      <main className="app__main">
        <UploadBox companyId={companyId} />
        <ChatWindow companyId={companyId} />
      </main>

      <footer className="app__footer">
        Agentic RAG · policy_search / account_api / honest “nahi pata” · Day 23
      </footer>
    </div>
  );
}
