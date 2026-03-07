from __future__ import annotations

from pathlib import Path

from backend.core.models import Document
from backend.core.logging import get_logger

logger = get_logger(__name__)


def load_document(source: str, doc_type: str) -> Document:
    """Load a document from disk and return a Document object."""
    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    doc_type = doc_type.lower()

    if doc_type == "pdf":
        content = _load_pdf(path)
    elif doc_type in ("txt", "md"):
        content = _load_text(path)
    else:
        raise ValueError(f"Unsupported doc_type: {doc_type}. Use 'pdf', 'txt', or 'md'.")

    doc = Document(
        source=str(path.resolve()),
        content=content,
        metadata={"filename": path.name, "doc_type": doc_type},
    )
    logger.info("Loaded document id=%s source=%s chars=%d", doc.id, path.name, len(content))
    return doc


def _load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_pdf(path: Path) -> str:
    try:
        import PyPDF2
    except ImportError as exc:
        raise ImportError("PyPDF2 is required for PDF loading. Run: pip install PyPDF2") from exc

    pages: list[str] = []
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n".join(pages)
