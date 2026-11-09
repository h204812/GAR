from __future__ import annotations

import os
from typing import Sequence

from openai import OpenAI

# text-embedding-3-small default output size
DEFAULT_MODEL = "text-embedding-3-small"
DEFAULT_DIMS = 1536


class OpenAIEmbedder:
    def __init__(
        self,
        *,
        model: str = DEFAULT_MODEL,
        api_key: str | None = None,
        batch_size: int = 64,
    ) -> None:
        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self.client = OpenAI(api_key=key)
        self.model = model
        self.batch_size = batch_size
        self.dims = DEFAULT_DIMS

    def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors: list[list[float]] = []
        for start in range(0, len(texts), self.batch_size):
            batch = list(texts[start : start + self.batch_size])
            resp = self.client.embeddings.create(model=self.model, input=batch)
            # API returns data possibly out of order — sort by index
            ordered = sorted(resp.data, key=lambda d: d.index)
            vectors.extend([list(d.embedding) for d in ordered])
        return vectors

    def embed_query(self, text: str) -> list[float]:
        return self.embed_texts([text])[0]
