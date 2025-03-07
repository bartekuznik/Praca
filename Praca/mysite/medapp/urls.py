from django.urls import path
from . import views
from django.urls import path
from .views import  ProductCreateView, ProductUpdateView, ProductDeleteView 

app_name = 'medapp'

urlpatterns = [
    path('product/<int:pk>/', views.product_detail, name='product-detail'),
    path('profile/<int:pk>/', views.profile_detail, name='profile-detail'),
    path('product/new/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('account/edit', views.edit , name='edit'),
    path('contact', views.contact , name='contact'),
]