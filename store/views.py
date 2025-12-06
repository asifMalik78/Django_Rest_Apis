import pprint
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.decorators import action , api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin , DestroyModelMixin , UpdateModelMixin , RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet , ReadOnlyModelViewSet , GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.pagination import LimitOffsetPagination , PageNumberPagination
from .models import OrderItem, Product, Collection, Review, Cart, CartItem, Customer, Order, OrderItem, ProductImage
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer, OrderItemSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer, ProductImageSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly, FullDjangoModelPermissions, ViewCustomerHistoryPermissions

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend , SearchFilter , OrderingFilter]
    # filterset_fields = ['collection_id' , 'unit_price']
    filterset_class = ProductFilter
    search_fields = ['title' , 'description']
    ordering_fields = ['unit_price' , 'updated_at' , 'inventory']
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self , request , *args , **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['id']).count() > 0:
            return Response({'error': 'Product has order items'} , status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request , *args , **kwargs)

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_id'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_id']}
    

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self , request , *args , **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection has products' , 'id': kwargs['pk']} , status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request , *args , **kwargs)
    
    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_id'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_id']}


class CartViewSet(CreateModelMixin, RetrieveModelMixin , DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    lookup_field = 'id'


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get' , 'post' , 'patch' , 'delete']
    lookup_field = 'id'
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_id']).select_related('product')

    def get_serializer_context(self):
        if self.request.method == 'PATCH ':
            return {'cart_id': self.kwargs['cart_id'] , 'cart_item_id': self.kwargs['id']}
        return {'cart_id': self.kwargs['cart_id']}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['GET'], permission_classes=[ViewCustomerHistoryPermissions])
    def history(self, request, id=None):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class OrderViewSet(ModelViewSet):
    http_method_names = ['get' , 'post' , 'patch' , 'delete' , 'head' , 'options']
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PATCH' , 'DELETE']:
            return [IsAdminUser()]

        return [IsAuthenticated()]  
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        customer = Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer.id)

    def create(self , request , *args , **kwargs):
        serializer = CreateOrderSerializer(data=request.data , context={'user_id': request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    