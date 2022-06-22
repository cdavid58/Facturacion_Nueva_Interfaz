from django.db import models
from translator import Translator

t = Translator()

class Company(models.Model):
	document_identification = models.TextField()
	dv = models.TextField()
	business_name = models.TextField()
	merchant_registration = models.TextField()
	address = models.TextField()
	phone = models.TextField()
	email = models.TextField()
	type_document_identification = models.TextField()
	type_organization = models.TextField()
	type_regime = models.TextField()
	certificate_generation_date = models.TextField()
	certificate_expiration_date = models.TextField()
	resolution_generation_date = models.TextField()
	resolution_expiration_date = models.TextField()
	resolution_number = models.TextField()
	prefix = models.TextField()
	

	def __str__(self):
		return t.decodificar(str(self.business_name))



class Consecutive_FE(models.Model):
	number = models.IntegerField(default=1)
	company = models.ForeignKey(Company,on_delete=models.CASCADE)

	def __str__(self):
		return t.translator(str(self.company.business_name))

class Consecutive_POS(models.Model):
	number = models.IntegerField(default=1)
	company = models.ForeignKey(Company,on_delete=models.CASCADE)

	def __str__(self):
		return t.translator(str(self.company.business_name))


class Consecutive_Payroll(models.Model):
	number = models.IntegerField(default=1)
	company = models.ForeignKey(Company,on_delete=models.CASCADE)

	def __str__(self):
		return t.translator(str(self.company.business_name))

class Consecutive_SupportDocument(models.Model):
	number = models.IntegerField(default=1)
	company = models.ForeignKey(Company,on_delete=models.CASCADE)

	def __str__(self):
		return t.translator(str(self.company.business_name))