import pytest
from starlette.testclient import TestClient

from app.main import service
from app.repository import estabulo_repository
from tests.constants import (
    CAPACIDADE_INVALIDA,
    CAPACIDADE_ESTABULO_10,
    CAPACIDADE_ESTABULO_MINIMA,
    ERRO_SERVICO_SIMULADO,
    ID_INEXISTENTE,
    IDADE_CAVALO,
    IDADE_ACIMA_DA_MINIMA,
    IDADE_INVALIDA,
    IDADE_MINIMA_PERMITIDA,
    NOME_CAVALO,
    NOME_COM_200_CARACTERES,
    NOME_COM_201_CARACTERES,
    NOME_COM_UM_CARACTERE,
    PESO_CAVALO,
    RACA_CAVALO,
    RACA_CAVALO_MINUSCULA,
    ROTA_ESTABULOS,
    ROTA_EQUINOS,
    ROTA_HEALTH,
    STATUS_CRIADO,
    STATUS_ERRO_REGRA,
    STATUS_ERRO_VALIDACAO,
    STATUS_OK,
    SEXO_INVALIDO,
    TEXTO_VAZIO,
)


def criar_equino(client: TestClient, payload: dict) -> str:
    response = client.post(ROTA_EQUINOS, json=payload)
    assert response.status_code == STATUS_CRIADO
    return response.json()["id"]


def criar_estabulo(client: TestClient, payload: dict) -> str:
    response = client.post(ROTA_ESTABULOS, json=payload)
    assert response.status_code == STATUS_CRIADO
    return response.json()["id"]


def associar_equino(client: TestClient, equino_id: str, estabulo_id: str):
    return client.post(f"{ROTA_EQUINOS}/{equino_id}/estabulo/{estabulo_id}")


@pytest.mark.integration
def test_criar_equino_com_sucesso(client: TestClient, payload_equino_valido: dict):
    """Testa o fluxo completo de criação de equino com sucesso."""

    # Act: Disparar requisição HTTP POST
    response = client.post(ROTA_EQUINOS, json=payload_equino_valido)

    # Assert: Validar contrato e persistencia
    assert response.status_code == STATUS_CRIADO
    dados = response.json()
    assert dados["nome"] == NOME_CAVALO
    assert dados["raca"] == RACA_CAVALO
    assert dados["idade"] == IDADE_CAVALO
    assert dados["peso"] == PESO_CAVALO

    # Validação de persistência via listagem de equinos
    equino_id = dados["id"]
    get_response = client.get(ROTA_EQUINOS)
    assert get_response.status_code == STATUS_OK
    equino_salvo = next(
        equino for equino in get_response.json() if equino["id"] == equino_id
    )
    assert equino_salvo["id"] == equino_id
    assert equino_salvo["nome"] == NOME_CAVALO


@pytest.mark.integration
def test_criar_equino_com_raca_invalida(
    client: TestClient, payload_equino__raca_invalida: dict
):
    """Testa o fluxo de criação de equino com raça inválida."""

    # Act: Disparar requisição HTTP POST
    response = client.post(ROTA_EQUINOS, json=payload_equino__raca_invalida)

    # Assert: Validar contrato e persistencia
    assert response.status_code == STATUS_ERRO_REGRA
    dados = response.json()
    assert "raça inválida" in dados["detail"].lower()
    assert client.get(ROTA_EQUINOS).json() == []


@pytest.mark.integration
def test_criar_estabulo_com_sucesso(client: TestClient, payload_estabulo_valido: dict):
    """Testa o fluxo completo de criação de estábulo com sucesso."""

    # Act: Disparar requisição HTTP POST
    response = client.post(ROTA_ESTABULOS, json=payload_estabulo_valido)

    # Assert: Validar contrato e persistencia
    assert response.status_code == STATUS_CRIADO
    dados = response.json()
    assert dados["nome_identificador"] == payload_estabulo_valido["nome_identificador"]
    assert dados["localizacao"] == payload_estabulo_valido["localizacao"]
    assert dados["capacidade"] == payload_estabulo_valido["capacidade"]

    # Validação de persistência via listagem de estábulos
    get_response = client.get(ROTA_ESTABULOS)
    assert get_response.status_code == STATUS_OK
    estabulo_salvo = next(
        estabulo
        for estabulo in get_response.json()
        if estabulo["nome_identificador"]
        == payload_estabulo_valido["nome_identificador"]
    )
    assert (
        estabulo_salvo["nome_identificador"]
        == payload_estabulo_valido["nome_identificador"]
    )


