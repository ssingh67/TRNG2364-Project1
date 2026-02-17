export default function Topbar({ status = "degraded", lastRun = "—", onRun, onRefresh }) {
  const dotClass =
    status === "ok" ? "f1-dot lime" : status === "offline" ? "f1-dot red" : "f1-dot";

  const label =
    status === "ok" ? "API CONNECTED" : status === "offline" ? "API OFFLINE" : "API DEGRADED";

  return (
    <div className="f1-panel-header">
      <div className="f1-top-left">
        <span className="f1-chip">
          <span className={dotClass} />
          {label}
        </span>

        <span className="f1-chip">
          <span className="f1-muted">LAST RUN</span>
          <span className="f1-strong">{lastRun}</span>
        </span>
      </div>

      <div className="f1-top-actions">
        <button className="f1-btn secondary" onClick={onRefresh}>
          Refresh
        </button>
        <button className="f1-btn" onClick={onRun}>
          ▶ Run ETL
        </button>
      </div>
    </div>
  );
}
