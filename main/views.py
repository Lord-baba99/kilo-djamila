from django.shortcuts import render
import requests
import json


BASE_TEMPLATE = 'layouts/base.html'

def home(request):
    
    url = 'http://kilo.bb-business.ovh/api/articles' 
    data = {}
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)   
    
    context = {
        'template_name': 'contents/index.html'
    }
    return render(request, BASE_TEMPLATE, context)

def service(request):
    
    context = {
        'template_name': 'contents/services/services.html',
    }
    return render(request, BASE_TEMPLATE, context)

def single_service(request):
    
    context = {
        'template_name': 'contents/services/single-services.html',
    }
    return render(request, BASE_TEMPLATE, context)