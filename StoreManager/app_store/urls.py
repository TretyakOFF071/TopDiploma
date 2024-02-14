from django.conf.urls.static import static
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import path
from .views import register_view, MyLogoutView, profile_view, CustomLoginView, MainView, GoodListView, add_good
from django.conf import settings

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('goods/', GoodListView.as_view(), name='good_list'),
    path('add_good/', add_good, name='add_good'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
