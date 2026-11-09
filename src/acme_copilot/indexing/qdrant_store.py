from __future__ import annotations

import hashlib
import uuid
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

from acme_copilot.indexing.chunker import TextChunk
from acme_copilot.indexing.embeddings import DEFAULT_DIMS


DEFAULT_COLLECTION = "acme_chunks"


def _point_id(chunk_id: str) -> str:
    """Stable UUID from chunk_id for idempotent re-indexing."""
    digest = hashlib.sha256(chunk_id.encode("utf-8")).hexdigest()
    return str(uuid.UUID(digest[:32]))


class QdrantChunkStore:
    def __init__(
        self,
        *,
        url: str = "http://localhost:6333",
        collection: str = DEFAULT_COLLECTION,
        vector_size: int = DEFAULT_DIMS,
    ) -> None:
        self.client = QdrantClient(url=url, check_compatibility=False)
        self.collection = collection
        self.vector_size = vector_size

    def recreate_collection(self) -> None:
        # Prefer delete+create for broad client compatibility
        names = {c.name for c in self.client.get_collections().collections}
        if self.collection in names:
            self.client.delete_collection(self.collection)
        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=qm.VectorParams(
                size=self.vector_size,
                distance=qm.Distance.COSINE,
            ),
        )

    def ensure_collection(self) -> None:
        names = {c.name for c in self.client.get_collections().collections}
        if self.collection not in names:
            self.recreate_collection()

    def upsert_chunks(
        self,
        chunks: list[TextChunk],
        vectors: list[list[float]],
        *,
        batch_size: int = 64,
    ) -> int:
        if len(chunks) != len(vectors):
            raise ValueError("chunks and vectors length mismatch")
        self.ensure_collection()
        total = 0
        for start in range(0, len(chunks), batch_size):
            batch_chunks = chunks[start : start + batch_size]
            batch_vecs = vectors[start : start + batch_size]
            points = [
                qm.PointStruct(
                    id=_point_id(ch.chunk_id),
                    vector=vec,
                    payload={
                        "chunk_id": ch.chunk_id,
                        "text": ch.text,
                        **_json_safe(ch.metadata),
                    },
                )
                for ch, vec in zip(batch_chunks, batch_vecs, strict=True)
            ]
            self.client.upsert(collection_name=self.collection, points=points)
            total += len(points)
        return total

    def count(self) -> int:
        info = self.client.count(self.collection, exact=True)
        return int(info.count)

    def search(
        self,
        query_vector: list[float],
        *,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        # qdrant-client >=1.14 uses query_points; older used .search
        if hasattr(self.client, "query_points"):
            response = self.client.query_points(
                collection_name=self.collection,
                query=query_vector,
                limit=limit,
                with_payload=True,
            )
            hits = response.points
        else:
            hits = self.client.search(
                collection_name=self.collection,
                query_vector=query_vector,
                limit=limit,
                with_payload=True,
            )
        results: list[dict[str, Any]] = []
        for hit in hits:
            payload = hit.payload or {}
            results.append(
                {
                    "score": float(hit.score),
                    "chunk_id": payload.get("chunk_id"),
                    "doc_id": payload.get("doc_id"),
                    "text": payload.get("text"),
                    "payload": payload,
                }
            )
        return results


def _json_safe(meta: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in meta.items():
        if v is None or isinstance(v, (str, int, float, bool)):
            out[k] = v
        else:
            out[k] = str(v)
    return out
