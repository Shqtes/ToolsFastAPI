# FastAPI Example

Пример полноценного API, реализованного на FastAPI + SQLAlchemy с внедрением JWT-авторизации.

## Status

🚧 MVP готов (Учебный проект)

## Tech Stack

**API:** FastAPI + SQLAlchemy

**СУБД**: PostgreSQL

**Валидация JSON**: Pydantic

## Features

- JWT Аутентификация
- Хеширование паролей (pwdlib)
- Операции CRUD
- Пагинация (skip / limit)
- Async SQLAlchemy ORM
- PostgreSQL database
- Валидация запросов (Pydantic)
- Конфигурация окружения (.env)

## Architecture

Проект построен по слоям:

- API (роутеры FastAPI)
- Schemas (Pydantic-модели)
- Models (SQLAlchemy ORM)
- Authentication (JWT + Хеширование паролей)
- Database (Асинхронные сессии SQLAlchemy)

## Installation

Клонирование кода репозитория:

```bash
git clone https://github.com/Shqtes/ToolsFastAPI
```

Установка зависимостей проекта:

```bash
pip install -r requirements.txt
```

Запуск API на ASGI-сервере:

```bash
  uvicorn main:app --reload
```

Создание таблиц БД:

```postgres-sql
CREATE TABLE IF NOT EXISTS users
(
	user_id SERIAL PRIMARY KEY NOT NULL,
	email TEXT NOT NULL UNIQUE,
	password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tools
(
	tool_id SERIAL NOT NULL,
	"name" VARCHAR(25) NOT NULL,
	description TEXT NULL,
	price NUMERIC(7, 2) NOT NULL,
	quantity INTEGER NOT NULL,
	CONSTRAINT pk_tools PRIMARY KEY (tool_id)
);
```

## Environment Variables

Создайте файл `.env`:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/database

JWT_SECRET_KEY=your_secret_key

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

REFRESH_TOKEN_EXPIRE_DAYS=7
```

## API Reference

### Регистрация в системе

```http
  POST /auth/register
```

#### Входные параметры:

| Параметр   | Тип      | Местоположение | Описание                               |
|:-----------|:---------|:---------------|:---------------------------------------|
| `Email`    | `String` | `Body`         | `Адрес электронной почты пользователя` |
| `Password` | `String` | `Body`         | `Пароль учётной записи пользователя`   |

#### Ответ сервера:

| STATUS_CODE     | Content-Type       |
|:----------------|:-------------------|
| `201 (Created)` | `application/json` |

Пример ответа:

```json
{
  "email": "new_user@example.com",
  "user_id": 1
}
```

| STATUS_CODE         | Content-Type       |
|:--------------------|:-------------------|
| `400 (Bad Request)` | `application/json` |

Пример ответа:

```json
{
  "detail": "Email already exists"
}
```

### Авторизация в системе

```http
  POST /auth/login
```

#### Входные параметры:

| Параметр   | Тип      | Местоположение | Описание                               |
|:-----------|:---------|:---------------|:---------------------------------------|
| `Email`    | `String` | `Body`         | `Адрес электронной почты пользователя` |
| `Password` | `String` | `Body`         | `Пароль учётной записи пользователя`   |

#### Ответ сервера:

| STATUS_CODE | Content-Type       |
|:------------|:-------------------|
| `200 (OK)`  | `application/json` |

Пример ответа:

```json
{
  "access_token": "your_token",
  "refresh_token": "your_refresh_token",
  "token_type": "bearer"
}
```

| STATUS_CODE          | Content-Type       |
|:---------------------|:-------------------|
| `401 (Unauthorized)` | `application/json` |

Пример ответа:

```json
{
  "detail": "Invalid credentials"
}
```

### Получить информацию о себе

```http
  GET /users/me
