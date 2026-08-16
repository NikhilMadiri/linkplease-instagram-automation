"""Basic smoke tests for the phase-one system endpoints."""

from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    """The liveness endpoint should not require a database connection."""
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.json() == {"status": "healthy"}
