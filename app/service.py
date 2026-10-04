import uuid
from app.schemas import CriarEstabulo, Equino, CriarEquino, Estabulo, LIstarEstabulo
from app.repository import (
    equino_repository,
    estabulo_repository,
    EquinoRepository,
    EstabuloRepository,
)


class EquinosService:
    """Serviço para gerenciar equinos"""

    racas_validas = ["MANGA-LARGA MARCHADOR", "QUARTO DE MILHA", "ANDALUZ", "LUSITANO"]

    def __init__(
        self,
        equinoRepository: EquinoRepository = equino_repository,
        estabuloRepository: EstabuloRepository = estabulo_repository,
    ):
        self.equinoRepository = equinoRepository
        self.estabuloRepository = estabuloRepository

    def criar_equino(self, request: CriarEquino) -> Equino:
        equino_id = str(uuid.uuid4())

        if not self.validar_racas_validas(request.raca):
            raise ValueError(
                f"Raça inválida: {request.raca}. Raças válidas são: {', '.join(self.racas_validas)}"
            )

        equino = Equino(
            id=equino_id,
            nome=request.nome,
            idade=request.idade,
            raca=request.raca,
            sexo=request.sexo,
            peso=request.peso,
            data_nascimento=request.data_nascimento,
        )
        self.equinoRepository.adicionar_equino(equino)
        return equino

    def listar_equinos(self) -> list[Equino]:
        """Lista todos os equinos e associa-os aos seus respectivos estábulos."""
        lista_equinos = self.equinoRepository.listar_equinos()
        lista_estabulos = self.estabuloRepository.listar_estabulos()

        for estabulo_id, estabulo in lista_estabulos.items():
            for equino_id in estabulo.equinos:
                if equino_id in lista_equinos:
                    lista_equinos[equino_id].estabulo_id = estabulo_id

        return list(lista_equinos.values())

    def associar_equino_estabulo(self, equino_id: str, estabulo_id: str) -> None:
        """Associa um equino a um estábulo."""
        equino = self.equinoRepository.obter_equino_por_id(equino_id)
        estabulo = self.estabuloRepository.obter_estabulo_por_id(estabulo_id)

        if not equino:
            raise ValueError(f"Equino com ID {equino_id} não encontrado.")
        if not estabulo:
            raise ValueError(f"Estábulo com ID {estabulo_id} não encontrado.")

        if not self.validar_capacidade_estabulo(estabulo.capacidade, estabulo.equinos):
            raise ValueError(
                f"Estábulo com ID {estabulo_id} atingiu sua capacidade máxima."
            )

        # Armazena apenas o ID do equino no estábulo.
        for existing_equino_id in estabulo.equinos:
            if existing_equino_id == equino.id:
                raise ValueError(
                    f"Equino com ID {equino_id} já está associado ao estábulo com ID {estabulo_id}."
                )
        estabulo.equinos. append(equino.id)

    def criar_estabulo(self, request: CriarEstabulo) -> Estabulo:
        """Cria um novo estábulo."""
        estabulo = Estabulo(
            id=str(uuid.uuid4()),
            nome_identificador=request.nome_identificador,
            localizacao=request.localizacao,
            capacidade=request.capacidade,
        )
        self.estabuloRepository.adicionar_estabulo(estabulo)
        return estabulo

    def listar_estabulos(self) -> list[LIstarEstabulo]:
        """Lista todos os estábulos."""
        lista_estabulos = self.estabuloRepository.listar_estabulos()
        lista_equinos = self.equinoRepository.listar_equinos()

        return [
            LIstarEstabulo(
                id=estabulo.id,
                nome_identificador=estabulo.nome_identificador,
                localizacao=estabulo.localizacao,
                capacidade=estabulo.capacidade,
                equinos=[
                    lista_equinos[equino_id]
                    for equino_id in estabulo.equinos
                    if equino_id in lista_equinos
                ],
            )
            for estabulo in lista_estabulos.values()
        ]

    def validar_racas_validas(self, raca: str) -> bool:
        """Valida se a raça do equino está na lista de raças válidas."""
        return raca.upper() in self.racas_validas

    def validar_capacidade_estabulo(self, capacidade: int, equinos: list[str]) -> bool:
        """Valida se o estábulo ainda tem capacidade para adicionar mais equinos."""
        return len(equinos) < capacidade