from translator import Translator
from employee.models import Employee
from company.models import Company
from client.models import Client
from inventory.models import Inventory
from invoice_fe.models import Invoice_FE,Invoice_FE_Details

t = Translator()

class Create_Invoice_FE_:
	def __init__(self,data):
		self.i = data['invoice']
		self.d = data['details']

	def Register(self):
		Invoice_FE(
			number = t.codificar(str(self.i['number'])),
			generated_date = t.codificar(str(self.i['generated_date'])),
			client = Client.objects.get(identification_number = t.codificar(self.i['client'])),
			employee = Employee.objects.get(documentIdentification=t.codificar(self.i['employee'])),
			company = Company.objects.get(document_identification=t.codificar(self.i['company']))
		).save()
		for i in self.d:
			Invoice_FE_Details(
				invoice = Invoice_FE.objects.get(number = t.codificar(str(self.i['number']))),
				product = t.codificar(str(i['product'])),
				quanty  = t.codificar(str(i['quanty'])),
				discount = t.codificar(str(i['discount'])),
				tax = t.codificar(str(i['tax'])),
				cost = t.codificar(str(i['cost'])),
				ico = t.codificar(str(i['ico'])),
				stronghold = t.codificar(str(i['stronghold'])),
				payment_method = t.codificar(str(i['payment_method'])),
				payment_due_date = t.codificar(str(i['payment_due_date'])),
				duration_measure = t.codificar(str(i['duration_measure'])),
				price = t.codificar(str(i['price'])),
				company = Company.objects.get(document_identification=t.codificar(self.i['company']))
			).save()

		return 'Success'