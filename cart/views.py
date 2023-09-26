from django.shortcuts import render, redirect
from .forms import NewUserForm, AddBookForm, BookSearchForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.db.models import query



def home(request):
    books=Book.objects.all()
    search_form = BookSearchForm()
    return render(request, 'home.html', {'search_form': search_form, 'books': books})



class BookView(DetailView):
	model = Book
	template_name = 'bookview.html'


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})



def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			# remember_me = form.cleaned_data['remember_me']
			user = authenticate(request,username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request,"You have successfully logged out.")
	return redirect("home")


 
def addbook(request):
    form=AddBookForm()
    if request.method=='POST':
        form=AddBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/')
 
    context={'form':form}
    return render(request,'addbook.html',context)
 
		

def addtocart(request, book_id):
		book=Book.objects.get(pk=book_id)
		user = request.user
		cart, created = Cart.objects.get_or_create(user=user, book=book)
		if not created:
			cart.quantity += 1
			cart.save()
		book.decrease_quantity(1)
		return redirect('viewcart')

def viewcart(request):
	cart = Cart.objects.filter(user = request.user)
	return render(request, 'viewcart.html', {'cart':cart})

def update_cart(request, cart_id):
    cart = Cart.objects.get(pk=cart_id)
    new_quantity = int(request.POST['quantity'])
    if new_quantity > 0:
        cart.quantity = new_quantity
        cart.save()
    return redirect('viewcart')


def search_books(request):
    query = request.GET.get('query')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'search.html', {'books': books, 'query': query})

