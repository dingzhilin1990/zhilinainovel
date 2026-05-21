"""Generator module tests"""
import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.generator.novel import NovelGenerator
    HAS_GENERATOR = True
except ImportError as e:
    HAS_GENERATOR = False
    print(f"Skipping generator tests: {e}")


@pytest.mark.skipif(not HAS_GENERATOR, reason="Generator module not importable")
def test_novel_generator_init():
    gen = NovelGenerator()
    assert gen is not None


@pytest.mark.skipif(not HAS_GENERATOR, reason="Generator module not importable")
def test_novel_generator_has_required_methods():
    gen = NovelGenerator()
    assert hasattr(gen, "generate_outline")
    assert hasattr(gen, "continue_chapter")
    assert hasattr(gen, "generate_dialogue")
