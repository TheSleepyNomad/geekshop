from django.db import models
from users.models import User
from productsapp.models import Product


# Create your models here.

class BasketQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for item in self:
            item.product.quantity += item.quantity
            item.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    @property
    def baskets(self):
        return Basket.objects.filter(user=self.user)

    def total_quantity(self):
        return sum(basket.quantity for basket in self.baskets)

    def total_sum(self):
        return sum(basket.sum() for basket in self.baskets)
