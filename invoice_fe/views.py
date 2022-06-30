from django.http import HttpResponse
from django.shortcuts import render
import home.views as view_home
import time, threading, queue
from .models import *
from translator import Translator
from timeit import default_timer as timer
from api.Send_Dian_Invoice import Send_Invoice_Dian
from company.models import Company
from numba import jit
import itertools
from operator import itemgetter


t = Translator()
my_queue = queue.Queue()

def storeInQueue(f):
  def wrapper(*args):
  	global my_queue
  	my_queue.put(f(*args))
  return wrapper

@jit
def GetInvoice_(data):
	_data = [
		{
			'pk':Invoice_FE.objects.filter(number = i[0]).last().pk,
			'number': t.decodificar(str(Invoice_FE.objects.filter(number = i[0]).last().number)),
			'client':t.decodificar(str(Invoice_FE.objects.filter(number = i[0]).last().client.name)),
			'date':t.decodificar(str(Invoice_FE.objects.filter(number = i[0]).last().generated_date)),
			'state':t.decodificar(str(Invoice_FE.objects.filter(number = i[0]).last().state))
		}
		for i in data
	]
	return _data


def List_Invoice_FE(request):
	if 'nit_company' in request.session:
		import sqlite3,time
		connect = sqlite3.connect('db.sqlite3')
		c = connect.cursor()
		c.execute("select DISTINCT number from invoice_fe_invoice_fe where company_id = "+str(request.session['nit_company'])+" order by id asc limit 200")
		data = c.fetchall()
		numbers = []
		for i in range(len(data)):
			numbers.append(int(t.decodificar(str(data[i][0]))))
		number = sorted(numbers, reverse=True)
		return render(request,'fe/list_invoice.html',{'data':GetInvoice_(data)})
	return render(request,'errors/403.html')

@jit
@storeInQueue
def send_dian_invoice(request,invoice):
	token = "654bcc733f62fa7a5e9548b16057712ed4e30166a7c11f86e76eae9224faf5c0"
	sid = Send_Invoice_Dian(invoice)
	response = sid.Send(token)
	try:
		data = (response['ResponseDian']['Envelope']['Body']['SendBillSyncResponse']['SendBillSyncResult']["StatusDescription"],True)
		if response['ResponseDian']['Envelope']['Body']['SendBillSyncResponse']['SendBillSyncResult']["ErrorMessage"]['string']:
			data = (response['ResponseDian']['Envelope']['Body']['SendBillSyncResponse']['SendBillSyncResult']["ErrorMessage"]['string'],False)
	except Exception as e:
		data = response
	return data

def Send_Dian(request):
	if 'nit_company' in request.session:
		if request.is_ajax():
			pk = request.GET.get('pk')
			start = time.time()
			invoice = Invoice_FE.objects.get(number = t.codificar(str(pk)),company = Company.objects.get(pk = request.session['nit_company']))
			u = threading.Thread(target=send_dian_invoice,args=(request,invoice), name='Invoice')
			u.start()
			data = my_queue.get()
			try:
				if data[1]:
					print("Correcto")
				else:
					print("Error")
			except Exception as e:
				if 'errors' in data:
					data = (data['errors'],)
			return HttpResponse(data[0])
	return render(request,'errors/403.html')


def DeleteInvoice(request):
	if request.is_ajax():
		return HttpResponse("")


def Tax(tax_values,tax):
    grupos = itertools.groupby(sorted(tax_values, key=itemgetter(tax)), key=itemgetter(tax))
    res = [{tax: sum(dicc[tax] for dicc in diccs)} for v, diccs in grupos]
    total = 0
    for i in res:
      for j in i.values():
        total += float(j)
    return total

def List_Tax(invoice,tax):
    global t
    data = [
      ({str(tax):i.Tax_Value() * float(t.decodificar(str(i.quanty)))} if int(t.decodificar(str(i.tax))) == tax else {str(tax):0})
      for i in invoice
    ]
    if data[0] == 0:
      return (0,[0])

    base = [ (i.Base() * float(t.decodificar(str(i.quanty))) if int(t.decodificar(str(i.tax))) == tax else 0) for i in invoice]
    return (str(Tax(data,str(tax))), base)

def View_Invoice(request,pk):
	if 'nit_company' in request.session:
		invoice = Invoice_FE.objects.get(number = t.codificar(str(pk)),company = Company.objects.get(pk = request.session['nit_company']))
		invoice_dt = Invoice_FE_Details.objects.filter(invoice = invoice, company = Company.objects.get(pk = request.session['nit_company']))
		data_info = {
			'number_invoice':t.decodificar(str(invoice.number)),
			'name_client':t.decodificar(str(invoice.client.name)),
			'phone_client':t.decodificar(str(invoice.client.phone)),
			'email_client':t.decodificar(str(invoice.client.email)),
			'identification_number_client':t.decodificar(str(invoice.client.identification_number)),
			'generated_date':t.decodificar(str(invoice.generated_date)),
			'payment_due_date':t.decodificar(str(invoice_dt.last().payment_due_date)),
			'payment_method':t.decodificar(str(invoice_dt.last().payment_method)),

		}

		data_invoice = [
			{
				'description':t.decodificar(str(i.product)),
				'quanty':t.decodificar(str(i.quanty)),
				'discount':t.decodificar(str(i.discount)),
				'tax':t.decodificar(str(i.tax)),
				'ico':t.decodificar(str(i.ico)),
				'price_base':i.Base(),
				'tax_val':i.Tax_Value(),
				'subtotal':i.Base() * float(t.decodificar(str(i.quanty))),
				'neto':float(t.decodificar(str(i.price))) * float(t.decodificar(str(i.quanty)))
			}
			for i in invoice_dt
		]

		tax_19,base_19 = List_Tax(invoice_dt,19)
		tax_5,base_5 = List_Tax(invoice_dt,5)
		tax_0,base_0 = List_Tax(invoice_dt,0)
		total_tax_value = float(tax_0) + float(tax_5) + float(tax_19)
		total_base = sum(base_0) + sum(base_5) + sum(base_19)
		total_invoice = total_tax_value + total_base
		neto = [ float(t.decodificar(str(i.price))) * float(t.decodificar(str(i.quanty)))  for i in invoice_dt]




		return render(request,'fe/invoice.html',{'data_info':data_info,'invoice':data_invoice,'tax_19':tax_19,'tax_5':tax_5,'tax_0':tax_0,
				'total_tax_value':total_tax_value, 'total_base':total_base, 'total_invoice':total_invoice,'neto':sum(neto)
			})
	return render(request,'errors/403.html')
