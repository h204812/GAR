from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from acme_copilot.indexing.chunker import chunk_documents
from acme_copilot.indexing.embeddings import OpenAIEmbedder
from acme_copilot.indexing.loader import load_corpus
from acme_copilot.indexing.qdrant_store import DEFAULT_COLLECTION, QdrantChunkStore


def index_corpus(
    corpus_dir: Path,
    *,
    qdrant_url: str | None = None,
    collection: str = DEFAULT_COLLECTION,
    chunk_size: int = 800,
    chunk_overlap: int = 120,
    recreate: bool = True,
) -> dict[str, Any]:
    """Load → chunk → embed → upsert. Returns a summary dict."""
    url = qdrant_url or os.environ.get("QDRANT_URL", "http://localhost:6333")
    docs = load_corpus(corpus_dir)
    chunks = chunk_documents(
        docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    embedder = OpenAIEmbedder()
    vectors = embedder.embed_texts([c.text for c in chunks])

    store = QdrantChunkStore(url=url, collection=collection, vector_size=embedder.dims)
    if recreate:
        store.recreate_collection()
    upserted = store.upsert_chunks(chunks, vectors)

    return {
        "documents": len(docs),
        "chunks": len(chunks),
        "upserted": upserted,
        "collection": collection,
        "qdrant_url": url,
        "embedding_model": embedder.model,
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
    }


def search_corpus(
    query: str,
    *,
    qdrant_url: str | None = None,
    collection: str = DEFAULT_COLLECTION,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Embed query and run cosine similarity search (payload returned, not filtered)."""
    url = qdrant_url or os.environ.get("QDRANT_URL", "http://localhost:6333")
    embedder = OpenAIEmbedder()
    store = QdrantChunkStore(url=url, collection=collection, vector_size=embedder.dims)
    vector = embedder.embed_query(query)
    return store.search(vector, limit=limit)
