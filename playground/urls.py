from django.urls import path
from . import views

urlpatterns = [
    # path('sayHellow/', views.say_hellow)
    path('sayHellow/', views.HellowView.as_view())
]