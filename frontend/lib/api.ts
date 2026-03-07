const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "API error");
  }
  return res.json() as Promise<T>;
}

// ---- Health ---------------------------------------------------------------
export const getHealth = () => request<{ status: string; ollama: string }>("/health");

// ---- Ingest ---------------------------------------------------------------
export interface IngestRequest { source: string; doc_type: string }
export interface IngestResponse { doc_id: string; chunk_count: number; latency_ms: number }
export const ingestDocument = (body: IngestRequest) =>
  request<IngestResponse>("/api/ingest", { method: "POST", body: JSON.stringify(body) });

// ---- Query ----------------------------------------------------------------
export interface Source { text: string; score: number; metadata: Record<string, unknown>; chunk_id: string; doc_id: string }
export interface QueryResult { query: string; answer: string; sources: Source[]; latency_ms: number }
export const queryDocuments = (query: string, k = 5) =>
  request<QueryResult>("/api/query", { method: "POST", body: JSON.stringify({ query, k }) });

// ---- Agent ----------------------------------------------------------------
export interface AgentResponse { result: string; trace: { node: string; output: string }[]; latency_ms: number }
export const runAgent = (task: string) =>
  request<AgentResponse>("/api/agent/run", { method: "POST", body: JSON.stringify({ task }) });

// ---- Evaluation -----------------------------------------------------------
export interface EvalResult { question: string; answer: string; ground_truth: string; recall_at_k: number; mrr: number; latency_ms: number }
export const startEvaluation = (dataset_path: string, k = 5) =>
  request<{ job_id: string }>("/api/eval/run", { method: "POST", body: JSON.stringify({ dataset_path, k }) });
export const getEvalResults = (job_id: string) =>
  request<EvalResult[]>(`/api/eval/results/${job_id}`);

// ---- Experiments ----------------------------------------------------------
export interface ExperimentConfig {
  name: string; embedding_model: string; chunk_size: number;
  chunk_overlap: number; retrieval_k: number; ollama_model: string; notes: string;
}
export interface Experiment { id: string; config: ExperimentConfig; results: EvalResult[]; avg_recall: number; avg_mrr: number; avg_latency_ms: number }
export const listExperiments = () => request<Experiment[]>("/api/experiments");
export const getExperiment = (id: string) => request<Experiment>(`/api/experiments/${id}`);
export const compareExperiments = (a: string, b: string) =>
  request<Record<string, unknown>>("/api/experiments/compare", {
    method: "POST",
    body: JSON.stringify({ experiment_a_id: a, experiment_b_id: b }),
  });
