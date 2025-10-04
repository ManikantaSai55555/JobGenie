"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";

type Job = {
  id: number;
  title: string;
  company?: string;
  location?: string;
  salary_min?: number;
  salary_max?: number;
  job_type?: string;
  url: string;
  source: string;
  match_score?: number;
};

export default function JobsPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [q, setQ] = useState("");
  const [location, setLocation] = useState("");
  const [orderBy, setOrderBy] = useState("latest");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function load() {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (q) params.set("q", q);
      if (location) params.set("location", location);
      if (orderBy) params.set("order_by", orderBy);
      const data = await api<Job[]>(`/api/v1/jobs/?${params.toString()}`);
      setJobs(data);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-5xl p-6">
      <h1 className="text-2xl font-semibold">Jobs</h1>
      <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-4">
        <input className="border p-2" placeholder="Keywords" value={q} onChange={(e) => setQ(e.target.value)} />
        <input className="border p-2" placeholder="Location" value={location} onChange={(e) => setLocation(e.target.value)} />
        <select className="border p-2" value={orderBy} onChange={(e) => setOrderBy(e.target.value)}>
          <option value="latest">Latest</option>
          <option value="match">Best match</option>
          <option value="salary">Top paying</option>
        </select>
        <button className="bg-blue-600 text-white p-2" onClick={load} disabled={loading}>{loading ? "Loading..." : "Search"}</button>
      </div>
      <ul className="mt-6 space-y-4">
        {jobs.map((j) => (
          <li key={j.id} className="border p-4 rounded">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-semibold">{j.title}</div>
                <div className="text-sm text-gray-600">{j.company} • {j.location} • {j.source}</div>
                {j.match_score != null && (
                  <div className="text-sm text-green-700">Match: {(j.match_score * 100).toFixed(0)}%</div>
                )}
              </div>
              <Link href={j.url} target="_blank" className="text-blue-600 hover:underline">View</Link>
            </div>
          </li>
        ))}
      </ul>
    </main>
  );
}
