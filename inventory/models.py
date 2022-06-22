from django.db import models
from translator import Translator
from company.models import Company

t = Translator()

class Inventory(models.Model):
	code = models.TextField(unique=True)
	product = models.TextField()
	quanty = models.TextField()
	cost = models.TextField()
	utility = models.TextField()
	tax = models.TextField()
	price = models.TextField()
	discount = models.TextField()
	initial_quanty = models.TextField()
	exhausted = models.TextField()
	company = models.ForeignKey(Company,on_delete=models.CASCADE,blank=True,null=True)
	
	def __str__(self):
		return t.decodificar(str(self.product))
