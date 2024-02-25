from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

from .views import register_view, CustomLoginView, CustomLogoutView, profile_view, ProviderAPIView, GoodAPIView, \
    ProviderDetailAPI, GoodDetailAPI, ProviderListView, GoodCategoryListView, delete_provider, edit_provider, \
    GoodsListView, delete_good, edit_good, delete_category, GoodDetailView, create_supply, supply_list

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('api/providers/', ProviderAPIView.as_view(), name='api_providers_list'),
    path('api/providers/<int:pk>/', ProviderDetailAPI.as_view(), name='api_provider_detail'),
    path('api/goods/', GoodAPIView.as_view(), name='api_goods_list'),
    path('api/goods/<int:pk>/', GoodDetailAPI.as_view(), name='api_good_detail'),
    path('providers_list/', ProviderListView.as_view(), name='providers_list'),
    path('delete_provider/<int:provider_id>/', delete_provider, name='delete_provider'),
    path('edit_provider/<int:provider_id>/', edit_provider, name='edit_provider'),
    path('categories_list/', GoodCategoryListView.as_view(), name='categories_list'),
    path('delete_category/<int:category_id>/', delete_category, name='delete_category'),
    path('goods_list/', GoodsListView.as_view(), name='goods_list'),
    path('delete_good/<int:good_id>/', delete_good, name='delete_good'),
    path('edit_good/<int:good_id>/', edit_good, name='edit_good'),
    path('good/<int:pk>/', GoodDetailView.as_view(), name='good_detail'),
    path('create_supply/', create_supply, name='create_supply'),
    path('supply_list/', supply_list, name='supply_list'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)