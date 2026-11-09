from pathlib import Path

from acme_copilot.indexing.chunker import chunk_documents
from acme_copilot.indexing.loader import load_corpus

ROOT = Path(__file__).resolve().parents[1]


def test_load_corpus_has_frontmatter():
    docs = load_corpus(ROOT / "data" / "corpus")
    assert len(docs) >= 45
    pto = next(d for d in docs if d.doc_id == "pto-policy")
    assert pto.metadata.get("doc_type") == "policy"
    assert "25 days" in pto.body


def test_chunks_copy_metadata():
    docs = load_corpus(ROOT / "data" / "corpus")
    chunks = chunk_documents(docs, chunk_size=400, chunk_overlap=50)
    assert len(chunks) >= len(docs)
    sample = next(c for c in chunks if c.metadata.get("doc_id") == "pto-policy")
    assert sample.metadata["doc_type"] == "policy"
    assert "chunk_index" in sample.metadata
    assert sample.text.strip()
