from enum import Enum
from pydantic import BaseModel, Field, model_validator


# Definição de Enums e Schemas para Equinos e Estábulos
class Sexo(str, Enum):
    MACHO = "MACHO"
    FEMEA = "FEMEA"


class Equino(BaseModel):
    id: str
    nome: str
    idade: int
    raca: str
    sexo: Sexo
    data_nascimento: str
    peso: float
    estabulo_id: str | None = Field(default=None)


class CriarEquino(BaseModel):
    nome: str = Field(..., min_length=1, max_length=200)
    idade: int = Field(..., ge=0)
    raca: str = Field(..., min_length=1)
    sexo: Sexo
    data_nascimento: str
    peso: float


class Estabulo(BaseModel):
    id: str
    nome_identificador: str = Field(..., min_length=1, max_length=200)
    localizacao: str
    capacidade: int    
    equinos: list[str] = Field(default_factory=list)

class LIstarEstabulo(BaseModel):
    id: str
    nome_identificador: str = Field(..., min_length=1, max_length=200)
    localizacao: str
    capacidade: int    
    equinos: list[Equino] = Field(default_factory=list)


class CriarEstabulo(BaseModel):
    nome_identificador: str = Field(..., min_length=1, max_length=200)
    localizacao: str = Field(..., min_length=1)
    capacidade: int = Field(..., gt=0)    


class EditarEstabulo(BaseModel):
    nome_identificador: str | None = Field(default=None, min_length=1, max_length=200)
    localizacao: str | None = Field(default=None, min_length=1)
    capacidade: int | None = Field(default=None, gt=0)
    quantidade_equinos: int | None = Field(default=None, ge=0)


class AdicionarEquinoEstabulo(BaseModel):
    equino_id: str | None = Field(default=None, min_length=1)
    estabulo_id: str | None = Field(default=None, min_length=1)


class RemoverEquinoEstabulo(BaseModel):
    equino_id: str | None = Field(default=None, min_length=1)
    estabulo_id: str | None = Field(default=None, min_length=1)
