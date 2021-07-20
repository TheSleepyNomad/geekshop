from django.contrib import admin
from productsapp.models import ProductCategory, Product

# Register your models here.
admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')  # Изменение вида таблицы раздела
    fields = ('name', 'image', 'description', ('price', 'quantity',), 'category')  # Вывод полей карточки
    readonly_fields = ('description',)  # Установка режима ТолькоЧтение
    ordering = ('-name',)  # Сортировка
    search_fields = ('name',)  # Добавляет поиск по выбранному полю
