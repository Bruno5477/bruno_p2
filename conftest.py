import os

import pytest
from fastapi.testclient import TestClient

# Garante que os testes usem o banco de teste no PostgreSQL via Docker
os.environ["DATABASE_URL"] = "postgresql+psycopg2://postgres:postgres@localhost:5433/produtos_db_test"

from main import Base, SessionLocal, app, engine, get_db  # noqa: E402


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def produto_existente(client):
    payload = {
        "nome": "Notebook Gamer",
        "preco": 4999.90,
        "estoque": 5,
        "ativo": True,
    }
    response = client.post("/produtos", json=payload)
    assert response.status_code == 201
    return response.json()