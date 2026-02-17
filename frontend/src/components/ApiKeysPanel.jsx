import { useEffect, useMemo, useState } from "react";

const STORAGE_KEY = "etl_api_keys_v1";

function safeId() {
  return Math.random().toString(16).slice(2) + Date.now().toString(16);
}

export default function ApiKeysPanel() {
  const [label, setLabel] = useState("");
  const [provider, setProvider] = useState("custom");
  const [keyValue, setKeyValue] = useState("");
  const [keys, setKeys] = useState([]);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) setKeys(JSON.parse(raw));
    } catch {
      setKeys([]);
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(keys));
  }, [keys]);

  const masked = (k) => (k.length <= 8 ? "********" : `${k.slice(0, 4)}****${k.slice(-4)}`);

  const canAdd = useMemo(() => {
    return label.trim().length > 0 && keyValue.trim().length > 0;
  }, [label, keyValue]);

  function addKey() {
    if (!canAdd) return;
    const newItem = {
      id: safeId(),
      label: label.trim(),
      provider,
      key: keyValue.trim(),
      createdAt: new Date().toISOString(),
    };
    setKeys((prev) => [newItem, ...prev]);
    setLabel("");
    setProvider("custom");
    setKeyValue("");
  }

  function removeKey(id) {
    setKeys((prev) => prev.filter((k) => k.id !== id));
  }

  function openInNewTab(item) {
    // Encode key so it’s URL-safe
    const url = `/external?provider=${encodeURIComponent(item.provider)}&label=${encodeURIComponent(
      item.label
    )}&key=${encodeURIComponent(item.key)}`;

    window.open(url, "_blank", "noopener,noreferrer");
  }

  return (
    <div style={{ padding: 16, border: "1px solid #222", borderRadius: 12 }}>
      <h2 style={{ fontSize: 18, marginBottom: 12 }}>API Keys</h2>

      <div style={{ display: "grid", gap: 10, gridTemplateColumns: "1fr 1fr" }}>
        <input
          value={label}
          onChange={(e) => setLabel(e.target.value)}
          placeholder="Label (e.g., OpenAI, Maps, News)"
          style={{ padding: 10, borderRadius: 10, border: "1px solid #333" }}
        />

        <select
          value={provider}
          onChange={(e) => setProvider(e.target.value)}
          style={{ padding: 10, borderRadius: 10, border: "1px solid #333" }}
        >
          <option value="custom">Custom</option>
          <option value="openai">OpenAI</option>
          <option value="newsapi">NewsAPI</option>
          <option value="googlemaps">Google Maps</option>
        </select>

        <input
          value={keyValue}
          onChange={(e) => setKeyValue(e.target.value)}
          placeholder="Paste API key"
          style={{ padding: 10, borderRadius: 10, border: "1px solid #333", gridColumn: "1 / -1" }}
        />

        <button
          onClick={addKey}
          disabled={!canAdd}
          style={{
            padding: 10,
            borderRadius: 10,
            border: "1px solid #333",
            cursor: canAdd ? "pointer" : "not-allowed",
            gridColumn: "1 / -1",
          }}
        >
          Add Key
        </button>
      </div>

      <div style={{ marginTop: 16, display: "grid", gap: 10 }}>
        {keys.length === 0 ? (
          <div style={{ opacity: 0.7 }}>No keys saved yet.</div>
        ) : (
          keys.map((item) => (
            <div
              key={item.id}
              style={{
                display: "flex",
                justifyContent: "space-between",
                gap: 12,
                padding: 12,
                border: "1px solid #333",
                borderRadius: 12,
                alignItems: "center",
              }}
            >
              <div>
                <div style={{ fontWeight: 600 }}>{item.label}</div>
                <div style={{ opacity: 0.75, fontSize: 13 }}>
                  Provider: {item.provider} • Key: {masked(item.key)}
                </div>
              </div>

              <div style={{ display: "flex", gap: 8 }}>
                <button
                  onClick={() => openInNewTab(item)}
                  style={{ padding: "8px 10px", borderRadius: 10, border: "1px solid #333" }}
                >
                  Open
                </button>
                <button
                  onClick={() => removeKey(item.id)}
                  style={{ padding: "8px 10px", borderRadius: 10, border: "1px solid #333" }}
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
