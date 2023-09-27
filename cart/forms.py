from django.forms import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm



class NewUserForm(UserCreationForm):
	email = models.EmailField(max_length=100,unique=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
	

class AddBookForm(ModelForm):
	
	class Meta:
		model = Book
		fields = ('title','author','genre','price','available_quantity','image')
		# labels = {
		# 	'title': '',
		# 	'author' : '',
		# 	'genre' : '',
		# 	'price' :'',
		# 	'avialable_quantity': '',
		# 	'image' : '',
		# }
	



