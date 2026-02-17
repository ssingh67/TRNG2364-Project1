import { useEffect, useMemo, useState } from "react";

import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";

import { fetchTables, fetchTableData } from "./api/client";
import External from "./pages/External";
import ApiKeysPanel from "./components/ApiKeysPanel";

import Leaderboard from "./pages/Leaderboard";
import Constructors from "./pages/Constructors";
import Drivers from "./pages/Drivers";

<Routes>
  <Route path="/" element={<TablesPage />} />
  <Route path="/leaderboard" element={<Leaderboard />} />
  <Route path="/constructors" element={<Constructors />} />
  <Route path="/drivers" element={<Drivers />} />
  <Route path="/keys" element={<ApiKeysPanel />} />
  <Route path="/external" element={<External />} />
</Routes>


/* ----------------------------- APP (Router) ----------------------------- */

export default function App() {
  return (
    <BrowserRouter>
      <div className="f1-carbon" style={{ minHeight: "100vh" }}>
        <TopNav />

        <Routes>
          {/* Existing table browser */}
          <Route path="/" element={<TablesPage />} />

          {/* New pages */}
          <Route path="/leaderboard" element={<LeaderboardPage />} />
          <Route path="/constructors" element={<ConstructorsPage />} />
          <Route path="/drivers" element={<DriversPage />} />

          {/* Your existing new-window route */}
          <Route path="/external" element={<External />} />

          {/* Optional: keys manager page */}
          <Route path="/keys" element={<KeysPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

/* ----------------------------- TOP NAV BAR ------------------------------ */

function TopNav() {
  const linkStyle = ({ isActive }) => ({
    padding: "10px 12px",
    borderRadius: 10,
    textDecoration: "none",
    fontWeight: 600,
    border: "1px solid rgba(255,255,255,0.10)",
    background: isActive ? "rgba(0,255,180,0.08)" : "rgba(255,255,255,0.03)",
    color: "var(--text, #e8eef6)",
  });

  return (
    <div
      style={{
        position: "sticky",
        top: 0,
        zIndex: 20,
        backdropFilter: "blur(10px)",
        background: "rgba(11,15,20,0.75)",
        borderBottom: "1px solid rgba(255,255,255,0.08)",
      }}
    >
      <div
        style={{
          maxWidth: 1200,
          margin: "0 auto",
          padding: "12px 16px",
          display: "flex",
          gap: 10,
          alignItems: "center",
          flexWrap: "wrap",
          justifyContent: "space-between",
        }}
      >
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          <NavLink to="/" style={linkStyle} end>
            Tables
          </NavLink>
          <NavLink to="/leaderboard" style={linkStyle}>
            Leaderboard
          </NavLink>
          <NavLink to="/constructors" style={linkStyle}>
            Constructors
          </NavLink>
          <NavLink to="/drivers" style={linkStyle}>
            Drivers
          </NavLink>
          <NavLink to="/keys" style={linkStyle}>
            API Keys
          </NavLink>
        </div>

        <div style={{ opacity: 0.75, fontSize: 13 }}>
          TRNG2364 • F1 Data Dashboard
        </div>
      </div>
    </div>
  );
}

/* --------------------------- PAGE: TABLES UI ---------------------------- */
/* This is your existing App body moved into a page component. */

function TablesPage() {
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

  const isUrlColumn = (c) => String(c).toLowerCase() === "url";

  return (
    <div className="f1-wrap" style={{ maxWidth: 1200, margin: "0 auto", padding: 16 }}>
      {/* LEFT: tables list */}
      <aside className="f1-card">
        <div className="f1-card-header">
          <div>
            <div className="f1-h1">Tables</div>
            <div className="f1-subtle">Select dataset</div>
          </div>
          <span className="f1-pill">
            <span className="f1-dot" />
            {tables.length}
          </span>
        </div>

        <div className="f1-side">
          {loadingTables ? (
            <span className="f1-subtle">Loading…</span>
          ) : (
            tables.map((t) => (
              <button
                key={t}
                onClick={() => {
                  setSelected(t);
                  setPage(1);
                  setSearch("");
                }}
                className={`f1-side-btn ${t === selected ? "active" : ""}`}
              >
                <span className="f1-side-name">{t}</span>
                <span className="f1-side-arrow">→</span>
              </button>
            ))
          )}
        </div>
      </aside>

      {/* RIGHT: table */}
      <main className="f1-card f1-main-stack">
        <div className="f1-card-header">
          <div>
            <div className="f1-h1">{selected ? `Table: ${selected}` : "Select a table"}</div>
            <div className="f1-subtle">
              Page {page}/{totalPages} · Total rows: {totalRows}
            </div>
          </div>

          <span className="f1-pill">
            <span className={error ? "f1-dot red" : "f1-dot lime"} />
            {error ? "DEGRADED" : "CONNECTED"}
          </span>
        </div>

        <div className="f1-controls">
          <div className="f1-controls-left">
            <button
              className="f1-btn"
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={!selected || loadingData || page <= 1}
            >
              ◀ Prev
            </button>

            <button
              className="f1-btn primary"
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={!selected || loadingData || page >= totalPages}
            >
              Next ▶
            </button>

            {loadingData && (
              <span className="f1-pill">
                <span className="f1-dot" />
                Loading…
              </span>
            )}
          </div>

          <input
            className="f1-search"
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            placeholder="Search…"
            disabled={!selected}
          />
        </div>

        {error && (
          <div style={{ padding: "12px 16px" }}>
            <span className="f1-pill" style={{ borderColor: "rgba(255,30,45,.35)" }}>
              <span className="f1-dot red" />
              {error}
            </span>
          </div>
        )}

        <div className="f1-table-wrap">
          <table className="f1-table">
            <thead>
              <tr>
                <th>POS</th>
                {columns.map((c) => (
                  <th key={c}>{c}</th>
                ))}
              </tr>
            </thead>

            <tbody>
              {!selected ? (
                <tr>
                  <td colSpan={999} style={{ padding: 16 }}>
                    Pick a table.
                  </td>
                </tr>
              ) : rows.length ? (
                rows.map((r, idx) => (
                  <tr key={idx}>
                    <td className="f1-pos">
                      <span className="f1-pos-badge">{(page - 1) * pageSize + (idx + 1)}</span>
                    </td>

                    {columns.map((c) => {
                      const val = r?.[c];
                      if (isUrlColumn(c) && val) {
                        return (
                          <td key={c} title={String(val)}>
                            <a
                              href={String(val)}
                              target="_blank"
                              rel="noreferrer"
                              style={{ color: "var(--cyan)", textDecoration: "none" }}
                            >
                              {String(val)}
                            </a>
                          </td>
                        );
                      }
                      return (
                        <td key={c} title={String(val ?? "")}>
                          {String(val ?? "")}
                        </td>
                      );
                    })}
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={999} style={{ padding: 16 }}>
                    No rows.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}

/* ------------------------ PAGE: LEADERBOARD ----------------------------- */

function LeaderboardPage() {
  const [limit, setLimit] = useState(10);
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        setErr("");
        const res = await fetch(`/api/core/leaderboard?limit=${encodeURIComponent(limit)}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setRows(Array.isArray(data) ? data : []);
      } catch (e) {
        setErr(e.message || "Failed to load leaderboard");
      } finally {
        setLoading(false);
      }
    })();
  }, [limit]);

  return (
    <PageWrap title="Leaderboard">
      <div className="f1-card" style={{ padding: 16 }}>
        <div style={{ display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap" }}>
          <div style={{ fontWeight: 700 }}>Top drivers</div>
          <div style={{ opacity: 0.75 }}>Limit:</div>
          <input
            type="number"
            min={1}
            max={50}
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value || 10))}
            className="f1-search"
            style={{ maxWidth: 140 }}
          />
          {loading && <span className="f1-pill"><span className="f1-dot" /> Loading…</span>}
          {err && <span className="f1-pill" style={{ borderColor: "rgba(255,30,45,.35)" }}><span className="f1-dot red" /> {err}</span>}
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
                  <td colSpan={999} style={{ padding: 16 }}>
                    {loading ? "Loading…" : "No data."}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </PageWrap>
  );
}

/* ---------------------- PAGE: CONSTRUCTORS BY YEAR ---------------------- */

function ConstructorsPage() {
  const currentYear = new Date().getFullYear();
  const [year, setYear] = useState(currentYear);
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        setErr("");
        const res = await fetch(`/api/core/constructors?year=${encodeURIComponent(year)}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setRows(Array.isArray(data) ? data : []);
      } catch (e) {
        setErr(e.message || "Failed to load constructors");
      } finally {
        setLoading(false);
      }
    })();
  }, [year]);

  return (
    <PageWrap title="Constructors">
      <div className="f1-card" style={{ padding: 16 }}>
        <div style={{ display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap" }}>
          <div style={{ fontWeight: 700 }}>Constructor points</div>
          <div style={{ opacity: 0.75 }}>Year:</div>
          <input
            type="number"
            min={1950}
            value={year}
            onChange={(e) => setYear(Number(e.target.value || currentYear))}
            className="f1-search"
            style={{ maxWidth: 160 }}
          />
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
                <th>Constructor ID</th>
              </tr>
            </thead>
            <tbody>
              {rows.length ? (
                rows.map((r, idx) => (
                  <tr key={`${r.constructor_id}-${idx}`}>
                    <td className="f1-pos">
                      <span className="f1-pos-badge">{idx + 1}</span>
                    </td>
                    <td>{r.constructor_name}</td>
                    <td>{r.total_points}</td>
                    <td>{r.constructor_id}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={999} style={{ padding: 16 }}>
                    {loading ? "Loading…" : "No data for that year."}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </PageWrap>
  );
}

/* -------------------------- PAGE: DRIVER STATS -------------------------- */

function DriversPage() {
  const [driverId, setDriverId] = useState(1);
  const [row, setRow] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  async function load() {
    try {
      setLoading(true);
      setErr("");
      setRow(null);

      const res = await fetch(`/api/core/drivers/${encodeURIComponent(driverId)}/stats`);
      if (!res.ok) {
        const msg = await safeJsonMessage(res);
        throw new Error(msg || `HTTP ${res.status}`);
      }
      const data = await res.json();
      setRow(data);
    } catch (e) {
      setErr(e.message || "Failed to load driver stats");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <PageWrap title="Drivers">
      <div className="f1-card" style={{ padding: 16 }}>
        <div style={{ display: "flex", gap: 10, alignItems: "center", flexWrap: "wrap" }}>
          <div style={{ fontWeight: 700 }}>Driver stats</div>

          <div style={{ opacity: 0.75 }}>Driver ID:</div>
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
              <StatLine label="Driver" value={row.driver_name} />
              <StatLine label="Races" value={row.races} />
              <StatLine label="Wins" value={row.wins} />
              <StatLine label="Podiums" value={row.podiums} />
              <StatLine label="Total Points" value={row.total_points} />
              <StatLine label="Driver ID" value={row.driver_id} />
            </div>
          ) : (
            <div style={{ opacity: 0.75 }}>
              {loading ? "Loading…" : "Enter a driver_id and hit Fetch."}
            </div>
          )}
        </div>
      </div>
    </PageWrap>
  );
}

function StatLine({ label, value }) {
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
      <div style={{ fontWeight: 700 }}>{String(value ?? "")}</div>
    </div>
  );
}

/* ---------------------------- PAGE: API KEYS ---------------------------- */

function KeysPage() {
  return (
    <PageWrap title="API Keys">
      <div style={{ maxWidth: 900 }}>
        <ApiKeysPanel />
      </div>
    </PageWrap>
  );
}

/* ------------------------------ PAGE WRAP ------------------------------- */

function PageWrap({ title, children }) {
  return (
    <div style={{ maxWidth: 1200, margin: "0 auto", padding: 16 }}>
      <div className="f1-card" style={{ padding: "14px 16px", marginBottom: 12 }}>
        <div className="f1-h1">{title}</div>
        <div className="f1-subtle">F1-style views powered by your FastAPI endpoints</div>
      </div>
      {children}
    </div>
  );
}

/* ----------------------------- UTILITIES -------------------------------- */

function useDebounced(value, delayMs) {
  const [v, setV] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setV(value), delayMs);
    return () => clearTimeout(t);
  }, [value, delayMs]);
  return v;
}

async function safeJsonMessage(res) {
  try {
    const data = await res.json();
    if (typeof data?.detail === "string") return data.detail;
    return "";
  } catch {
    return "";
  }
}
