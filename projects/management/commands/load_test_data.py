from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from projects.models import Project
from users.models import Skill

User = get_user_model()

PASSWORD = "testpass123"

TEST_DATA = [
    {
        "email": "ivan@example.com",
        "name": "Иван",
        "surname": "Петров",
        "about": "Бэкенд-разработчик, пишу на Python.",
        "skills": ["Python", "Django", "PostgreSQL"],
        "projects": [
            ("Трекер привычек", "Веб-приложение для отслеживания ежедневных привычек."),
            (
                "Бот для заметок",
                "Telegram-бот, который сохраняет заметки и напоминает о них.",
            ),
        ],
    },
    {
        "email": "anna@example.com",
        "name": "Анна",
        "surname": "Смирнова",
        "about": "Фронтенд-разработчица.",
        "skills": ["JavaScript", "React", "CSS"],
        "projects": [
            ("Портфолио для дизайнеров", "Конструктор простых сайтов-портфолио."),
        ],
    },
    {
        "email": "oleg@example.com",
        "name": "Олег",
        "surname": "Кузнецов",
        "about": "Дизайнер интерфейсов.",
        "skills": ["Figma", "CSS"],
        "projects": [
            ("Библиотека иконок", "Открытый набор иконок для веб-проектов."),
        ],
    },
    {
        "email": "maria@example.com",
        "name": "Мария",
        "surname": "Волкова",
        "about": "Изучаю анализ данных.",
        "skills": ["Python", "SQL"],
        "projects": [
            ("Анализ цен на квартиры", "Сбор и визуализация данных о ценах на жильё."),
        ],
    },
    {
        "email": "alexey@example.com",
        "name": "Алексей",
        "surname": "Соколов",
        "about": "Разрабатываю серверные приложения и автоматизацию.",
        "skills": ["Go", "Docker", "Redis"],
        "projects": [
            (
                "Мониторинг сервисов",
                "Небольшая панель для проверки состояния веб-сервисов.",
            ),
            (
                "Личный бюджет",
                "Сервис для учёта расходов и планирования накоплений.",
            ),
        ],
    },
    {
        "email": "elena@example.com",
        "name": "Елена",
        "surname": "Морозова",
        "about": "Создаю удобные интерфейсы для веб-приложений.",
        "skills": ["TypeScript", "Vue.js", "Доступность интерфейсов"],
        "projects": [
            (
                "Каталог мастерских",
                "Карта локальных мастерских и небольших студий.",
            ),
        ],
    },
    {
        "email": "timur@example.com",
        "name": "Тимур",
        "surname": "Ахметов",
        "about": "Настраиваю окружения разработки и CI/CD.",
        "skills": ["Linux", "Kubernetes", "GitLab CI", "Bash"],
        "projects": [
            (
                "Планировщик релизов",
                "Инструмент для подготовки и отслеживания выпусков.",
            ),
            (
                "Домашняя лаборатория",
                "Набор конфигураций для учебного серверного стенда.",
            ),
        ],
    },
]


class Command(BaseCommand):
    """Заполняет базу небольшим набором демонстрационных данных."""

    help = "Создаёт тестовых пользователей и проекты"

    def handle(self, *args, **options):
        """Добавляет отсутствующие профили, навыки и проекты."""
        for item in TEST_DATA:
            if User.objects.filter(email=item["email"]).exists():
                continue
            user = User.objects.create_user(
                email=item["email"],
                password=PASSWORD,
                name=item["name"],
                surname=item["surname"],
                about=item["about"],
            )
            for skill_name in item["skills"]:
                skill, _ = Skill.objects.get_or_create(name=skill_name)
                user.skills.add(skill)
            for name, description in item["projects"]:
                project = Project.objects.create(
                    name=name, description=description, owner=user
                )
                project.participants.add(user)
        self.stdout.write(self.style.SUCCESS("Тестовые данные загружены"))
