from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter

from acme_copilot.indexing.loader import CorpusDocument


@dataclass
class TextChunk:
    chunk_id: str
    text: str
    metadata: dict[str, Any]
    chunk_index: int


def chunk_documents(
    docs: list[CorpusDocument],
    *,
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> list[TextChunk]:
    """Split document bodies; copy frontmatter onto every chunk payload."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )
    chunks: list[TextChunk] = []
    for doc in docs:
        pieces = splitter.split_text(doc.body)
        for i, text in enumerate(pieces):
            meta = {
                **doc.metadata,
                "doc_id": doc.doc_id,
                "source_path": str(doc.path),
                "chunk_index": i,
                "chunk_count": len(pieces),
            }
            chunk_id = f"{doc.doc_id}::{i}"
            chunks.append(
                TextChunk(
                    chunk_id=chunk_id,
                    text=text,
                    metadata=meta,
                    chunk_index=i,
                )
            )
    return chunks
