const API_BASE = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000/docs";

async function request(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Request failed ${res.status}: ${text || res.statusText}`);
  }
  return res.json();
}

export function fetchTables() {
  return request("/api/tables");
}

export function fetchTableData(table, { page = 1, pageSize = 25, search = "" } = {}) {
  const params = new URLSearchParams({
    page: String(page),
    page_size: String(pageSize),
    search: search || "",
  });
  return request(`/api/tables/${encodeURIComponent(table)}?${params.toString()}`);
}
