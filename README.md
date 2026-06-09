# Meeting Room Booking API

Сервис бронирования переговорных комнат с JWT-аутентификацией и ролями (админ/сотрудник)

---

## Быстрый старт

Запустите PostgreSQL через Docker:

docker run --name postgres_booking -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
docker exec -it postgres_booking psql -U postgres -c "CREATE DATABASE booking_db"

Затем запустите приложение:

docker-compose up --build

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

## Запуск тестов

Важно: Тесты не очищают базу автоматически. Перед запуском нужно очистить таблицу bookings.

docker exec -it postgres_booking psql -U postgres -d booking_db -c "DELETE FROM bookings;"
poetry run pytest test_main.py -v

Если имя контейнера изменилось, посмотрите его через docker ps и подставьте в команду.

---

## Остановка

docker-compose down
docker start postgres_booking

---

## Структура проекта

booking_project/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── config.py
├── test_main.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
└── README.md

---

## Технологии

- Python 3.12
- FastAPI
- PostgreSQL + SQLAlchemy
- JWT (AuthX)
- Docker / Docker Compose
- Pytest
