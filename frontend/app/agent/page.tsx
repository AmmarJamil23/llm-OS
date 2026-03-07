"use client";

import { useState } from "react";
import { runAgent, type AgentResponse } from "@/lib/api";

export default function AgentPage() {
  const [task, setTask] = useState("");
  const [result, setResult] = useState<AgentResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRun = async () => {
    if (!task.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await runAgent(task);
      setResult(res);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Agent run failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold text-white">Agent Reasoning</h1>

      <div className="bg-gray-900 rounded-lg border border-gray-800 p-5 space-y-3">
        <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Task</h2>
        <textarea
          className="w-full bg-gray-800 text-white rounded px-3 py-2 text-sm border border-gray-700 focus:outline-none focus:border-indigo-500 h-28 resize-none"
          placeholder="Describe your research task..."
          value={task}
          onChange={(e) => setTask(e.target.value)}
        />
        <button
          className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded text-sm transition-colors disabled:opacity-50"
          onClick={handleRun}
          disabled={loading}
        >
          {loading ? "Running agent..." : "Run Agent"}
        </button>
        {error && <p className="text-red-400 text-sm">{error}</p>}
      </div>

      {result && (
        <div className="space-y-4">
          {/* Result */}
          <div className="bg-gray-900 rounded-lg border border-indigo-800 p-5">
            <div className="flex justify-between items-start mb-2">
              <h2 className="text-sm font-semibold text-indigo-400 uppercase tracking-wider">Result</h2>
              <span className="text-xs text-gray-500">{result.latency_ms}ms</span>
            </div>
            <p className="text-gray-200 whitespace-pre-wrap text-sm leading-relaxed">{result.result}</p>
          </div>

          {/* Reasoning trace */}
          <div className="bg-gray-900 rounded-lg border border-gray-800 p-5 space-y-3">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Reasoning Trace</h2>
            <div className="space-y-2">
              {result.trace.map((step, i) => (
                <div key={i} className="flex gap-3">
                  <span className="shrink-0 text-xs font-mono bg-gray-800 text-indigo-400 px-2 py-1 rounded">
                    {step.node}
                  </span>
                  <p className="text-sm text-gray-300 leading-relaxed">{step.output}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
