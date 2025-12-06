from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models import Q , Count , Sum , Avg , Max , Min
from store.models import Product , Customer , Collection
from django.db import transaction , connection
import os
from pathlib import Path

from django.core.mail import send_mail , mail_admins , BadHeaderError , EmailMessage
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from templated_mail.mail import BaseEmailMessage
from email.mime.image import MIMEImage
from .tasks import notify_customers
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)
# Create your views here.
# @transaction.atomic()

class HellowView(APIView):
    # @method_decorator(cache_page(60))
    def get(self , request):
        try:
            logger.info('Calling httpbin API')
            response = requests.get('https://httpbin.org/delay/1')
            logger.info('Response from httpbin API')
            response.raise_for_status() # Check for HTTP errors
            data = response.json()
            return render(request , 'hellow.html' , {'url': data['url']})
        except requests.RequestException as e:
            logger.critical(f'Error calling httpbin API: {str(e)}')
            return render(request , 'hellow.html' , {'url': 'Error calling httpbin API'})

# @cache_page(60)
# def say_hellow(request):
#     request = requests.get('https://httpbin.org/delay/2')
#     data = request.json()
#     return render(request , 'hellow.html' , {'url': data['url']})


# def say_hellow(request):
#     if cache.get('httpbin_result') is None:
#         response = requests.get('https://httpbin.org/delay/2')
#         data = response.json()
#         print(data)
#         cache.set('httpbin_result' , data['url'])
#     return render(request , 'hellow.html' , {'url': cache.get('httpbin_result')})
#     notify_customers.delay('Hello')
#     return HttpResponse('hello')
#     try:
#         base_dir_name = Path(__file__).resolve().parent.parent
#         file_path = os.path.join(base_dir_name , 'media' , '123156919.jpg')
        
#         message = BaseEmailMessage(
#             template_name='emails/hellow.html',
#             context={'full_name': 'John Doe' , 'username': 'Johnnybhai'}
#         )
        
#         with open(file_path, 'rb') as f:
#             img = MIMEImage(f.read())
#             img.add_header('Content-ID', '<custom_image>')
#             message.attach(img)
            
#         message.send(['asif@solobundle.com'] , from_email='test@solobundle.com')
#     except BadHeaderError:
#         return HttpResponse('Invalid header found.')
#     return HttpResponse('email sended')

#     with transaction.atomic():
#         products_prices = Product.get_total_price_by_collection()
#         product_average_prices = Product.get_average_price_by_collection()
#         product_max_prices = Product.get_max_price_by_collection()
#         product_min_prices = Product.get_min_price_by_collection()
#         product_no_of_products = Product.get_no_products_by_collection()
#         print(products_prices)
#         print(product_average_prices)
#         print(product_max_prices)
#         print(product_min_prices)
#         print(product_no_of_products)
#         all_products = Product.objects.all()
#         gold_members = Customer.objects.filter(membership=Customer.MEMBERSHIP_GOLD).only('first_name' , 'last_name')
        
#         raw_sql = Product.objects.raw('SELECT * FROM store_product')
#         print(raw_sql)
        
#         with connection.cursor() as cursor:
#             cursor.execute('SELECT * FROM store_product')
#             cursor.callproc('get_all_products' , [1 , 'Product 1'])
#             raw_sql = cursor.fetchall()
#             print(raw_sql)
#     return render(request,'hellow.html' , {'items': all_products , 'gold_members': gold_members})