@pytest.mark.integration
def test_associar_equino_estabulo_com_sucesso(
    client: TestClient, payload_equino_valido: dict, payload_estabulo_valido: dict
):
    """Testa o fluxo completo de associação de equino a estábulo com sucesso."""

    # Arrange: Criar equino e estabulo
    equino_id = criar_equino(client, payload_equino_valido)
    estabulo_id = criar_estabulo(client, payload_estabulo_valido)
    # Act: Disparar requisição HTTP POST para associar equino ao estábulo
    response = associar_equino(client, equino_id, estabulo_id)

    # Assert: Validar contrato e persistencia
    assert response.status_code == STATUS_OK
    dados = response.json()
    assert f"Equino {equino_id} associado ao estábulo {estabulo_id}" in dados["message"]

    # Validação de persistência via listagem de estábulos
    get_response = client.get(ROTA_ESTABULOS)
    assert get_response.status_code == STATUS_OK
    estabulo_salvo = next(
        estabulo
        for estabulo in get_response.json()
        if estabulo["nome_identificador"]
        == payload_estabulo_valido["nome_identificador"]
    )
    ids_dos_equinos = [equino["id"] for equino in estabulo_salvo["equinos"]]
    assert equino_id in ids_dos_equinos


@pytest.mark.integration
@pytest.mark.parametrize(
    "capacidade", [CAPACIDADE_ESTABULO_MINIMA, CAPACIDADE_ESTABULO_10]
)
def test_estabulo_aceita_quantidade_exata_de_equinos(
    client: TestClient,
    payload_equino_valido: dict,
    payload_estabulo_valido: dict,
    capacidade: int,
):
    # Arrange
    estabulo_id = criar_estabulo(
        client, {**payload_estabulo_valido, "capacidade": capacidade}
    )

    # Act
    ids_associados = []
    for _ in range(capacidade):
        equino_id = criar_equino(client, payload_equino_valido)
        response = associar_equino(client, equino_id, estabulo_id)
        assert response.status_code == STATUS_OK
        ids_associados.append(equino_id)

    # Assert: a capacidade exata é aceita e o repositório mantém IDs em texto.
    estabulo_persistido = estabulo_repository.obter_estabulo_por_id(estabulo_id)
    assert estabulo_persistido.equinos == ids_associados
    listagem = client.get(ROTA_ESTABULOS)
    assert listagem.status_code == STATUS_OK
    assert [equino["id"] for equino in listagem.json()[0]["equinos"]] == ids_associados


@pytest.mark.integration
@pytest.mark.parametrize(
    "capacidade", [CAPACIDADE_ESTABULO_MINIMA, CAPACIDADE_ESTABULO_10]
)
def test_estabulo_lotado_recusa_mais_um_equino_sem_alterar_associacoes(
    client: TestClient,
    payload_equino_valido: dict,
    payload_estabulo_valido: dict,
    capacidade: int,
):
    # Arrange
    estabulo_id = criar_estabulo(
        client, {**payload_estabulo_valido, "capacidade": capacidade}
    )
    ids_associados = []
    for _ in range(capacidade):
        equino_id = criar_equino(client, payload_equino_valido)
        assert associar_equino(client, equino_id, estabulo_id).status_code == STATUS_OK
        ids_associados.append(equino_id)
    equino_excedente_id = criar_equino(client, payload_equino_valido)

    # Act
    response = associar_equino(client, equino_excedente_id, estabulo_id)

    # Assert: criar outro equino é permitido; associá-lo ao estábulo lotado, não.
    assert response.status_code == STATUS_ERRO_REGRA
    assert "capacidade máxima" in response.json()["detail"]
    estabulo_persistido = estabulo_repository.obter_estabulo_por_id(estabulo_id)
    assert estabulo_persistido.equinos == ids_associados
    listagem = client.get(ROTA_ESTABULOS)
    assert listagem.status_code == STATUS_OK
    assert [equino["id"] for equino in listagem.json()[0]["equinos"]] == ids_associados
    assert equino_excedente_id in [
        equino["id"] for equino in client.get(ROTA_EQUINOS).json()
    ]


