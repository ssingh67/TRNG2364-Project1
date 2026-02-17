import { useEffect, useState } from "react";
import { getConstructors } from "../api/f1";

export default function Constructors() {
  const [year, setYear] = useState(2021); // IMPORTANT: use a year that exists in your DB
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        setErr("");
        const data = await getConstructors(year);
        setRows(Array.isArray(data) ? data : []);
      } catch (e) {
        setErr(e.message || "Failed to load constructors");
        setRows([]);
      } finally {
        setLoading(false);
      }
    })();
  }, [year]);

  return (
    <div style={{ maxWidth: 1200, margin: "0 auto", padding: 16 }}>
      <div className="f1-card" style={{ padding: "14px 16px", marginBottom: 12 }}>
        <div className="f1-h1">Constructors</div>
        <div className="f1-subtle">/api/core/constructors?year=YYYY</div>
      </div>

      <div className="f1-card" style={{ padding: 16 }}>
        <div style={{ display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap" }}>
          <div style={{ fontWeight: 800 }}>Constructor Points</div>

          <div className="f1-subtle">Year:</div>
          <input
            type="number"
            min={1950}
            value={year}
            onChange={(e) => setYear(Number(e.target.value || 2021))}
            className="f1-search"
            style={{ maxWidth: 160 }}
          />

          <span className="f1-pill">
            <span className="f1-dot" />
            Rows: {rows.length}
          </span>

          {loading && <span className="f1-pill"><span className="f1-dot" /> Loading…</span>}
          {err && <span className="f1-pill" style={{ borderColor: "rgba(255,30,45,.35)" }}><span className="f1-dot red" /> {err}</span>}
        </div>

        <div className="f1-table-wrap" style={{ marginTop: 12 }}>
          <table className="f1-table">
            <thead>
              <tr>
                <th>POS</th>
                <th>Constructor</th>
                <th>Total Points</th>
                <th>ID</th>
              </tr>
            </thead>
            <tbody>
              {rows.length ? (
                rows.map((r, idx) => (
                  <tr key={`${r.constructor_id}-${idx}`}>
                    <td className="f1-pos"><span className="f1-pos-badge">{idx + 1}</span></td>
                    <td>{r.constructor_name}</td>
                    <td>{r.total_points}</td>
                    <td>{r.constructor_id}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={10} style={{ padding: 16 }}>
                    {loading ? "Loading…" : "No rows returned for that year."}
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
