from app.schemas import Equino, Estabulo


class EquinoRepository:
    def __init__(self):
        self.equinos: dict[str, Equino] = {}

    def adicionar_equino(self, equino):
        self.equinos[equino.id] = equino

    def listar_equinos(self):
        return self.equinos

    def obter_equino_por_id(self, id: str) -> Equino:
        return self.equinos.get(id, None)

    def limpar(self) -> None:
        self.equinos.clear()


class EstabuloRepository:
    def __init__(self):
        self.estabulos: dict[str, Estabulo] = {}

    def adicionar_estabulo(self, estabulo: Estabulo):
        self.estabulos[estabulo.id] = estabulo

    def listar_estabulos(self):
        return self.estabulos

    def obter_estabulo_por_id(self, id: str) -> Estabulo:
        return self.estabulos.get(id, None)

    def limpar(self) -> None:
        self.estabulos.clear()


equino_repository = EquinoRepository()
estabulo_repository = EstabuloRepository()
