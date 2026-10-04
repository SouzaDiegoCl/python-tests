"""Testes do domínio com repositórios independentes e sem cliente HTTP."""

from uuid import UUID

import pytest
from pydantic import ValidationError

from app.repository import EquinoRepository, EstabuloRepository
from app.schemas import CriarEquino, CriarEstabulo, LIstarEstabulo
from app.service import EquinosService
from tests.constants import (
    CAPACIDADE_ESTABULO_10,
    CAPACIDADE_ESTABULO_MINIMA,
    CAPACIDADE_INVALIDA,
    ID_EQUINO_TESTE,
    ID_ESTABULO_TESTE,
    ID_INEXISTENTE,
    ID_OUTRO_EQUINO_TESTE,
    IDADE_INVALIDA,
    IDADE_MINIMA_PERMITIDA,
    NOME_CAVALO,
    NOME_COM_200_CARACTERES,
    NOME_COM_201_CARACTERES,
    NOME_COM_UM_CARACTERE,
    RACA_CAVALO,
    RACA_CAVALO_MINUSCULA,
    RACA_INVALIDA,
    RACAS_VALIDAS,
    SEXO_INVALIDO,
    TEXTO_VAZIO,
)
from tests.factories import EquinoFactory, EstabuloFactory


@pytest.fixture
def equino_repo() -> EquinoRepository:
    return EquinoRepository()


@pytest.fixture
def estabulo_repo() -> EstabuloRepository:
    return EstabuloRepository()


@pytest.fixture
def servico(
    equino_repo: EquinoRepository, estabulo_repo: EstabuloRepository
) -> EquinosService:
    return EquinosService(
        equinoRepository=equino_repo, estabuloRepository=estabulo_repo
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    ("campo", "valor"),
    [
        ("nome", NOME_COM_UM_CARACTERE),
        ("nome", NOME_COM_200_CARACTERES),
        ("idade", IDADE_MINIMA_PERMITIDA),
    ],
    ids=["nome-minimo", "nome-maximo", "idade-minima"],
)
def test_schema_equino_aceita_limites_validos(
    payload_equino_valido: dict, campo: str, valor: str | int
):
    # Arrange
    payload = {**payload_equino_valido, campo: valor}

    # Act
    equino = CriarEquino(**payload)

    # Assert
    assert getattr(equino, campo) == valor


@pytest.mark.unit
@pytest.mark.parametrize(
    ("alteracao", "campo"),
    [
        ({"nome": TEXTO_VAZIO}, "nome"),
        ({"nome": NOME_COM_201_CARACTERES}, "nome"),
        ({"idade": IDADE_INVALIDA}, "idade"),
        ({"raca": TEXTO_VAZIO}, "raca"),
        ({"sexo": SEXO_INVALIDO}, "sexo"),
    ],
    ids=["nome-vazio", "nome-longo", "idade-negativa", "raca-vazia", "sexo-invalido"],
)
def test_schema_equino_rejeita_entradas_invalidas(
    payload_equino_valido: dict, alteracao: dict, campo: str
):
    # Arrange
    payload = {**payload_equino_valido, **alteracao}

    # Act / Assert
    with pytest.raises(ValidationError) as erro:
        CriarEquino(**payload)
    assert erro.value.errors()[0]["loc"][-1] == campo


@pytest.mark.unit
@pytest.mark.parametrize(
    ("campo", "valor"),
    [
        ("nome_identificador", NOME_COM_UM_CARACTERE),
        ("nome_identificador", NOME_COM_200_CARACTERES),
        ("capacidade", CAPACIDADE_ESTABULO_MINIMA),
    ],
    ids=["nome-minimo", "nome-maximo", "capacidade-minima"],
)
def test_schema_estabulo_aceita_limites_validos(
    payload_estabulo_valido: dict, campo: str, valor: str | int
):
    # Arrange
    payload = {**payload_estabulo_valido, campo: valor}

    # Act
    estabulo = CriarEstabulo(**payload)

    # Assert
    assert getattr(estabulo, campo) == valor


@pytest.mark.unit
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
def test_schema_estabulo_rejeita_entradas_invalidas(
    payload_estabulo_valido: dict, alteracao: dict, campo: str
):
    # Arrange
    payload = {**payload_estabulo_valido, **alteracao}

    # Act / Assert
    with pytest.raises(ValidationError) as erro:
        CriarEstabulo(**payload)
    assert erro.value.errors()[0]["loc"][-1] == campo


