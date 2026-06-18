import pytest

from main import Produto, SessionLocal


def test_listar_produtos_quando_banco_esta_vazio(client):
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == []


def test_criar_produto_e_verificar_persistencia_no_banco(client):
    payload = {
        "nome": "Teclado Mecânico",
        "preco": 350.0,
        "estoque": 10,
        "ativo": True,
    }

    response = client.post("/produtos", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] > 0
    assert data["nome"] == payload["nome"]
    assert data["preco"] == payload["preco"]
    assert data["estoque"] == payload["estoque"]
    assert data["ativo"] is True

    db = SessionLocal()
    try:
        produto_db = db.get(Produto, data["id"])
        assert produto_db is not None
        assert produto_db.nome == payload["nome"]
        assert produto_db.preco == payload["preco"]
        assert produto_db.estoque == payload["estoque"]
        assert produto_db.ativo is True
    finally:
        db.close()


def test_criar_produto_e_verificar_que_aparece_na_listagem(client):
    payload = {
        "nome": "Mouse Gamer",
        "preco": 199.9,
        "estoque": 7,
        "ativo": True,
    }

    response = client.post("/produtos", json=payload)
    assert response.status_code == 201
    produto_criado = response.json()

    response_list = client.get("/produtos")
    assert response_list.status_code == 200

    produtos = response_list.json()
    assert any(p["id"] == produto_criado["id"] for p in produtos)


def test_buscar_produto_por_id_com_sucesso(client, produto_existente):
    produto_id = produto_existente["id"]

    response = client.get(f"/produtos/{produto_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == produto_id
    assert data["nome"] == produto_existente["nome"]
    assert data["preco"] == produto_existente["preco"]
    assert data["estoque"] == produto_existente["estoque"]
    assert data["ativo"] == produto_existente["ativo"]


def test_buscar_produto_com_id_inexistente_retorna_404(client):
    response = client.get("/produtos/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"


def test_deletar_produto_retorna_204(client, produto_existente):
    produto_id = produto_existente["id"]

    response = client.delete(f"/produtos/{produto_id}")
    assert response.status_code == 204
    assert response.text == ""


def test_deletar_produto_e_confirmar_remocao_com_get_subsequente(client, produto_existente):
    produto_id = produto_existente["id"]

    response_delete = client.delete(f"/produtos/{produto_id}")
    assert response_delete.status_code == 204

    response_get = client.get(f"/produtos/{produto_id}")
    assert response_get.status_code == 404


def test_deletar_produto_inexistente_retorna_404(client):
    response = client.delete("/produtos/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"


@pytest.mark.parametrize(
    "payload",
    [
        {"nome": "", "preco": 100.0, "estoque": 1, "ativo": True},     # nome vazio
        {"nome": "Produto", "preco": 0, "estoque": 1, "ativo": True},  # preço zero
        {"nome": "Produto", "preco": -10.0, "estoque": 1, "ativo": True},  # preço negativo
        {"preco": 100.0, "estoque": 1, "ativo": True},                 # nome ausente
        {"nome": "Produto", "estoque": 1, "ativo": True},              # preco ausente
        {"nome": "Produto", "preco": 100.0, "estoque": -1, "ativo": True}, # estoque negativo
    ],
)
def test_payloads_invalidos_retorna_422(client, payload):
    response = client.post("/produtos", json=payload)
    assert response.status_code == 422


def test_banco_isolado_entre_execucoes(client):
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == []