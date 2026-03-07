from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.core.models import IngestRequest, IngestResponse
from backend.core.logging import get_logger
from backend.ingestion.pipeline import run_ingestion
from backend.retrieval.store import get_vector_store

logger = get_logger(__name__)
router = APIRouter()


@router.post("/ingest", response_model=IngestResponse, tags=["ingest"])
async def ingest_document(request: IngestRequest) -> IngestResponse:
    """Ingest a document into the vector store."""
    try:
        store = get_vector_store()
        return run_ingestion(request, store)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        logger.exception("Ingestion failed: %s", exc)
        raise HTTPException(status_code=500, detail="Ingestion failed. Check server logs.")
