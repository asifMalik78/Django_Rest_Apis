from rest_framework.test import APIClient
from pytest import fixture

@fixture
def api_client():
    return APIClient()


@fixture
def authenticate(api_client):
    def do_authenticate(user):
        return api_client.force_authenticate(user=user)
    return do_authenticate