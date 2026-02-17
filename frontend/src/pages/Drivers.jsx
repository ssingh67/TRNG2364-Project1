import { useEffect, useState } from "react";
import { getDriverStats } from "../api/f1";

export default function Drivers() {
  const [driverId, setDriverId] = useState(1);
  const [row, setRow] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  async function load() {
    try {
      setLoading(true);
      setErr("");
      const data = await getDriverStats(driverId);
      setRow(data);
    } catch (e) {
      setErr(e.message || "Failed to load driver stats");
      setRow(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div style={{ maxWidth: 1200, margin: "0 auto", padding: 16 }}>
      <div className="f1-card" style={{ padding: "14px 16px", marginBottom: 12 }}>
        <div className="f1-h1">Drivers</div>
        <div className="f1-subtle">/api/core/drivers/&lt;driver_id&gt;/stats</div>
      </div>

      <div className="f1-card" style={{ padding: 16 }}>
        <div style={{ display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap" }}>
          <div style={{ fontWeight: 800 }}>Driver Stats</div>

          <div className="f1-subtle">Driver ID:</div>
          <input
            type="number"
            min={1}
            value={driverId}
            onChange={(e) => setDriverId(Number(e.target.value || 1))}
            className="f1-search"
            style={{ maxWidth: 160 }}
          />

          <button className="f1-btn primary" onClick={load} disabled={loading}>
            Fetch
          </button>

          {loading && <span className="f1-pill"><span className="f1-dot" /> Loading…</span>}
          {err && <span className="f1-pill" style={{ borderColor: "rgba(255,30,45,.35)" }}><span className="f1-dot red" /> {err}</span>}
        </div>

        <div style={{ marginTop: 12 }}>
          {row ? (
            <div style={{ display: "grid", gap: 10 }}>
              <Stat label="Driver" value={row.driver_name} />
              <Stat label="Races" value={row.races} />
              <Stat label="Wins" value={row.wins} />
              <Stat label="Podiums" value={row.podiums} />
              <Stat label="Total Points" value={row.total_points} />
            </div>
          ) : (
            <div className="f1-subtle">{loading ? "Loading…" : "No driver loaded."}</div>
          )}
        </div>
      </div>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div
      style={{
        border: "1px solid rgba(255,255,255,0.10)",
        borderRadius: 12,
        padding: "12px 14px",
        display: "flex",
        justifyContent: "space-between",
        gap: 12,
      }}
    >
      <div style={{ opacity: 0.75 }}>{label}</div>
      <div style={{ fontWeight: 900 }}>{String(value ?? "")}</div>
    </div>
  );
}
