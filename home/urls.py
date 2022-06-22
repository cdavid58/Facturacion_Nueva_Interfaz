from django.conf.urls import url
from .views import *

urlpatterns=[
		url(r'^$',Login,name="Login"),
		url(r'^Index/$',Index,name="Index"),
		url(r'^LogOut/$',LogOut,name="LogOut"),
		url(r'^Forgot_Password/$',Forgot_Password,name="Forgot_Password"),
		url(r'^Reset_Password/(\d+)/(\w+)/$',Reset_Password,name="Reset_Password"),	
	]