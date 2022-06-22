from django.http import HttpResponse,FileResponse
from django.shortcuts import render,redirect
from employee.models import Employee
from translator import Translator
from emails.send_email import Send_Email
from data.models import Token
from create_token import GetToken
from jinja2 import Environment, FileSystemLoader
from template.make_pdf import *
import os,constants
from company.models import Company
from invoice_fe.models import Invoice_FE
from from_number_to_letters import numero_a_letras,Thousands_Separator


t = Translator()

LIST_REQUEST = []

def Create_token(request,key,value):
	LIST_REQUEST.append(key)
	request.session[key] = value


def LogOut(request):
	for i in LIST_REQUEST:
		del request.session[i]
	return redirect('/')


def Login(request):
	if request.method == 'POST':
		try:
			_data = request.POST
			employee = Employee.objects.get(user = t.codificar(str(_data.get('username'))), passwd= t.codificar(str(_data.get('passwd'))))
			Create_token(request,'name_employee',employee.company.pk)
			return redirect('List_Invoice_FE')	
		except Employee.DoesNotExist as e:
			print(e)
		
	return render(request,'home/login.html')

def Index(request):
	GetPDF(request,1)
	return render(request,'base.html')

def Forgot_Password(request):
	if request.is_ajax():
		message = ""
		try:
			try:
				employee = Employee.objects.get( email = t.codificar(str(request.GET.get('email'))))
			except Employee.DoesNotExist as ex:
				print(ex)
				message = "not allowed"
				return HttpResponse(message)
			print(employee)
			if str(t.decodificar(str(employee.post))) == "Administrador":
				message = "Permitted"
				name = t.decodificar(str(employee.firstname))+' '+t.decodificar(str(employee.surname))
				token = GetToken()
				Token(
					number = token
				).save()
				Send_Email('emails/recovery_passwd.html',{'name':name,'token':token,'pk':employee.pk}).Send_Email_Recover()
		except Exception as e:
			print(e)
			message = "not allowed"
		return HttpResponse(message)
	return render(request,'home/forgot-password.html')

def Reset_Password(request,pk,token):
	message = ""
	if request.method == 'POST':
		try:
			e = Employee.objects.get(pk = pk)
			e.passwd = t.codificar(str(request.POST.get('password')))
			e.save()
			return redirect('/')
		except Employee.DoesNotExist:
			message = "El Administrador no existe en nuestra base de datos."
	try:
		Token.objects.get(number = token).delete()
	except Token.DoesNotExist:
		return render(request,'errors/error_token')
	return render(request,'home/reset-password.html',{'message':message})



def Create_PDF_Invoice(request,pk):
	company = Company.objects.get(document_identification= t.codificar(str(900541566)))
	invoice = Invoice_FE.objects.filter(number = t.codificar(str(pk)), company = company )
	env = Environment(loader=FileSystemLoader("template"))
	template = env.get_template("invoice.html")
	name_doc = "FES-"+str(company.prefix)+str(pk)
	# _data = [
	# 	{
	# 		"name":t.decodificar(str(i.product)),
	# 		"quanty":Thousands_Separator(round(float(t.decodificar(str(i.quanty))))),
	# 		"price":Thousands_Separator(round(float(t.decodificar(str(i.price))),2)),
	# 		'tax_value':Thousands_Separator(round(float(t.decodificar(str(i.tax))),2)),
	# 		'ico':t.decodificar(str(i.ipo)),
	# 		'discount':Thousands_Separator(i.Totals_Discount()),
	# 		'totals_tax':Thousands_Separator(i.Tax_Value()),
	# 		'totals':Thousands_Separator(i.Base_Product_WithOut_Discount())
	# 	}
	# 	for i in invoice
	# ]
	# subtotal = 0
	# tax = 0
	# for i in invoice:
	# 	subtotal += i.Base_Product_WithOut_Discount()
	# 	tax += i.Tax_Value()
	# subtotal_ = Thousands_Separator(round(subtotal,2))
	# print(invoice)
	# data = {
	# 	'name_client':t.decodificar(str(invoice.last().client.name)),
	# 	"email_client":t.decodificar(str(invoice.last().client.email)),
	# 	"address_client":t.decodificar(str(invoice.last().client.address)),
	# 	'phone_client':t.decodificar(str(invoice.last().client.phone)),
	# 	"data": _data,
	# 	'cufe':'a7e53384eb9bb4251a19571450465d51809e0b7046101b87c4faef96b9bc904cf7f90035f444952dfd9f6084eeee2457433f3ade614712f42f80960b2fca43ff',
	# 	'subtotal_invoice':subtotal_,
	# 	'total_invoice':Thousands_Separator(round(subtotal + tax,2)),
	# 	'title':name_doc,
	# 	'name_company':t.decodificar(str(invoice.last().empleoyee.company.business_name)),
	# 	'address_company':t.decodificar(str(invoice.last().empleoyee.company.address)),
	# 	'email_company':t.decodificar(str(invoice.last().empleoyee.company.email)),
	# 	'phone_company':t.decodificar(str(invoice.last().empleoyee.company.phone)),
	# 	'resolution_number':invoice.last().empleoyee.company.resolution_number,
	# 	'type_organization':invoice.last().empleoyee.company.type_organization.name,
	# 	'date':t.decodificar(str(i.date)),
	# 	'total_letters': numero_a_letras(subtotal + tax).upper(),
	# 	'type_invoice':"Factura Electonica de venta",
	# 	'consecutive':t.decodificar(str(invoice.last().number)),
	# 	'logo':'https://c2.staticflickr.com/4/3123/2710432413_9f8aedce5f.jpg'
	# }
	
	# tax = {}
	# tax_0 = 0
	# tax_5 = 0
	# tax_19 = 0
	# for i in invoice:
	# 	inventory = Inventory.objects.get(code = i.code)
	# 	tax_product = t.decodificar(str(inventory.tax))
	# 	if int(tax_product) == 0:
	# 		tax_0 += round(float(t.decodificar(str(inventory.price))),2)
	# 	if int(tax_product) == 5:
	# 		tax_5 += round(i.Tax_Value(),2)
	# 	if int(tax_product) == 19:
	# 		tax_19 += round(i.Tax_Value(),2)

	# if tax_19 > 0:
	# 	data['tax_19'] = Thousands_Separator(tax_19)
	# if tax_5 > 5:
	# 	data['tax_5'] = Thousands_Separator(tax_5)
	# if tax_0 > 0:
	# 	data['tax_0'] = Thousands_Separator(tax_0)
	data = {}
	html = template.render(data)
	file = open("template/pdfs/"+name_doc+".html",'w')
	file.write(html)
	file.close()
	path = "./media/company/"+str(900541566)
	GeneratePDF(name_doc,path)
	os.remove('template/pdfs/'+name_doc+'.html')


def GetPDF(request,pk):
	company = Company.objects.get(document_identification= t.codificar(str(900541566)))	
	name_doc = "FES-"+str(company.prefix)+str(pk)
	path_dir = "/media/company/"+str(900541566)+'/'+name_doc+'.pdf'
	if not os.path.exists(path_dir):
		Create_PDF_Invoice(request,pk)
	return FileResponse(open(path_dir,'rb'),content_type='application/pdf')