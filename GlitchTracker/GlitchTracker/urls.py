"""
URL configuration for GlitchTracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from anomalies.views import register
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from anomalies.api_views import AnomalyListCreateView, AnomalyRetrieveUpdateDestroyView
from theories.api_views import TheoryListCreateView, TheoryRetrieveUpdateDestroyView
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from anomalies.api_views import AnomalyListCreateView, AnomalyRetrieveUpdateDestroyView
from theories.api_views import TheoryListCreateView, TheoryRetrieveUpdateDestroyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('proofs/', include('proofs.urls')),
    path('theories/', include('theories.urls')),
    path('', include('anomalies.urls')),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html',
             email_template_name='registration/password_reset_email.html',
             success_url=reverse_lazy('password_reset_done')
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url=reverse_lazy('password_reset_complete')
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
         
    path('api/anomalies/', AnomalyListCreateView.as_view(), name='api_anomaly_list'),
    path('api/anomalies/<int:pk>/', AnomalyRetrieveUpdateDestroyView.as_view(), name='api_anomaly_detail'),
    path('api/theories/', TheoryListCreateView.as_view(), name='api_theory_list'),
    path('api/theories/<int:pk>/', TheoryRetrieveUpdateDestroyView.as_view(), name='api_theory_detail'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # dj-rest-auth (REST-эндпоинты для логина/логаута/регистрации)
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/',include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls'))
]