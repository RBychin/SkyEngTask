# SkyEng (Тестовое задание)
## Описание:
Сервис проверяет загруженые файлы с расширением *.py на соответствие стандартам написания кода (PEP8).
Реализована регистрация и авторизация пользователей, авторизированые пользователи могут загружать файлы. Владелец файла может изменять или удалять файл.
После загрузки файла - для этого файла создается лог, который фиксирует время и дату загрузки, изменения файла и статус проверки исходного кода.
Проверка исходного кода проводиться по заданым интервалам, после чего владелец файла получает email уведомление о статусе проверки и найденых ошибках.
Вся информация о количестве предупреждений, дате размещения или обновления, статусе email уведомления - находится на странице файла.

## Стэк:

 - Python 3.10 
 - Django 4.2 
 - Django Celery Beat 2.5 
 - Celery 5.3 
 - Django AllAuth 0.54 
 - PostgreSQL 13.4-alpha
 - Nginx 1.19.3-alpha
 - Gunicorn 21.2
 - Docker (docker compose) 
 - DockerHub
 - PyCharm 
 - GitHub 
 - Ubuntu 22.04

## Запуск:
Для запуска необходимо разместить на сервере директорию `infra` в проекте.
После чего запустить `docker compose` командой: `docker compose up`.
Необходимые образы находятся на Docker Hub и подгрузятся самостоятельно.
После запуска контейнеров, необходимо в контейнере `web` сделать миграции и собрать статику, для этого можно воспользоваться командами:
- `docker-compose exec web python manage.py collectstatic`
- `docker-compose exec web python manage.py makemigrations`
- `docker-compose exec web python manage.py migrate`
Сервис запущен и почти готов к работе.
Командой `docker-compose exec web python manage.py createsuperuser` создайте нового суперпользователя в системе, перейдите в админ панель и создайте правило для отработки задачи в определенный интервал времени.

### Разработчик:
Бычин Роман

По Тестовому заданию от SkyEng