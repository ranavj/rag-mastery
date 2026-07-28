import type { Source } from "../api/types";

// Ek citation chip — page number dikhta, hover pe poora snippet (title).
export default function Citation({ source }: { source: Source }) {
  return (
    <span className="citation" title={source.text}>
      📎 page {source.page ?? "?"}
    </span>
  );
}
