from django.shortcuts import render, redirect
from .forms import NewUserForm, AddBookForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.db.models import Q

def home(request):
    books=Book.objects.all()
    context={'books':books}
    # if request.user.is_staff:
    #     return render(request,'adminhome.html',context)
    # else:    
    return render(request,'home.html',context)

# def index(request):
# 	search_book = request.GET.get('search')

# 	if search_book:
# 		book = Book.objects.filter(Q(title__icontains=search_book) & Q(content__icontains=search_book))
# 	else:
# 		book = Book.objects.all().order_by("-date_created")

# 	return render(request,'base.html',{'book':book})

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



