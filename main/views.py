from urllib.parse import urlencode
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
import requests
from django.core.paginator import Paginator


BASE_TEMPLATE = 'layouts/base.html'

def make_pagination(request, model, number_per_page):
    paginator = Paginator(model, number_per_page)
    page_number = request.GET.get('page_number')
    # print(page_number)
    if not page_number:
        page_number = 1
    # print(page_number)
    pagination = paginator.get_page(page_number)
    # print(pagination.object_list)
    # obj_count = paginator.page(page_number).object_list
    # print(obj_count)
    return pagination #, obj_count.count()

def home(request):
    try:
        url = 'http://kilo.bb-business.ovh/api/articles' 
        data = {}
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers)   
        
        articles = response.json()
    except Exception as e:
        messages.error(request, "Impossible d'atteindre le serveur distant")
        articles = {}

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
        
        headers = {
            'Content-Type': 'application/json'
        }
        try:
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
        except Exception as e:
                messages.error(request, "Impossible d'atteindre le serveur distant")
    else: colis_id = ''        
    
    context = {
        'track_id': colis_id,
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

def shop(request):
    url = 'http://kilo.bb-business.ovh/api/articles'
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers)   
        articles = response.json()
    except Exception as e:
        messages.error(request, "Impossible d'atteindre le serveur distant")
        articles = []
    articles = make_pagination(request, articles, 1)
    context = {
        'articles': articles,
        'template_name': 'contents/shop/blog.html'
    }
    return render(request, BASE_TEMPLATE, context)

def contact(request):
    
    context = {
        'template_name': 'contents/contact.html'    
    }
    
    return render(request, BASE_TEMPLATE, context)