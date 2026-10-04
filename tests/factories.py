import random

from faker import Faker

from app.schemas import Estabulo, CriarEstabulo, Equino, CriarEquino
from tests.constants import (
    CAPACIDADE_ALEATORIA_MAXIMA,
    CAPACIDADE_ALEATORIA_MINIMA,
    CASAS_DECIMAIS_PESO,
    ID_ALEATORIO_MAXIMO,
    ID_ALEATORIO_MINIMO,
    IDADE_ALEATORIA_MAXIMA,
    IDADE_ALEATORIA_MINIMA,
    LOCALE_FAKER,
    PESO_ALEATORIO_MAXIMO,
    PESO_ALEATORIO_MINIMO,
    PREFIXO_ID_EQUINO,
    PREFIXO_ID_ESTABULO,
    RACAS_VALIDAS,
    SEXOS_VALIDOS,
)

fake = Faker(LOCALE_FAKER)


def _id_aleatorio(prefixo: str) -> str:
    numero = fake.unique.random_int(
        min=ID_ALEATORIO_MINIMO, max=ID_ALEATORIO_MAXIMO
    )
    return f"{prefixo}-{numero}"


class EstabuloFactory:
    """Gerador de dados sintéticos para estábulos"""

    @classmethod
    def build(cls, **kwargs) -> Estabulo:
        """Cria um estábulo com dados sintéticos."""
        estabulo_id = kwargs.pop("id", None) or _id_aleatorio(PREFIXO_ID_ESTABULO)

        dados = {
            "id": estabulo_id,
            "nome_identificador": fake.word().capitalize()
            + " "
            + fake.word().capitalize(),
            "localizacao": fake.city(),
            "capacidade": random.randint(
                CAPACIDADE_ALEATORIA_MINIMA, CAPACIDADE_ALEATORIA_MAXIMA
            ),
            "equinos": [],
        }
        dados.update(kwargs)
        return Estabulo(**dados)


class EquinoFactory:
    """Gerador de dados sintéticos para equinos"""

    @classmethod
    def build(cls, **kwargs) -> Equino:
        """Cria um equino com dados sintéticos."""
        equino_id = kwargs.pop("id", None) or _id_aleatorio(PREFIXO_ID_EQUINO)
        sexo = random.choice(SEXOS_VALIDOS)
        raca = random.choice(RACAS_VALIDAS)

        dados = {
            "id": equino_id,
            "nome": fake.first_name(),
            "idade": random.randint(IDADE_ALEATORIA_MINIMA, IDADE_ALEATORIA_MAXIMA),
            "raca": raca,
            "sexo": sexo,
            "data_nascimento": fake.date_of_birth(
                minimum_age=IDADE_ALEATORIA_MINIMA,
                maximum_age=IDADE_ALEATORIA_MAXIMA,
            ).isoformat(),
            "peso": round(
                random.uniform(PESO_ALEATORIO_MINIMO, PESO_ALEATORIO_MAXIMO),
                CASAS_DECIMAIS_PESO,
            ),
            "estabulo_id": None,
        }
        dados.update(kwargs)
        return Equino(**dados)


class CriarEstabuloFactory:
    """Gerador de dados sintéticos para criação de estábulos"""

    @classmethod
    def build(cls, **kwargs) -> CriarEstabulo:
        """Cria um payload para criar um estábulo com dados sintéticos."""
        dados = {
            "nome_identificador": fake.word().capitalize()
            + " "
            + fake.word().capitalize(),
            "localizacao": fake.city(),
            "capacidade": random.randint(
                CAPACIDADE_ALEATORIA_MINIMA, CAPACIDADE_ALEATORIA_MAXIMA
            ),
        }
        dados.update(kwargs)
        return CriarEstabulo(**dados)


class CriarEquinoFactory:
    """Gerador de dados sintéticos para criação de equinos"""

    @classmethod
    def build(cls, **kwargs) -> CriarEquino:
        """Cria um payload para criar um equino com dados sintéticos."""
        dados = {
            "nome": fake.first_name(),
            "idade": random.randint(IDADE_ALEATORIA_MINIMA, IDADE_ALEATORIA_MAXIMA),
            "raca": random.choice(RACAS_VALIDAS),
            "sexo": random.choice(SEXOS_VALIDOS),
            "data_nascimento": fake.date_of_birth(
                minimum_age=IDADE_ALEATORIA_MINIMA,
                maximum_age=IDADE_ALEATORIA_MAXIMA,
            ).isoformat(),
            "peso": round(
                random.uniform(PESO_ALEATORIO_MINIMO, PESO_ALEATORIO_MAXIMO),
                CASAS_DECIMAIS_PESO,
            ),
        }
        dados.update(kwargs)
        return CriarEquino(**dados)


class AssociarEquinoEstabuloFactory:
    """Gerador de dados sintéticos para associação de equinos a estábulos"""

    @classmethod
    def build(cls, **kwargs) -> dict:
        """Cria um payload para associar um equino a um estábulo com dados sintéticos."""
        dados = {
            "equino_id": _id_aleatorio(PREFIXO_ID_EQUINO),
            "estabulo_id": _id_aleatorio(PREFIXO_ID_ESTABULO),
        }
        dados.update(kwargs)
        return dados
