from django.contrib import admin
from django.conf import settings
from django.db import models
from django.db.models import Max , Min
from django.core.validators import MinValueValidator , MaxValueValidator
from uuid import uuid4



# Promotion model
class Promotion(models.Model):
    description = models.CharField(max_length = 255)
    discount = models.FloatField()
    
    def __str__(self):
        return self.description


# Collection model
class Collection(models.Model):
    title = models.CharField(max_length = 255)
    featured_product = models.ForeignKey('Product' , on_delete = models.SET_NULL , null = True , related_name = 'featured_product')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']

# Product model
class ProductManager(models.Manager):
    def get_all_products(self):
        return Product.objects.all();
    
    def get_products_by_collection(self , collection_id):
        return Product.objects.filter(collection_id = collection_id);
    
    def get_products_min_and_max_price(self , min_price , max_price):
        return Product.objects.filter(unit_price__gte = min_price , unit_price__lte = max_price).aggregate(Min('unit_price') , Max('unit_price'));
    
    
class Product(models.Model):
    objects = ProductManager()
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2 , validators = [MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0) , MaxValueValidator(100)])
    collection = models.ForeignKey(Collection , on_delete = models.PROTECT , null = True , related_name = 'products')
    promotions = models.ManyToManyField(Promotion , blank = True , null = True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields = ['title'])
        ]

class ProductImage(models.Model):
    product = models.ForeignKey(Product , on_delete = models.CASCADE , related_name = 'images')
    image = models.ImageField()
    
    def __str__(self):
        return self.product.title
        
# Customer model
class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    phone = models.CharField(max_length = 255)
    birth_date = models.DateField(null = True)
    membership = models.CharField(max_length = 1 , choices = MEMBERSHIP_CHOICES , default = MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete = models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    @admin.display(ordering = 'user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering = 'user__last_name')
    def last_name(self):
        return self.user.last_name
    
    class Meta:
        # db_table = 'store_customers'
        # indexes = [
        #     models.Index(fields = ['last_name' , 'first_name'])
        # ]
        ordering = ['user__first_name' , 'user__last_name']
        permissions = [
            ('view_history' , 'Can view history')
        ]


# Order model
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING , 'Pending'),
        (PAYMENT_STATUS_COMPLETE , 'Complete'),
        (PAYMENT_STATUS_FAILED , 'Failed'),
    ]

    placed_at = models.DateTimeField(auto_now_add = True)
    payment_status = models.CharField(max_length = 1 , choices = PAYMENT_STATUS_CHOICES , default = PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete = models.PROTECT)

    def __str__(self):
        return f"{self.customer.user.first_name} {self.customer.user.last_name}"

    class Meta:
        permissions = [
            ('cancel_order', 'can cancel order')
        ]


# OrderItem model
class OrderItem(models.Model):
    order = models.ForeignKey(Order , on_delete = models.CASCADE , related_name='items')
    product = models.ForeignKey(Product , on_delete = models.PROTECT , related_name = 'orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits = 6 , decimal_places = 2)


# Address model
class Address(models.Model):
    street = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    zip_code = models.CharField(max_length = 255)
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)

# Cart model
class Cart(models.Model):
    id = models.UUIDField(primary_key=True , default=uuid4)
    created_at = models.DateTimeField(auto_now_add = True)


# CartItem model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart , on_delete = models.CASCADE , related_name='items')
    product = models.ForeignKey(Product , on_delete = models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators = [MinValueValidator(1)])
    class Meta:
        unique_together = [['cart' , 'product']]

# Review model
class Review(models.Model):
    product = models.ForeignKey(Product , on_delete = models.CASCADE)
    name = models.CharField(max_length = 255)
    description = models.TextField()
    date = models.DateField(auto_now_add = True)