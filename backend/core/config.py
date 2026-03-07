from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # LLM
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:3b-instruct"

    # Embeddings
    embedding_model: str = "all-MiniLM-L6-v2"

    # Vector store
    vector_store_type: str = "faiss"
    faiss_index_path: str = "data/indices/main.index"

    # Ingestion
    chunk_size: int = 500
    chunk_overlap: int = 50

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
