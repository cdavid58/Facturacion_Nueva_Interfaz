from django.shortcuts import render

def handler404(request, exception, template_name="errors/404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response

def handler500(request, *args, **argv):
	return render(request, 'errors/500.html', status=500)