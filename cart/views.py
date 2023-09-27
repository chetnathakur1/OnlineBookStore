from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm, AddBookForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.views.generic import DetailView
from django.contrib.auth.models import User
from .models import Order 
from django.core.paginator import Paginator



def home(request):
	books=Book.objects.all()
	paginator = Paginator(books, 9)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	genre = Book.objects.values('genre').distinct()
	context = {'page_obj': page_obj,'genre':genre}
	return render(request, 'home.html',context)
	


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
    if request.method == 'POST':
        form = AddBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = AddBookForm()
    return render(request, 'addbook.html', {'form': form})
 
		

def addtocart(request, book_id):
		book=Book.objects.get(pk=book_id)
		user = request.user
		if user.is_authenticated:
			try:
				cart_item = Cart.objects.get(user=user, book=book)
				cart_item.quantity += 1
				cart_item.save()
			except Cart.DoesNotExist:
				Cart.objects.create(user=user, book=book, quantity=1)
		return redirect('viewcart')



def viewcart(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_total = 0  
    for item in cart_items:
        item.total_price = item.book.price * item.quantity  # Calculate total price for each item
        cart_total += item.total_price  # Add to the cart total
    return render(request, 'viewcart.html', {'cart_items': cart_items, 'cart_total': cart_total})


def update_cart(request, cart_item_id):
    cart_item = Cart.objects.get(pk=cart_item_id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if int(quantity) > 0:
            cart_item.quantity = quantity
            cart_item.save()
    return redirect('viewcart')
		

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id)
    cart_item.delete()
    return redirect('viewcart')


def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'checkout.html', context)


def place_order(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        order = Order.objects.create(user=request.user)
        for item in cart_items:
            order.items.create(book=item.book, quantity=item.quantity)
            item.book.quantity_available -= item.quantity
            item.book.save()
        cart_items.delete()
        return redirect('order_confirmation') 
    return redirect('checkout')



def search_books(request):
	if request.method == "POST":
		searched = request.POST['searched']
		books = Book.objects.filter(title__contains=searched)

		return render(request,'search.html',{'searched':searched, 'books':books})
	else:
	   return render(request,'search.html',{})



def filterbooks(request,category):
	book_category = Book.objects.filter(genre=category)
	genre = Book.objects.values('genre').distinct()
	return render(request, 'filter.html', context={'book_category':book_category,'genre':genre})
			


