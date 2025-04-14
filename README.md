# Upload Service
Это сервис загрузки файлов, основанный на FastAPI, который позволяет загружать файлы в MinIO, сохранять метаданные в PostgreSQL и получать файлы и метаданные через RESTful API. Сервис поддерживает определенные типы файлов (DICOM, JPEG, PNG, PDF) и предоставляет конечные точки для загрузки, получения метаданных и скачивания файлов.
# Структура проекта
```text
├── alembic.ini
├── docker-compose.yaml
├── docker.env
├── Dockerfile
├── docker_run.sh
├── local_run.sh
├── pytest.ini
├── requirements.txt
├── upload_service
│   ├── adapters
│   │   ├── __init__.py
│   │   ├── minio_client.py
│   │   └── repository.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── routers.py
│   │   └── upload.py
│   ├── config.py
│   ├── di
│   │   ├── database.py
│   │   ├── __init__.py
│   │   ├── minio_client.py
│   │   ├── repository.py
│   │   └── upload_service.py
│   ├── domain
│   │   ├── dto.py
│   │   ├── __init__.py
│   │   ├── models.py
│   ├── entrypoints
│   │   ├── fastapi_app.py
│   │   ├── __init__.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── env.py
│   │   ├── README
│   │   ├── script.py.mako
│   │   └── versions
│   │       ├── 149e78bc7b69_change_filemetadata_id_to_file_id.py
│   │       ├── c33ca3b8ce5c_initial_migration.py
│   ├── services
│   │   ├── __init__.py
│   │   └── upload_service.py
│   └── tests
│       ├── conftest.py
│       ├── __init__.py
│       └── test_upload_api.py
```
# Предварительные требования
### Для Docker
* Docker: Установите [Docker](https://docs.docker.com/get-started/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/)

### Для локального запуска:
* Python3.13: Установите [Python 3.13](https://www.python.org/downloads/)
* PostgreSQL: Установите [PostgreSQL 15](https://www.postgresql.org/download/) и убедитесь, что сервер запущен локально
* MinIO: Установите и запустите [MinIO](https://min.io/docs/minio/linux/index.html) локально или используйте Docker-контейнер

# Настройка
### Конфигурация окружения
Как для docker, так и для локального запуска используются переменные окружения.
Файлы ```docker.env``` и ```.env``` уже созданы. 

Если запускать через docker - ничего можно не настраивать.

Если локально - обновить переменные окружения в ```.env```

# Запуск приложения
### Через Docker
1. ***Клонируйте репозиторий***
```bash
# через http
git clone https://github.com/MaxPositive/upload_service_test_task.git
# через ssh
git clone git@github.com:MaxPositive/upload_service_test_task.git
cd upload_service_test_task
```
2. ***Запускает docker-compose***
```bash
docker compose up
```
* Собирает образ upload-service.
* Запускает upload-service (FastAPI на http://localhost:8000), postgres (порт 5433) и minio (порты 9000 для API, 9001 для консоли).
Для проверки MinIO можно перейти по адресу http://localhost:9001
* Применяет миграции базы данных через docker_run.sh.
* Флаг --reload включает авто-перезагрузку для разработки.
3. ***Доступ к приложению***
* API: Откройте http://localhost:8000/docs для Swagger UI
* Консоль MinIO: Откройте http://localhost:9001 (логин: ```minioadmin```, пароль: ```minioadmin```)
* PostgreSQL: Подключитесь к ```localhost:5433``` c ```user=postgres, password=postgres, database=diagnosix```

4. ***Остановка сервисов***
```bash
docker compose down
```
* Для удаления томов (очистка базы данных и данных MinIO):
* ```bash
    docker-compose down -v
    ```

#### Локально
1. ***Клонируйте репозиторий***
```bash
# через http
git clone https://github.com/MaxPositive/upload_service_test_task.git
# через ssh
git clone git@github.com:MaxPositive/upload_service_test_task.git
cd upload_service_test_task
```
2. ***Настройте PostgreSQL***
* Запустите локальный сервер PostgreSQL или используйте Docker:
* ```bash
  docker run -d --name postgres -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=diagnosix postgres:15
    ```
* Обновите ```.env```, если используется другой хост/порт:
* ```bash
  POSTGRES_URL=postgresql+psycopg://postgres:postgres@localhost:5432/diagnosix
    ```
3. ***Настройка MinIO***:
* Запустите локальный сервер MinIO:
* ```bash
  docker run -d --name minio -p 9000:9000 -p 9001:9001 -e MINIO_ROOT_USER=minioadmin -e MINIO_ROOT_PASSWORD=minioadmin minio/minio server /data --console-address ":9001"
    ```
* Обновите ```.env```
* ```bash
  MINIO_ENDPOINT=localhost:9000
    ```
4. ***Запустите приложение***
* Используйте предоставленный скрипт ```local_run.sh```
* ```bash
  chmod +x local_run.sh
  ./local_run.sh
    ```
* Скрипт:
  * Проверяет наличие Python 3.13
  * Создает и активирует виртуальное окружение (.venv)
  * Устанавливает зависимости из requirements.txt
  * Применяет миграции базы данных с помощью alembic
  * Запускает сервер FastAPI на http://localhost:8000 с флагом --reload

5. Доступ к приложению
* API: Откройте http://localhost:8000/docs.
* Консоль MinIO: Откройте http://localhost:9001 (если MinIO запущен).
* PostgreSQL: Подключитесь к localhost:5432 (если запущен локально).

6. Остановка приложения
* Остановите контейнеры MinIO и PostgreSQL (если использовались):
* ```bash
    docker stop minio postgres
    docker rm minio postgres
    ```
# Запуск тестов
### Через Docker
Запустите контейнер через docker compose и выполните следующую команду в консоли:
```bash
docker-compose run -it upload-service pytest upload_service/tests/ -v
```

### Локально
Запускает тесты в консоли через команду:
```bash
pytest upload_service/tests -v
```

# API

* ```POST /upload/```:
  * Загружает файл в MinIO и сохраняет метаданные в PostgreSQL
  * Запрос: ```multipart/form-data``` с файлом (поддерживаемые типы: ```application/dicom, image/jpeg, image/png, application/pdf```)
  * Ответ: ```201 Created``` с ```FileUploadResponse``` (```file_id, filename, content_type, file_size, minio_url```)
  * Ошибка: ```422 Unprocessable Content ``` для неподдерживаемых типов файлов

* ```GET /upload/{file_id}```:
  * Получает метаданные файла из PostgreSQL
  * Ответ: ```200 OK``` с ```FileUploadResponse (```file_id, filename, content_type, file_size, minio_url```)
  * Ошибка: ```404 Not Found``` если файл или метаданные отсутствуют
* ```GET /upload/{file_id}/download```
  * Загружает файл из MinIO
  * Ответ: ```200 OK``` и загруженный файл
  * Ошибка: ```404 Not Found``` если файл или метаданные не найдены
  

# Примеры запросов
1. [```POST /upload/```](images/upload_file.png)
2. [```GET /upload/{file_id}```](images/get_file_metadata.png)
3. [```GET /upload/{file_id}``` с ошибкой](images/get_unexisted_file_metadata.png)
4. [```GET /upload/{file_id}/download```](images/downloading_file.png)
5. [```GET /upload/{file_id}/download``` с ошибкой](images/download_file_error.png)
 
