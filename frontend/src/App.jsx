import { useEffect, useMemo, useState } from "react";
import { fetchTables, fetchTableData } from "./api/client";

export default function App() {
  const [tables, setTables] = useState([]);
  const [selected, setSelected] = useState("");
  const [columns, setColumns] = useState([]);
  const [rows, setRows] = useState([]);

  const [loadingTables, setLoadingTables] = useState(false);
  const [loadingData, setLoadingData] = useState(false);
  const [error, setError] = useState("");

  const [page, setPage] = useState(1);
  const [pageSize] = useState(25);
  const [totalRows, setTotalRows] = useState(0);

  const [search, setSearch] = useState("");
  const debouncedSearch = useDebounced(search, 350);

  useEffect(() => {
    (async () => {
      try {
        setLoadingTables(true);
        setError("");
        const data = await fetchTables();
        const list = data.tables ?? [];
        setTables(list);
        setSelected(list[0] ?? "");
      } catch (e) {
        setError(e.message || "Failed to load tables");
      } finally {
        setLoadingTables(false);
      }
    })();
  }, []);

  useEffect(() => {
    if (!selected) return;

    (async () => {
      try {
        setLoadingData(true);
        setError("");
        const data = await fetchTableData(selected, {
          page,
          pageSize,
          search: debouncedSearch,
        });
        setColumns(data.columns ?? []);
        setRows(data.rows ?? []);
        setTotalRows(data.total_rows ?? 0);
      } catch (e) {
        setError(e.message || "Failed to load table data");
      } finally {
        setLoadingData(false);
      }
    })();
  }, [selected, page, pageSize, debouncedSearch]);

  const totalPages = useMemo(
    () => Math.max(1, Math.ceil((totalRows || 0) / pageSize)),
    [totalRows, pageSize]
  );

  return (
    <div style={{ display: "grid", gridTemplateColumns: "260px 1fr", gap: 16, padding: 16, height: "100vh", boxSizing: "border-box", fontFamily: "system-ui, sans-serif" }}>
      <aside style={{ border: "1px solid #eee", borderRadius: 14, padding: 14, overflow: "auto" }}>
        <h3 style={{ marginTop: 0 }}>Tables</h3>

        {loadingTables ? (
          <div>Loading…</div>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {tables.map((t) => (
              <button
                key={t}
                onClick={() => { setSelected(t); setPage(1); setSearch(""); }}
                style={{
                  textAlign: "left",
                  padding: "10px 12px",
                  borderRadius: 10,
                  border: "1px solid #ddd",
                  background: t === selected ? "#f3f4f6" : "white",
                  cursor: "pointer",
                  fontWeight: t === selected ? 700 : 500
                }}
              >
                {t}
              </button>
            ))}
          </div>
        )}
      </aside>

      <main style={{ border: "1px solid #eee", borderRadius: 14, padding: 14, overflow: "hidden" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
          <h2 style={{ margin: 0 }}>{selected ? `Table: ${selected}` : "Select a table"}</h2>

          <input
            value={search}
            onChange={(e) => { setSearch(e.target.value); setPage(1); }}
            placeholder="Search…"
            style={{
              marginLeft: "auto",
              padding: "10px 12px",
              borderRadius: 10,
              border: "1px solid #ddd",
              minWidth: 240
            }}
            disabled={!selected}
          />
        </div>

        {error && (
          <div style={{ marginTop: 12, padding: 12, borderRadius: 10, border: "1px solid #fecaca", background: "#fff1f2" }}>
            <b>Error:</b> {error}
          </div>
        )}

        <div style={{ marginTop: 12, display: "flex", alignItems: "center", gap: 10 }}>
          <button onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={!selected || loadingData || page <= 1}>◀ Prev</button>
          <button onClick={() => setPage((p) => Math.min(totalPages, p + 1))} disabled={!selected || loadingData || page >= totalPages}>Next ▶</button>
          <span style={{ opacity: 0.8 }}>
            Page <b>{page}</b> / <b>{totalPages}</b> · Total rows: <b>{totalRows}</b>
          </span>
          {loadingData && <span style={{ marginLeft: "auto" }}>Loading…</span>}
        </div>

        <div style={{ marginTop: 12, border: "1px solid #eee", borderRadius: 12, overflow: "auto", height: "calc(100vh - 190px)" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                {columns.map((c) => (
                  <th key={c} style={{ position: "sticky", top: 0, background: "#fafafa", textAlign: "left", padding: "10px 12px", borderBottom: "1px solid #eee", whiteSpace: "nowrap" }}>
                    {c}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {!selected ? (
                <tr><td style={{ padding: 14 }} colSpan={999}>Pick a table.</td></tr>
              ) : rows.length ? (
                rows.map((r, idx) => (
                  <tr key={idx}>
                    {columns.map((c) => (
                      <td key={c} style={{ padding: "10px 12px", borderBottom: "1px solid #f1f1f1" }}>
                        {String(r?.[c] ?? "")}
                      </td>
                    ))}
                  </tr>
                ))
              ) : (
                <tr><td style={{ padding: 14 }} colSpan={999}>No rows.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}

function useDebounced(value, delayMs) {
  const [v, setV] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setV(value), delayMs);
    return () => clearTimeout(t);
  }, [value, delayMs]);
  return v;
}