@pytest.mark.integration
def test_associacao_repetida_e_recusada_sem_duplicar_id(
    client: TestClient, payload_equino_valido: dict, payload_estabulo_valido: dict
):
    # Arrange
    estabulo_id = criar_estabulo(client, payload_estabulo_valido)
    equino_id = criar_equino(client, payload_equino_valido)
    assert associar_equino(client, equino_id, estabulo_id).status_code == STATUS_OK

    # Act
    response = associar_equino(client, equino_id, estabulo_id)

    # Assert
    assert response.status_code == STATUS_ERRO_REGRA
    assert "já está associado" in response.json()["detail"]
    assert estabulo_repository.obter_estabulo_por_id(estabulo_id).equinos == [equino_id]


@pytest.mark.integration
@pytest.mark.parametrize("entidade_ausente", ["equino", "estabulo"])
def test_associacao_recusa_referencia_inexistente(
    client: TestClient,
    payload_equino_valido: dict,
    payload_estabulo_valido: dict,
    entidade_ausente: str,
):
    # Arrange
    equino_id = criar_equino(client, payload_equino_valido)
    estabulo_id = criar_estabulo(client, payload_estabulo_valido)
    if entidade_ausente == "equino":
        equino_id = ID_INEXISTENTE
    else:
        estabulo_id = ID_INEXISTENTE

    # Act
    response = associar_equino(client, equino_id, estabulo_id)

    # Assert
    assert response.status_code == STATUS_ERRO_REGRA
    assert "não encontrado" in response.json()["detail"]
    assert client.get(ROTA_ESTABULOS).json()[0]["equinos"] == []


@pytest.mark.integration
def test_listagens_ignoram_referencia_a_equino_inexistente(
    client: TestClient, payload_equino_valido: dict, payload_estabulo_valido: dict
):
    # Arrange: simula uma referência antiga no repositório.
    equino_id = criar_equino(client, payload_equino_valido)
    estabulo_id = criar_estabulo(client, payload_estabulo_valido)
    assert associar_equino(client, equino_id, estabulo_id).status_code == STATUS_OK
    estabulo_persistido = estabulo_repository.obter_estabulo_por_id(estabulo_id)
    estabulo_persistido.equinos.append(ID_INEXISTENTE)

    # Act
    resposta_equinos = client.get(ROTA_EQUINOS)
    resposta_estabulos = client.get(ROTA_ESTABULOS)

    # Assert
    assert resposta_equinos.status_code == STATUS_OK
    assert resposta_equinos.json()[0]["estabulo_id"] == estabulo_id
    assert resposta_estabulos.status_code == STATUS_OK
    assert [equino["id"] for equino in resposta_estabulos.json()[0]["equinos"]] == [
        equino_id
    ]


@pytest.mark.integration
def test_health_check(client: TestClient):
    # Act
    response = client.get(ROTA_HEALTH)

    # Assert
    assert response.status_code == STATUS_OK
    assert response.json()["status"] == "ok"


@pytest.mark.integration
@pytest.mark.parametrize(
    "alteracao",
    [
        {"nome": NOME_COM_UM_CARACTERE},
        {"nome": NOME_COM_200_CARACTERES},
        {"idade": IDADE_MINIMA_PERMITIDA},
        {"idade": IDADE_ACIMA_DA_MINIMA},
    ],
    ids=["nome-minimo", "nome-maximo", "idade-minima", "idade-apos-minima"],
)
def test_criar_equino_aceita_valores_limite_validos(
    client: TestClient, payload_equino_valido: dict, alteracao: dict
):
    # Arrange
    payload = {**payload_equino_valido, **alteracao}

    # Act
    response = client.post(ROTA_EQUINOS, json=payload)

    # Assert
    assert response.status_code == STATUS_CRIADO
    campo = next(iter(alteracao))
    assert response.json()[campo] == alteracao[campo]


@pytest.mark.integration
def test_criar_equino_aceita_raca_em_minusculas_preservando_valor(
    client: TestClient, payload_equino_valido: dict
):
    # Arrange
    payload = {**payload_equino_valido, "raca": RACA_CAVALO_MINUSCULA}

    # Act
    response = client.post(ROTA_EQUINOS, json=payload)

    # Assert
    assert response.status_code == STATUS_CRIADO
    assert response.json()["raca"] == RACA_CAVALO_MINUSCULA


