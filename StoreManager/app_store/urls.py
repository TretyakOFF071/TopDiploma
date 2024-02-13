from django.conf.urls.static import static
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import path
from .views import register_view, MyLogoutView, profile_view, main_view, CustomLoginView
from django.conf import settings

urlpatterns = [
    path('', main_view, name='main'),
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
