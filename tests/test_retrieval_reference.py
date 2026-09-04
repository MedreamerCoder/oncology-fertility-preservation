from repro.retrieval_reference import build_parallel_queries, regional_legal_query


def test_china_legal_query_uses_disclosed_specification_terms():
    query = regional_legal_query("卵子冷冻", "中国")
    assert "人类辅助生殖技术规范" in query


def test_three_parallel_paths_are_defined():
    assert set(build_parallel_queries("question", "France")) == {
        "tumour_treatment",
        "fertility_preservation",
        "legal_regulation",
    }
