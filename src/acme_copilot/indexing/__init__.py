"""Phase 1 indexing: load → chunk → embed → Qdrant."""

from acme_copilot.indexing.pipeline import index_corpus, search_corpus

__all__ = ["index_corpus", "search_corpus"]
