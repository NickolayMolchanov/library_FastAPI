FastAPI Library

REST API для управления библиотекой книг.

Проект разработан на FastAPI и предназначен для работы с книгами и авторами. Реализованы CRUD-операции, связь книг с авторами, поиск, фильтрация, сортировка и пагинация.

Возможности
создание, получение, изменение и удаление книг;
создание, получение, изменение и удаление авторов;
связь книг и авторов по принципу many-to-many;
поиск книг по названию;
фильтрация книг по году и автору;
сортировка книг по году;
пагинация результатов;
валидация входных данных;
обработка HTTP-ошибок;
асинхронная работа с базой данных;
управление структурой базы данных с помощью Alembic.
Стек технологий
Python
FastAPI
SQLAlchemy
Pydantic
SQLite
aiosqlite
Alembic
pytest
Ruff
Структура проекта
fastapi_library/
│
├── app/
│   ├── crud/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── database.py
│   └── main.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
Установка

Клонировать репозиторий:

git clone https://github.com/NickolayMolchanov/library_FastAPI
cd fastapi_library

Создать виртуальное окружение:

python -m venv .venv

Активировать виртуальное окружение в Windows:

.venv\Scripts\activate

Установить зависимости:

pip install -r requirements.txt
База данных

Для создания таблиц необходимо применить миграции Alembic:

alembic upgrade head
Запуск

Запустить приложение:

uvicorn app.main:app --reload

После запуска API будет доступно по адресу:

http://127.0.0.1:8000

Интерактивная документация Swagger:

http://127.0.0.1:8000/docs

Создание новой миграции:

alembic revision --autogenerate -m "описание изменений"

Применение миграций:

alembic upgrade head

Откат последней миграции:

alembic downgrade -1
