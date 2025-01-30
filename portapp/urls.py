from django.urls import path
from django.conf import settings
from port import urls
from .views import *


urlpatterns = [
    path('contact/', ContactSet.as_view(), name='contact-create'),
    path('contactget/', ContactGet.as_view(), name='contactget'),
    ]