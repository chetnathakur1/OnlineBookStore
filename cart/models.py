from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
    genre = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True) 
    def __str__(self):
        return self.genre


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre,on_delete = models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    available_quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=None,blank=True,null = True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    slug = models.SlugField(unique=True,blank=True, null=True)
    avg_rating = models.FloatField(default=0)

    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
    def decrease_quantity(self,quantity):
        if self.available_quantity >= quantity: 
            self.available_quantity -= quantity
            self.save()

    def get_unique_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        num = 1

        while Book.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{num}"
            num += 1

        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)



class Cart(models.Model):
    user = models.ForeignKey(User, blank=True,null=True,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,blank=True,null=True,on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return f"{self.quantity} x {self.book.title}"



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    items = models.ManyToManyField(Book, through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True) 
    
    status_choices = (
        ('cart', 'Cart'),
        ('completed', 'Completed'),
    )
    status = models.CharField(max_length=20, choices=status_choices, default='cart')


    def __str__(self):
        return f'Order #{self.pk}'

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order,related_name='order_item',null=True, on_delete=models.CASCADE)
    book = models.ForeignKey(Book,null=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, null=True) 

    def __str__(self):
        return f'{self.quantity} x {self.book.title}'
    

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank = True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    street = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    postal_code = models.CharField(max_length=10, null=True)
    country = models.CharField(max_length=50, null=True)
    date_added = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Shipping Address"
    


class BookRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, validators= [MinValueValidator(1), MaxValueValidator(5)])    

    def __str__(self):
        return f" {self.book.title}: {self.rating}"