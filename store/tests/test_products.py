from rest_framework import status
import pytest
from core.models import User
from store.models import Product
from model_bakery import baker


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/' , product)
    return do_create_product

@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_returns_401(self , api_client, create_product):
        product_data = {
            'title':'a',
            'slug':'a',
            'description':'a',
            'price':1,
            'inventory':1
        }

        response = create_product(product_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    

    def test_if_user_is_not_admin_returns_403(self , api_client , authenticate , create_product):
        authenticate(user=User(is_staff=False))
        product_data = {
            'title':'a',
            'slug':'a',
            'description':'a',
            'price':1,
            'inventory':1
        }
        response = create_product(product_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_data_is_invalid_returns_400(self , api_client , authenticate , create_product):
        authenticate(user=User(is_staff=True))
        product_data = {
            'title':'a',
            'slug':'a',
            'description':'a',
            'price':1,
            'inventory':1,
            'unit_price':24.99,
        }
        response = create_product(product_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['collection'] is not None
    
    def test_if_data_is_valid_returns_201(self , api_client , authenticate , create_product):
        authenticate(user=User(is_staff=True))
        product_data = {
            'title':'a',
            'slug':'a',
            'description':'a',
            'price':1,
            'inventory':1,
            'unit_price':24.99,
            'collection':1
        }
        response = create_product(product_data)
        assert response.status_code == status.HTTP_201_CREATED
        response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveProduct:
    def test_if_product_exists_returns_200(self , api_client):
        product = baker.make(Product)
        response = api_client.get(f'/store/products/{product.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == product.id
        assert response.data['slug'] == product.slug
        assert response.data['title'] == product.title
        assert response.data['description'] == product.description
        assert response.data['unit_price'] == product.unit_price
        assert response.data['inventory'] == product.inventory
