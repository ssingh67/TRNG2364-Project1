export default function Sidebar({ active, onNav }) {
  const items = [
    { key: "overview", label: "Race Control" },
    { key: "tables", label: "Telemetry Tables" },
    { key: "run", label: "Run ETL" },
    { key: "logs", label: "Logs" },
  ];

  return (
    <div className="f1-aside-inner">
      <div className="f1-panel-header">
        <div>
          <div className="f1-brand">ETL PITWALL</div>
          <div className="f1-sub">F1-style data console</div>
        </div>
        <span className="f1-chip">
          <span className="f1-dot" />
          LIVE
        </span>
      </div>

      <div className="f1-nav">
        {items.map((it) => {
          const isActive = active === it.key;
          return (
            <button
              key={it.key}
              onClick={() => onNav(it.key)}
              className={`f1-nav-btn ${isActive ? "active" : ""}`}
            >
              <span className="f1-nav-label">{it.label}</span>
              <span className="f1-nav-arrow">→</span>
            </button>
          );
        })}
      </div>

      <div className="f1-aside-foot">
        <div className="f1-mini">
          <div className="f1-title">Session</div>
          <div className="f1-mini-row">
            <span className="f1-chip"><span className="f1-dot lime" /> OK</span>
            <span className="f1-chip"><span className="f1-dot" /> API</span>
            <span className="f1-chip"><span className="f1-dot red" /> ERR</span>
          </div>
        </div>
      </div>
    </div>
  );
}
