async function jsonOrThrow(res, label) {
  if (res.ok) return res.json();

  let msg = "";
  try {
    const data = await res.json();
    msg = data?.detail || "";
  } catch {}
  throw new Error(msg || `${label} failed: HTTP ${res.status}`);
}

export async function getTables() {
  const res = await fetch("/api/tables");
  return jsonOrThrow(res, "GET /api/tables");
}

export async function getTableData(table, { page = 1, page_size = 25, search = "" } = {}) {
  const url =
    `/api/tables/${encodeURIComponent(table)}` +
    `?page=${encodeURIComponent(page)}` +
    `&page_size=${encodeURIComponent(page_size)}` +
    `&search=${encodeURIComponent(search)}`;
  const res = await fetch(url);
  return jsonOrThrow(res, `GET /api/tables/${table}`);
}

export async function getLeaderboard(limit = 10) {
  const res = await fetch(`/api/core/leaderboard?limit=${encodeURIComponent(limit)}`);
  return jsonOrThrow(res, "GET /api/core/leaderboard");
}

export async function getConstructors(year) {
  const res = await fetch(`/api/core/constructors?year=${encodeURIComponent(year)}`);
  return jsonOrThrow(res, "GET /api/core/constructors");
}

export async function getDriverStats(driverId) {
  const res = await fetch(`/api/core/drivers/${encodeURIComponent(driverId)}/stats`);
  return jsonOrThrow(res, "GET /api/core/drivers/{driver_id}/stats");
}
