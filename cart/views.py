from django.shortcuts import render, redirect
from .forms import NewUserForm, AddBookForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import *



def home(request):
    books=Book.objects.all()
    context={'books':books}
    # if request.user.is_staff:
    #     return render(request,'adminhome.html',context)
    # else:    
    return render(request,'home.html',context)

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
			user = authenticate(username=username, password=password)
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
        form=AddBookForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
 
    context={'form':form}
    return render(request,'addbook.html',context)
 


# def viewcart(request):
#     cust=Customer.objects.filter(user=request.user)
#     for c in cust:
#         carts=Cart.objects.all()
#         for cart in carts:
#             if(cart.customer==c):
#                 context={
#                     'cart':cart
#                 }
#                 return render(request,'book/viewcart.html',context)  
#         else:
#             return render(request,'book/emptycart.html')