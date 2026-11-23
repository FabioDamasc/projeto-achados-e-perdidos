import pytest
from fastapi.testclient import TestClient

from main import app, resetar_banco

client = TestClient(app)


@pytest.fixture(autouse=True)
def limpar_estado():
    """Garante que cada teste comece com o banco limpo e não dependa da ordem de execução."""
    resetar_banco()
    yield
    resetar_banco()


def test_01_listagem_de_objetos():
    """Teste 01: Verifica se GET /objetos retorna 200 e uma coleção (lista) de objetos."""
    client.post("/objetos", json={"descricao": "Chave de carro", "local": "Estacionamento"})

    response = client.get("/objetos")

    assert response.status_code == 200
    dados = response.json()
    assert isinstance(dados, list)
    assert len(dados) == 1
    assert dados[0]["descricao"] == "Chave de carro"


def test_02_consulta_de_objeto_existente():
    """Teste 02: Consulta um objeto previamente cadastrado pelo ID e valida seus dados."""
    cadastro = client.post(
        "/objetos",
        json={"descricao": "Celular Samsung", "local": "Biblioteca"},
    )
    objeto_criado = cadastro.json()
    objeto_id = objeto_criado["id"]

    response = client.get(f"/objetos/{objeto_id}")

    assert response.status_code == 200
    dados = response.json()
    assert dados["id"] == objeto_id
    assert dados["descricao"] == "Celular Samsung"
    assert dados["local"] == "Biblioteca"


def test_03_consulta_de_objeto_inexistente():
    """Teste 03: Consulta um ID inexistente e confirma retorno 404 Not Found."""
    response = client.get("/objetos/9999")

    assert response.status_code == 404
    assert "detail" in response.json()


def test_04_cadastro_valido():
    """Teste 04: Cadastra um objeto válido e verifica status 201 Created e dados retornados."""
    payload = {
        "descricao": "Carregador de notebook",
        "local": "Laboratório 02",
    }

    response = client.post("/objetos", json=payload)

    assert response.status_code == 201
    dados = response.json()
    assert isinstance(dados["id"], int)
    assert dados["descricao"] == payload["descricao"]
    assert dados["local"] == payload["local"]


def test_05_cadastro_com_informacoes_incompletas():
    """Teste 05: Tenta cadastrar sem o campo obrigatório 'descricao' e espera 422."""
    payload_incompleto = {
        "local": "Laboratório 02",
    }

    response = client.post("/objetos", json=payload_incompleto)

    assert response.status_code == 422


def test_06_parametro_invalido():
    """Teste 06: Consulta usando texto no lugar de inteiro no ID e espera 422."""
    response = client.get("/objetos/abc")

    assert response.status_code == 422
