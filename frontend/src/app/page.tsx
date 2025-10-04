import Link from "next/link";

export default function Home() {
  return (
    <main className="mx-auto max-w-5xl p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">JobScout</h1>
        <nav className="space-x-4">
          <Link href="/jobs" className="text-blue-600 hover:underline">Jobs</Link>
          <Link href="/dashboard" className="text-blue-600 hover:underline">Dashboard</Link>
          <Link href="/resume" className="text-blue-600 hover:underline">Resume</Link>
        </nav>
      </div>
      <p className="mt-4 text-gray-600">Discover and track jobs across the web, refreshed daily.</p>
    </main>
  );
}
