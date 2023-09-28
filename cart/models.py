from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Customer(models.Model):
    username = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=12)
    # password1 = models.CharField(max_length=12)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.username

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    available_quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=None,blank=True,null = True)

    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
    def decrease_quantity(self,quantity):
        if self.available_quantity >= quantity:
            self.available_quantity -= quantity
            self.save()

   
class Cart(models.Model):
    user = models.ForeignKey(User, null=True,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,null=True,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    items = models.ManyToManyField(Book, through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=True) 

    status_choices = (
        ('cart', 'Cart'),
        ('completed', 'Completed'),
    )
    status = models.CharField(max_length=20, choices=status_choices, default='cart')


    def __str__(self):
        return f'Order #{self.pk}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='order_item',null=True, on_delete=models.CASCADE)
    book = models.ForeignKey(Book,null=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, null=True) 

    def __str__(self):
        return f'{self.quantity} x {self.book.title}'
    