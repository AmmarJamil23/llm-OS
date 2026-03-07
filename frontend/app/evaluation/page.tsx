"use client";

import { useState } from "react";
import { startEvaluation, getEvalResults, type EvalResult } from "@/lib/api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

export default function EvaluationPage() {
  const [datasetPath, setDatasetPath] = useState("");
  const [k, setK] = useState(5);
  const [jobId, setJobId] = useState("");
  const [results, setResults] = useState<EvalResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRun = async () => {
    if (!datasetPath.trim()) return;
    setLoading(true);
    setError("");
    setResults([]);
    try {
      const { job_id } = await startEvaluation(datasetPath, k);
      setJobId(job_id);
      const res = await getEvalResults(job_id);
      setResults(res);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Evaluation failed");
    } finally {
      setLoading(false);
    }
  };

  const avgRecall = results.length ? (results.reduce((s, r) => s + r.recall_at_k, 0) / results.length).toFixed(3) : "—";
  const avgMrr = results.length ? (results.reduce((s, r) => s + r.mrr, 0) / results.length).toFixed(3) : "—";
  const avgLatency = results.length ? (results.reduce((s, r) => s + r.latency_ms, 0) / results.length).toFixed(1) : "—";

  const chartData = results.map((r, i) => ({
    name: `Q${i + 1}`,
    recall: r.recall_at_k,
    mrr: r.mrr,
  }));

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold text-white">Evaluation</h1>

      <div className="bg-gray-900 rounded-lg border border-gray-800 p-5 space-y-3">
        <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Run Evaluation</h2>
        <div className="flex gap-2">
          <input
            className="flex-1 bg-gray-800 text-white rounded px-3 py-2 text-sm border border-gray-700 focus:outline-none focus:border-indigo-500"
            placeholder="Dataset path (JSON or CSV)"
            value={datasetPath}
            onChange={(e) => setDatasetPath(e.target.value)}
          />
          <input
            type="number"
            min={1}
            max={20}
            className="w-16 bg-gray-800 text-white rounded px-3 py-2 text-sm border border-gray-700"
            value={k}
            onChange={(e) => setK(Number(e.target.value))}
            title="Top-K"
          />
          <button
            className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded text-sm transition-colors disabled:opacity-50"
            onClick={handleRun}
            disabled={loading}
          >
            {loading ? "Running..." : "Run"}
          </button>
        </div>
        {error && <p className="text-red-400 text-sm">{error}</p>}
        {jobId && <p className="text-xs text-gray-500">Job ID: {jobId}</p>}
      </div>

      {results.length > 0 && (
        <>
          {/* Summary cards */}
          <div className="grid grid-cols-3 gap-4">
            {[
              { label: "Avg Recall@K", value: avgRecall },
              { label: "Avg MRR", value: avgMrr },
              { label: "Avg Latency (ms)", value: avgLatency },
            ].map((m) => (
              <div key={m.label} className="bg-gray-900 rounded-lg border border-gray-800 p-4 text-center">
                <p className="text-2xl font-bold text-indigo-400">{m.value}</p>
                <p className="text-xs text-gray-400 mt-1">{m.label}</p>
              </div>
            ))}
          </div>

          {/* Chart */}
          <div className="bg-gray-900 rounded-lg border border-gray-800 p-5">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-4">Per-Question Metrics</h2>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="name" tick={{ fill: "#9ca3af", fontSize: 11 }} />
                <YAxis domain={[0, 1]} tick={{ fill: "#9ca3af", fontSize: 11 }} />
                <Tooltip contentStyle={{ background: "#111827", border: "1px solid #374151" }} />
                <Bar dataKey="recall" name="Recall@K" fill="#6366f1" radius={[3, 3, 0, 0]} />
                <Bar dataKey="mrr" name="MRR" fill="#10b981" radius={[3, 3, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Table */}
          <div className="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-gray-800 text-gray-400 text-xs uppercase">
                <tr>
                  {["Question", "Recall@K", "MRR", "Latency (ms)"].map((h) => (
                    <th key={h} className="px-4 py-3 text-left">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {results.map((r, i) => (
                  <tr key={i} className="border-t border-gray-800 hover:bg-gray-800/50">
                    <td className="px-4 py-3 text-gray-300 max-w-xs truncate" title={r.question}>{r.question}</td>
                    <td className="px-4 py-3 text-indigo-400">{r.recall_at_k.toFixed(3)}</td>
                    <td className="px-4 py-3 text-emerald-400">{r.mrr.toFixed(3)}</td>
                    <td className="px-4 py-3 text-gray-400">{r.latency_ms}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}
