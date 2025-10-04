"use client";
import { useState } from "react";
import { register } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await register(email, password, fullName);
      router.push("/login");
    } catch (e) {
      setError("Register failed");
    }
  }

  return (
    <main className="mx-auto max-w-md p-6">
      <h1 className="text-2xl font-semibold">Create account</h1>
      <form className="mt-4 space-y-3" onSubmit={onSubmit}>
        <input className="border p-2 w-full" placeholder="Full name" value={fullName} onChange={(e) => setFullName(e.target.value)} />
        <input className="border p-2 w-full" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="border p-2 w-full" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        {error && <div className="text-red-600">{error}</div>}
        <button className="bg-blue-600 text-white p-2 w-full" type="submit">Register</button>
      </form>
    </main>
  );
}
