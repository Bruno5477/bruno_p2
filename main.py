import os
from typing import Generator, List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Boolean, Column, Float, Integer, String, create_engine, text
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from urllib.parse import quote_plus
from sqlalchemy.engine.url import make_url
import logging

logging.basicConfig(level=logging.INFO)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5433/produtos_db_test",
)

def safe_database_url(db_url: str) -> str:
    try:
        url = make_url(db_url)
    except Exception:
        return db_url

    user = url.username or ""
    pwd = url.password or ""
    if any(ord(c) > 127 for c in (user + pwd)):
        user_enc = quote_plus(user) if user else ""
        pwd_enc = quote_plus(pwd) if pwd else ""
        host = url.host or ""
        port = f":{url.port}" if url.port else ""
        db = f"/{url.database}" if url.database else ""
        return f"{url.drivername}://{user_enc}:{pwd_enc}@{host}{port}{db}"
    return db_url

DATABASE_URL = safe_database_url(DATABASE_URL)

def _mask_db_url(db_url: str) -> str:
    try:
        url = make_url(db_url)
        user = url.username or ""
        host = url.host or ""
        port = f":{url.port}" if url.port else ""
        db = f"/{url.database}" if url.database else ""
        return f"{url.drivername}://{user}:***@{host}{port}{db}"
    except Exception:
        return "(invalid-dsn)"

logging.info("Using DATABASE_URL: %s", _mask_db_url(DATABASE_URL))

try:
    engine = create_engine(DATABASE_URL)
except UnicodeDecodeError as e:
    logging.error("UnicodeDecodeError when creating engine: %s", e)
    logging.error("DATABASE_URL repr: %r", DATABASE_URL)
    try:
        parsed = make_url(DATABASE_URL)
        logging.error("Parsed URL username repr: %r", parsed.username)
        logging.error("Parsed URL password repr: %r", parsed.password)
        logging.error("Parsed URL host: %s, port: %s, db: %s", parsed.host, parsed.port, parsed.database)
    except Exception as ex:
        logging.error("Failed parsing DATABASE_URL: %s", ex)
    raise
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI(title="API de Gerenciamento de Produtos")


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False, default=0, server_default=text("0"))
    ativo = Column(Boolean, nullable=False, default=True, server_default=text("true"))


class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1)
    preco: float = Field(..., gt=0)
    estoque: int = Field(default=0, ge=0)
    ativo: bool = True
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "Caneca",
                "preco": 29.9,
                "estoque": 12,
                "ativo": True,
            }
        }
    )


class ProdutoCreate(ProdutoBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "Teclado Mecânico",
                "preco": 350.0,
                "estoque": 10,
                "ativo": True,
            }
        }
    )


class ProdutoRead(ProdutoBase):
    id: int
    model_config = ConfigDict(from_attributes=True,
                              json_schema_extra={
                                  "example": {
                                      "id": 1,
                                      "nome": "Notebook Gamer",
                                      "preco": 4999.9,
                                      "estoque": 5,
                                      "ativo": True,
                                  }
                              })


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    logging.info("on_startup: masked DATABASE_URL: %s", _mask_db_url(DATABASE_URL))
    logging.info("on_startup: DATABASE_URL repr: %r", DATABASE_URL)
    Base.metadata.create_all(bind=engine)


@app.get("/produtos", response_model=List[ProdutoRead])
def listar_produtos(db: Session = Depends(get_db)):
    produtos = db.query(Produto).all()
    return produtos


@app.post("/produtos", response_model=ProdutoRead, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = Produto(
        nome=produto.nome,
        preco=produto.preco,
        estoque=produto.estoque,
        ativo=produto.ativo,
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto


@app.get("/produtos/{produto_id}", response_model=ProdutoRead)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return produto


@app.delete("/produtos/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

    db.delete(produto)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)