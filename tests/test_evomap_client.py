"""EvoMap client tests"""
import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.evomap.client import (
        create_novel_gene,
        create_novel_capsule,
        create_evolution_event,
        create_genes,
        EvoMapClient,
    )
    HAS_CLIENT = True
except ImportError as e:
    HAS_CLIENT = False
    print(f"Skipping evomap tests: {e}")


@pytest.mark.skipif(not HAS_CLIENT, reason="EvoMap client not importable")
def test_create_novel_gene():
    gene = create_novel_gene("都市", ["职场", "甜宠"], "生活流")
    assert gene["type"] == "Gene"
    assert gene["category"] == "都市"
    assert "asset_id" in gene


@pytest.mark.skipif(not HAS_CLIENT, reason="EvoMap client not importable")
def test_create_evolution_event_no_gene_error():
    """Regression test: create_evolution_event must not reference undefined 'gene' variable"""
    event = create_evolution_event("测试问题", "测试解决方案", True)
    assert event["type"] == "EvolutionEvent"
    assert "测试问题" in str(event.get("content", {}))


@pytest.mark.skipif(not HAS_CLIENT, reason="EvoMap client not importable")
def test_create_genes_returns_list():
    genes = create_genes()
    assert isinstance(genes, list)
    assert len(genes) > 0
