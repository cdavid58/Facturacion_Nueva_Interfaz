from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^Create_Company$',Create_Company,name="Create_Company"),
		url(r'^Create_Employee$',Create_Employee,name="Create_Employee"),
		url(r'^Add_Inventory$',Add_Inventory,name="Add_Inventory"),
		url(r'^Create_Client$',Create_Client,name="Create_Client"),
		url(r'^Create_Invoice$',Create_Invoice,name="Create_Invoice"),
	]