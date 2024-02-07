from urllib.parse import urlencode
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
import requests


BASE_TEMPLATE = 'layouts/base.html'

def home(request):
    
    url = 'http://kilo.bb-business.ovh/api/articles' 
    data = {}
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)   
    
    articles = response.json()

    context = {
        'articles': articles,
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

def create_shipping(request):
    context = {
        'template_name': 'contents/shipping/create-shipping.html'
    }
    
    return render(request, BASE_TEMPLATE, context)

def tracking(request):
    
    if request.POST:
        user_id = request.POST.get('user_id')
        colis_id = request.POST.get('trackid')
        url = f'http://kilo.bb-business.ovh/api/client-tracking-check/{user_id}/{colis_id}'
        
        # print(url)
        # data = {
        #     'id': user_id,
        #     'qr_colis': colis_id,
        # }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers)   
        if response.status_code == 200:
            track = response.json()
            
            redirect_url = reverse('tracking-result')
            request.session['track'] = track
            # params = urlencode({'track': track,})
            # target = f'{redirect_url}?{params}'
            
            return redirect(redirect_url)
        
        elif response.status_code == 404:
            messages.error(request, "Id du track incorrect")
            
    
    context = {
        'template_name': 'contents/shipping/tracking.html',
    }
    return render(request, BASE_TEMPLATE, context)

def tracking_result(request):
    
    track = request.session.get('track')
    
    # print('track', track)
    
    context = {
        'track': track[0],
        'template_name': 'contents/shipping/tracking-result.html',
    }
    return render(request, BASE_TEMPLATE, context)