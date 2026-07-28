import { useEffect, useRef, useState } from "react";

import { api } from "../api/client";
import type { ChatResponse } from "../api/types";
import Citation from "./Citation";
import ToolBadge from "./ToolBadge";

// ek chat message: user (sirf text) ya assistant (poora ChatResponse — answer+sources+tool_used)
type Msg =
  | { role: "user"; text: string }
  | { role: "assistant"; data: ChatResponse };

const SAMPLES = [
  "EMI bounce charge kitna hai?",
  "VJ-100 ka balance batao",
  "Aaj Mumbai ka mausam?",
];

export default function ChatWindow({ companyId }: { companyId: string }) {
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function send(q: string) {
    const question = q.trim();
    if (!question || loading) return;
    setInput("");
    setError(null);
    setMessages((m) => [...m, { role: "user", text: question }]);
    setLoading(true);
    try {
      const data = await api.chat({ company_id: companyId, question });
      setMessages((m) => [...m, { role: "assistant", data }]);
    } catch {
      setError("Backend se jawab nahi mila — server chal raha hai?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="card chat">
      <h2 className="card__title">💬 Support chat</h2>

      <div className="chat__messages">
        {messages.length === 0 && !loading && (
          <div className="chat__empty">
            <p>Koi sawaal poochho 👇</p>
            <div className="chat__samples">
              {SAMPLES.map((s) => (
                <button key={s} className="chip" onClick={() => send(s)}>
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((m, i) =>
          m.role === "user" ? (
            <div key={i} className="bubble bubble--user">
              {m.text}
            </div>
          ) : (
            <div key={i} className="bubble bubble--bot">
              <div className="bubble__meta">
                <ToolBadge tool={m.data.tool_used} />
              </div>
              <div className="bubble__text">{m.data.answer}</div>
              {m.data.sources.length > 0 && (
                <div className="bubble__sources">
                  {m.data.sources.map((s, j) => (
                    <Citation key={j} source={s} />
                  ))}
                </div>
              )}
            </div>
          )
        )}

        {loading && <div className="bubble bubble--bot bubble--loading">soch raha hoon…</div>}
        <div ref={endRef} />
      </div>

      {error && <div className="chat__error">{error}</div>}

      <div className="chat__input">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send(input)}
          placeholder="Apna sawaal likho…"
          disabled={loading}
        />
        <button onClick={() => send(input)} disabled={loading || !input.trim()}>
          Bhejo
        </button>
      </div>
    </section>
  );
}
