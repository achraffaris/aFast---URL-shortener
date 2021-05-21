from django.shortcuts import render, redirect
from django.http import JsonResponse

from .forms import URLdataForm
from .models import URLdata, User
import random, string,json


def home(request):
    form = URLdataForm()
    urls = URLdata.objects.all()
    
    if request.method == 'POST': 
        slug = ''.join(random.choice(string.ascii_letters)
                        for x in range(10))
        url = request.POST.get('url')
        response_data = {}  
        response_data['slug'] = slug
        if request.user.is_authenticated:
            new_url = URLdata(url=url,slug=slug,user=request.user)
        else:
            new_url = URLdata(url=url,slug=slug)
        if new_url.validate_url():
            new_url.save()
            base_url =  "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)+slug
            return JsonResponse({"final_url":base_url})
        else:
            return JsonResponse({"final_url":"Invalid URL"})
    else:
        form = URLdataForm()

    context = {
        'form':form,
        'urls':urls,
    }
    return render(request,"front/home.html",context)


import urllib, json

def URLredirect(request,slug):
    instance = URLdata.objects.filter(slug=slug).first()
    instance.Clicked()
    return redirect(instance.url)

        
    
    
        
    