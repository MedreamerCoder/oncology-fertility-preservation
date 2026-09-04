"""Provider-neutral reference components reconstructed from the manuscript.

This module is intentionally not presented as the production YuHub pipeline. It
captures inspectable orchestration primitives that can be tested without API
keys or clinical data while the exact Dify export remains an author-supplied
artifact.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, Sequence


@dataclass(frozen=True)
class RetrievedEvidence:
    path: str
    document_id: str
    text: str
    source_title: str
    source_url: str | None
    version: str | None
    retrieval_score: float
    rerank_score: float | None = None
    metadata: dict[str, str] = field(default_factory=dict)


class Retriever(Protocol):
    def search(self, query: str, path: str, top_k: int) -> Sequence[RetrievedEvidence]: ...


class Reranker(Protocol):
    def rerank(
        self, query: str, evidence: Sequence[RetrievedEvidence], top_k: int
    ) -> Sequence[RetrievedEvidence]: ...


def regional_legal_query(question: str, country: str) -> str:
    normalized = country.strip()
    if normalized.casefold() in {"china", "cn", "中国", "中华人民共和国"}:
        return f"{question} 人类辅助生殖技术规范 法律 伦理"
    return f"{question} {normalized} fertility preservation law regulation ethics"


def build_parallel_queries(question: str, country: str) -> dict[str, str]:
    return {
        "tumour_treatment": f"oncology treatment gonadotoxicity timing: {question}",
        "fertility_preservation": f"fertility preservation guideline options: {question}",
        "legal_regulation": regional_legal_query(question, country),
    }


def retrieve_with_provenance(
    question: str,
    country: str,
    retriever: Retriever,
    reranker: Reranker,
    per_path_top_k: int = 8,
    final_top_k: int = 10,
) -> list[RetrievedEvidence]:
    candidates: list[RetrievedEvidence] = []
    for path, query in build_parallel_queries(question, country).items():
        candidates.extend(retriever.search(query=query, path=path, top_k=per_path_top_k))
    deduplicated: dict[tuple[str, str], RetrievedEvidence] = {}
    for item in candidates:
        key = (item.document_id, item.text)
        previous = deduplicated.get(key)
        if previous is None or item.retrieval_score > previous.retrieval_score:
            deduplicated[key] = item
    ranked = reranker.rerank(question, list(deduplicated.values()), final_top_k)
    return list(ranked)[:final_top_k]
