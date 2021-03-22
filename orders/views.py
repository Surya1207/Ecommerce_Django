from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
import json
from requests import request
from django.shortcuts import redirect
from .models import *
from cart.models import *


# Create your views here.
def customer_orders(request):
    user_id = request.user
    orders = Order.objects.filter(customer__name__contains=user_id)
    context = {
        'orders':orders,
       }
    return render(request, 'orders/customer_orders.html', context)
