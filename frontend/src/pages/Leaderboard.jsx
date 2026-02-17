import { useEffect, useState } from "react";
import { getLeaderboard } from "../api/f1";

export default function Leaderboard() {
  const [limit, setLimit] = useState(10);
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        setErr("");
        const data = await getLeaderboard(limit);
        setRows(Array.isArray(data) ? data : []);
      } catch (e) {
        setErr(e.message || "Failed to load leaderboard");
        setRows([]);
      } finally {
        setLoading(false);
      }
    })();
  }, [limit]);

  return (
    <div style={{ maxWidth: 1200, margin: "0 auto", padding: 16 }}>
      <div className="f1-card" style={{ padding: 16 }}>
        <div style={{ display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap" }}>
          <div style={{ fontWeight: 800 }}>Top Drivers</div>

          <div className="f1-subtle">Limit:</div>
          <input
            type="number"
            min={1}
            max={50}
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value || 10))}
            className="f1-search"
            style={{ maxWidth: 140 }}
          />

          <span className="f1-pill">
            <span className="f1-dot" />
            Rows: {rows.length}
          </span>

          {loading && (
            <span className="f1-pill">
              <span className="f1-dot" /> Loading…
            </span>
          )}

          {err && (
            <span className="f1-pill" style={{ borderColor: "rgba(255,30,45,.35)" }}>
              <span className="f1-dot red" /> {err}
            </span>
          )}
        </div>

        <div className="f1-table-wrap" style={{ marginTop: 12 }}>
          <table className="f1-table">
            <thead>
              <tr>
                <th>POS</th>
                <th>Driver</th>
                <th>Total Points</th>
                <th>Driver ID</th>
              </tr>
            </thead>
            <tbody>
              {rows.length ? (
                rows.map((r, idx) => (
                  <tr key={`${r.driver_id}-${idx}`}>
                    <td className="f1-pos">
                      <span className="f1-pos-badge">{idx + 1}</span>
                    </td>
                    <td>{r.driver_name}</td>
                    <td>{r.total_points}</td>
                    <td>{r.driver_id}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={10} style={{ padding: 16 }}>
                    {loading ? "Loading…" : "No rows returned."}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
