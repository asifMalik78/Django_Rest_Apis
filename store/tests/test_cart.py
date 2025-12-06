from rest_framework import status
import pytest
from store.models import Cart , CartItem , Product
from model_bakery import baker


@pytest.mark.django_db
class TestCartCreate:
    def test_if_cart_not_exists_returns_405(self , api_client):
        response = api_client.get('/store/carts/')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_if_product_added_to_cart_returns_201(self , api_client):
        product = baker.make(Product)
        cart = baker.make(Cart)
        response = api_client.post(f'/store/carts/{cart.id}/items/' , {'product_id':product.id , 'quantity':1})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
    
    def test_if_invalid_product_added_to_cart_returns_400(self , api_client):
        cart = baker.make(Cart)
        response = api_client.post(f'/store/carts/{cart.id}/items/' , {'product_id':1 , 'quantity':1})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_if_invalid_quantity_added_to_cart_returns_400(self , api_client):
        cart = baker.make(Cart)
        response = api_client.post(f'/store/carts/{cart.id}/items/' , {'product_id':1 , 'quantity':-1})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    


@pytest.mark.django_db
class TestRetrieveCart:
    def test_if_cart_exists_returns_201(self , api_client):
        cart = baker.make(Cart)
        response = api_client.get(f'/store/carts/{cart.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == str(cart.id)
