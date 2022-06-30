from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^List_Client/$',List_Client,name="List_Client"),
	url(r'^ProfileClient/(\d+)/$',ProfileClient,name="ProfileClient"),
	url(r'^DeleteClient/$',DeleteClient,name="DeleteClient"),
	]