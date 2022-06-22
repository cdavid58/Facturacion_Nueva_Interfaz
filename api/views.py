from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.shortcuts import render
import base64
from django.utils.crypto import get_random_string
from .CreateCompany import Create_Company_
from .CreateEmployee import Create_Employee_
from .Create_Inventory import Create_Product
from .Create_Client import CreateClient
from .Create_Invoice_FE import Create_Invoice_FE_

@api_view(['POST'])
def Create_Company(request):
	data = request.data
	c = Create_Company_(data)
	message = c.Register()
	return Response({'Message':message})

@api_view(['POST'])
def Create_Employee(request):
	data = request.data
	e = Create_Employee_(data)
	passwd = get_random_string(length=96)
	message = e.Register(passwd)
	return Response({'Message':message})

@api_view(['POST'])
def Add_Inventory(request):
	data = request.data
	i = Create_Product(data)
	message = i.Register()
	return Response({'Message':message})

@api_view(['POST'])
def Create_Client(request):
	data = request.data
	c = CreateClient(data)
	message = c.Register()
	return Response({'Message':message})


@api_view(['POST'])
def Create_Invoice(request):
	data = request.data
	i = Create_Invoice_FE_(data)
	message = i.Register()
	return Response({'Message':message})


