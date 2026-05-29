import pytest
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from catalog.models import Category, Product
from orders.models import Order, OrderItem
from reviews.models import Review
from users.models import Profile

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def category(db):
    return Category.objects.create(name="Смартфоны", slug="smartphones")

@pytest.fixture
def product(db, category):
    return Product.objects.create(
        category=category,
        title="iPhone 15",
        description="Крутой телефон",
        price=Decimal("99999.99"),
        stock=10,
        is_available=True,
    )

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="alice",
        password="pass123",
        email="alice@example.com",
    )

@pytest.fixture
def user2(db):
    return User.objects.create_user(username="bob", password="pass123", email="bob@example.com")

@pytest.fixture
def order(db, user):
    return Order.objects.create(user=user)

@pytest.fixture
def review(db, product, user):
    return Review.objects.create(
        product=product,
        user=user,
        rating=5,
        text="Отличный телефон!",
    )


@pytest.mark.django_db
class TestProductsAPI:
    def test_products_list(self, api_client, product):
        """GET /api/products/ - список товаров (200)"""
        url = reverse('product-list')
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['title'] == 'iPhone 15'
        assert data[0]['price'] == '99999.99'

    def test_product_detail_nested_category(self, api_client, product, category):
        """GET /api/products/{id}/ - проверка вложенной категории"""
        url = reverse('product-detail', args=[product.id])
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert 'category' in data
        assert data['category']['name'] == category.name
        assert data['category']['slug'] == category.slug
        assert data['title'] == product.title


@pytest.mark.django_db
class TestCategoriesAPI:
    def test_categories_list(self, api_client, category):
        """GET /api/categories/ - список категорий"""
        url = reverse('category-list')
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['name'] == 'Смартфоны'
        assert 'slug' in data[0]


@pytest.mark.django_db
class TestOrdersAPI:
    def test_orders_list_unauthenticated(self, api_client):
        """GET /api/orders/ - неавторизованный получает 401/403"""
        url = reverse('order-list')
        response = api_client.get(url)
        assert response.status_code in (401, 403)

    def test_orders_list_authenticated(self, api_client, user, order):
        """GET /api/orders/ - авторизованный получает список своих заказов (200)"""
        api_client.force_authenticate(user=user)
        url = reverse('order-list')
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert 'id' in data[0]


@pytest.mark.django_db
class TestReviewsAPI:
    def test_reviews_list(self, api_client, review):
        """GET /api/reviews/ - список отзывов (200, правильные поля)"""
        url = reverse('review-list')
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['rating'] == 5
        assert 'text' in data[0]

@pytest.mark.django_db
class TestUsersAPI:
    def test_profile_authenticated(self, api_client, user):
        """GET /api/profile/ - авторизованный получает свой профиль (200)"""
        api_client.force_authenticate(user=user)
        url = reverse('my-profile')
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data['user']['username'] == user.username
        assert 'phone' in data
        assert 'address' in data

    def test_profile_unauthenticated(self, api_client):
        """GET /api/profile/ - неавторизованный получает 401/403"""
        url = reverse('my-profile')
        response = api_client.get(url)
        assert response.status_code in (401, 403)