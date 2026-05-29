import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from anomalies.models import Anomaly
from theories.models import Theory

@pytest.fixture
def api_client():
    """Возвращает APIClient"""
    return APIClient()

@pytest.fixture
def user(db):
    """Создаёт пользователя"""
    return User.objects.create_user(username="настя123", password="настя123", email="nastya@mail.ru")

@pytest.fixture
def user2(db):
    """Создаёт второго пользователя"""
    return User.objects.create_user(username="рада", password="рада", email="rada@mail.ru")

@pytest.fixture
def anomaly(db, user):
    """Создаёт аномалию"""
    return Anomaly.objects.create(
        title="Телепортация носка",
        description="Носок исчез...",
        location="Моя квартира",
        danger_level="Средний",
        resolved=False,
        author=user,
    )

@pytest.fixture
def theory(db, anomaly, user):
    """Создаёт теорию, связанную с аномалией"""
    return Theory.objects.create(
        anomaly=anomaly,
        title="Сбой в матрице",
        explanation="Мы живём в симуляции",
        votes=10,
        author=user,
    )

@pytest.mark.django_db
class TestAnomalyAPI:
    def test_anomaly_list_unauthenticated(self, api_client):
        """GET /api/anomalies/ - неавторизованный пользователь. Ожидается статус 200 OK"""
        url = "/api/anomalies/"
        response = api_client.get(url)
        assert response.status_code == 200
        assert isinstance(response.data, list)

    def test_anomaly_create_authenticated(self, api_client, user):
        """POST /api/anomalies/ - авторизованный пользователь создаёт новую аномалию. Ожидается статус 201 Created"""
        api_client.force_authenticate(user=user)
        url = "/api/anomalies/"
        data = {
            "title": "Новая аномалия",
            "description": "Описание",
            "location": "Москва",
            "danger_level": "Высокий",
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == 201
        assert response.data["title"] == "Новая аномалия"
        assert response.data["author"]["username"] == user.username

    def test_anomaly_update_owner(self, api_client, anomaly, user):
        """PATCH /api/anomalies/{id}/ - владелец аномалии обновляет её.Ожидается статус 200 OK"""
        api_client.force_authenticate(user=user)
        url = f"/api/anomalies/{anomaly.id}/"
        data = {"title": "Обновлённая аномалия"}
        response = api_client.patch(url, data, format="json")
        assert response.status_code == 200
        assert response.data["title"] == "Обновлённая аномалия"

    def test_anomaly_update_non_owner(self, api_client, anomaly, user2):
        """PATCH /api/anomalies/{id}/ - чужой пользователь пытается обновить аномалию. Ожидается статус 403 доступ запрещён."""
        api_client.force_authenticate(user=user2)
        url = f"/api/anomalies/{anomaly.id}/"
        data = {"title": "Чужая правка"}
        response = api_client.patch(url, data, format="json")
        assert response.status_code == 403

    def test_anomaly_delete_owner(self, api_client, anomaly, user):
        """DELETE /api/anomalies/{id}/ - владелец удаляет свою аномалию. Ожидается статус 204"""
        api_client.force_authenticate(user=user)
        url = f"/api/anomalies/{anomaly.id}/"
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Anomaly.objects.filter(id=anomaly.id).exists()

@pytest.mark.django_db
class TestTheoryAPI:
    def test_theory_list(self, api_client):
        """GET /api/theories/ - неавторизованный пользователь получает список теорий. Ожидается статус 200 OK"""
        url = "/api/theories/"
        response = api_client.get(url)
        assert response.status_code == 200

    def test_theory_create_authenticated(self, api_client, user, anomaly):
        """POST /api/theories/ - авторизованный пользователь создаёт теорию, указывая ID существующей аномалии. Ожидается 201 Created"""
        api_client.force_authenticate(user=user)
        url = "/api/theories/"
        data = {
            "title": "Новая теория",
            "explanation": "Объяснение",
            "anomaly": anomaly.id,
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == 201
        assert response.data["title"] == "Новая теория"
        assert response.data["author"]["username"] == user.username

    def test_theory_update_owner(self, api_client, theory, user):
        """PATCH /api/theories/{id}/ - владелец теории обновляет её. Ожидается статус 200 OK"""
        api_client.force_authenticate(user=user)
        url = f"/api/theories/{theory.id}/"
        data = {"explanation": "Новое объяснение"}
        response = api_client.patch(url, data, format="json")
        assert response.status_code == 200
        assert response.data["explanation"] == "Новое объяснение"

    def test_theory_delete_owner(self, api_client, theory, user):
        """DELETE /api/theories/{id}/ - владелец удаляет свою теорию. Ожидается статус 204 No Content"""
        api_client.force_authenticate(user=user)
        url = f"/api/theories/{theory.id}/"
        response = api_client.delete(url)
        assert response.status_code == 204