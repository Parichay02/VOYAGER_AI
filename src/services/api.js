const BASE_URL = "http://localhost:8000";

export async function createSession() {
  const res = await fetch(`${BASE_URL}/session/new`, {
    method: "POST",
  });

  return await res.json();
}

export async function healthCheck() {
  const res = await fetch(`${BASE_URL}/health`);
  return await res.json();
}