from django.core.management.base import BaseCommand
from django.utils import timezone
from appeals.models import AppealCategory
from parking.models import Parking
from content.models import ArticleCategory, Article, FAQCategory, FAQ, News, Contact


class Command(BaseCommand):
    help = 'Создаёт демонстрационные данные проекта'

    def handle(self, *args, **options):
        categories = ['Доступная среда', 'Транспорт', 'Парковка', 'Социальная защита', 'Здравоохранение', 'Образование', 'Жилищные вопросы', 'Нарушение прав', 'Другое']
        for name in categories:
            AppealCategory.objects.get_or_create(name=name, slug=name.lower().replace(' ', '-'))
        parking = [
            ('Демо-парковка «Центр»', 'Невский проспект, 28', 59.9343, 30.3351, 80, 8, False, True),
            ('Демо-парковка «Петроградская»', 'Каменноостровский проспект, 42', 59.9667, 30.3113, 45, 5, True, False),
            ('Демо-парковка «Московский район»', 'Московский проспект, 192', 59.8517, 30.3215, 60, 6, False, True),
        ]
        for name, address, lat, lng, total, accessible, paid, open24 in parking:
            Parking.objects.get_or_create(name=name, defaults={'address': address, 'latitude': lat, 'longitude': lng, 'total_spaces': total, 'accessible_spaces': accessible, 'paid': paid, 'open_24h': open24, 'accessibility': 'Пандус, широкие места', 'description': 'Демонстрационные данные проекта.'})
        ac, _ = ArticleCategory.objects.get_or_create(name='Доступная среда', slug='accessible-environment')
        Article.objects.get_or_create(slug='rights-of-people-with-disabilities', defaults={'title': 'Права людей с инвалидностью', 'category': ac, 'short_description': 'Базовая информация о праве на доступную среду.', 'content': 'Материал подготовлен для демонстрации учебного проекта. Проверяйте актуальность норм в официальных источниках.', 'published_at': timezone.now()})
        fc, _ = FAQCategory.objects.get_or_create(name='Общие вопросы')
        FAQ.objects.get_or_create(category=fc, question='Как подать обращение?', defaults={'answer': 'Авторизуйтесь, заполните форму и сохраните номер обращения.'})
        FAQ.objects.get_or_create(category=fc, question='Как проверить статус обращения?', defaults={'answer': 'Откройте раздел «Мои обращения» в личном кабинете.'})
        News.objects.get_or_create(slug='project-launch', defaults={'title': 'Запуск учебного проекта ПравоСПб', 'preview': 'Демонстрационная новость о проекте.', 'content': 'Это демонстрационные данные проекта.', 'published_at': timezone.now()})
        Contact.objects.get_or_create(title='Контакты проекта', defaults={'value': 'demo@example.org', 'description': 'Демонстрационные данные проекта. Не являются официальными контактами.'})
        self.stdout.write(self.style.SUCCESS('Демонстрационные данные созданы.'))
