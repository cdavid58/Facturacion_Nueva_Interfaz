import json, requests

class Send_Invoice_Dian:
  def __init__(self,invoice):
    self.invoice = invoice

  def Customer(self):
    return {
      "identification_number": 89008003,
      "dv": 2,
      "name": "INVERSIONES DAVAL SAS",
      "phone": 3103891693,
      "address": "CLL 4 NRO 33-90",
      "email": "alexanderobandolondono@gmail.com",
      "merchant_registration": "0000000-00",
      "type_document_identification_id": 6,
      "type_organization_id": 1,
          "type_liability_id": 7,
      "municipality_id": 822,
      "type_regime_id": 1
    }

  def PaymentForm(self):
    return {
      "payment_form_id": 2,
      "payment_method_id": 30,
      "payment_due_date": "2022-05-21",
      "duration_measure": "30"
    }

  def Legal_Monetary_Totals(self):
    return {
      "line_extension_amount": "840336.134",
      "tax_exclusive_amount": "840336.134",
      "tax_inclusive_amount": "1000000.00",
      "payable_amount": "1000000.00"
    }

  def Tax_Totals(self):
    return [
      {
        "tax_id": 1,
        "tax_amount": "159663.865",
        "percent": "19.00",
        "taxable_amount": "840336.134"
      }
    ]

  def Invoice_Lines(self):
    return [
      {
        "unit_measure_id": 70,
        "invoiced_quantity": "1",
        "line_extension_amount": "840336.134",
        "free_of_charge_indicator": False,
        "tax_totals": [
          {
            "tax_id": 1,
            "tax_amount": "159663.865",
            "taxable_amount": "840336.134",
            "percent": "19.00"
          }
        ],
        "description": "COMISION POR SERVICIOS",
              "notes": "ESTA ES UNA PRUEBA DE NOTA DE DETALLE DE LINEA.",
        "code": "COMISION",
        "type_item_identification_id": 4,
        "price_amount": "1000000.00",
        "base_quantity": "1"
      }
    ]

  def Data(self):
    return {
      "number": 2500,
      "type_document_id": 1,
      "date": "2022-04-21",
      "time": "04:08:12",
      "resolution_number": "18760000001",
      "prefix": "SETP",
      "notes": "ESTA ES UNA NOTA DE PRUEBA, ESTA ES UNA NOTA DE PRUEBA, ESTA ES UNA NOTA DE PRUEBA, ESTA ES UNA NOTA DE PRUEBA, ESTA ES UNA NOTA DE PRUEBA, ESTA ES UNA NOTA DE PRUEBA, ESTA ES UNA NOTA DE PRUEBA, ESTA ES UNA NOTA DE PRUEBA, ESTA ES UNA NOTA DE PRUEBA, ESTA ES UNA NOTA DE PRUEBA, ESTA ES UNA NOTA DE PRUEBA, ESTA ES UNA NOTA DE PRUEBA, ESTA ES UNA NOTA DE PRUEBA, ESTA ES UNA NOTA DE PRUEBA",
      "disable_confirmation_text": True,
      "establishment_name": "TORRE SOFTWARE",
      "establishment_address": "BRR LIMONAR MZ 6 CS 3 ET 1 PISO 2",
      "establishment_phone": "3226563672",
      "establishment_municipality": 1
    }

  def Send(self,token):
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