from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from anomalies.models import Anomaly, GlitchProfile
from theories.models import Theory
from random import choice, randint

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **options):
        self._create_users()
        self._create_anomalies()
        self._create_theories()
        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))

    def _create_users(self):
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            GlitchProfile.objects.get_or_create(
                user=admin,
                defaults={'nickname': 'admin', 'belief_level': 100, 'bio': 'Создатель системы'}
            )
        for i in range(1, 4):
            user, created = User.objects.get_or_create(
                username=f'tester{i}',
                defaults={'email': f'tester{i}@glitch.com'}
            )
            if created:
                user.set_password('testpass123')
                user.save()
                GlitchProfile.objects.get_or_create(
                    user=user,
                    defaults={'nickname': f'Tester{i}', 'belief_level': 50, 'bio': 'Любитель глитчей'}
                )
        self.stdout.write(f'Создано пользователей: {User.objects.count()}')

    def _create_anomalies(self):
        users = list(User.objects.all())
        titles = ['Пропавший носок', 'Двойник в метро', 'Изменённый логотип', 'Телепортация телефона']
        locations = ['Моя квартира', 'Москва', 'Санкт-Петербург', 'Интернет']
        danger_levels = ['Критический', 'Высокий', 'Средний', 'Низкий']

        for i in range(5):
            anomaly, _ = Anomaly.objects.get_or_create(
                title=f'{choice(titles)} {i+1}',
                defaults={
                    'description': 'Странное совпадение...',
                    'location': choice(locations),
                    'danger_level': choice(danger_levels),
                    'resolved': choice([True, False]),
                    'author': choice(users)
                }
            )
        self.stdout.write(f'Создано аномалий: {Anomaly.objects.count()}')

    def _create_theories(self):
        anomalies = list(Anomaly.objects.all())
        users = list(User.objects.all())
        for i in range(8):
            Theory.objects.get_or_create(
                title=f'Теория {i+1}',
                defaults={
                    'explanation': 'Это всё симуляция!',
                    'votes': randint(0, 100),
                    'anomaly': choice(anomalies),
                    'author': choice(users)
                }
            )
        self.stdout.write(f'Создано теорий: {Theory.objects.count()}')