# Database Setup – Guia do Administrador

> **Stack:** FastAPI · async SQLAlchemy 2 · Alembic · asyncpg · **PostgreSQL (Neon)**

---

## Índice

1. [Pré-requisitos](#1-pré-requisitos)
2. [Criar o banco no Neon](#2-criar-o-banco-no-neon)
3. [Configurar variáveis de ambiente](#3-configurar-variáveis-de-ambiente)
4. [Instalar dependências Python](#4-instalar-dependências-python)
5. [Inicializar as tabelas](#5-inicializar-as-tabelas)
6. [Migrações com Alembic](#6-migrações-com-alembic)
7. [Popular com dados iniciais (seed)](#7-popular-com-dados-iniciais-seed)
8. [Verificar a instalação](#8-verificar-a-instalação)
9. [Tabelas criadas](#9-tabelas-criadas)
10. [Referência rápida de comandos](#10-referência-rápida-de-comandos)

---

## 1. Pré-requisitos

| Ferramenta | Versão mínima | Observação |
|------------|--------------|------------|
| Python     | 3.11+        | `python --version` |
| pip        | 23+          | `pip --version` |
| Conta Neon | –            | <https://neon.tech> (plano free disponível) |

---

## 2. Criar o banco no Neon

1. Acesse <https://console.neon.tech> e faça login.
2. Clique em **New Project** → dê um nome (ex.: `renovacao-locacao`).
3. Na aba **Connection Details**, selecione o branch `main` e copie a **Connection String**. Ela tem o formato:

   ```
   postgresql://usuario:senha@hostname.neon.tech/nomedb?sslmode=require
   ```

4. Guarde esta string; ela será usada na próxima etapa.

> **Dica:** O Neon habilita SSL por padrão. A string já inclui `?sslmode=require`, o que é necessário para conexões externas.

---

## 3. Configurar variáveis de ambiente

Dentro do diretório `backend/`, copie o arquivo de exemplo e edite-o:

```bash
cd backend
cp .env.example .env
```

Edite o arquivo `.env` com as suas credenciais:

```dotenv
# String de conexão do Neon (substitua pelos seus valores reais)
DATABASE_URL=postgresql://usuario:senha@hostname.neon.tech/nomedb?sslmode=require

# Chave secreta para assinar os JWTs – gere uma string aleatória longa
SECRET_KEY=troque-por-uma-string-longa-e-aleatoria

# Algoritmo JWT (não altere)
ALGORITHM=HS256

# Tempo de expiração do token de acesso em minutos
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Ambiente: development | production
ENVIRONMENT=development
```

### Gerar um SECRET_KEY seguro

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

> **Atenção:** nunca commite o arquivo `.env` no repositório. Ele já está no `.gitignore`.

---

## 4. Instalar dependências Python

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 5. Inicializar as tabelas

### Opção A – Auto-criação via inicialização do servidor (recomendado para desenvolvimento)

O backend cria todas as tabelas automaticamente ao iniciar, através do evento `lifespan` em `src/main.py`:

```python
async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
```

Basta iniciar o servidor:

```bash
cd backend
uvicorn src.main:app --reload
```

Na primeira execução, todas as tabelas serão criadas no banco do Neon.

### Opção B – Criar tabelas via script seed (sem iniciar o servidor)

O script `scripts/seed.py` também chama `create_all` antes de inserir dados:

```bash
cd backend
python -m scripts.seed
```

### Opção C – Migrações Alembic (recomendado para produção)

Veja a seção [6. Migrações com Alembic](#6-migrações-com-alembic) abaixo.

---

## 6. Migrações com Alembic

O projeto usa [Alembic](https://alembic.sqlalchemy.org/) para controle de versão do schema.

> **Como o Alembic sabe a URL do banco?**  
> O arquivo `alembic/env.py` lê automaticamente a variável `DATABASE_URL` do `.env`, portanto **não edite** o `alembic.ini` manualmente.

### 6.1 Gerar a primeira migration (estado inicial)

```bash
cd backend
alembic revision --autogenerate -m "initial_schema"
```

Um arquivo será criado em `alembic/versions/`. Revise-o e então aplique:

```bash
alembic upgrade head
```

### 6.2 Aplicar todas as migrations pendentes

```bash
alembic upgrade head
```

### 6.3 Ver o histórico de migrations

```bash
alembic history --verbose
```

### 6.4 Reverter a última migration

```bash
alembic downgrade -1
```

### 6.5 Reverter tudo

```bash
alembic downgrade base
```

---

## 7. Popular com dados iniciais (seed)

O script `backend/scripts/seed.py` insere dados de exemplo para facilitar testes e desenvolvimento. Ele é idempotente: execuções repetidas não duplicam registros.

```bash
cd backend
python -m scripts.seed
```

### O que é criado

| Tipo | E-mail | Senha | Papel |
|------|--------|-------|-------|
| Usuário Admin | `admin@renovacao.com` | `Admin@123` | `ADMIN` |
| Proprietário | `owner@renovacao.com` | `Owner@123` | `OWNER` |
| Locatário | `renter@renovacao.com` | `Renter@123` | `RENTER` |

Além disso, cria:
- **1 perfil de proprietário** (CPF `12345678901`) associado ao usuário `OWNER`.
- **1 perfil de locatário** (CPF `98765432100`, CNH categoria AB, válida até 31/12/2028) associado ao usuário `RENTER`.
- **1 veículo** Toyota Corolla 2023, placa `ABC1D23`, diária R$ 180,00, status `AVAILABLE`.

> **Aviso de segurança:** as senhas acima são apenas para desenvolvimento. Em produção, crie um usuário admin com senha forte via API ou altere diretamente no banco, e remova os usuários de exemplo.

### Criar o administrador em produção via API

```bash
curl -X POST https://seu-dominio.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@suaempresa.com",
    "password": "SenhaForte@2024",
    "full_name": "Administrador",
    "role": "ADMIN"
  }'
```

---

## 8. Verificar a instalação

### 8.1 Endpoint de health check

```bash
curl http://localhost:8000/health
# Resposta esperada: {"status":"ok","environment":"development"}
```

### 8.2 Documentação interativa (Swagger)

Acesse <http://localhost:8000/docs> no navegador.

### 8.3 Testar login com o admin seed

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@renovacao.com","password":"Admin@123"}'
```

A resposta deve retornar um `access_token` JWT.

---

## 9. Tabelas criadas

| Tabela | Domínio DDD | Descrição |
|--------|-------------|-----------|
| `users` | auth | Credenciais e papéis dos usuários |
| `owners` | owner | Perfis dos proprietários de veículos |
| `vehicles` | vehicle | Veículos cadastrados |
| `vehicle_documents` | vehicle | Documentos dos veículos |
| `renters` | renter | Perfis dos locatários |
| `rentals` | rental | Contratos de locação |
| `vehicle_costs` | finance | Custos operacionais dos veículos |

### Diagrama simplificado de relacionamentos

```
users (1) ──< owners (1) ──< vehicles (1) ──< vehicle_documents
users (1) ──< renters
vehicles (1) ──< rentals >── (1) renters
vehicles (1) ──< vehicle_costs
```

> Os relacionamentos são mantidos por UUIDs de referência. O banco **não possui foreign keys declaradas** no momento (SQLAlchemy `Column(UUID)`); a integridade é garantida pela camada de aplicação.

---

## 10. Referência rápida de comandos

```bash
# ── Ambiente ──────────────────────────────────────────────────
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# ── Configuração ──────────────────────────────────────────────
cp .env.example .env
# editar .env com DATABASE_URL do Neon e SECRET_KEY

# ── Inicializar schema ────────────────────────────────────────
# Opção 1: iniciar o servidor (cria tabelas automaticamente)
uvicorn src.main:app --reload

# Opção 2: via Alembic (recomendado para produção)
alembic revision --autogenerate -m "initial_schema"
alembic upgrade head

# ── Popular banco com dados iniciais ──────────────────────────
python -m scripts.seed

# ── Verificar ─────────────────────────────────────────────────
curl http://localhost:8000/health
# abrir http://localhost:8000/docs
```

---

## Solução de problemas comuns

### `asyncpg.exceptions.InvalidCatalogNameError: database "renovacao_db" does not exist`

Verifique se o nome do banco na `DATABASE_URL` corresponde ao banco criado no Neon.

### `SSL connection is required`

O Neon exige SSL. A string de conexão deve terminar com `?sslmode=require`. O asyncpg aceita este parâmetro automaticamente via SQLAlchemy.

### `ModuleNotFoundError: No module named 'src'`

Execute sempre a partir do diretório `backend/` usando `python -m scripts.seed` (não `python scripts/seed.py`).

### Erro de autenticação no Neon (`password authentication failed`)

Regenere as credenciais no painel do Neon: **Settings → Roles → Reset password**.
