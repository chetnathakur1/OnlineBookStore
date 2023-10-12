from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm, AddBookForm, ShippingAddressForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RememberMeAuthenticationForm
from .models import *
from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.db.models import Avg

def home(request):
    books=Book.objects.all().order_by()
    paginator = Paginator(books, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    genre = Genre.objects.all().order_by('genre')
    if request.user.is_authenticated:
        user_ratings = BookRating.objects.filter(user=request.user, book__in=books)
    else:
        user_ratings = None
    context = {'page_obj': page_obj,'genre':genre, 'user_ratings': user_ratings}
    return render(request, 'home.html',context)
    


class BookView(DetailView):
    model = Book
    template_name = 'bookview.html'


def catch_all_view(request):
    return HttpResponseNotFound("This page doesn't exist. 	&#128521; #404")



class RegistrationView(CreateView):
    form_class = NewUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)




def login_request(request):
    if request.method == "POST":
        form = RememberMeAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                if remember_me:
                    request.session.set_expiry(60 * 60 * 24 * 14)
                else:
                    request.session.set_expiry(1800)

                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = RememberMeAuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})



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
 

def search_books(request):
    if request.method == "POST":
        searched = request.POST['searched']
        books = Book.objects.filter(title__contains=searched)

        return render(request,'search.html',{'searched':searched, 'books':books})
    else:
       return render(request,'search.html',{})



def filterbooks(request,genre_slug):
    genre = get_object_or_404(Genre, slug=genre_slug)

    book_category = Book.objects.filter(genre=genre)
    genre = Genre.objects.all().order_by('genre')
    return render(request, 'filter.html', context={'book_category':book_category,'genre':genre})


@login_required(login_url='login')
def addtocart(request, slug):

    book = get_object_or_404(Book, slug=slug)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            raise ValueError()
    except (TypeError, ValueError):
        messages.error(request, 'Please enter a valid quantity.')
        return redirect('viewcart')
    
    if quantity > book.available_quantity:
        return render(request, 'emptycart.html', {'message': 'Cannot add more items than available!'})

    user = request.user     
    created = Cart.objects.filter(user=user, book = book).first()
    
    if created:
        created.quantity += quantity
        created.save()
    else:
        cart_item = Cart(user=user,book=book,quantity=quantity)
        cart_item.save()
    
    book.available_quantity -= quantity
    book.save()
    
    return redirect('bookview', slug) 
    


@login_required
def viewcart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('-date_added')
    cart_total = 0  
    for item in cart_items:
        item.total_price = item.book.price * item.quantity  
        cart_total += item.total_price  
    return render(request, 'viewcart.html', {'cart_items': cart_items, 'cart_total': cart_total})

@login_required
def update_cart(request, cart_item_id):
    cart_item = Cart.objects.get(pk=cart_item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if quantity <= 0:
            messages.error(request, 'Please enter a valid quantity.')

        elif quantity > cart_item.book.available_quantity:
            messages.error(request, 'The requested quantity exceeds the available quantity.')

        else:
            new_quantity = quantity - cart_item.quantity
            cart_item.quantity = quantity
            cart_item.save()
            cart_item.book.available_quantity  -= new_quantity
            cart_item.book.save()
    return redirect('viewcart')
        


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id, user=request.user)
    
    if cart_item.user == request.user:
        cart_quantity = cart_item.quantity
        book = cart_item.book
        
        cart_item.delete()
        book.available_quantity += cart_quantity
        book.save()
    return redirect('viewcart')



@login_required(login_url='login')
def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    cart_total = 0  
    for item in cart_items:
        item.total_price = item.book.price * item.quantity  
        cart_total += item.total_price 
    
    try:
        default_shipping_address = ShippingAddress.objects.get(user=user, is_default=True)
    except ShippingAddress.DoesNotExist:
        default_shipping_address = None

    other_shipping_addresses = ShippingAddress.objects.filter(user=user, is_default =False)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = user
            shipping_address.save()

            ShippingAddress.objects.filter(user=user).exclude(id=shipping_address.id).update(is_default=False)
       
            order = Order(user=user, cart_total=cart_total)
            order.save()
            order.items.set(cart_items)

            

            messages.success(request,'Order Placed Successfully!')
            return redirect('home')

    else:
        form = ShippingAddressForm(instance=default_shipping_address)
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'form': form,
        'shipping_address': default_shipping_address,
        'other_addresses': other_shipping_addresses,
    }

    return render(request, 'checkout.html', context)





@login_required
def add_shipping_address(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        try:
            if form.is_valid():
                shipping_address = form.save(commit=False)
                shipping_address.user = request.user
                shipping_address.is_default = True 
                shipping_address.save()

                ShippingAddress.objects.filter(user=request.user).exclude(id=shipping_address.id).update(is_default=False)

                messages.success(request, 'Shipping address added successfully.')
            else:
                messages.error(request, 'Invalid shipping address data. Please check your inputs.')
        except Exception as e:
            messages.error(request, 'An error occurred while adding the shipping address. Please try again later.')
        return redirect('checkout')  
    else:
        form = ShippingAddressForm()
    
    return render(request, 'add_address.html', {'form': form})


@login_required
def set_default_address(request, address_id):
     address = get_object_or_404(ShippingAddress, pk=address_id, user = request.user)
     address.is_default = True
     address.save()
     ShippingAddress.objects.filter(user=request.user).exclude(pk=address_id).update(is_default=False)
     messages.success(request, 'Default address set successfully.')
     return redirect('checkout')




@login_required
def rate_book(request, slug):
    if request.method == "POST":
        book = get_object_or_404(Book, slug=slug)
        rating = request.POST.get('rating')
        user = request.user

        try:
            rating = int(rating)
            if 1 <= rating <= 5:
                book_rating, created = BookRating.objects.get_or_create(user=user, book=book)
                book_rating.rating = rating
                book_rating.save()


                avg_rating = BookRating.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg']
                book.average_rating = avg_rating
                book.save()

            else:
                return render(request, 'error.html', {'message': 'Invalid rating range'})
        except ValueError:
            return render(request, 'error.html', {'message': 'Invalid rating format'})

    return redirect('bookview', slug=slug)



 

