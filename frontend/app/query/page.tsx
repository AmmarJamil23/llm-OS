"use client";

import { useState } from "react";
import { queryDocuments, ingestDocument, type QueryResult } from "@/lib/api";

export default function QueryPage() {
  const [query, setQuery] = useState("");
  const [k, setK] = useState(5);
  const [result, setResult] = useState<QueryResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Ingest state
  const [ingestPath, setIngestPath] = useState("");
  const [docType, setDocType] = useState("txt");
  const [ingestMsg, setIngestMsg] = useState("");

  const handleQuery = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError("");
    try {
      const res = await queryDocuments(query, k);
      setResult(res);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Query failed");
    } finally {
      setLoading(false);
    }
  };

  const handleIngest = async () => {
    if (!ingestPath.trim()) return;
    setIngestMsg("Ingesting...");
    try {
      const res = await ingestDocument({ source: ingestPath, doc_type: docType });
      setIngestMsg(`✓ Ingested ${res.chunk_count} chunks in ${res.latency_ms}ms`);
    } catch (e: unknown) {
      setIngestMsg(`Error: ${e instanceof Error ? e.message : "Ingestion failed"}`);
    }
  };

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold text-white">Semantic Search</h1>

      {/* Ingest panel */}
      <div className="bg-gray-900 rounded-lg border border-gray-800 p-5 space-y-3">
        <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Ingest Document</h2>
        <div className="flex gap-2">
          <input
            className="flex-1 bg-gray-800 text-white rounded px-3 py-2 text-sm border border-gray-700 focus:outline-none focus:border-indigo-500"
            placeholder="Absolute file path (e.g. /home/user/docs/paper.pdf)"
            value={ingestPath}
            onChange={(e) => setIngestPath(e.target.value)}
          />
          <select
            className="bg-gray-800 text-white rounded px-3 py-2 text-sm border border-gray-700"
            value={docType}
            onChange={(e) => setDocType(e.target.value)}
          >
            <option value="txt">TXT</option>
            <option value="md">MD</option>
            <option value="pdf">PDF</option>
          </select>
          <button
            className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded text-sm transition-colors"
            onClick={handleIngest}
          >
            Ingest
          </button>
        </div>
        {ingestMsg && <p className="text-sm text-gray-400">{ingestMsg}</p>}
      </div>

      {/* Query panel */}
      <div className="bg-gray-900 rounded-lg border border-gray-800 p-5 space-y-3">
        <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Query</h2>
        <div className="flex gap-2">
          <input
            className="flex-1 bg-gray-800 text-white rounded px-3 py-2 text-sm border border-gray-700 focus:outline-none focus:border-indigo-500"
            placeholder="Ask a question..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleQuery()}
          />
          <input
            type="number"
            min={1}
            max={20}
            className="w-16 bg-gray-800 text-white rounded px-3 py-2 text-sm border border-gray-700"
            value={k}
            onChange={(e) => setK(Number(e.target.value))}
            title="Top-K results"
          />
          <button
            className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded text-sm transition-colors disabled:opacity-50"
            onClick={handleQuery}
            disabled={loading}
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </div>
        {error && <p className="text-red-400 text-sm">{error}</p>}
      </div>

      {/* Results */}
      {result && (
        <div className="space-y-4">
          <div className="bg-gray-900 rounded-lg border border-indigo-800 p-5">
            <div className="flex justify-between items-start mb-2">
              <h2 className="text-sm font-semibold text-indigo-400 uppercase tracking-wider">Answer</h2>
              <span className="text-xs text-gray-500">{result.latency_ms}ms</span>
            </div>
            <p className="text-gray-200 whitespace-pre-wrap text-sm leading-relaxed">{result.answer}</p>
          </div>
          <div className="space-y-2">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Sources ({result.sources.length})</h2>
            {result.sources.map((src) => (
              <div key={src.chunk_id} className="bg-gray-900 rounded-lg border border-gray-800 p-4">
                <div className="flex justify-between items-start mb-1">
                  <span className="text-xs text-gray-500">{src.metadata?.filename as string ?? src.doc_id}</span>
                  <span className="text-xs text-indigo-400">score: {src.score}</span>
                </div>
                <p className="text-sm text-gray-300 line-clamp-4">{src.text}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
