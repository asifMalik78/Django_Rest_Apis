from django.db import transaction
from rest_framework import serializers
from decimal import Decimal
from .models import Collection, Product, Review, Cart, CartItem, Customer, Order, OrderItem, ProductImage
from .signals import order_created


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title' , 'products_count' , 'products']
    
    products_count = serializers.IntegerField(read_only=True)
    # products = serializers.RelatedField(many=True, read_only=True)


class ProductImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = ProductImage
        fields = ['id' , 'image']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['id', 'title', 'images', 'slug', 'description', 'unit_price', 'price_with_tax', 'collection', 'inventory', 'updated_at', 'created_at']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # description = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2 , source='unit_price')
    images = ProductImageSerializer(many=True , read_only=True)
    collection = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all()
    )
    # collection = serializers.StringRelatedField()
    # collection = CollectionSerializer()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail',
    # )
    # inventory = serializers.IntegerField()
    # updated_at = serializers.DateTimeField()
    # created_at = serializers.DateTimeField()
    
    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')
    def get_price_with_tax(self , product):
        return product.unit_price * Decimal(1.1)
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']
        
    def create(self , validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id' , 'title' , 'unit_price']
    

class CartItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    total_price = serializers.SerializerMethodField()
    def get_total_price(self , cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price
    
    class Meta:
        model = CartItem
        fields = ['id' , 'product', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True , read_only=True)
    total_price = serializers.SerializerMethodField()
    def get_total_price(self , cart:Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    
    class Meta:
        model = Cart
        fields = ['id' , 'items' , 'total_price']

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self , value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found.')
        return value
    
    def validate_cart_id(self , value):
        if not Cart.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No cart with the given ID was found.')
        return value
    
    def save(self , **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            self.instance = cart_item
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id' , 'product_id' , 'quantity']    

class UpdateCartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()

    def save(self):
        cart_item_id = self.context['cart_item_id']
        cart_id = self.context['cart_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id , id=cart_item_id)
            cart_item.quantity = quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            raise serializers.ValidationError('No cart item with the given ID was found.')
        return self.instance

    class Meta:
        model = CartItem
        fields = ['quantity']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id' , 'user_id' , 'phone' , 'birth_date' , 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id' , 'product' , 'quantity' , 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id' , 'customer' , 'payment_status', 'placed_at', 'items']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self , cart_id):
        if not Cart.objects.filter(id=cart_id).exists():
            raise serializers.ValidationError('Invalid cart ID.')
        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Cart is empty.')
        return cart_id
    
    def save(self , **kwargs):
        cart_id = self.validated_data.get('cart_id')
        user_id = self.context.get('user_id')
        with transaction.atomic():
            customer = Customer.objects.get(user_id=user_id)
            order = Order.objects.create(customer=customer)
            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)

            order_items = [OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.unit_price
            ) for item in cart_items]

            OrderItem.objects.bulk_create(order_items)
            CartItem.objects.filter(cart_id=cart_id).delete()
            order.save()
            order_created.send_robust(sender=self.__class__ , order=order)
            self.instance = order
            return self.instance

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']