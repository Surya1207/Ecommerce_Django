"""grocery_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from cart import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),

    path('register_page/', views.RegisterPage, name='RegisterPage'),
    path('login_page/', views.LoginPage, name='login-page'),


    path('cart/', views.cart, name="cart"),
    path('apply/', views.coupon_apply, name='apply'),
    path('checkout/', views.checkout, name="checkout"),
    path('order_review/', views.order_review, name="order-review"),
    path('product-status/', views.product_status, name="product-status"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('search/', views.search, name="search"),
    path('remove/<int:pk>/', views.cart_remove, name='remove'),
    #path('pro_review/<int:pk>/', views.product_review, name="pro_review"),
    path('wishlist/<int:id>/', views.add_to_wishlist, name="wishlist"),
    path('wishlists/', views.wishlist, name="wishlisting"),



    path('store/', views.store, name="store"),
    path('order-confirmation/', views.order_confirmation, name="order-confirmation"),
    path('<slug:category_slug>/<slug:slug>/', views.detail, name="detail"),
    path('<slug:slug>/', views.category_detail, name="category_detail")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)