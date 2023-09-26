from django.urls import path
from . import views
from .views import BookView

urlpatterns = [
    path("",views.home,name = 'home'),
    path('bookview/<int:pk>',BookView.as_view(),name='bookview'),  
    path("register",views.register_request,name='register'),
    path("login",views.login_request,name="login"),
    path("logout",views.logout_request,name="logout"),
    path('addbook',views.addbook,name='addbook'),
    path('viewcart', views.viewcart,name='viewcart'),
    path('addtocart/<int:book_id>',views.addtocart,name='addtocart'),
    path('update_cart/<int:cart_id>/', views.update_cart,name='update_cart'),
    path('search',views.search_books,name='search'),
]


