# Blog

Учебный Django-блог: публикации доступны всем, а создавать и изменять их могут авторизованные авторы. Редактирование чужих публикаций запрещено.

## Возможности

- публичная лента, новые записи сверху, отдельные страницы;
- регистрация, вход, POST-выход;
- создание публикаций и редактирование только автором;
- admin с поиском, фильтрами и навигацией по датам;
- тесты публичного доступа и прав владельца.

## Локальный запуск

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Проверки: `python manage.py check && python manage.py test`.

## Docker

Скопируйте `.env.example` в `.env` и запустите `docker compose up --build`. Порт: `8002`.

Hub: https://github.com/Denbay0/practice_hub

## Screenshots

Скриншоты можно добавить в `docs/screenshots/` после запуска.
