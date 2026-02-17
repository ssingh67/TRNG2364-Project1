export default function Layout({ sidebar, topbar, children }) {
  return (
    <div className="f1-carbon f1-root">
      <div className="f1-shell">
        <aside className="f1-aside">
          <div className="f1-panel f1-aside-panel">{sidebar}</div>
        </aside>

        <main className="f1-main">
          <div className="f1-panel f1-topbar">{topbar}</div>
          <div className="f1-content">{children}</div>
        </main>
      </div>
    </div>
  );
}
