# Renovação Locação – Backend

FastAPI backend com arquitetura DDD para o marketplace de locação de veículos.

## Pré-requisitos

- Python 3.11+
- PostgreSQL 14+

## Configuração

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # Edite DATABASE_URL e SECRET_KEY
```

## Banco de dados

```bash
# Criar as tabelas via Alembic
alembic upgrade head
```

## Rodar o servidor

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Documentação interativa: http://localhost:8000/docs

## Domínios

| Domínio     | Prefixo API           | Acesso              |
|-------------|----------------------|---------------------|
| auth        | `/api/v1/auth`       | Público             |
| owner       | `/api/v1/owners`     | OWNER / ADMIN       |
| vehicle     | `/api/v1/vehicles`   | OWNER / ADMIN / Público (listagem) |
| renter      | `/api/v1/renters`    | RENTER / ADMIN      |
| rental      | `/api/v1/rentals`    | RENTER / ADMIN      |
| finance     | `/api/v1/finance`    | ADMIN only          |

## Estrutura DDD por domínio

```
domains/<domain>/
├── domain/          # Entidades, value objects, eventos, interfaces de repositório
├── application/     # Use cases, DTOs (Pydantic)
├── infrastructure/  # Modelos SQLAlchemy + implementações de repositório
└── presentation/    # Rotas FastAPI (APIRouter)
```
