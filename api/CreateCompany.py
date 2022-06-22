from validate import Validate_Email,Validate_Phone
from company.models import Company
from translator import Translator
from data.models import *

t = Translator()


class Create_Company_:
	def __init__(self,data):
		self.data = data

	def Register(self):
		try:			
			if self.Validate()[0]:
				if Validate_Email(self.data['email']):
					if Validate_Phone(self.data['phone']):
						Company(
							document_identification = t.codificar(str(self.data['document_identification'])),
							dv = t.codificar(str(self.data['dv'])),
							business_name = t.codificar(str(self.data['business_name'])),
							merchant_registration = t.codificar(str(self.data['merchant_registration'])),
							address = t.codificar(str(self.data['address'])),
							phone = t.codificar(str(self.data['phone'])),
							email = t.codificar(str(self.data['email'])),
							type_document_identification = Type_Document_Identification.objects.get(_id = self.data['type_document_identification_id']),
							type_organization = Type_Organization.objects.get(_id = self.data['type_organization_id']),
							type_regime = Type_Regime.objects.get(_id = self.data['type_regime_id']),
							certificate_generation_date = t.codificar(str(self.data['certificate_generation_date'])),
							certificate_expiration_date = t.codificar(str(self.data['certificate_expiration_date'])),
							resolution_generation_date = t.codificar(str(self.data['resolution_generation_date'])),
							resolution_expiration_date = t.codificar(str(self.data['resolution_expiration_date'])),
							resolution_number = t.codificar(str(self.data['resolution_number'])),
							prefix = t.codificar(str(self.data['prefix']))
						).save()
					else:
						return "Invalid phone number"
				else:
					return "Invalid E-mail"	
			return self.Validate()[1]
		except Exception as e:
			print(e)
			return str(e)
		

	def Validate(self):
		for i in self.data:
			if self.data[i] == "" or self.data[i] == None:
				return (False,"Missing data or wrong data")
		return (True,'Successfully created company')