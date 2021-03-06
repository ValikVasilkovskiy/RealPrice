
# SCRAP PERIODIC TEMPLATE #
import os
import django
from django.utils import timezone
from time import sleep
from random import randint

from mysite.settings import MEDIA_ROOT
from . import scrapers

from django.core.mail import send_mail
from django.conf import settings

import tldextract

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
dir = os.path.abspath(os.path.dirname(__file__))
download_path = MEDIA_ROOT + '/images/'

def random_sleep(start=1, end=3):
    sleep(randint(start, end))


def all_scraper_periodic(products):
    for product in products:
        try:
            scraper = tldextract.extract(product.link).domain
            if scraper == 'agro-market':
                scraper = "agro_market"
            method_to_call = getattr(scrapers, scraper)
            random_sleep()
            data = method_to_call(product.link)
            # add price
            if product.current_price != data['product_price']:
                product.prices.create(price=data['product_price'])
                product.current_price = data['product_price']

                # send email if change price
                subject = '{}% {}'.format(product.get_discount(), product.product_name)
                message = 'Изменилась стоимость товара - {} \n' \
                          'Процент роста\падения составляет: {}%\n' \
                          'Просмотреть график роста\падения цены - {} \n' \
                          'Купить товар - {}'.format(
                    product.product_name,
                    product.get_discount(),
                    'http://realprice.com.ua/prices_chart/{}'.format(product.id),
                    product.link,
                )
                email_from = settings.EMAIL_HOST_USER
                recipient_list = []
                for user in product.users.all():
                    recipient_list.append(user.email)
                    send_mail(subject, message, email_from, recipient_list)

            # update field Last update and discount
            product.last_update = timezone.now()
            product.discount = product.get_discount()
            product.operation_result = True
            product.save()
        except:
            product.operation_result = False
            product.save()

            continue



