@pytest.mark.unit
@pytest.mark.parametrize(
    ("raca", "esperado"),
    [(raca, True) for raca in RACAS_VALIDAS]
    + [(RACA_CAVALO_MINUSCULA, True), (RACA_INVALIDA, False)],
)
def test_validar_raca_por_particoes(
    servico: EquinosService, raca: str, esperado: bool
):
    # Act
    resultado = servico.validar_racas_validas(raca)

    # Assert
    assert resultado is esperado


@pytest.mark.unit
def test_criar_equino_persiste_dados_e_id_uuid(
    servico: EquinosService,
    equino_repo: EquinoRepository,
    payload_equino_valido: dict,
):
    # Arrange
    request = CriarEquino(**payload_equino_valido)

    # Act
    equino = servico.criar_equino(request)

    # Assert
    assert UUID(equino.id).version == 4
    assert equino.nome == NOME_CAVALO
    assert equino.raca == RACA_CAVALO
    assert equino.estabulo_id is None
    assert equino_repo.obter_equino_por_id(equino.id) is equino


@pytest.mark.unit
def test_criar_equino_preserva_raca_em_minusculas(
    servico: EquinosService, payload_equino_valido: dict
):
    # Arrange
    request = CriarEquino(
        **{**payload_equino_valido, "raca": RACA_CAVALO_MINUSCULA}
    )

    # Act
    equino = servico.criar_equino(request)

    # Assert
    assert equino.raca == RACA_CAVALO_MINUSCULA


@pytest.mark.unit
def test_criar_equino_com_raca_invalida_nao_persiste(
    servico: EquinosService,
    equino_repo: EquinoRepository,
    payload_equino_valido: dict,
):
    # Arrange
    request = CriarEquino(**{**payload_equino_valido, "raca": RACA_INVALIDA})

    # Act / Assert
    with pytest.raises(ValueError, match="Raça inválida"):
        servico.criar_equino(request)
    assert equino_repo.listar_equinos() == {}


@pytest.mark.unit
@pytest.mark.parametrize(
    ("quantidade", "esperado"),
    [
        (CAPACIDADE_ESTABULO_10 - 1, True),
        (CAPACIDADE_ESTABULO_10, False),
        (CAPACIDADE_ESTABULO_10 + 1, False),
    ],
    ids=["abaixo", "exata", "acima"],
)
def test_validar_capacidade_no_limite(
    servico: EquinosService, quantidade: int, esperado: bool
):
    # Arrange
    ids_equinos = [str(indice) for indice in range(quantidade)]

    # Act
    resultado = servico.validar_capacidade_estabulo(
        CAPACIDADE_ESTABULO_10, ids_equinos
    )

    # Assert
    assert resultado is esperado


@pytest.mark.unit
def test_associar_equino_armazena_apenas_id(
    servico: EquinosService,
    equino_repo: EquinoRepository,
    estabulo_repo: EstabuloRepository,
):
    # Arrange
    equino = EquinoFactory.build(id=ID_EQUINO_TESTE)
    estabulo = EstabuloFactory.build(
        id=ID_ESTABULO_TESTE, capacidade=CAPACIDADE_ESTABULO_MINIMA
    )
    equino_repo.adicionar_equino(equino)
    estabulo_repo.adicionar_estabulo(estabulo)

    # Act
    servico.associar_equino_estabulo(equino.id, estabulo.id)

    # Assert
    assert estabulo.equinos == [equino.id]
    assert all(isinstance(equino_id, str) for equino_id in estabulo.equinos)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("ausente", "mensagem"),
    [("equino", "Equino"), ("estabulo", "Estábulo")],
)
def test_associar_rejeita_id_inexistente_sem_mudar_repositorio(
    servico: EquinosService,
    equino_repo: EquinoRepository,
    estabulo_repo: EstabuloRepository,
    ausente: str,
    mensagem: str,
):
    # Arrange
    equino = EquinoFactory.build(id=ID_EQUINO_TESTE)
    estabulo = EstabuloFactory.build(id=ID_ESTABULO_TESTE)
    equino_repo.adicionar_equino(equino)
    estabulo_repo.adicionar_estabulo(estabulo)
    equino_id = ID_INEXISTENTE if ausente == "equino" else equino.id
    estabulo_id = ID_INEXISTENTE if ausente == "estabulo" else estabulo.id

    # Act / Assert
    with pytest.raises(ValueError, match=mensagem):
        servico.associar_equino_estabulo(equino_id, estabulo_id)
    assert estabulo.equinos == []
    assert equino.estabulo_id is None


