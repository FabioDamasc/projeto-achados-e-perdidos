# API de Controle de Objetos Encontrados — Testes Automatizados 

## Estrutura do Projeto
```text
projeto-achados-e-perdidos/
├── main.py
├── pytest.ini
├── requirements.txt
├── README.md
└── tests/
    └── test_objetos.py
```

## Como Executar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar os testes automatizados
python -m pytest -v

# 3. (Opcional) Subir a API localmente
uvicorn main:app --reload
```

---

## Explicação de um dos Testes Desenvolvidos (`test_04_cadastro_valido`)
O teste `test_04_cadastro_valido` valida o cenário positivo de criação de um novo objeto:
1. Monta um dicionário (`payload`) com os campos obrigatórios `descricao` e `local`.
2. Usa `client.post("/objetos", json=payload)` para simular uma requisição HTTP `POST` sem precisar subir o servidor manualmente.
3. Verifica com `assert response.status_code == 201` se a API retornou `201 Created`.
4. Confirma que o JSON retornado contém um `id` inteiro gerado pela aplicação e que `descricao` e `local` correspondem exatamente aos dados enviados.

---

## Respostas às Perguntas de Revisão

1. **Qual é a finalidade do Pytest?**
   O Pytest é um framework de testes em Python utilizado para escrever, organizar e executar testes automatizados de forma simples e legível, gerando relatórios claros sobre quais cenários passaram ou falharam.

2. **Qual é a função do TestClient?**
   O `TestClient` (do FastAPI/Starlette) permite simular requisições HTTP (`GET`, `POST`, `PUT`, `DELETE`) diretamente contra a aplicação FastAPI em memória, sem a necessidade de iniciar um servidor externo com Uvicorn.

3. **O que significa utilizar `assert` em um teste?**
   A instrução `assert` verifica se uma condição esperada é verdadeira (por exemplo, se o status HTTP é `200` ou se um campo possui determinado valor). Se a condição for falsa, o Python lança uma exceção e o Pytest marca o teste como falho (`FAILED`).

4. **Qual a diferença entre um teste positivo e um teste negativo?**
   - **Teste positivo:** valida o comportamento esperado quando a aplicação recebe dados válidos e requisições corretas (ex.: cadastrar objeto válido retornando `201`).
   - **Teste negativo:** valida se a aplicação trata e rejeita corretamente entradas inválidas, ausentes ou inexistentes (ex.: buscar ID inexistente retornando `404` ou enviar campo faltando retornando `422`).

5. **Por que um teste não deve depender da execução de outro?**
   Porque os testes precisam ser isolados e determinísticos. Se um teste depender de dados criados por outro, uma falha inicial gera falhas em cascata, dificulta encontrar a causa real do erro e impede rodar testes individualmente ou em paralelo.
