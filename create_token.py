from django.utils.crypto import get_random_string

def GetToken():
	return get_random_string(length=96)