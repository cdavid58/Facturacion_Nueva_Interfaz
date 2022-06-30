import json, requests, time
from numba import jit
from invoice_fe.models import Invoice_FE_Details
from translator import Translator
from datetime import datetime,date
import itertools
from operator import itemgetter
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings

warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)


t = Translator()

class Send_Invoice_Dian:
  def __init__(self,invoice):
    self.invoice = invoice
    self.details = Invoice_FE_Details.objects.filter(invoice=self.invoice)

  def Customer(self):
    return {
      "identification_number": 900541566,
      "dv": 2,
      "name": t.decodificar(str(self.invoice.client.name)),
      "phone": t.decodificar(str(self.invoice.client.phone)),
      "address": t.decodificar(str(self.invoice.client.address)),
      "email": t.decodificar(str(self.invoice.client.email)),
      "merchant_registration": t.decodificar(str(self.invoice.client.merchant_registration)),
      "type_document_identification_id": self.invoice.client.type_documentI.pk,
      "type_organization_id": self.invoice.client.type_organization.pk,
      "type_liability_id": 14,
      "municipality_id": self.invoice.client.municipality.pk,
      "type_regime_id": self.invoice.client.type_regime.pk
    }

  def PaymentForm(self):
    return {
      "payment_form_id": 1 if int(t.decodificar(str(self.details.last().payment_method))) == 10 else 2,
      "payment_method_id": t.decodificar(str(self.details.last().payment_method)),
      "payment_due_date": t.decodificar(str(self.details.last().payment_due_date)),
      "duration_measure": t.decodificar(str(self.details.last().duration_measure))
    }

  @jit
  def GetBaseTotals(self):
    return [i.Base() * float(t.decodificar(str(i.quanty))) for i in self.details]

  @jit
  def GetTotals(self):
    return [i.Totals() for i in self.details]

  def Legal_Monetary_Totals(self):
    return {
      "line_extension_amount": sum(self.GetBaseTotals()),
      "tax_exclusive_amount": sum(self.GetBaseTotals()),
      "tax_inclusive_amount": sum(self.GetTotals()),
      "payable_amount": sum(self.GetTotals())
    }

  
  def Tax(self,tax_values,tax):
    grupos = itertools.groupby(sorted(tax_values, key=itemgetter(tax)), key=itemgetter(tax))
    res = [{tax: sum(dicc[tax] for dicc in diccs)} for v, diccs in grupos]
    total = 0
    for i in res:
      for j in i.values():
        total += float(j)
    return total

  @jit
  def List_Tax(self,tax):
    global t
    data = [
      ({str(tax):i.Tax_Value() * float(t.decodificar(str(i.quanty)))} if int(t.decodificar(str(i.tax))) == tax else {str(tax):0})
      for i in self.details
    ]
    print('VALORES IVA',data)
    if data[0] == 0:
      return (0,[0])

    base = [ (i.Base() * float(t.decodificar(str(i.quanty))) if int(t.decodificar(str(i.tax))) == tax else 0) for i in self.details]
    return (str(self.Tax(data,str(tax))), base)


  @jit 
  def Tax_Totals(self):
    return [    
      {
        "tax_id": 1,
        "tax_amount": self.List_Tax(19)[0],
        "percent": "19.00",
        "taxable_amount": str(sum(self.List_Tax(19)[1]))
      },
      {
        "tax_id": 1,
        "tax_amount": self.List_Tax(5)[0],
        "percent": "5.00",
        "taxable_amount": str(sum(self.List_Tax(5)[1]))
      },
      {
        "tax_id": 1,
        "tax_amount": self.List_Tax(0)[0],
        "percent": "0.00",
        "taxable_amount": str(sum(self.List_Tax(0)[1]))
      },
    ]

  def Invoice_Lines(self):
    return [
      {
        "unit_measure_id": 70,
        "invoiced_quantity": t.decodificar(str(i.quanty)),
        "line_extension_amount": i.Base() * float(t.decodificar(str(i.quanty))),
        "free_of_charge_indicator": False,
        "tax_totals": [
          {
            "tax_id": 1,
            "tax_amount": i.Tax_Value() * float(t.decodificar(str(i.quanty))),
            "taxable_amount": i.Base(),
            "percent": t.decodificar(str(i.tax))
          }
        ],
        "description": t.decodificar(str(i.product)),
        "notes": "",
        "code": "001",
        "type_item_identification_id": 4,
        "price_amount": t.decodificar(str(i.price)),
        "base_quantity": t.decodificar(str(i.quanty))
      }
      for i in self.details
    ]

  def Data(self):
    print(str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second),'Hora')
    return {
      "number": 2500,
      "type_document_id": 1,
      "date": str(date.today()),
      "time":"04:08:12" ,
      "resolution_number": t.decodificar(str(self.invoice.company.resolution_number)),
      "prefix": t.decodificar(str(self.invoice.company.prefix)),
      "notes": "No hay",
      "establishment_name": t.decodificar(str(self.invoice.company.business_name)),
      "establishment_address": t.decodificar(str(self.invoice.company.address)),
      "establishment_phone": t.decodificar(str(self.invoice.company.phone)),
      "establishment_municipality": 1
    }
  

  @jit
  def Send(self,token):
    self.List_Tax(19)
    url = "http://localhost/api_solo_pdf/public/api/ubl2.1/invoice"
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'host': 'apidian2022.oo',
      'Authorization': 'Bearer '+str(token)
    }

    data = {}
    data = self.Data()
    data['customer'] = self.Customer()
    data['payment_form'] = self.PaymentForm()
    data['legal_monetary_totals'] = self.Legal_Monetary_Totals()
    data['tax_totals'] = self.Tax_Totals()
    data['invoice_lines'] = self.Invoice_Lines()
    payload = json.dumps(data)
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)