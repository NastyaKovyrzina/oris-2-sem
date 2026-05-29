import pytest
from django.contrib.auth.models import User
from anomalies.models import Anomaly
from theories.models import Theory
from proofs.models import Proof
from users.models import GlitchProfile

@pytest.fixture
def user(db):
    """Создает пользователя"""
    return User.objects.create_user(username="настя123", password="настя123")

@pytest.fixture
def glitch_profile(db, user):
    """Создаёт или обновляет профиль"""
    profile, created = GlitchProfile.objects.update_or_create(
        user=user,
        defaults={
            'nickname': "настя",
            'belief_level': 75,
            'bio': "Охотница за аномалиями"
        }
    )
    return profile

@pytest.fixture
def anomaly(db, user):
    """Создает аномалию"""
    return Anomaly.objects.create(
        title="Телепортация носка",
        description="Носок исчез в стиральной машине и появился в холодильнике",
        location="Моя квартира",
        danger_level="Средний",
        resolved=False,
        author=user
    )

@pytest.fixture
def theory(db, anomaly, user):
    """Создаёт теорию, связанную с аномалией"""
    return Theory.objects.create(
        anomaly=anomaly,
        title="Сбой в матрице",
        explanation="Мы живём в симуляции, кто-то перепутал координаты",
        votes=10,
        author=user
    )

@pytest.fixture
def proof(db, theory):
    """Создаёт доказательство, связанное с теорией"""
    return Proof.objects.create(
        theory=theory,
        title="Фото носка в холодильнике",
        description="Чёткое фото с датой",
        evidence_link="https://example.com/photo.jpg",
        verified=True
    )

class TestAnomaly:
    def test_anomaly_creation(self, anomaly):
        """Проверяет, что аномалия создаётся с правильными полями"""
        assert anomaly.title == "Телепортация носка"
        assert anomaly.author.username == "настя123"
        assert anomaly.resolved is False
        assert str(anomaly) == f"Аномалия: {anomaly.title}"

class TestTheory:
    def test_theory_creation(self, theory, anomaly):
        """Проверяет создание теории"""
        assert theory.title == "Сбой в матрице"
        assert theory.anomaly == anomaly
        assert theory.votes == 10
        assert str(theory) == theory.title

class TestProof:
    def test_proof_creation(self, proof, theory):
        """Проверяет создание доказательства"""
        assert proof.title == "Фото носка в холодильнике"
        assert proof.theory == theory
        assert proof.verified is True
        assert proof.evidence_link == "https://example.com/photo.jpg"
        assert str(proof) == proof.title

class TestGlitchProfile:
    def test_profile_creation(self, glitch_profile, user):
        """Проверяет создание профиля"""
        assert glitch_profile.user == user
        assert glitch_profile.nickname == "настя"
        assert glitch_profile.belief_level == 75
        assert glitch_profile.bio == "Охотница за аномалиями"
        assert str(glitch_profile) == "настя"