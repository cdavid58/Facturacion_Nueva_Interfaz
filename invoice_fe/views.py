from django.http import HttpResponse
from django.shortcuts import render
import home.views as view_home
import time, threading, queue
from .models import *
from translator import Translator

t = Translator()
my_queue = queue.Queue()

def storeInQueue(f):
  def wrapper(*args):
  	global my_queue
  	my_queue.put(f(*args))
  return wrapper

def List_Invoice_FE(request):
	import sqlite3
	connect = sqlite3.connect('db.sqlite3')
	c = connect.cursor()
	c.execute("select DISTINCT number from invoice_fe_invoice_fe where company_id = "+str(request.session['name_employee'])+" order by number desc")
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
	return render(request,'fe/list_invoice.html',{'data':_data})


@storeInQueue
def send_dian_invoice(request):
	return 'hola'
def Send_Dian(request):
	if request.is_ajax():
		start = time.time()
		u = threading.Thread(target=send_dian_invoice,args=(request,), name='Invoice')
		u.start()
		data = my_queue.get()
		return HttpResponse("Hola")



def View_Invoice(request):

	return render(request,'fe/invoice.html')
