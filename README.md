# Medicine Schedule Service

Сервис для создания и получения расписания приёма лекарств. Поддерживает REST и gRPC-интерфейсы. Использует PostgreSQL.

## Зависимости

Перед тем как развернуть приложение, убедитесь, что у вас установлены следующие инструменты:

- Python 3.12
- PostgreSQL
- Docker + Docker Compose
- just

## Шаги для развертывания

### 1. Клонируйте репозиторий

Скачайте репозиторий на свою локальную машину.

   ```bash
   git clone https://github.com/polinaboevaa/python-mobile-app.git
   cd your-repository-folder
   ```

### 2. Создайте `.env` файл

Создайте файл `.env` в корне проекта по примеру:

#### настройки БД для разработки:
- DEV_DB_USER=
- DEV_DB_PASS=
- DEV_DB_NAME=
- DEV_DB_PORT=
- DEV_DB_HOST=

#### настройки БД для тестирования:
- TEST_DB_USER=
- TEST_DB_PASS=
- TEST_DB_NAME=
- TEST_DB_PORT=
- TEST_DB_HOST=

### 2. Соберите и запустите контейнеры

```bash
docker-compose up -d
```

### 3. Примените миграции к базе данных разработки

```bash
docker-compose exec app alembic upgrade head
```

### Доступ к сервисам

| Тип  | Адрес                   |
| ---- | ----------------------- |
| REST | `http://localhost:8002` |
| gRPC | `localhost:50051`       |

### Тестирование

Для тестов запустите команду

```bash
just test
```


