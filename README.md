# Blog

Python 3.12, Django 5.2 LTS, django-bootstrap4 и WhiteNoise. Исходник: https://github.com/Denbay0/blog. Публикации публичны; редактировать может только автор. Каталог приложения `blogs` сохраняет внутреннюю метку миграций `posts` ради переноса старой базы. Миграция 0002 переименовывает модель и поля, сохраняя записи и владельцев. Три демонстрационные записи создайте после `createsuperuser` через `/admin/`.

## Локально

```bash
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Для каждого проекта создайте собственное окружение. Проверки: `python manage.py check`, `python manage.py test`, `python manage.py makemigrations --check --dry-run`, `python manage.py migrate --plan`.

## Docker и сервер

Скопируйте `.env.example` в `.env`. Установите уникальный случайный `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` с IP/доменом сервера и свободный `APP_PORT` (локально 8002). `.env` не коммитить.

```bash
docker compose up -d --build
docker compose logs --tail 100 web
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py check --deploy
docker compose restart web
```

При запуске контейнер применяет миграции; Dockerfile собирает статику. SQLite хранится в именованном томе, который сохраняется при пересборке и перезапуске. Перед обновлением экспортируйте том или сделайте резервную копию базы. Для обновления загрузите новые исходники и повторите `docker compose up -d --build`. Не выполняйте `down -v`.

Обязательные переменные: `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `APP_PORT`. `DJANGO_DEBUG=0` и путь базы внутри тома задаются Compose. При запуске без Docker база находится в `db.sqlite3`; путь можно задать через `DJANGO_DB_PATH`.

Через HTTP по учебному IP `check --deploy` ожидаемо сообщает предупреждения HSTS/HTTPS и secure cookie. Для боевого HTTPS настройте TLS и соответствующие флаги Django.
