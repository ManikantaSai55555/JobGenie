"use client";
import { useState } from "react";

export default function ResumePage() {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  async function upload() {
    if (!file) return;
    const form = new FormData();
    form.append("file", file);
    const token = localStorage.getItem("token");
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/users/me/resume`, {
      method: "POST",
      body: form,
      headers: token ? { Authorization: `Bearer ${token}` } : undefined,
    });
    if (!res.ok) {
      setMessage("Upload failed");
      return;
    }
    setMessage("Resume uploaded and parsed");
  }

  return (
    <main className="mx-auto max-w-3xl p-6">
      <h1 className="text-2xl font-semibold">Upload Resume</h1>
      <div className="mt-4 space-y-2">
        <input type="file" accept=".pdf,.docx,.txt" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button className="bg-blue-600 text-white p-2" onClick={upload}>Upload</button>
        {message && <div className="text-green-700">{message}</div>}
      </div>
    </main>
  );
}
