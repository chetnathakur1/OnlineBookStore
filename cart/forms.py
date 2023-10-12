from django.forms import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm
from django import forms

	


class NewUserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User	    
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        if username[0].isdigit():
            raise forms.ValidationError("Username cannot start with a numeric value!")
        return username

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

class BookRatingForm(forms.Form):
    rating = forms.IntegerField(
        label='Rating',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'class': 'rating'}),
    )