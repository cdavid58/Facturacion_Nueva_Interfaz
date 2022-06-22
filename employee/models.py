from django.db import models
from company.models import Company
from translator import Translator

t = Translator()

class Employee(models.Model):
	documentIdentification = models.TextField()
	firstname = models.TextField()
	surname = models.TextField()
	address = models.TextField()
	type_contract = models.TextField()
	payroll_type_document_identification = models.TextField()
	type_worker = models.TextField()
	phone = models.TextField()
	email = models.TextField()
	company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
	salary = models.TextField()
	user = models.TextField()
	post = models.TextField()
	hiring_date = models.TextField()
	type = models.TextField()
	passwd = models.TextField(default = "")

	def __str__(self):
		return t.decodificar(str(self.firstname))+' '+t.decodificar(str(self.surname))