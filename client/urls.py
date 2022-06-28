from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^List_Client/$',List_Client,name="List_Client"),
	]