import pytest
from starlette.testclient import TestClient
from app.repository import repositorio_estabulo, repositorio_equino
from app.main import app


@pytest.fixture(autouse=True)
def resetar_estado_repositorio():
    """Garante isolamento entre testes limpando o repositorio em memoria."""
    repositorio_estabulo.limpar()
    yield
    repositorio_equino.limpar()


@pytest.fixture(autouse=True)
def test_client():
    return TestClient(app)


@pytest.fixture
def payload_equino_valido() -> dict:
    """Fixture com payload padrao valido para criacao de equino."""
    return {
        "nome": "Relâmpago",
        "raca": "Mangalarga",
        "idade": 5,
        "peso": 450.0
    }

@pytest.fixture
def payload_estabulo_valido() -> dict:
    """Fixture com payload padrao valido para criacao de estabulo."""
    return {
        "nome_identificador": "Estábulo Central",
        "localizacao": "Fazenda Verde",
        "capacidade": 10
    }