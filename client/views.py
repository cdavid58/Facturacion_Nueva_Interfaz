from django.shortcuts import render
from .models import *
from company.models import Company
from numba import jit
from translator import Translator
from timeit import default_timer as timer
from invoice_fe.models import Invoice_FE
import numba

# this_size = numba.typed.Dict.empty(key_type=numba.types.float64, value_type=numba.types.float64)

@jit
def GetListClient(clients):
	_data = [
		{
			'number':t.decodificar(str(i.number)),
			'date': t.decodificar(str(i.generated_date)),
		}
		for i in clients
	]
	return _data

def List_Client(request):
	client = Invoice_FE.objects.filter(company = Company.objects.get(pk = request.session['nit_company']))
	s = timer()
	data = GetListClient(client)
	e = timer()
	print(e - s)
	return render(request,'client/list_client.html',{'clients':data})