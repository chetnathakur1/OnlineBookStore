from django.contrib import admin
from .models import Genre, Book, Cart, Order, OrderItem, ShippingAddress



admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre','price', 'available_quantity')
    list_filter = ('genre',)
    search_fields = ['title', 'author', 'genre']
    prepopulated_fields = {'slug':('title',)}

class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre',)
    prepopulated_fields = {'slug':('genre',)}

admin.site.register(Genre, GenreAdmin)
admin.site.register(Book,BookAdmin)