from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^List_Invoice_FE/$',List_Invoice_FE,name="List_Invoice_FE"),
		url(r'^Send_Dian/$',Send_Dian,name="Send_Dian"),		
		url(r'^View_Invoice/$',View_Invoice,name="View_Invoice"),		
	]