@pytest.mark.unit
def test_associar_recusa_estabulo_lotado_sem_alteracao(
    servico: EquinosService,
    equino_repo: EquinoRepository,
    estabulo_repo: EstabuloRepository,
):
    # Arrange
    equino = EquinoFactory.build(id=ID_EQUINO_TESTE)
    outro = EquinoFactory.build(id=ID_OUTRO_EQUINO_TESTE)
    estabulo = EstabuloFactory.build(
        id=ID_ESTABULO_TESTE,
        capacidade=CAPACIDADE_ESTABULO_MINIMA,
        equinos=[outro.id],
    )
    equino_repo.adicionar_equino(equino)
    equino_repo.adicionar_equino(outro)
    estabulo_repo.adicionar_estabulo(estabulo)

    # Act / Assert
    with pytest.raises(ValueError, match="capacidade máxima"):
        servico.associar_equino_estabulo(equino.id, estabulo.id)
    assert estabulo.equinos == [outro.id]
    assert equino.estabulo_id is None


@pytest.mark.unit
def test_associar_recusa_duplicidade_sem_alteracao(
    servico: EquinosService,
    equino_repo: EquinoRepository,
    estabulo_repo: EstabuloRepository,
):
    # Arrange
    equino = EquinoFactory.build(id=ID_EQUINO_TESTE)
    estabulo = EstabuloFactory.build(
        id=ID_ESTABULO_TESTE,
        capacidade=CAPACIDADE_ESTABULO_10,
        equinos=[equino.id],
    )
    equino_repo.adicionar_equino(equino)
    estabulo_repo.adicionar_estabulo(estabulo)

    # Act / Assert
    with pytest.raises(ValueError, match="já está associado"):
        servico.associar_equino_estabulo(equino.id, estabulo.id)
    assert estabulo.equinos == [equino.id]


@pytest.mark.unit
def test_listar_equinos_atribui_estabulo_e_ignora_id_inexistente(
    servico: EquinosService,
    equino_repo: EquinoRepository,
    estabulo_repo: EstabuloRepository,
):
    # Arrange
    associado = EquinoFactory.build(id=ID_EQUINO_TESTE)
    avulso = EquinoFactory.build(id=ID_OUTRO_EQUINO_TESTE)
    estabulo = EstabuloFactory.build(
        id=ID_ESTABULO_TESTE,
        equinos=[associado.id, ID_INEXISTENTE],
    )
    equino_repo.adicionar_equino(associado)
    equino_repo.adicionar_equino(avulso)
    estabulo_repo.adicionar_estabulo(estabulo)

    # Act
    resultado = servico.listar_equinos()

    # Assert
    assert {equino.id for equino in resultado} == {associado.id, avulso.id}
    assert associado.estabulo_id == estabulo.id
    assert avulso.estabulo_id is None


@pytest.mark.unit
def test_criar_estabulo_persiste_dados_e_id_uuid(
    servico: EquinosService,
    estabulo_repo: EstabuloRepository,
    payload_estabulo_valido: dict,
):
    # Arrange
    request = CriarEstabulo(**payload_estabulo_valido)

    # Act
    estabulo = servico.criar_estabulo(request)

    # Assert
    assert UUID(estabulo.id).version == 4
    assert estabulo.capacidade == CAPACIDADE_ESTABULO_10
    assert estabulo.equinos == []
    assert estabulo_repo.obter_estabulo_por_id(estabulo.id) is estabulo


@pytest.mark.unit
def test_listar_estabulos_expande_equinos_validos_sem_mudar_ids(
    servico: EquinosService,
    equino_repo: EquinoRepository,
    estabulo_repo: EstabuloRepository,
):
    # Arrange
    equino = EquinoFactory.build(id=ID_EQUINO_TESTE)
    estabulo = EstabuloFactory.build(
        id=ID_ESTABULO_TESTE,
        equinos=[equino.id, ID_INEXISTENTE],
    )
    equino_repo.adicionar_equino(equino)
    estabulo_repo.adicionar_estabulo(estabulo)

    # Act
    resultado = servico.listar_estabulos()

    # Assert
    assert len(resultado) == CAPACIDADE_ESTABULO_MINIMA
    assert isinstance(resultado[0], LIstarEstabulo)
    assert [item.id for item in resultado[0].equinos] == [equino.id]
    assert estabulo.equinos == [equino.id, ID_INEXISTENTE]
