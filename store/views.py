import random
from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from requests import request
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect

from cart.models import Order
from cart.utils import cartData
from .filters import OrderFilter
from .forms import ReviewForm
from .models import *
from django.utils import timezone
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from django.db.models import Q


# Create your views here.


def index(request):
    data = cartData(request)
    order = data['order']
    popular_products = Product.objects.all().order_by('-num_visits')[0:5]
    category = Category.objects.all()
    context = {'popular_products': popular_products, 'order': order, 'category': category}
    return render(request, 'store/index.html', context)


def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 1)
    try:
        products_list = paginator.page(page)
    except PageNotAnInteger:
        products_list = paginator.page(1)
    except EmptyPage:
        products_list = paginator.page(paginator.num_pages)

    context = {'products': products, 'products_list': products_list, 'cartItems': cartItems, 'order':order}
    return render(request, 'store/store.html', context)


def detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)
    product.num_visits = product.num_visits + 1
    product.last_visit = datetime.datetime.now()
    recently_viewed_products = Product.objects.all().order_by('-last_visit')[0:4]
    product.save()
    #product = Product.objects.get(pk=pk)
    related_products = list(product.category.products.filter(parent=None).exclude(id=product.id))

    if len(related_products) >= 3:
        related_products = random.sample(related_products, 3)


    if product.parent:
        return redirect('detail', category_slug=category_slug, slug=product.parent.slug)


    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Review saved")
        else:
            messages.error(request, "Invalid form")
    else:
        form = ReviewForm()


    #if request.method == 'POST' and request.user.is_authenticated:
     #   rating = request.POST.get('rating')
      #  comment = request.POST.get('comment')

       # review = Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
        #return redirect('detail')

    context = {
        'product': product,
        'related_products': related_products,
        'recently_viewed_products': recently_viewed_products,
        'form': form
    }
    return render(request, 'store/Item_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(parent=None)
    context = {
        'category': category,
        'products': products
    }

    return render(request, 'store/category_detail.html', context)


def order_confirmation(request):
    order = Order.objects.get(pk=1)
    return render(request, 'store/order_confirmation.html', {'order': order})