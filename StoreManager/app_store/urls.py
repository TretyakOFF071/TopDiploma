from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

from .views import register_view, CustomLoginView, CustomLogoutView, ProfileView,ProviderListView, \
    GoodCategoryListView,delete_provider, edit_provider,GoodsListView, delete_good, edit_good, delete_category, \
    GoodDetailView, create_supply, SupplyListView, CreateSaleView,SalesListView, GetGoodPriceView
from .api_views import ProviderAPIView, GoodAPIView, ProviderDetailAPI, GoodDetailAPI

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
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
    path('supply_list/', SupplyListView.as_view(), name='supply_list'),
    path('create_sale/', CreateSaleView.as_view(), name='create_sale'),
    path('get_good_price/<int:good_id>/', GetGoodPriceView.as_view(), name='get_good_price'),
    path('sales_list/', SalesListView.as_view(), name='sales_list'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)