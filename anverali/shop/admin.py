from django.contrib import admin
from .models import User, Product


admin.site.register([User, Product])

