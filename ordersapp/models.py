from django.db import models
from django.conf import settings
from productsapp.models import Product
# Create your models here.


class Order(models.Model):

    FORMING = 'FM'
    SEND_TO_PROCEED = 'STP'
    PAID = 'PD'
    PROCEED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_CHOICES = (
        (FORMING, 'Формирование'),
        (SEND_TO_PROCEED, 'Отправлено в обработку'),
        (PAID, 'Оплачено'),
        (PROCEED, 'Обрабатывается'),
        (READY, 'Готов к выдаче'),
        (CANCEL, 'Отмена'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE
                             )
    create_at = models.DateTimeField(verbose_name='created_at',
                                     auto_now_add=True
                                     )
    update_at = models.DateTimeField(verbose_name='update_at',
                                     auto_now=True
                                     )
    status = models.CharField(verbose_name='status',
                              max_length=3,
                              default=FORMING,
                              choices=ORDER_CHOICES
                              )
    is_active = models.BooleanField(verbose_name='active', default=True)

    def get_total_qty(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.qty, items)))

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.get_total_qty(), items)))

    def __str__(self):
        return f'Текущий заказ {self.pk}'

    def delete(self, using=None, keep_parents=False):
        for item in self.orderitems.select_related():
            item.products.quantity += item.quantity
            item.products.save()
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='orderitems', on_delete=models.CASCADE)
    products = models.ForeignKey(
        Product, verbose_name='product', on_delete=models.CASCADE)
    qty = models.PositiveBigIntegerField(verbose_name='quantity', default=0)

    def get_total_qty(self):
        return self.products.price * self.qty

    def __str__(self):
        return f'Текущий заказ {self.pk}'
