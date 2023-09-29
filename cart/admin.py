from django.contrib import admin
from .models import Customer, Cart, Order, OrderItem, ShippingAddress
from cart import models


admin.site.register(Customer)

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

class Admin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre','price', 'available_quantity')
    list_filter = ('genre',)
    search_fields = ['title', 'author', 'genre']


admin.site.register(models.Book,Admin)