# booking_project
Сервис бронирования переговорных комнат на FastAPI


# Meeting Room Booking API

Сервис для бронирования переговорных комнат.  
Реализована JWT-аутентификация, разграничение ролей (админ/сотрудник), хранение данных в PostgreSQL.

## Быстрый старт

```bash
# Клонировать репозиторий
git clone https://github.com/Kirill-5/booking_project.git
cd booking_project

# Запустить через Docker Compose
docker-compose up --build


После запуска API доступно по адресу: http://localhost:8000/docs

Тестовые пользователи
Роль	Логин	Пароль
Администратор	admin	admin123
Сотрудник	employee1	pass123
Сотрудник	employee2	pass456
API Эндпоинты
Все эндпоинты (кроме /login) требуют JWT токен в заголовке:
Authorization: Bearer <ваш_токен>

Метод	Эндпоинт	Описание
POST	/login	Получить JWT токен
GET	/rooms	Список всех комнат
GET	/availability?date=YYYY-MM-DD	Расписание на дату (свободные / занятые слоты)
POST	/bookings	Создать бронирование
GET	/bookings	Мои бронирования
DELETE	/bookings/{id}	Отменить бронирование

Запуск тестов
⚠️ Важно: Тесты не очищают базу данных автоматически. Перед запуском нужно очистить таблицу бронирований.
# Очистить бронирования (обязательно!)
docker exec -it postgres_booking psql -U postgres -d booking_db -c "DELETE FROM bookings;"

# Запустить тесты
poetry run pytest test_main.py -v

Структура проекта
booking_project/
├── main.py              # Эндпоинты и бизнес-логика
├── database.py          # Подключение к PostgreSQL
├── models.py            # SQLAlchemy модели
├── schemas.py           # Pydantic схемы
├── config.py            # Настройки из .env
├── test_main.py         # Pytest тесты
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml       # Зависимости (poetry)
├── poetry.lock
└── README.md


Технологии
Python 3.12
FastAPI
PostgreSQL + SQLAlchemy
JWT (AuthX)
Docker / Docker Compose
Pytest
