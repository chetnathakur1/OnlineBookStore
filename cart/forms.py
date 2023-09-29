from django.forms import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm
from django import forms


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
		
	

class RememberMeAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )



class ShippingAddressForm(forms.ModelForm):
	class Meta:
		model = ShippingAddress
		fields = ['street', 'city', 'state', 'postal_code', 'country']
