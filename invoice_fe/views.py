from django.http import HttpResponse
from django.shortcuts import render
import home.views as view_home
import time, threading, queue
from .models import *
from translator import Translator
from api.Send_Dian_Invoice import Send_Invoice_Dian
from company.models import Company

t = Translator()
my_queue = queue.Queue()

def storeInQueue(f):
  def wrapper(*args):
  	global my_queue
  	my_queue.put(f(*args))
  return wrapper

def List_Invoice_FE(request):
	import sqlite3,time
	start = time.time()
	print('Inicie')
	connect = sqlite3.connect('db.sqlite3')
	c = connect.cursor()
	c.execute("select DISTINCT number from invoice_fe_invoice_fe where company_id = "+str(request.session['nit_company'])+" order by number desc")
	data = c.fetchall()
	_data = []
	for i in data:
		invoice = Invoice_FE.objects.filter(number = i[0]).last()
		_data.append({
				'pk':invoice.pk,
				'number': t.decodificar(str(invoice.number)),
				'client':t.decodificar(str(invoice.client.name)),
				'date':t.decodificar(str(invoice.generated_date)),
				'state':t.decodificar(str(invoice.state))
			})
	print("Final",time.time() - start)
	return render(request,'fe/list_invoice.html',{'data':_data})


@storeInQueue
def send_dian_invoice(request,invoice):
	token = "654bcc733f62fa7a5e9548b16057712ed4e30166a7c11f86e76eae9224faf5c0"
	sid = Send_Invoice_Dian(invoice)
	response = sid.Send(token)
	data = response['ResponseDian']['Envelope']['Body']['SendBillSyncResponse']['SendBillSyncResult']["StatusDescription"]
	if response['ResponseDian']['Envelope']['Body']['SendBillSyncResponse']['SendBillSyncResult']["ErrorMessage"]['string']:
		data = response['ResponseDian']['Envelope']['Body']['SendBillSyncResponse']['SendBillSyncResult']["ErrorMessage"]['string']
	return data

def Send_Dian(request):
	if request.is_ajax():
		pk = request.GET.get('pk')
		start = time.time()
		invoice = Invoice_FE.objects.filter(number = t.codificar(str(pk)),company = Company.objects.get(pk = request.session['nit_company']))
		print(invoice)
		u = threading.Thread(target=send_dian_invoice,args=(request,invoice), name='Invoice')
		u.start()
		data = my_queue.get()
		return HttpResponse(data)


def DeleteInvoice(request):
	if request.is_ajax():
		return HttpResponse("")



def View_Invoice(request,pk):
	invoice = Invoice_FE.objects.get(number = t.codificar(str(pk)),company = Company.objects.get(pk = request.session['nit_company']))
	print(invoice)
	invoice_dt = Invoice_FE_Details.objects.filter(invoice = invoice, company = Company.objects.get(pk = request.session['nit_company']))
	print(invoice_dt)
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
			'tax_val':i.Tax_Value()
		}
		for i in invoice_dt
	]



	return render(request,'fe/invoice.html',{'data_info':data_info,'invoice':data_invoice})
