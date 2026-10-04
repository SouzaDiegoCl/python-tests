from fastapi import FastAPI, status, HTTPException
from app.schemas import CriarEstabulo, CriarEquino, Equino
from app.service import EquinosService

app = FastAPI(
    title="Serviço de Gerenciamento de Equinos",
    description="API para gerenciamento de informações de equinos, incluindo criação, atualização e consulta de registros em um haras",
    version="1.0.0",
)


service = EquinosService()


@app.get("/health", status_code=200)
def health_check():
    return {"status": "ok", "service": "servico-equinos"}


@app.post("/equinos", response_model=Equino, status_code=status.HTTP_201_CREATED)
def criar_equino(payload: CriarEquino):
    try:
        equino = service.criar_equino(payload)
        return equino
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@app.get("/equinos", response_model=list[Equino], status_code=status.HTTP_200_OK)
def listar_equinos():
    try:
        equinos = service.listar_equinos()
        return equinos
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@app.post("/equinos/{equino_id}/estabulo/{estabulo_id}", status_code=status.HTTP_200_OK)
def associar_equino_estabulo(equino_id: str, estabulo_id: str):
    try:
        service.associar_equino_estabulo(equino_id, estabulo_id)
        return {
            "message": f"Equino {equino_id} associado ao estábulo {estabulo_id} com sucesso."
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@app.post("/estabulos", status_code=status.HTTP_201_CREATED)
def criar_estabulo(payload: CriarEstabulo):
    try:
        estabulo = service.criar_estabulo(payload)
        return estabulo
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@app.get("/estabulos", status_code=status.HTTP_200_OK)
def listar_estabulos():
    try:
        estabulos = service.listar_estabulos()
        return estabulos
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
