import { API_URL } from "@/lib/api";

export type LoginResponse = { access_token: string; token_type: string };

export async function login(email: string, password: string): Promise<void> {
  const res = await fetch(`${API_URL}/api/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error("Login failed");
  const data: LoginResponse = await res.json();
  localStorage.setItem("token", data.access_token);
}

export async function register(email: string, password: string, fullName?: string): Promise<void> {
  const res = await fetch(`${API_URL}/api/v1/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, full_name: fullName }),
  });
  if (!res.ok) throw new Error("Register failed");
}

export function logout() {
  localStorage.removeItem("token");
}

export function getToken(): string | null {
  return typeof window !== "undefined" ? localStorage.getItem("token") : null;
}
