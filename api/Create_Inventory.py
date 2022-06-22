from django.db import IntegrityError
from inventory.models import Inventory
from translator import Translator
from company.models import Company

t = Translator()

class Create_Product:
	def __init__(self,data):
		self.data = data
		print(self.data)

	def Register(self):
		try:
			Inventory(
				code = t.codificar(str(self.data['code'])),
				product = t.codificar(str(self.data['product'])),
				quanty = t.codificar(str(self.data['quanty'])),
				cost = t.codificar(str(self.data['cost'])),
				utility = t.codificar(str(self.data['utility'])),
				tax = t.codificar(str(self.data['tax'])),
				price = t.codificar(str(self.data['price'])),
				discount = t.codificar(str(self.data['discount'])),
				initial_quanty = t.codificar(str(self.data['initial_quanty'])),
				exhausted = t.codificar(str(self.data['exhausted'])),
				company = Company.objects.get(document_identification = t.codificar(str(self.data['company'])))
			).save()
		except Exception as i:
			return i
		return "Success"





