from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from company.models import Company
from numba import jit
from translator import Translator
from timeit import default_timer as timer
from invoice_fe.models import Invoice_FE
import numba
from data.models import *

# this_size = numba.typed.Dict.empty(key_type=numba.types.float64, value_type=numba.types.float64)

@jit
def GetListClient(clients):
	_data = [
		{
			'pk':i.pk,
			'name':t.decodificar(str(i.name)),
			'phone': t.decodificar(str(i.phone)),
			'email': t.decodificar(str(i.email)),
			'address': t.decodificar(str(i.address))
		}
		for i in clients
	]
	return _data

def List_Client(request):
	client = Client.objects.filter(company = Company.objects.get(pk = request.session['nit_company']))
	s = timer()
	data = GetListClient(client)
	e = timer()
	print(e - s)


	return render(request,'client/list_client.html',{'clients':data})


def ProfileClient(request,pk):

	i = Client.objects.get(pk = pk)

	if request.is_ajax():
		data = request.GET

		i.identification_number = t.codificar(str(data['identification_number']))
		i.dv = t.codificar(str(data['dv']))
		i.name = t.codificar(str(data['name']))
		i.phone = t.codificar(str(data['phone']))
		i.address = t.codificar(str(data['address']))
		i.email = t.codificar(str(data['email']))
		i.merchant_registration = t.codificar(str(data['merchant_registration']))
		i.type_documentI = Type_Document_Identification.objects.get(pk = data['type_document_identification_id'])
		# i.type_organization = Type_Organization.objects.get(_id = data['type_organization_id'])
		i.type_regime = Type_Regime.objects.get(pk = data['type_regime_id'])
		i.municipality = Municipality.objects.get(pk = data['municipality_id'])
		i.save()
		return HttpResponse("Correcto")


	data = {
		'pk':i.pk,
		'name':t.decodificar(str(i.name)),
		'email':t.decodificar(str(i.email)),
		'phone':t.decodificar(str(i.phone)),
		'address':t.decodificar(str(i.address)),
		'municipality':i.municipality.name,
		'regime':i.type_regime.name,
		'type_documentI':i.type_documentI.name,
		'identification_number':t.decodificar(str(i.identification_number)),
		'dv':t.decodificar(str(i.dv)),
		'merchant_registration':t.decodificar(str(i.merchant_registration))
	}

	documentIdentification = Type_Document_Identification.objects.all()
	type_organization = Type_Organization.objects.all()
	regimen = Type_Regime.objects.all()


	return render(request,'client/profile.html',{'info':data,'organizations':type_organization,
			'regime':regimen,'documentIdentification':documentIdentification, 'munici':Municipality.objects.all()
	})


def DeleteClient(request):
	if request.is_ajax():
		print(request.GET.get('id'))
		return HttpResponse("Eliminado")