from django.urls import path , include
# from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products' , views.ProductViewSet , basename='products')
router.register('collections' , views.CollectionViewSet , basename='collections')
router.register('carts' , views.CartViewSet , basename='carts')
router.register('customers' , views.CustomerViewSet , basename='customers')
router.register('orders' , views.OrderViewSet , basename='orders')

product_router = routers.NestedDefaultRouter(router , 'products' , lookup='product')
product_router.register('reviews' , views.ReviewViewSet , basename='product-reviews')
product_router.register('images' , views.ProductImageViewSet , basename='product-images')

cart_router = routers.NestedDefaultRouter(router , 'carts' , lookup='cart')
cart_router.register('items' , views.CartItemViewSet , basename='cart-items')


urlpatterns = router.urls + product_router.urls + cart_router.urls   
# urlpatterns = [
#     # path('', include(router.urls)),
#     # path('products/', views.ProductList.as_view()),
#     # path('products/<int:id>/', views.ProductDetail.as_view()),
#     # path('collections/', views.CollectionList.as_view()),
#     # path('collections/<int:pk>/', views.CollectionDetail.as_view() , name='collection-detail'),
# ]