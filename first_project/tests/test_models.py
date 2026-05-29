import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from catalog.models import Category, Product
from orders.models import Order, OrderItem
from reviews.models import Review
from users.models import Profile

@pytest.fixture
def category(db):
    """Создаёт категорию товара"""
    return Category.objects.create(name="Смартфоны", slug="smartphones")

@pytest.fixture
def product(db, category):
    """Создаёт товар"""
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
    """Создаёт пользователя"""
    return User.objects.create_user(username="alice", password="pass123")

@pytest.fixture
def order(db, user):
    """Создаёт заказ"""
    return Order.objects.create(user=user)

@pytest.fixture
def review(db, product, user):
    """Создаёт отзыв"""
    return Review.objects.create(
        product=product,
        user=user,
        rating=5,
        text="Отличный телефон!",
    )

@pytest.mark.django_db
class TestCategory:
    def test_str(self, category):
        """Category.__str__ должен возвращать название категории"""
        assert str(category) == "Смартфоны"

@pytest.mark.django_db
class TestProduct:
    def test_str(self, product):
        """Product.__str__ """
        assert str(product) == f"{product.title} ({product.price} руб.)"

@pytest.mark.django_db
class TestOrder:
    def test_str(self, order):
        """Order.__str__ """
        assert str(order).startswith("Заказ №")
        assert order.user.username in str(order)

@pytest.mark.django_db
class TestOrderItem:
    def test_price_snapshot(self, order, product):
        """
        Цена в OrderItem – снимок на момент заказа, не меняется при изменении цены товара.
        """
        item = OrderItem.objects.create(
            order=order,
            product=product,
            price=Decimal("12345.00"),
            quantity=1,
        )
        product.price = Decimal("1.00")
        product.save()
        item.refresh_from_db()
        assert item.price == Decimal("12345.00")

@pytest.mark.django_db
class TestReview:
    def test_str(self, review):
        """Review.__str__ должен содержать имя пользователя и название товара"""
        expected = f"Отзыв от {review.user.username} на товар {review.product.title}"
        assert str(review) == expected

    def test_rating_range(self, product, user):
        """Рейтинг должен быть в диапазоне 1-5, иначе исключение ValidationError"""
        from django.core.exceptions import ValidationError
        with pytest.raises(ValidationError):
            review = Review(product=product, user=user, rating=6, text="Слишком высокий рейтинг")
            review.full_clean()
            review.save()

@pytest.mark.django_db
class TestProfileSignals:
    def test_auto_created_on_user_create(self):
        """При создании пользователя автоматически создаётся профиль"""
        new_user = User.objects.create_user(username="bob", password="pass")
        assert Profile.objects.filter(user=new_user).exists()