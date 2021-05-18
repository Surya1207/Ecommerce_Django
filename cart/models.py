import uuid
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from store.models import Product


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, default=True, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200)
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.name:
            name = self.name
        else:
            name = self.device
        return str(name)


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, default=True, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, blank=True)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country_code = models.CharField(max_length=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    order_key = models.CharField(max_length=200)
    payment_option = models.CharField(max_length=200, blank=True)
    billing_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, default=True, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=30, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=False, blank=True)
    city = models.CharField(max_length=200, null=False, blank=True)
    state = models.CharField(max_length=200, null=False, blank=True)
    zipcode = models.CharField(max_length=200, null=False, blank=True)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, verbose_name="Customer", on_delete=models.CASCADE)
    full_name = models.CharField("Full Name", max_length=150)
    phone = models.CharField("Phone Number", max_length=50)
    postcode = models.CharField("Postcode", max_length=50)
    address_line = models.CharField("Address Line 1", max_length=255)
    address_line2 = models.CharField("Address Line 2", max_length=255)
    town_city = models.CharField("Town/City/State", max_length=150)
    delivery_instructions = models.CharField("Delivery Instructions", max_length=255)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    default = models.BooleanField("Default", default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return "{} Address".format(self.full_name)


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=True)
    active = models.BooleanField()

    def __str__(self):
        return self.code


class DeliveryOptions(models.Model):
        """
        The Delivery methods table contining all delivery
        """

        DELIVERY_CHOICES = [
            ("IS", "In Store"),
            ("HD", "Home Delivery"),
            ("DD", "Digital Delivery"),
        ]

        delivery_name = models.CharField(
            verbose_name=("delivery_name"),
            help_text=("Required"),
            max_length=255,
        )
        delivery_price = models.DecimalField(
            verbose_name=("delivery price"),
            help_text=("Maximum 999.99"),
            error_messages={
                "name": {
                    "max_length": ("The price must be between 0 and 999.99."),
                },
            },
            max_digits=5,
            decimal_places=2,
        )
        delivery_method = models.CharField(
            choices=DELIVERY_CHOICES,
            verbose_name=("delivery_method"),
            help_text=("Required"),
            max_length=255,
        )
        delivery_timeframe = models.CharField(
            verbose_name=("delivery timeframe"),
            help_text=("Required"),
            max_length=255,
        )
        delivery_window = models.CharField(
            verbose_name=("delivery window"),
            help_text=("Required"),
            max_length=255,
        )
        order = models.IntegerField(verbose_name=("list order"), help_text=("Required"), default=0)
        is_active = models.BooleanField(default=True)

        class Meta:
            verbose_name = ("Delivery Option")
            verbose_name_plural = ("Delivery Options")

        def __str__(self):
            return self.delivery_name


class PaymentSelections(models.Model):
        """
        Store payment options
        """

        name = models.CharField(
            verbose_name=("name"),
            help_text=("Required"),
            max_length=255,
        )

        is_active = models.BooleanField(default=True)

        class Meta:
            verbose_name = ("Payment Selection")
            verbose_name_plural = ("Payment Selections")

        def __str__(self):
            return self.name
