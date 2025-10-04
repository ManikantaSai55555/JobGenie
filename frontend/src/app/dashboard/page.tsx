"use client";
import { useEffect, useState } from "react";

export default function DashboardPage() {
  const [saved, setSaved] = useState<any[]>([]);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    const token = localStorage.getItem("token");
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/saved/`, {
      headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      cache: "no-store",
    });
    if (res.ok) setSaved(await res.json());
  }

  return (
    <main className="mx-auto max-w-5xl p-6">
      <h1 className="text-2xl font-semibold">My Dashboard</h1>
      <ul className="mt-4 space-y-4">
        {saved.map((s) => (
          <li key={s.id} className="border p-4">
            <div className="font-semibold">{s.job?.title}</div>
            <div className="text-sm text-gray-600">{s.job?.company} • {s.status}</div>
          </li>
        ))}
      </ul>
    </main>
  );
}
