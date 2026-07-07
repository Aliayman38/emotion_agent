import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.tools import normalize_arabic_text

client = TestClient(app)

def test_arabic_text_normalization():
    """Tests the standalone isolation regex rule cleaning functions."""
    raw_text = "والله اليوووم مبسووطووون كّثيييراً!!! "
    normalized = normalize_arabic_text(raw_text)
    
    # Ensure repeated letters are reduced and punctuation/harakat stripped
    assert "ّ" not in normalized
    assert "اً" not in normalized
    assert "!!!" not in normalized

def test_api_health_check_endpoint():
    """Asserts that health parameters remain reachable."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"

def test_api_validation_error_on_empty_payload():
    """Ensures input layer handles empty arrays or fields correctly."""
    response = client.post("/predict", json={"text": "   "})
    assert response.status_code == 422