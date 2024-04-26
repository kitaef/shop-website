from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name ='profile'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<int:product_id>/add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('product/<int:product_id>/remove', views.remove_product, name='remove_product'),
    path('add_product', views.add_product, name='add_product'),
    path('product/<int:product_id>/update/', views.update_product, name='update_product'),
    path('cart/<int:item_id>/remove_from_cart', views.remove_from_cart, name='remove_from_cart'),
]