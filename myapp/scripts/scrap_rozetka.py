# Scrap URL from rozetka.com.ua shop #
import os
import django

from datetime import datetime
from myapp.models import Product, Shop
from mysite.settings import MEDIA_ROOT

from bs4 import BeautifulSoup
import requests
import wget

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
dir = os.path.abspath(os.path.dirname(__file__))
download_path = MEDIA_ROOT + '/images/'


def scrap_rozetka_script(products):
    for product in products:
        data_source = requests.get(product.link)
        soup = BeautifulSoup(data_source.text, "html.parser")

        # get product fields
        product_name = soup.find("div", class_="product__heading").find("h1").text
        price = soup.find("div", class_="product-prices__inner").find_all("p")[0].text
        product_image_link = soup.find("figure", class_="product-photo__large-inner").find("img").get('src')

        product_price = ''
        for i in price.encode("utf-8").decode('windows-1251'):
            if str(i).isnumeric():
                product_price += i
        product_price = int(product_price)

        # update database fields
        product.now_price = product_price

        if product.min_price > product_price or product.min_price == 0:
            product.min_price = product_price
        if product.max_price < product_price or product.max_price == 0:
            product.max_price = product_price
        if product.product_name == 'Wait robot tracking':
            product.product_name = product_name

        # update field Last update
        now = datetime.now()
        product.last_update = now.strftime("%Y-%m-%d %H:%M:%S")

        shop = Shop.objects.get(shop_name='rozetka.com.ua')
        product.shop = shop

        # TODO сделать проверку на наличие файла картинки в папке
        if product.operation_result == False:
            filename = wget.download(product_image_link)
            os.rename(filename, os.path.join(download_path, filename))
            product.product_image = 'images/{}'.format(filename)

        product.operation_result = True
        product.save()







