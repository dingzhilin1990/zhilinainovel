"""API endpoint tests"""
import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.api.main import app
    from fastapi.testclient import TestClient
    HAS_API = True
except ImportError as e:
    HAS_API = False
    print(f"Skipping API tests: {e}")


@pytest.mark.skipif(not HAS_API, reason="API module not importable")
def test_read_root():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.skipif(not HAS_API, reason="API module not importable")
def test_docs_available():
    client = TestClient(app)
    response = client.get("/docs")
    assert response.status_code == 200
