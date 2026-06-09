# Meeting Room Booking API

Сервис бронирования переговорных комнат с JWT-аутентификацией и ролями (админ/сотрудник)

---

## Быстрый старт

Запустить PostgreSQL через Docker:  
​
```bash
docker run --name postgres_booking -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
docker exec -it postgres_booking psql -U postgres -c "CREATE DATABASE booking_db"
```

Затем запустить приложение: ​

```bash
docker-compose up --build
```

API будет доступно по адресу: http://localhost:8000/docs

---

## Тестовые пользователи

| Роль | Логин | Пароль |
|------|-------|--------|
| Администратор | admin | admin123 |
| Сотрудник | employee1 | pass123 |
| Сотрудник | employee2 | pass456 |

---

## API Эндпоинты

Все эндпоинты (кроме /login) требуют заголовок: Authorization: Bearer <ваш_токен>

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | /login | Получить JWT токен |
| GET | /rooms | Список всех комнат |
| GET | /availability?date=YYYY-MM-DD | Расписание на дату |
| POST | /bookings | Создать бронирование |
| GET | /bookings | Мои бронирования |
| DELETE | /bookings/{id} | Отменить бронирование |

---

# Запуск тестов

⚠️ **Важно:** Тесты не очищают базу автоматически. Каждый тест нужно запускать отдельно, очищая БД перед каждым.

## 1. Тесты логина (очистка не требуется)


```bash
poetry run pytest test_main.py::test_login_success -v
poetry run pytest test_main.py::test_login_fail -v
```

2. Тесты бронирования (очищать БД перед каждым)

# Очистить БД
```bash
docker exec -it postgres_booking psql -U postgres -d booking_db -c "DELETE FROM bookings;"
```

# Тест успешного создания
```bash
poetry run pytest test_main.py::test_create_booking_success -v
```

# Снова очистить БД
```bash
docker exec -it postgres_booking psql -U postgres -d booking_db -c "DELETE FROM bookings;"
```

# Тест конфликта
```bash
poetry run pytest test_main.py::test_create_booking_conflict -v
```



<details>
<summary>Результаты тестов</summary>

```bash
test_main.py::test_login_success PASSED                [ 50%]
test_main.py::test_login_fail PASSED                   [100%]
test_main.py::test_create_booking_success PASSED       [100%]
test_main.py::test_create_booking_conflict PASSED      [100%]
```
</details>


## Структура проекта

```
booking_project/
├── main.py              # FastAPI приложениие, эндпоинты, бизнес-логика
├── database.py          # Подключение к PostgreSQL, сессии, базовый класс
├── models.py            # SQLalchemy модели (User, Room, Slot, Booking)
├── schemas.py           # Pydantic схемы для валидации входа/ выхода
├── config.py            # Настройки из .env (подключение к бд)
├── test_main.py         # Тесты (pytest)
├── Dockerfile           # Инструкция для сборки контейнера
├── docker-compose.yml   # Запуск приложения и postgres
├── pyproject.toml       # Зависимости проекта в poetry)
├── poetry.lock          # Фиксация версий зависимостей
└── README.md            # Документация
```

---

## Технологии

- Python 3.12
- FastAPI
- PostgreSQL + SQLAlchemy
- JWT (AuthX)
- Docker / Docker Compose
- Pytest

