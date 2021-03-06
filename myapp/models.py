from django.contrib.auth.models import User
from django.db import models

DEFAULT_PRODUCT_NAME = 'Untracked'
DEFAULT_IMAGE_PATH = '../media/images/default_img.jpg'
DEFAULT_VISIBILITY_STATUS = 1

class Shop(models.Model):
    shop_name = models.CharField(max_length=64, null=False)

    def __str__(self):
        return self.shop_name

class Product(models.Model):
    public_visibility = 1
    private_visibility = 2
    visibility = (
        (public_visibility, 'public'),
        (private_visibility, 'private'),
    )
    users = models.ManyToManyField(User)
    product_name = models.CharField(max_length=256, default=DEFAULT_PRODUCT_NAME)
    link = models.CharField(max_length=1024, null=False, blank=True)
    product_image = models.ImageField(upload_to='images', default=DEFAULT_IMAGE_PATH)

    current_price = models.IntegerField(blank=True, default=0)
    discount = models.IntegerField(blank=True, default=0)

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    visibility_status = models.PositiveSmallIntegerField(choices=visibility, default=DEFAULT_VISIBILITY_STATUS)

    # Robot tracking result (True/False)
    operation_result = models.BooleanField(default=False)

    # Status of products (disabled = False / enabled = True)
    status = models.BooleanField(default=True)
    last_update = models.DateTimeField(auto_now_add=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=False)


    def get_current_price(self):
        current_price = self.prices.order_by('-date')[0].price
        return current_price

    def get_discount(self):
        start_price = self.prices.order_by('date')[0].price
        last_price = self.prices.order_by('-date')[0].price
        discount = int(last_price / start_price * 100 - 100)
        return discount

    def __str__(self):
        return self.product_name

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        default_related_name = 'prices'

    def __int__(self):
        return self.price

class News(models.Model):
    title = models.CharField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(upload_to='images', default=DEFAULT_IMAGE_PATH)
    text = models.TextField(blank=True)

    def __str__(self):
        return self.title















