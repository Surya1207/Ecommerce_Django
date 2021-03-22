from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    COLORS = (
        ('Red', 'Red'),
        ('Yellow', 'Yellow'),
        ('Green', 'Green'),
        ('Black', 'Black'),
        ('White', 'White'),
        ('Pink', 'Pink'),
        ('Maroon', 'Maroon'),
    )
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE, default=True)
    parent = models.ForeignKey('self', related_name='variants', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image1 = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    color = models.CharField(max_length=100, null=True, choices=COLORS)
    description = models.TextField(blank=True, null=True)
    num_available = models.IntegerField(default=1)
    num_visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True, null=True)
    wished_item = models.ManyToManyField(User, related_name='favourite',
                  default=None, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image1.url
        except:
            url = ''
        return url


class Review(models.Model):
    user = models.ForeignKey(User, default=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=True)
    comment = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    rating = models.IntegerField(default=10, validators=[MaxValueValidator(10), MinValueValidator(1)])
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return self.comment
