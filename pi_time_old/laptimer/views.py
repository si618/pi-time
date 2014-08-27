from django.shortcuts import render_to_response
import logging


logger = logging.getLogger('laptimer')

def home(request):
	return render_to_response('laptimer/home.html', {'track': 'tracks'})
