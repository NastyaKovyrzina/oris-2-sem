from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from catalog.api_views import CategoryListCreateView, CategoryRetrieveUpdateDestroyView,ProductListCreateView, ProductRetrieveUpdateDestroyView
from orders.api_views import OrderListCreateView, OrderRetrieveUpdateDestroyView
from reviews.api_views import ReviewListCreateView, ReviewRetrieveUpdateDestroyView
from users.api_views import MyProfileRetrieveUpdateView, UserRegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('', include('orders.urls')),
    path('', include('reviews.urls')),
    path('users/', include('users.urls')),
    path('reviews/', include('reviews.urls')),
    path('catalog/', include('catalog.urls')), 
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             success_url=reverse_lazy('password_reset_done')
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url=reverse_lazy('password_reset_complete')
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('api/schema/', SpectacularAPIView.as_view(), name="schema"),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # dj-rest-auth (REST-эндпоинты для логина/логаута/регистрации)
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/',include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('api/categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    path('api/products/', ProductListCreateView.as_view(), name='product-list'),
    path('api/products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('api/orders/', OrderListCreateView.as_view(), name='order-list'),
    path('api/orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),
    path('api/reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('api/reviews/<int:pk>/', ReviewRetrieveUpdateDestroyView.as_view(), name='review-detail'),
    path('api/profile/', MyProfileRetrieveUpdateView.as_view(), name='my-profile'),
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
]