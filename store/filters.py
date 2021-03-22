import django_filters

from cart.models import Order
from .models import *


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = '__all__'