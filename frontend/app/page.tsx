"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getHealth } from "@/lib/api";

export default function DashboardPage() {
  const [health, setHealth] = useState<{ status: string; ollama: string } | null>(null);

  useEffect(() => {
    getHealth().then(setHealth).catch(() => setHealth({ status: "error", ollama: "unavailable" }));
  }, []);

  const features = [
    { title: "Semantic Search", desc: "Ingest documents and retrieve with vector similarity.", href: "/query" },
    { title: "Agent Reasoning", desc: "Run multi-step LangGraph agents over your knowledge base.", href: "/agent" },
    { title: "Evaluation", desc: "Benchmark retrieval quality with Recall@K and MRR.", href: "/evaluation" },
    { title: "Experiments", desc: "Compare embedding models, chunk sizes, and prompts.", href: "/experiments" },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">LLM Research OS</h1>
        <p className="text-gray-400">Local-first AI research platform for semantic search, agent reasoning, and evaluation.</p>
      </div>

      {/* System status */}
      <div className="bg-gray-900 rounded-lg border border-gray-800 p-4 flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span className={`w-2 h-2 rounded-full ${health?.status === "ok" ? "bg-green-500" : "bg-red-500"}`} />
          <span className="text-sm text-gray-300">API: {health?.status ?? "checking..."}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className={`w-2 h-2 rounded-full ${health?.ollama === "available" ? "bg-green-500" : "bg-yellow-500"}`} />
          <span className="text-sm text-gray-300">Ollama: {health?.ollama ?? "checking..."}</span>
        </div>
      </div>

      {/* Feature cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {features.map((f) => (
          <Link
            key={f.href}
            href={f.href}
            className="bg-gray-900 rounded-lg border border-gray-800 p-5 hover:border-indigo-500 transition-colors group"
          >
            <h2 className="text-base font-semibold text-white group-hover:text-indigo-400 transition-colors mb-1">{f.title}</h2>
            <p className="text-sm text-gray-400">{f.desc}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
