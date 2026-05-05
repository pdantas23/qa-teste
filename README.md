# Suite de Automação QA
**Disciplina:** Teste e Qualidade de Software — Período 2026.1

Framework de automação de testes completo, cobrindo testes de API REST e testes de interface Web (UI), com integração contínua via GitHub Actions.

---

## O que este projeto testa?

| Alvo | Tipo | Sistema |
|---|---|---|
| [Petstore API](https://petstore.swagger.io) | Testes de API (REST) | API pública de exemplo — simula uma petshop |
| [SauceDemo](https://www.saucedemo.com) | Testes Web (UI) | Loja virtual de exemplo criada para QA |

---

## Tecnologias

| Camada | Biblioteca | Versão |
|---|---|---|
| Linguagem | Python | 3.11+ |
| Runner de testes | pytest | 8.x |
| Automação Web | Selenium | 4.18+ |
| Cliente HTTP | requests | 2.31+ |
| Validação de Schema | jsonschema | 4.21+ |
| Geração de dados | Faker | 24.x |
| Logging | Loguru | 0.7+ |
| Relatórios | Allure + pytest-html | 2.13+ / 4.1+ |
| Execução paralela | pytest-xdist | 3.5+ |
| Linting | Ruff | 0.3+ |

---

## Arquitetura

O projeto é dividido em duas frentes: **API** e **Web**. Ambas seguem o mesmo princípio: separar a lógica de interação com o sistema da lógica de verificação (asserções).

### Testes de API — Service Object Pattern

```
ClienteBase  (core/api/base_client.py)
  └─ Gerencia: sessão HTTP, headers, timeout, logs de requisição/resposta
  └─ Retorna: RespostaHTTP

RespostaHTTP  (core/api/tratador_resposta.py)
  └─ .verificar_status(codigo)           → verifica o código HTTP
  └─ .verificar_schema(schema)           → valida a estrutura do JSON
  └─ .verificar_tempo_abaixo_de(ms)      → verifica tempo de resposta

ServicoPet / ServicoLoja / ServicoUsuario  (services/)
  └─ Cada método = uma operação de negócio (ex: adicionar_pet, buscar_por_id)
  └─ Sem asserções nos serviços — apenas nos testes
```

**Fluxo de dados:**

```
Teste → Service Object → ClienteBase → Requisição HTTP → RespostaHTTP → Asserção
```

---

### Testes Web — Page Object Model (POM)

```
PaginaBase  (core/web/base_page.py)
  └─ Gerencia: WebDriverWait, esperas explícitas, screenshots
  └─ Helpers: _clicar, _digitar, _encontrar, _esta_visivel

PaginaLogin → PaginaInventario → PaginaCarrinho → PaginaCheckout  (pages/)
  └─ Cada página expõe ações do usuário, não seletores brutos
  └─ Métodos de navegação retornam o próximo Page Object (encadeamento)
```

**Exemplo de encadeamento de páginas:**

```python
confirmacao = (
    PaginaLogin(driver)
    .fazer_login(usuario, senha)
    .adicionar_produto_carrinho("Sauce Labs Backpack")
    .ir_para_carrinho()
    .ir_para_checkout()
    .preencher_dados_cliente("João", "Silva", "12345")
    .continuar_para_resumo()
    .finalizar_pedido()
)
assert "Thank you" in confirmacao.obter_mensagem_confirmacao()
```

---

## Estrutura de Pastas

```
suite-automacao-qa/
├── .github/
│   └── workflows/
│       └── main.yml
├── config/
│   └── configuracoes.py
├── core/
│   ├── api/
│   │   ├── base_client.py
│   │   └── tratador_resposta.py
│   └── web/
│       ├── base_page.py
│       └── driver_factory.py
├── services/
│   ├── pet_service.py
│   ├── store_service.py
│   └── user_service.py
├── pages/
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── api/
│   │   ├── conftest.py
│   │   ├── test_pet.py
│   │   ├── test_store.py
│   │   └── test_user.py
│   └── web/
│       ├── conftest.py
│       └── test_e2e_sauce.py
├── utils/
│   ├── data_factory.py
│   └── logger.py
├── reports/
├── pyproject.toml
└── .env.example
```

---

## Como Executar

### Pré-requisitos

- Python 3.11 ou superior
- Google Chrome ou Firefox instalado
- Git

### 1. Clonar e instalar

```bash
git clone <url-do-repositorio>
cd suite-automacao-qa

python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate

pip install -e ".[dev]"
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

O arquivo `.env.example` já contém os valores padrão para execução local. Nenhuma alteração é necessária para começar.

### 3. Executar todos os testes

```bash
pytest
```

### 4. Executar por camada

```bash
pytest tests/api/ -m api -v

pytest tests/web/ -m web -v
```

### 5. Executar em modo headless (sem abrir o browser)

```bash
NAVEGADOR_SEM_INTERFACE=true pytest tests/web/ -m web -v
```

### 6. Execução paralela

```bash
pytest -n auto
pytest -n 4
```

### 7. Gerar relatórios

```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results

pytest --html=reports/html/relatorio.html --self-contained-html
```

---

## CI/CD — GitHub Actions

O arquivo `.github/workflows/main.yml` define um pipeline automático com três jobs:

```
testes-api ──────────────────────────────────┐
                                              ├─→ publicar-relatorio-allure (apenas na main)
testes-web (Chrome headless) ────────────────┘
```

### Gatilhos do pipeline

| Evento | Comportamento |
|---|---|
| Push para `main` ou `develop` | Executa suítes de API + Web |
| Pull Request | Executa suítes de API + Web |
| Agendamento diário às 06:00 UTC | Regressão completa |
| `workflow_dispatch` | Manual — escolha de suíte e ambiente |

### Artefatos gerados por execução

| Artefato | Retenção |
|---|---|
| `allure-results-api` | 30 dias |
| `allure-results-web` | 30 dias |
| `relatorio-html-api` | 30 dias |
| `relatorio-html-web` | 30 dias |
| `screenshots-falha` | 7 dias (apenas em falha) |

O relatório Allure é publicado automaticamente no GitHub Pages a cada push na branch `main`.

### Segredos necessários no GitHub

| Secret | Descrição |
|---|---|
| `PETSTORE_BASE_URL` | URL base da API Petstore |
| `SAUCEDEMO_BASE_URL` | URL do SauceDemo |
| `SAUCEDEMO_USER` | Usuário do SauceDemo |
| `SAUCEDEMO_PASSWORD` | Senha do SauceDemo |

---

## Pipeline em Funcionamento

> Screenshots da execução mais recente no GitHub Actions

**Testes de API — 26 testes, todos passando:**

![Pipeline API](docs/pipeline-api.png)

**Testes Web — 16 testes, todos passando:**

![Pipeline Web](docs/pipeline-web.png)

**Relatório Allure publicado no GitHub Pages:**

![Allure Report](docs/allure-report.png)

---

## Decisões de Design

| Decisão | Motivo |
|---|---|
| Sem `time.sleep()` | Todas as esperas usam `WebDriverWait` com condições explícitas para eliminar flakiness |
| Sem asserções em Service/Page Objects | Separação total entre interação e verificação |
| Fixtures com `yield` | Garante teardown mesmo em caso de falha no teste |
| Screenshots automáticos em falha | Hook `pytest_runtest_makereport` captura evidências sem boilerplate nos testes |
| Dados dinâmicos com Faker | Evita colisão de dados em execuções paralelas |
