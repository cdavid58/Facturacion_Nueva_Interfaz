from django.db import models
from translator import Translator
from company.models import Company
from client.models import Client
from employee.models import Employee

t = Translator()

class Invoice_FE(models.Model):
	number = models.TextField()
	generated_date = models.TextField()
	state = models.TextField(default='01010011,01101001,01101110,00100000,01100101,01101110,01110110,01101001,01100001,01110010,00100000,01100001,00100000,01101100,01100001,00100000,01000100,01001001,01000001,01001110')	
	client = models.ForeignKey(Client,on_delete=models.CASCADE)
	employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
	company = models.ForeignKey(Company,on_delete=models.CASCADE)

	def __str__(self):
		return t.decodificar(str(self.number))


class Invoice_FE_Details(models.Model):
	invoice = models.ForeignKey(Invoice_FE,on_delete=models.CASCADE)
	product = models.TextField()
	quanty  = models.TextField()
	discount = models.TextField()
	tax = models.TextField()
	cost = models.TextField()
	ico = models.TextField()
	stronghold = models.TextField()
	payment_method = models.TextField()
	payment_due_date = models.TextField()
	duration_measure = models.TextField()













