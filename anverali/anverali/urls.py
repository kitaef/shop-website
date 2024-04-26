from django.contrib import admin
from django.urls import include, path
from shop import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', include('shop.urls')),
    path('admin/', admin.site.urls)
]


