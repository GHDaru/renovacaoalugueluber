<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Renovação Locação – Marketplace de Aluguel de Veículos

Plataforma de locação de veículos para motoristas de aplicativos, construída com arquitetura **DDD (Domain-Driven Design)**.

## Tech Stack

| Camada    | Tecnologia                       |
|-----------|----------------------------------|
| Frontend  | React 19 + Vite + TypeScript     |
| Backend   | FastAPI + SQLAlchemy 2 + Alembic |
| Banco     | PostgreSQL                       |
| Auth      | JWT (python-jose)                |

---

## Estrutura do Projeto

```
renovacaoalugueluber/
├── frontend/          # React 19 + Vite (landing page + páginas futuras)
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── src/
│       ├── App.tsx
│       ├── index.tsx
│       ├── components/          # Componentes da landing page
│       ├── pages/               # Páginas por papel de usuário
│       │   ├── LandingPage.tsx
│       │   ├── admin/           # Dashboard, VehicleCosts
│       │   ├── owner/           # RegisterVehicle
│       │   ├── marketplace/     # VehicleListing
│       │   └── renter/          # Register
│       ├── services/api.ts      # Cliente Axios com JWT
│       └── types/index.ts       # Interfaces TypeScript para todos os domínios
│
└── backend/           # FastAPI DDD API
    ├── alembic/       # Migrações de banco de dados
    ├── alembic.ini
    ├── requirements.txt
    └── src/
        ├── main.py              # App, CORS, routers, /health
        ├── config.py            # pydantic-settings
        ├── shared/
        │   ├── domain/          # BaseEntity, BaseRepository[T], value objects
        │   └── infrastructure/  # async SQLAlchemy engine + get_db
        └── domains/
            ├── auth/            # JWT + roles: ADMIN / OWNER / RENTER
            ├── owner/           # Proprietários de veículos
            ├── vehicle/         # Cadastro + aprovação (PENDING/APPROVED/REJECTED/SUSPENDED)
            ├── renter/          # Motoristas locatários (CNH)
            ├── rental/          # Contratos diários (PENDING→ACTIVE→COMPLETED/CANCELLED)
            └── finance/         # Custos e resumo financeiro – somente ADMIN
```

Cada domínio segue a estrutura de 4 camadas:

```
<domain>/
├── domain/          # Entidades, value objects, eventos, interfaces de repositório
├── application/     # Use cases, DTOs (Pydantic v2)
├── infrastructure/  # Modelos SQLAlchemy + implementações dos repositórios
└── presentation/    # Rotas FastAPI (APIRouter)
```

---

## Como Rodar o Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # Ajuste DATABASE_URL e SECRET_KEY

# Criar as tabelas
alembic upgrade head

# Iniciar o servidor
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Documentação interativa: http://localhost:8000/docs

---

## Como Rodar o Frontend

```bash
cd frontend
npm install
cp .env.example .env   # VITE_API_URL=http://localhost:8000
npm run dev
```

A aplicação sobe em http://localhost:3000.

---

## Domínios

| Domínio     | Prefixo API            | Descrição                                                           |
|-------------|------------------------|---------------------------------------------------------------------|
| **auth**    | `/api/v1/auth`         | Registro, login JWT, papéis: ADMIN / OWNER / RENTER                 |
| **owner**   | `/api/v1/owners`       | Proprietários – cadastro + verificação admin                        |
| **vehicle** | `/api/v1/vehicles`     | Veículos – cadastro, documentos, fluxo de aprovação                 |
| **renter**  | `/api/v1/renters`      | Motoristas – cadastro com CNH + verificação admin                   |
| **rental**  | `/api/v1/rentals`      | Contratos de locação diária com ciclo de vida completo              |
| **finance** | `/api/v1/finance`      | Custos por veículo (MAINTENANCE/IPVA/FINE/…) + resumo financeiro   |


## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`
