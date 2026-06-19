# API de Produtos com FastAPI + PostgreSQL + Pytest

Projeto desenvolvido para a atividade avaliativa da disciplina **Desenvolvimento de APIs com FastAPI**.

## Funcionalidades

A API possui os seguintes endpoints:

- `GET /produtos` → lista todos os produtos
- `POST /produtos` → cria um produto
- `GET /produtos/{id}` → busca um produto por ID
- `DELETE /produtos/{id}` → remove um produto por ID

## Modelo de Produto

- `id` → inteiro, gerado automaticamente
- `nome` → obrigatório, não pode ser vazio
- `preco` → obrigatório, maior que zero
- `estoque` → padrão `0`
- `ativo` → padrão `True`

---

## Como subir os bancos com Docker

### Banco de desenvolvimento

```bash
docker-compose up -d db_dev

seu_repositorio/
├── main.py
├── conftest.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── README.md
└── tests/
    ├── __init__.py
    └── test_produtos.py
```

## Para rodar os testes
```bash

python -m pytest --cov=main -v
 ```
### Resultados dos testes

---------- coverage: platform win32, python 3.13.14-final-0 ----------
Name      Stmts   Miss  Cover
-----------------------------
main.py     107      6    94%
-----------------------------
TOTAL       107      6    94%

================================================================= 21 passed, 3 warnings in 0.80s ==================================================================


### Como o isolamento entre testes funciona
O isolamento dos testes é garantido por uma fixture chamada client, definida no arquivo conftest.py.

Essa fixture faz o seguinte:

Cria as tabelas antes de cada teste com Base.metadata.create_all()
Substitui a dependência get_db usando app.dependency_overrides
Fornece um TestClient para os testes executarem requisições na API
Ao final do teste, remove os overrides e apaga as tabelas com Base.metadata.drop_all()
Com isso, cada teste começa com o banco limpo, sem depender de dados deixados por testes anteriores.
Além disso, o banco de testes roda em um container PostgreSQL separado, sem volume persistente, então os dados são descartados ao reiniciar o ambiente.