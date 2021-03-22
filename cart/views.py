import code

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
import json

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from requests import request
from django.shortcuts import redirect, HttpResponseRedirect

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import datetime

from store.models import Review
from store.views import *
from accounts.views import *
from .forms import CouponApplyForm
from .models import *
from .utils import cookieCart, cartData, guestOrder


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    disc_price = Coupon.objects.all()
    coupon_apply_form = CouponApplyForm()
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'coupon_apply_form': coupon_apply_form, 'disc_price': disc_price}
    return render(request, 'cart/cartview.html', context)


def cart_remove(request, pk):
    item_to_delete = OrderItem.objects.filter(pk=pk)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect('cart:cart')


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

        subject = 'Thank You for Your Order'
        message = 'Welcome to Obaju! we appriciate Your business'
        from_email = settings.EMAIL_HOST_USER
        to_list = [order.email, settings.EMAIL_HOST_USER]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        html = render_to_string('store/order_confirmation.html', {'order': order})
        send_mail('Order Confirmation', 'Your order has been sent!', 'noreply@suryabalasundaram1207@gmail.com', ['mail@suryabalasundaram1207@gmail.com', order.email], fail_silently=False, html_message=html)

    return JsonResponse('Payment submitted..', safe=False)


def product_status(request):
    data = cartData(request)
    user_id = request.user
    order = data['order']
    address = ShippingAddress.objects.all()
    orders = OrderItem.objects.filter(order__customer__name__contains=user_id)
    context = {
        'order': order,
        'orders': orders,
        'address': address
    }
    return render(request, 'cart/product_status.html', context)


def order_review(request):
    data = cartData(request)
    user_id = request.user
    order = data['order']
    orders = OrderItem.objects.filter(order__customer__name__contains=user_id)
    context = {
        'order': order,
        'orders': orders,
    }
    return render(request, 'cart/order_review.html', context)


def customer_orders(request):
    user_id = request.user
    orders = Order.objects.filter(customer__name__contains=user_id)
    context = {
        'orders': orders,
    }
    return render(request, 'cart/customer_orders.html', context)


def search(request):
    q = request.GET.get('q')
    products = Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    context = {
        'q': q,
        'products': products
    }
    return render(request, 'cart/search.html', context)


#def product_review(request, pk):
    #    user = Customer.objects.all()
    #product = get_object_or_404(Product, pk=pk)
    #if request.method == 'POST' and request.user.is_authenticated:
    #    rating = request.POST.get('rating', 3)
    #   comment = request.POST.get('comment', '')

    #   review = Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
    #return render(request, 'cart/rating_reviews.html')


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.wished_item.filter(id=request.user.id).exists():
        product.wished_item.remove(request.user)
    else:
        product.wished_item.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    # detail',slug=slug)


@login_required
def wishlist(request):
    new = Product.objects.filter(wished_item=request.user)
    return render(request, 'cart/wishlist.html', {'new': new})


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']

        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
        except Coupon.DoesNotExist:
            request.user = None
    return redirect('cart')