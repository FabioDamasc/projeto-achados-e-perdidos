from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="API de Objetos Encontrados",
    description="API REST para cadastro e consulta de objetos encontrados nas dependências.",
    version="1.0.0",
)


class ObjetoCreate(BaseModel):
    descricao: str
    local: str


class ObjetoResponse(BaseModel):
    id: int
    descricao: str
    local: str


# Armazenamento em memória
objetos_db: list[dict] = []
proximo_id: int = 1


def resetar_banco() -> None:
    """Limpa os dados em memória (usado nos testes para garantir independência)."""
    global proximo_id
    objetos_db.clear()
    proximo_id = 1


@app.get("/objetos", response_model=list[ObjetoResponse], summary="Listar objetos cadastrados")
def listar_objetos():
    return objetos_db


@app.get("/objetos/{objeto_id}", response_model=ObjetoResponse, summary="Consultar objeto pelo ID")
def consultar_objeto(objeto_id: int):
    for obj in objetos_db:
        if obj["id"] == objeto_id:
            return obj
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Objeto não encontrado.",
    )


@app.post(
    "/objetos",
    response_model=ObjetoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar um novo objeto",
)
def cadastrar_objeto(objeto: ObjetoCreate):
    global proximo_id
    novo_objeto = {
        "id": proximo_id,
        "descricao": objeto.descricao,
        "local": objeto.local,
    }
    objetos_db.append(novo_objeto)
    proximo_id += 1
    return novo_objeto
