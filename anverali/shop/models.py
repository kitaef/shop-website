from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (1, 'customer'),
      (2, 'seller'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    
    def add_to_cart(self, product, quantity):
        try:
            cart_item = CartItem.objects.get(user=self, product=product)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(user=self, product=product, quantity=quantity)
    
    def remove_from_cart(self, product):
        CartItem.objects.filter(user=self, product=product).delete()
    
    def update_cart_item(self, product, quantity):
        cart_item = CartItem.objects.get(user=self, product=product)
        cart_item.quantity = quantity
        cart_item.save()
    
    def clear_cart(self):
        self.cart.all().delete()


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=16)
    remaining = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


