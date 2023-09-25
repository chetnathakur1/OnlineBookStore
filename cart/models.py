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
    image = models.ImageField(upload_to='media/images',blank=True,null = True)

    def __str__(self):
        return self.title

   
class Cart(models.Model):
    customer = models.OneToOneField(Customer, null=True,on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return str(self.customer)
    