```

#### Входные параметры:

| Параметр        | Тип            | Местоположение | Описание                |
|:----------------|:---------------|:---------------|:------------------------|
| `Authorization` | `Bearer-Token` | `Headers`      | `Токен для авторизации` |

#### Ответ сервера:

| STATUS_CODE | Content-Type       |
|:------------|:-------------------|
| `200 (OK)`  | `application/json` |

Пример ответа:

```json
{
  "id": 3,
  "email": "shqtes@gmail.com"
}
```

| STATUS_CODE          | Content-Type       |
|:---------------------|:-------------------|
| `401 (Unauthorized)` | `application/json` |

Пример ответа:

```json
{
  "detail": "Invalid token"
}
```

### Получить новый access-токен

```http
  POST /auth/refresh
```

#### Входные параметры:

| Параметр        | Тип      | Местоположение | Описание                     |
|:----------------|:---------|:---------------|:-----------------------------|
| `Refresh-token` | `String` | `Body`         | `Refresh-токен пользователя` |

#### Ответ сервера:

| STATUS_CODE | Content-Type       |
|:------------|:-------------------|
| `200 (OK)`  | `application/json` |

Пример ответа:

```json
{
  "access_token": "your_access_token",
  "token_type": "bearer"
}
```

| STATUS_CODE          | Content-Type       |
|:---------------------|:-------------------|
| `401 (Unauthorized)` | `application/json` |

Пример ответа:

```json
{
  "detail": "Invalid refresh token"
}
```

### Получить все инструменты

```http
  GET /tools/
```

#### Входные параметры:

| Параметр        | Тип            | Местоположение | Описание                                               |
|:----------------|:---------------|:---------------|:-------------------------------------------------------|
| `Authorization` | `Bearer-Token` | `Headers`      | `Токен для авторизации`                                |
| `Skip`          | `Int`          | `Query`        | `Параметр для пропуска ненужных записей`               |
| `Limit`         | `Int`          | `Query`        | `Параметр для ограничения кол-ва возвращаемых записей` |

#### Ответ сервера:

| STATUS_CODE | Content-Type       |
|:------------|:-------------------|
| `200 (OK)`  | `application/json` |

Пример ответа:

```json
[
  {
    "name": "Отвёртка",
    "description": "Крутая отвёртка",
    "price": "999.99",
    "quantity": 1,
    "tool_id": 1
  },
  {
    "name": "Пила",
    "description": "Makita",
    "price": "5999.99",
    "quantity": 1,
    "tool_id": 2
  }
]
```

| STATUS_CODE          | Content-Type       |
|:---------------------|:-------------------|
| `401 (Unauthorized)` | `application/json` |

Пример ответа:

```json
{
  "detail": "Invalid token"
}
```

Или

```json
{
  "detail": "Token required"
}
```

### Получить инструмент

```http
  GET /tools/{tool_id}
```

#### Входные параметры:

| Параметр        | Тип            | Местоположение | Описание                |
|:----------------|:---------------|:---------------|:------------------------|
| `Authorization` | `Bearer-Token` | `Headers`      | `Токен для авторизации` |
| `tool_id`       | `Int`          | `Path`         | `Идентификатор ресурса` |

#### Ответ сервера:

| STATUS_CODE | Content-Type       |
|:------------|:-------------------|
| `200 (OK)`  | `application/json` |

Пример ответа:

```json
{
  "name": "Отвёртка",
  "description": "Крутая отвёртка",
  "price": "999.99",
  "quantity": 1,
  "tool_id": 1
}
```

| STATUS_CODE          | Content-Type       |
|:---------------------|:-------------------|
| `401 (Unauthorized)` | `application/json` |

Пример ответа:

```json
{
  "detail": "Token required"
}
```

Или

```json
{
  "detail": "Invalid token"
}
```

| STATUS_CODE       | Content-Type       |
|:------------------|:-------------------|
| `404 (Not Found)` | `application/json` |

Пример ответа:

```json
{
  "detail": "Tool not found"
}
```

### Добавить инструмент

```http
  POST /tools/
