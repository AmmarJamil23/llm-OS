"use client";

import { useEffect, useState } from "react";
import { listExperiments, compareExperiments, type Experiment } from "@/lib/api";

export default function ExperimentsPage() {
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [selected, setSelected] = useState<[string, string]>(["", ""]);
  const [comparison, setComparison] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    listExperiments().then(setExperiments).catch(() => setExperiments([]));
  }, []);

  const handleCompare = async () => {
    if (!selected[0] || !selected[1]) return;
    setError("");
    try {
      const res = await compareExperiments(selected[0], selected[1]);
      setComparison(res);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Comparison failed");
    }
  };

  type MetricEntry = { a: number; b: number; delta: number; delta_pct: number };

  const renderMetricRow = (label: string, data: MetricEntry) => (
    <tr key={label} className="border-t border-gray-800">
      <td className="px-4 py-3 text-gray-400 text-sm">{label}</td>
      <td className="px-4 py-3 text-indigo-300 text-sm">{typeof data.a === "number" ? data.a.toFixed(4) : data.a}</td>
      <td className="px-4 py-3 text-indigo-300 text-sm">{typeof data.b === "number" ? data.b.toFixed(4) : data.b}</td>
      <td className={`px-4 py-3 text-sm font-medium ${data.delta >= 0 ? "text-emerald-400" : "text-red-400"}`}>
        {data.delta >= 0 ? "+" : ""}{data.delta.toFixed(4)} ({data.delta_pct}%)
      </td>
    </tr>
  );

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold text-white">Experiments</h1>

      {/* Experiments list */}
      {experiments.length === 0 ? (
        <p className="text-gray-500 text-sm">No experiments found. Run an evaluation and save it as an experiment via the API.</p>
      ) : (
        <div className="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-800 text-gray-400 text-xs uppercase">
              <tr>
                {["Name", "Embedding", "Chunk Size", "K", "Avg Recall", "Avg MRR", "Avg Latency"].map((h) => (
                  <th key={h} className="px-4 py-3 text-left">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {experiments.map((exp) => (
                <tr key={exp.id} className="border-t border-gray-800 hover:bg-gray-800/50">
                  <td className="px-4 py-3 text-white">{exp.config.name}</td>
                  <td className="px-4 py-3 text-gray-300">{exp.config.embedding_model}</td>
                  <td className="px-4 py-3 text-gray-300">{exp.config.chunk_size}</td>
                  <td className="px-4 py-3 text-gray-300">{exp.config.retrieval_k}</td>
                  <td className="px-4 py-3 text-indigo-400">{exp.avg_recall.toFixed(3)}</td>
                  <td className="px-4 py-3 text-emerald-400">{exp.avg_mrr.toFixed(3)}</td>
                  <td className="px-4 py-3 text-gray-400">{exp.avg_latency_ms}ms</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Compare panel */}
      {experiments.length >= 2 && (
        <div className="bg-gray-900 rounded-lg border border-gray-800 p-5 space-y-3">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Compare Experiments</h2>
          <div className="flex gap-2 flex-wrap">
            <select
              className="bg-gray-800 text-white rounded px-3 py-2 text-sm border border-gray-700"
              value={selected[0]}
              onChange={(e) => setSelected([e.target.value, selected[1]])}
            >
              <option value="">Select A</option>
              {experiments.map((e) => <option key={e.id} value={e.id}>{e.config.name}</option>)}
            </select>
            <select
              className="bg-gray-800 text-white rounded px-3 py-2 text-sm border border-gray-700"
              value={selected[1]}
              onChange={(e) => setSelected([selected[0], e.target.value])}
            >
              <option value="">Select B</option>
              {experiments.map((e) => <option key={e.id} value={e.id}>{e.config.name}</option>)}
            </select>
            <button
              className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded text-sm transition-colors"
              onClick={handleCompare}
            >
              Compare
            </button>
          </div>
          {error && <p className="text-red-400 text-sm">{error}</p>}

          {comparison && (
            <div className="mt-4 overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-800 text-gray-400 text-xs uppercase">
                  <tr>
                    <th className="px-4 py-3 text-left">Metric</th>
                    <th className="px-4 py-3 text-left">A</th>
                    <th className="px-4 py-3 text-left">B</th>
                    <th className="px-4 py-3 text-left">Δ</th>
                  </tr>
                </thead>
                <tbody>
                  {(["avg_recall", "avg_mrr", "avg_latency_ms"] as const).map((key) =>
                    renderMetricRow(key, comparison[key] as MetricEntry)
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
