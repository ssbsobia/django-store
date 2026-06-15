from django.urls import path
from .views import home, product_detail, product_list, filter_products

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('products/latest/', product_list, {'list_type': 'latest'}, name='latest_products'),
    path('products/featured/', product_list, {'list_type': 'featured'}, name='featured_products'),
    path('products/category/<slug:slug>/', filter_products, {'filter_type': 'category'}, name='category_products'),
    path('products/brand/<slug:slug>/', filter_products, {'filter_type': 'brand'}, name='brand_products'),
]