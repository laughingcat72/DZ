# llm-p

FastAPI service with JWT auth, SQLite, and OpenRouter LLM proxy.

## Установка

```bash
pip install uv
uv venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

## Зависимости

```bash
uv pip install -e .
```

## .env

Создать файл `.env` по примеру `.env.example`.

```env
APP_NAME=llm-p
ENV=local

JWT_SECRET=change_me_super_secret
JWT_ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

SQLITE_PATH=./app.db

OPENROUTER_API_KEY=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openrouter/free
OPENROUTER_SITE_URL=https://example.com
OPENROUTER_APP_NAME=llm-fastapi-openrouter
```

В `OPENROUTER_API_KEY` необходимо вставить API-ключ OpenRouter.

## Запуск

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Структура проекта

```text
llm-p/
├── pyproject.toml
├── README.md
├── .env.example
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── errors.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── session.py
│   │   └── models.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── chat.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── chat_messages.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── openrouter_client.py
│   ├── usecases/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── chat.py
│   └── api/
│       ├── __init__.py
│       ├── deps.py
│       ├── routes_auth.py
│       └── routes_chat.py
└── app.db
```

## Эндпоинты

```text
POST   /auth/register
POST   /auth/login
GET    /auth/me

POST   /chat
GET    /chat/history
DELETE /chat/history

GET    /health
```

## Проверка работы

### Регистрация пользователя

```text
POST /auth/register
```

Email для проверки:

```text
student_surname@email.com
```

![alt text](<Снимок экрана 2026-05-07 182151.png>)

### Логин и получение JWT

```text
POST /auth/login
```

![alt text](<Снимок экрана 2026-05-07 182516.png>)

### Авторизация через Swagger

```text
Authorize
```

![alt text](<Снимок экрана 2026-05-07 182605.png>)
![alt text](<Снимок экрана 2026-05-07 183214.png>)

### Получение текущего пользователя

```text
GET /auth/me
```

![alt text](<Снимок экрана 2026-05-07 183449.png>)


### Запрос к LLM

```text
POST /chat
```

![alt text](<Снимок экрана 2026-05-07 184150.png>)

### Получение истории

```text
GET /chat/history
```

![alt text](<Снимок экрана 2026-05-07 184835.png>)

### Очистка истории

```text
DELETE /chat/history
```

![alt text](<Снимок экрана 2026-05-07 184944.png>)

### Проверка пустой истории

```text
GET /chat/history
```

![alt text](<Снимок экрана 2026-05-07 185055.png>)



