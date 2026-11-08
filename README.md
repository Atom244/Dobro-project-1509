# ПравоСПб

Учебный Django-проект по задаче №1509: сервис о правах граждан, доступной среде и обращениях жителей Санкт-Петербурга.

## Запуск локально

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Основные адреса: `/`, `/appeals/`, `/parking/`, `/rights/`, `/news/`, `/faq/`, `/api/docs/`, `/admin/`.

Полная схема базы данных с ER-диаграммой находится в [`DATABASE_SCHEMA.md`](DATABASE_SCHEMA.md).

Для пользователей с флагом `is_staff` в шапке появляется **Кабинет сотрудника** (`/staff/appeals/`). Это рабочий интерфейс поверх сайта: сводка по статусам, поиск обращений, фильтры, просмотр карточек и изменение статуса с комментарием. Полная техническая настройка контента и пользователей по-прежнему доступна в `/admin/`.

## Docker

Создайте `.env` на основе `.env.example`, задайте `DATABASE_URL=postgresql://pravo_spb:change-me@postgres:5432/pravo_spb`, затем выполните `docker compose up --build`. Docker Desktop должен быть установлен; в текущей среде Docker не доступен.

## Vercel

`vercel.json` использует serverless entrypoint `api/index.py` с `@vercel/python` и перед сборкой автоматически выполняет `migrate` и `collectstatic`. В настройках Vercel укажите корень репозитория (`./`), preset Django и передеплойте проект после добавления этих файлов. Задайте `SECRET_KEY`, `DEBUG=False`, `DATABASE_URL` и `CSRF_TRUSTED_ORIGINS=https://<ваш-домен>.vercel.app`. Настройка `ALLOWED_HOSTS` дополнительно принимает домены `*.vercel.app`; если используется собственный домен, добавьте его в `ALLOWED_HOSTS`, а полный `https://`-адрес — в `CSRF_TRUSTED_ORIGINS`. Serverless-файловая система Vercel эфемерна, поэтому загруженные файлы требуют внешнего хранилища; для production также рекомендуется отдельный хостинг статики.

Данные команды `seed_demo` и контакт demo@example.org являются демонстрационными и не являются официальными сведениями.
