from django.shortcuts import render
from django.views.defaults import page_not_found
 
def mi_error_404(request, exception, template_name="errors/404.html"):
	print("Entre")
	response = render_to_response(template_name)
	response.status_code = 404
	print(response.status_code)
	return response