# Lab6 — файловый менеджер (FastAPI)

Веб-приложение с полным функционалом лабораторной работы:

1. Файловый менеджер: загрузка, просмотр списка, скачивание, удаление файлов.
2. Аутентификация по логину и паролю из текстового файла `users.txt`.
3. Аутентификация по логину и паролю из MySQL.

Доступ к файловому менеджеру только после входа. На странице входа выберите источник учётных данных.

## Установка

```bash
cd c:\My\Univer\VT\Lab6
pip install -r requirements.txt
```

## Настройка MySQL

Выполните скрипт в MySQL (Workbench, командная строка и т.д.):

```bash
mysql -u root -p < schema.sql
```

Пароль и другие настройки можно положить в файл `.env` в корне проекта (загружается автоматически):

```
DB_PASSWORD=ваш_пароль_mysql
DB_HOST=localhost
DB_USER=root
DB_NAME=lab6_auth
SECRET_KEY=случайная-строка-для-сессий
```

## Запуск

```bash
uvicorn main:app --reload
```

Откройте в браузере: http://127.0.0.1:8000

## Учётные записи для проверки

| Источник | Логин   | Пароль    |
|----------|---------|-----------|
| Файл     | admin   | admin123  |
| Файл     | user    | pass      |
| MySQL    | admin   | admin123  |
| MySQL    | dbuser  | dbpass    |

## Проверка

1. Без входа откройте `/` — редирект на `/login`.
2. Вход с источником «Текстовый файл» и учёткой из `users.txt`.
3. Вход с источником «MySQL» и учёткой из БД.
4. Загрузите файл, убедитесь, что он в списке, скачайте и удалите.
5. `/logout` — снова требуется вход.

> В production пароли следует хранить в виде хеша (bcrypt, argon2), а не в открытом виде.

## Деплой через Docker

Нужны [Docker Desktop](https://www.docker.com/products/docker-desktop/) (или Docker Engine + Docker Compose).

### 1. Подготовка

Скопируйте пример настроек и задайте пароль MySQL и секрет сессий:

```powershell
cd c:\My\Univer\VT\Lab6
copy .env.example .env
# Отредактируйте .env: DB_PASSWORD, SECRET_KEY
```

В `.env` должен быть `DB_PASSWORD` — он используется и контейнером MySQL, и приложением.

### 2. Сборка и запуск

```powershell
docker compose up -d --build
```

Первый запуск занимает 1–2 минуты: MySQL поднимается, выполняется `schema.sql`, затем стартует приложение.

Откройте: http://localhost:8000

### 3. Полезные команды

```powershell
docker compose ps          # статус контейнеров
docker compose logs -f app # логи приложения
docker compose down        # остановить
docker compose down -v     # остановить и удалить тома (БД и uploads сбросятся)
```

### 4. Добавить пользователя в MySQL в Docker

```powershell
docker compose exec db mysql -uroot -p%DB_PASSWORD% lab6_auth -e "INSERT INTO users (username, password) VALUES ('Pavel', '0227');"
```

В PowerShell пароль подставьте вручную (из `.env`):

```powershell
docker compose exec db mysql -uroot -p0227 lab6_auth -e "INSERT INTO users (username, password) VALUES ('Pavel', '0227');"
```

### 5. Что поднимается

| Сервис | Описание |
|--------|----------|
| `db` | MySQL 8, данные в томе `mysql_data` |
| `app` | FastAPI на порту `APP_PORT` (по умолчанию 8000) |

Файл `users.txt` монтируется в контейнер — вход через «Текстовый файл» работает без пересборки образа. Загруженные файлы хранятся в томе `uploads_data`.

### Локальный запуск vs Docker

| Параметр | Локально (`uvicorn`) | Docker Compose |
|----------|----------------------|----------------|
| `DB_HOST` | `localhost` | `db` (имя сервиса) |
| MySQL | ваш MySQL80 на Windows | контейнер `lab6-mysql` |
