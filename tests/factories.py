import random
from faker import Faker
from app.schemas import Estabulo, CriarEstabulo, Equino, CriarEquino

fake = Faker("pt_BR")


class EstabuloFactory:
    """Gerador de dados sintéticos para estábulos"""

    @classmethod
    def build(cls, **kwargs) -> Estabulo:
        """Cria um estábulo com dados sintéticos."""
        estabulo_id = (
            kwargs.pop("id", None)
            or f"EST-{fake.unique.random_int(min=1000, max=9999)}"
        )

        dados = {
            "id": estabulo_id,
            "nome_identificador": fake.word().capitalize()
            + " "
            + fake.word().capitalize(),
            "localizacao": fake.city(),
            "capacidade": random.randint(1, 50),
            "equinos": [],
        }
        dados.update(kwargs)
        return Estabulo(**dados)


class EquinoFactory:
    """Gerador de dados sintéticos para equinos"""

    @classmethod
    def build(cls, **kwargs) -> Equino:
        """Cria um equino com dados sintéticos."""
        equino_id = (
            kwargs.pop("id", None)
            or f"EQU-{fake.unique.random_int(min=1000, max=9999)}"
        )
        sexo = random.choice(["MACHO", "FEMEA"])
        raca = random.choice(
            ["MANGALARGA", "PURO SANGUE", "QUARTO DE MILHA", "ARABE", "LUSITANO"]
        )

        dados = {
            "id": equino_id,
            "nome": fake.first_name(),
            "idade": random.randint(1, 20),
            "raca": raca,
            "sexo": sexo,
            "data_nascimento": fake.date_of_birth(
                minimum_age=1, maximum_age=20
            ).isoformat(),
            "peso": round(random.uniform(300.0, 600.0), 2),
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
            "capacidade": random.randint(1, 50),
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
            "idade": random.randint(1, 20),
            "raca": random.choice(
                ["MANGALARGA", "PURO SANGUE", "QUARTO DE MILHA", "ARABE", "LUSITANO"]
            ),
            "sexo": random.choice(["MACHO", "FEMEA"]),
            "data_nascimento": fake.date_of_birth(
                minimum_age=1, maximum_age=20
            ).isoformat(),
            "peso": round(random.uniform(300.0, 600.0), 2),
        }
        dados.update(kwargs)
        return CriarEquino(**dados)


class AssociarEquinoEstabuloFactory:
    """Gerador de dados sintéticos para associação de equinos a estábulos"""

    @classmethod
    def build(cls, **kwargs) -> dict:
        """Cria um payload para associar um equino a um estábulo com dados sintéticos."""
        dados = {
            "equino_id": f"EQU-{fake.unique.random_int(min=1000, max=9999)}",
            "estabulo_id": f"EST-{fake.unique.random_int(min=1000, max=9999)}",
        }
        dados.update(kwargs)
        return dados