@pytest.mark.integration
@pytest.mark.parametrize(
    ("alteracao", "campo"),
    [
        ({"nome": TEXTO_VAZIO}, "nome"),
        ({"nome": NOME_COM_201_CARACTERES}, "nome"),
        ({"idade": IDADE_INVALIDA}, "idade"),
        ({"raca": TEXTO_VAZIO}, "raca"),
        ({"sexo": SEXO_INVALIDO}, "sexo"),
        ({"data_nascimento": None}, "data_nascimento"),
    ],
    ids=[
        "nome-vazio",
        "nome-longo",
        "idade-negativa",
        "raca-vazia",
        "sexo-invalido",
        "data-nula",
    ],
)
def test_criar_equino_recusa_payload_invalido_sem_persistir(
    client: TestClient, payload_equino_valido: dict, alteracao: dict, campo: str
):
    # Arrange
    payload = {**payload_equino_valido, **alteracao}

    # Act
    response = client.post(ROTA_EQUINOS, json=payload)

    # Assert
    assert response.status_code == STATUS_ERRO_VALIDACAO
    assert any(erro["loc"][-1] == campo for erro in response.json()["detail"])
    assert client.get(ROTA_EQUINOS).json() == []


@pytest.mark.integration
def test_criar_equino_recusa_campo_obrigatorio_ausente(
    client: TestClient, payload_equino_valido: dict
):
    # Arrange
    payload = payload_equino_valido.copy()
    payload.pop("data_nascimento")

    # Act
    response = client.post(ROTA_EQUINOS, json=payload)

    # Assert
    assert response.status_code == STATUS_ERRO_VALIDACAO
    assert client.get(ROTA_EQUINOS).json() == []


@pytest.mark.integration
@pytest.mark.parametrize(
    "nome",
    [NOME_COM_UM_CARACTERE, NOME_COM_200_CARACTERES],
    ids=["nome-minimo", "nome-maximo"],
)
def test_criar_estabulo_aceita_nomes_nos_limites(
    client: TestClient, payload_estabulo_valido: dict, nome: str
):
    # Arrange
    payload = {**payload_estabulo_valido, "nome_identificador": nome}

    # Act
    response = client.post(ROTA_ESTABULOS, json=payload)

    # Assert
    assert response.status_code == STATUS_CRIADO
    assert response.json()["nome_identificador"] == nome


@pytest.mark.integration
@pytest.mark.parametrize(
    ("alteracao", "campo"),
    [
        ({"nome_identificador": TEXTO_VAZIO}, "nome_identificador"),
        ({"nome_identificador": NOME_COM_201_CARACTERES}, "nome_identificador"),
        ({"localizacao": TEXTO_VAZIO}, "localizacao"),
        ({"capacidade": CAPACIDADE_INVALIDA}, "capacidade"),
    ],
    ids=["nome-vazio", "nome-longo", "localizacao-vazia", "capacidade-zero"],
)
def test_criar_estabulo_recusa_payload_invalido_sem_persistir(
    client: TestClient, payload_estabulo_valido: dict, alteracao: dict, campo: str
):
    # Arrange
    payload = {**payload_estabulo_valido, **alteracao}

    # Act
    response = client.post(ROTA_ESTABULOS, json=payload)

    # Assert
    assert response.status_code == STATUS_ERRO_VALIDACAO
    assert any(erro["loc"][-1] == campo for erro in response.json()["detail"])
    assert client.get(ROTA_ESTABULOS).json() == []


@pytest.mark.integration
def test_criar_estabulo_recusa_campo_obrigatorio_ausente(
    client: TestClient, payload_estabulo_valido: dict
):
    # Arrange
    payload = payload_estabulo_valido.copy()
    payload.pop("capacidade")

    # Act
    response = client.post(ROTA_ESTABULOS, json=payload)

    # Assert
    assert response.status_code == STATUS_ERRO_VALIDACAO
    assert client.get(ROTA_ESTABULOS).json() == []


@pytest.mark.integration
@pytest.mark.mocks
@pytest.mark.parametrize(
    ("metodo", "rota"),
    [
        ("listar_equinos", ROTA_EQUINOS),
        ("criar_estabulo", ROTA_ESTABULOS),
        ("listar_estabulos", ROTA_ESTABULOS),
    ],
)
def test_api_converte_erro_do_servico_em_http_400(
    client: TestClient,
    payload_estabulo_valido: dict,
    mocker,
    metodo: str,
    rota: str,
):
    # Arrange
    mocker.patch.object(service, metodo, side_effect=ValueError(ERRO_SERVICO_SIMULADO))

    # Act
    if metodo == "criar_estabulo":
        response = client.post(rota, json=payload_estabulo_valido)
    else:
        response = client.get(rota)

    # Assert
    assert response.status_code == STATUS_ERRO_REGRA
    assert response.json()["detail"] == ERRO_SERVICO_SIMULADO
