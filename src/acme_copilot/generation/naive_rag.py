from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

from openai import OpenAI

from acme_copilot.indexing.pipeline import search_corpus
from acme_copilot.indexing.qdrant_store import DEFAULT_COLLECTION

DEFAULT_CHAT_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are Acme Knowledge Copilot.
Answer ONLY using the provided context chunks from the company knowledge base.
If the context is insufficient, say you do not know based on the available documents.
Cite source doc_id values in square brackets, e.g. [pto-policy].
Be concise and factual."""


@dataclass
class RagAnswer:
    question: str
    answer: str
    citations: list[str] = field(default_factory=list)
    contexts: list[dict[str, Any]] = field(default_factory=list)
    model: str = DEFAULT_CHAT_MODEL
    top_k: int = 5
    collection: str = DEFAULT_COLLECTION


def _format_context(hits: list[dict[str, Any]]) -> str:
    blocks: list[str] = []
    for i, hit in enumerate(hits, start=1):
        doc_id = hit.get("doc_id") or "unknown"
        score = hit.get("score")
        text = (hit.get("text") or "").strip()
        blocks.append(
            f"[{i}] doc_id={doc_id} score={score:.4f}\n{text}"
        )
    return "\n\n".join(blocks)


def ask(
    question: str,
    *,
    top_k: int = 5,
    collection: str = DEFAULT_COLLECTION,
    model: str | None = None,
    api_key: str | None = None,
) -> RagAnswer:
    """Naive RAG: embed question → cosine top-k in Qdrant → LLM answer.

    Phase 2 scope:
    - Similarity: dense cosine over acme_chunks
    - Stores: Qdrant only (no Postgres / Neo4j)
    - No query translation (multi-query, HyDE, etc.)
    """
    chat_model = model or os.environ.get("OPENAI_CHAT_MODEL", DEFAULT_CHAT_MODEL)
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    hits = search_corpus(question, collection=collection, limit=top_k)
    context = _format_context(hits)
    citations = []
    for hit in hits:
        doc_id = hit.get("doc_id")
        if doc_id and doc_id not in citations:
            citations.append(str(doc_id))

    client = OpenAI(api_key=key)
    user_prompt = (
        f"Question:\n{question}\n\n"
        f"Context chunks:\n{context}\n\n"
        "Answer:"
    )
    resp = client.chat.completions.create(
        model=chat_model,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    answer = (resp.choices[0].message.content or "").strip()

    return RagAnswer(
        question=question,
        answer=answer,
        citations=citations,
        contexts=hits,
        model=chat_model,
        top_k=top_k,
        collection=collection,
    )
