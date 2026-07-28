import type { ChatResponse } from "../api/types";

// tool_used ko dikhne-layak badge me — capstone ka differentiator VISIBLE.
const META: Record<ChatResponse["tool_used"], { label: string; cls: string }> = {
  policy_search: { label: "📄 policy_search", cls: "badge--policy" },
  account_api: { label: "🔢 account_api", cls: "badge--account" },
  none: { label: "🚫 no tool", cls: "badge--none" },
};

export default function ToolBadge({ tool }: { tool: ChatResponse["tool_used"] }) {
  const m = META[tool];
  return <span className={`badge ${m.cls}`}>{m.label}</span>;
}
