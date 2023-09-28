from django.urls import path
from . import views
from .views import BookView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("",views.home,name = 'home'),
    path('bookview/<int:pk>',BookView.as_view(),name='bookview'),  
    path("register",views.register_request,name='register'),
    path("login",views.login_request,name="login"),
    path("logout",views.logout_request,name="logout"),
    path('addbook',views.addbook,name='addbook'),
    path('viewcart', views.viewcart,name='viewcart'),
    path('addtocart/<int:book_id>',views.addtocart,name='addtocart'),
    path('update_cart/<int:cart_item_id>/', views.update_cart,name='update_cart'),
    path('remove_from_cart/<int:cart_item_id>',views.remove_from_cart,name='remove_from_cart'),
    path('checkout',views.checkout,name='checkout'),
    path('placeorder',views.place_order,name='placeorder'),
    path('search',views.search_books,name='search'),
    path('filterbygenre/<str:category>',views.filterbooks,name='filterbygenre'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset/password_reset.html',
        email_template_name='password_reset/password_reset_email.html',
        subject_template_name='password_reset/password_reset_subject.txt'), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset/password_reset_complete.html'
    ), name='password_reset_complete'),
]





    

