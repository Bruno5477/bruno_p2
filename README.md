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


### Resultados dos testes

==================================================================================================== test session starts =====================================================================================================
platform win32 -- Python 3.13.14, pytest-8.3.4, pluggy-1.6.0 -- C:\Users\UNIVASSOURAS\Documents\bruno_p2\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\UNIVASSOURAS\Documents\bruno_p2
configfile: pytest.ini
plugins: anyio-4.14.0, cov-6.0.0
collected 15 items                                                                                                                                                                                                            

test/test_produtos.py::test_listar_produtos_quando_banco_esta_vazio PASSED                                                                                                                                              [  6%]
test/test_produtos.py::test_criar_produto_e_verificar_persistencia_no_banco PASSED                                                                                                                                      [ 13%]
test/test_produtos.py::test_criar_produto_e_verificar_que_aparece_na_listagem PASSED                                                                                                                                    [ 20%]
test/test_produtos.py::test_buscar_produto_por_id_com_sucesso PASSED                                                                                                                                                    [ 26%]
test/test_produtos.py::test_buscar_produto_com_id_inexistente_retorna_404 PASSED                                                                                                                                        [ 33%]
test/test_produtos.py::test_deletar_produto_retorna_204 PASSED                                                                                                                                                          [ 40%]
test/test_produtos.py::test_deletar_produto_e_confirmar_remocao_com_get_subsequente PASSED                                                                                                                              [ 46%]
test/test_produtos.py::test_deletar_produto_inexistente_retorna_404 PASSED                                                                                                                                              [ 53%]
test/test_produtos.py::test_payloads_invalidos_retorna_422[payload0] PASSED                                                                                                                                             [ 60%]
test/test_produtos.py::test_payloads_invalidos_retorna_422[payload1] PASSED                                                                                                                                             [ 66%]
test/test_produtos.py::test_payloads_invalidos_retorna_422[payload2] PASSED                                                                                                                                             [ 73%]
test/test_produtos.py::test_payloads_invalidos_retorna_422[payload3] PASSED                                                                                                                                             [ 80%]
test/test_produtos.py::test_payloads_invalidos_retorna_422[payload4] PASSED                                                                                                                                             [ 86%]
test/test_produtos.py::test_payloads_invalidos_retorna_422[payload5] PASSED                                                                                                                                             [ 93%]
test/test_produtos.py::test_banco_isolado_entre_execucoes PASSED                                                                                                                                                        [100%]

====================================================================================================== warnings summary ======================================================================================================
main.py:57
  C:\Users\UNIVASSOURAS\Documents\bruno_p2\main.py:57: DeprecationWarning: 
          on_event is deprecated, use lifespan event handlers instead.
  
          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
          
    @app.on_event("startup")

venv\Lib\site-packages\fastapi\applications.py:4495
  C:\Users\UNIVASSOURAS\Documents\bruno_p2\venv\Lib\site-packages\fastapi\applications.py:4495: DeprecationWarning: 
          on_event is deprecated, use lifespan event handlers instead.
  
          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
          
    return self.router.on_event(event_type)

venv\Lib\site-packages\_pytest\config\__init__.py:1500
  C:\Users\UNIVASSOURAS\Documents\bruno_p2\venv\Lib\site-packages\_pytest\config\__init__.py:1500: PytestConfigWarning: No files were found in testpaths; consider removing or adjusting your testpaths configuration. Searching recursively from the current directory instead.
    self.args, self.args_source = self._decide_args(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

---------- coverage: platform win32, python 3.13.14-final-0 ----------
Name      Stmts   Miss  Cover
-----------------------------
main.py      62      4    94%
-----------------------------
TOTAL        62      4    94%