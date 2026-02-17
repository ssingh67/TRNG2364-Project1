import { useMemo, useState } from "react";

function useQuery() {
  return useMemo(() => new URLSearchParams(window.location.search), []);
}

export default function External() {
  const q = useQuery();
  const provider = q.get("provider") || "custom";
  const label = q.get("label") || "Unnamed";
  const key = q.get("key") || "";

  const [result, setResult] = useState("");

  async function testCall() {
    setResult("Testing...");

    try {
      // Example: call YOUR backend (recommended) rather than third-party directly
      // But if you want third-party direct calls, that’s provider-specific.
      const res = await fetch("/api/tables"); // simple test to confirm tab works
      const data = await res.json();
      setResult(JSON.stringify({ provider, label, keyPreview: key.slice(0, 4) + "****", data }, null, 2));
    } catch (e) {
      setResult(String(e));
    }
  }

  return (
    <div style={{ padding: 18 }}>
      <h1 style={{ fontSize: 22, marginBottom: 6 }}>{label}</h1>
      <div style={{ opacity: 0.8, marginBottom: 14 }}>Provider: {provider}</div>

      <div style={{ marginBottom: 12 }}>
        <div style={{ fontWeight: 600 }}>Key preview</div>
        <div style={{ fontFamily: "monospace" }}>
          {key ? `${key.slice(0, 4)}****${key.slice(-4)}` : "(none)"}
        </div>
      </div>

      <button
        onClick={testCall}
        style={{ padding: 10, borderRadius: 10, border: "1px solid #333" }}
      >
        Test Call
      </button>

      <pre
        style={{
          marginTop: 14,
          padding: 12,
          border: "1px solid #333",
          borderRadius: 12,
          whiteSpace: "pre-wrap",
        }}
      >
        {result || "No output yet."}
      </pre>
    </div>
  );
}