```

#### Входные параметры:

| Параметр        | Тип            | Местоположение | Описание                |
|:----------------|:---------------|:---------------|:------------------------|
| `Authorization` | `Bearer-Token` | `Headers`      | `Токен для авторизации` |
| `name`          | `String`       | `Body`         | `Название инструмента`  |
| `description`   | `String`       | `Body`         | `Описание инструмента`  |
| `price`         | `Decimal`      | `Body`         | `Цена инструмента`      |
| `quantity`      | `Int`          | `Body`         | `Кол-во инструментов`   |

#### Ответ сервера:

| STATUS_CODE     | Content-Type       |
|:----------------|:-------------------|
| `201 (Created)` | `application/json` |

Пример ответа:

```json
{
  "name": "Циркулярная пила",
  "description": "Сделана в Китае",
  "price": "9999.99",
  "quantity": 1,
  "tool_id": 3
}
```

| STATUS_CODE          | Content-Type       |
|:---------------------|:-------------------|
| `401 (Unauthorized)` | `application/json` |

Пример ответа:

```json
{
  "detail": "Token required"
}
```

Или

```json
{
  "detail": "Invalid token"
}
```

| STATUS_CODE                  | Content-Type       |
|:-----------------------------|:-------------------|
| `422 (Unprocessable Entity)` | `application/json` |

Пример ответа:

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "price"
      ],
      "msg": "Field required",
      "input": {
        "name": "string",
        "quantity": 0
      }
    }
  ]
}
```

### Обновить информацию об инструменте

```http
  PATCH /tools/{tool_id}
```

Все поля, кроме Authorization, необязательны.
Передаются только изменяемые значения.

#### Входные параметры:

| Параметр        | Тип            | Местоположение | Описание                |
|:----------------|:---------------|:---------------|:------------------------|
| `Authorization` | `Bearer-Token` | `Headers`      | `Токен для авторизации` |
| `name`          | `String`       | `Body`         | `Название инструмента`  |
| `description`   | `String`       | `Body`         | `Описание инструмента`  |
| `price`         | `Decimal`      | `Body`         | `Цена инструмента`      |
| `quantity`      | `Int`          | `Body`         | `Кол-во инструментов`   |

#### Ответ сервера:

| STATUS_CODE | Content-Type       |
|:------------|:-------------------|
| `200 (OK)`  | `application/json` |

Пример ответа:

```json
{
  "name": "Новый инструмент",
  "description": "Описание",
  "price": "99.99",
  "quantity": 1,
  "tool_id": 9
}
```

| STATUS_CODE          | Content-Type       |
|:---------------------|:-------------------|
| `401 (Unauthorized)` | `application/json` |

Пример ответа:

```json
{
  "detail": "Token required"
}
```

Или

```json
{
  "detail": "Invalid token"
}
```

| STATUS_CODE       | Content-Type       |
|:------------------|:-------------------|
| `404 (Not Found)` | `application/json` |

Пример ответа:

```json
{
  "detail": "Tool not found"
}
```

### Удалить инструмент

```http
  DELETE /tools/{tool_id}
```

#### Входные параметры:

| Параметр        | Тип            | Местоположение | Описание                |
|:----------------|:---------------|:---------------|:------------------------|
| `Authorization` | `Bearer-Token` | `Headers`      | `Токен для авторизации` |
| `tool_id`       | `Int`          | `Path`         | `Идентификатор ресурса` |

#### Ответ сервера:

| STATUS_CODE        | Content-Type       |
|:-------------------|:-------------------|
| `204 (No Content)` |                    |
| `404 (Not Found)`  | `application/json` |

Пример ответа:

```json
{
  "detail": "Tool not found"
}
```

| STATUS_CODE          | Content-Type       |
|:---------------------|:-------------------|
| `401 (Unauthorized)` | `application/json` |

Пример ответа:

```json
{
  "detail": "Token required"
}
```

Или

```json
{
  "detail": "Invalid token"
}
```

## API Documentation

После запуска приложения документация доступна по адресам:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Screenshots

### Swagger UI

![Swagger UI](docs/swagger_ui.png)

### Login endpoint

![Login](docs/login.png)

### Tools

![Tools](docs/tools.png)

## Authors

- [@shqtes](https://github.com/Shqtes)
