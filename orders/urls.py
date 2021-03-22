from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
	path('customer-orders/', views.customer_orders, name="customer-orders"),
]