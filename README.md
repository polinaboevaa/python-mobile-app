﻿# Мобильное приложение

Это серверная часть для мобильного приложения, которое напоминает пользователям о приёме лекарств. Приложение написано на **FastAPI** и использует **Docker** для удобства развертывания.

## Требования

Перед тем как развернуть приложение, убедитесь, что у вас установлены следующие инструменты:

- **Docker**: для контейнеризации приложения.

## Шаги для развертывания

1. **Клонируйте репозиторий**:

   Скачайте репозиторий на свою локальную машину.

   ```bash
   git clone https://github.com/polinaboevaa/python-mobile-app.git
   cd your-repository-folder

2. **Построение Docker-образа**:

    Используйте команду Docker для сборки образа. Убедитесь, что в корневой директории проекта есть Dockerfile.

    ```bash
    docker build -t mobile-app .

3. **Запуск приложения через Docker**:

    Запустите приложение с помощью Docker, указав порт, на котором приложение будет работать.

    Это откроет приложение на порту 8000. Если вам нужно изменить порт, вы можете отредактировать команду (например, -p 8080:8000).

    ```bash
    docker run -d -p 8000:8000 mobile-app

4. **Проверьте работу приложения**:

    Откройте браузер и перейдите по адресу:

    http://localhost:8000

    Вы должны увидеть рабочий API, и Swagger документацию на странице http://localhost:8000/docs.


