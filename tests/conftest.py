import pytest
from starlette.testclient import TestClient

from app.main import app
from app.repository import estabulo_repository, equino_repository
from tests.constants import (
    CAPACIDADE_ESTABULO_10,
    DATA_NASCIMENTO_CAVALO,
    IDADE_CAVALO,
    LOCALIZACAO_ESTABULO,
    NOME_CAVALO,
    NOME_ESTABULO,
    PESO_CAVALO,
    RACA_CAVALO,
    RACA_INVALIDA,
    SEXO_CAVALO,
)


@pytest.fixture(autouse=True)
def resetar_estado_repositorio():
    """Garante isolamento entre testes limpando o repositorio em memoria."""
    estabulo_repository.limpar()
    equino_repository.limpar()
    yield
    estabulo_repository.limpar()
    equino_repository.limpar()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def payload_equino_valido() -> dict:
    """Fixture com payload padrao valido para criacao de equino."""
    return {
        "nome": NOME_CAVALO,
        "raca": RACA_CAVALO,
        "idade": IDADE_CAVALO,
        "peso": PESO_CAVALO,
        "sexo": SEXO_CAVALO,
        "data_nascimento": DATA_NASCIMENTO_CAVALO,
    }


@pytest.fixture
def payload_equino__raca_invalida(payload_equino_valido: dict) -> dict:
    """Fixture com raça inválida e os demais campos válidos."""
    return {**payload_equino_valido, "raca": RACA_INVALIDA}


@pytest.fixture
def payload_estabulo_valido() -> dict:
    """Fixture com payload padrao valido para criacao de estabulo."""
    return {
        "nome_identificador": NOME_ESTABULO,
        "localizacao": LOCALIZACAO_ESTABULO,
        "capacidade": CAPACIDADE_ESTABULO_10,
    }
