# TeamFinder

``` Мордасов Кирилл Олегович | Вариант 2```

## Требования

- Python 3.10 или новее
- Docker Desktop с Docker Compose

## Установка

1. Клонируйте репозиторий:

   ```powershell
   git clone https://github.com/Cosmic-Man/team-finder-ad.git
   ```

2. Перейдите в папку проекта:

   ```powershell
   cd team-finder-ad
   ```

Создайте виртуальное окружение, активируйте его и установите зависимости:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Скопируйте файл с примером настроек:

```powershell
Copy-Item .env_example .env
```

В Linux или macOS используйте `cp .env_example .env`. Перед запуском укажите
значения в `.env`:

| Переменная | Назначение |
| --- | --- |
| `DJANGO_SECRET_KEY` | Секретный ключ Django. Используйте случайное приватное значение. |
| `DJANGO_DEBUG` | Включает режим отладки при локальной разработке. |
| `POSTGRES_DB` | Имя базы данных. |
| `POSTGRES_USER` | Пользователь базы данных. |
| `POSTGRES_PASSWORD` | Пароль пользователя базы данных. |
| `POSTGRES_HOST` | Хост базы данных; при локальном запуске Django укажите `localhost`. |
| `POSTGRES_PORT` | Порт базы данных; по умолчанию `5432`. |

Сгенерировать ключ Django можно командой:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Запуск базы и приложения

Запустите PostgreSQL:

```powershell
docker compose up -d
```

Примените миграции. Команда загрузки демонстрационных профилей и проектов
необязательна:

```powershell
python manage.py migrate
python manage.py load_test_data
```

Запустите сервер разработки:

```powershell
python manage.py runserver
```

Откройте [TeamFinder](http://127.0.0.1:8000). Команда `load_test_data` создаёт
семь тестовых пользователей с навыками и проектами. Повторный запуск команды не
создаёт дубликаты. Пароль всех тестовых пользователей — `testpass123`.

| Автор (ФИО) | Контакт-ссылка |
| --- | --- |
| Иван Петров | [ivan@example.com](mailto:ivan@example.com) |
| Анна Смирнова | [anna@example.com](mailto:anna@example.com) |
| Олег Кузнецов | [oleg@example.com](mailto:oleg@example.com) |
| Мария Волкова | [maria@example.com](mailto:maria@example.com) |
| Алексей Соколов | [alexey@example.com](mailto:alexey@example.com) |
| Елена Морозова | [elena@example.com](mailto:elena@example.com) |
| Тимур Ахметов | [timur@example.com](mailto:timur@example.com) |

Создать учётную запись администратора можно так:

```powershell
python manage.py createsuperuser
```

## Структура проекта

- `team_finder/` — настройки Django и корневая конфигурация URL.
- `users/` — аккаунты, профили и навыки.
- `projects/` — проекты и команда демонстрационных данных.
- `templates_var2/` — HTML-шаблоны этого варианта.
- `static/` — стили, JavaScript и статические изображения.

Пространства имён Django-приложений — `users` и `projects`. Например, ссылки на
маршруты записываются как `users:detail` и `projects:list`.

## Проверка конфигурации

Проверить настройки Django и соответствие моделей миграциям можно командами:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
```

Для проверки стиля Python установите `flake8` и запустите его:

```powershell
pip install flake8
flake8
```

Автор: [Cosmic-Man](https://github.com/Cosmic-Man)