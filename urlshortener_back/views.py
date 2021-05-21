from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .forms import CreateUserForm
from django.db.models import Sum, Count
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from urlshortener_front.models import URLdata, User
from django.http import JsonResponse

from urlshortener_front.forms import URLdataForm
import random, string,json

def user_login(request):
    context = {}
    if request.user.is_authenticated:
        return redirect(dashboard)
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect(dashboard)
            else:
                messages.info(request,'Username or Password is incorrect')
                return render(request,"back/login.html",context)
        
        return render(request,"back/login.html",context)



@login_required(login_url=user_login) #check if the user is logged otherwise redirect them to the login FUNCTION
def dashboard(request):
    form = URLdataForm()
    urls = URLdata.objects.all()
    if request.method == 'POST': 
        slug = ''.join(random.choice(string.ascii_letters)
                        for x in range(10))
        url = request.POST.get('url')
        response_data = {}  
        response_data['slug'] = slug  
        new_url = URLdata(url=url,slug=slug)
        if new_url.validate_url():
            new_url.save()
            base_url =  "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)+slug
            return JsonResponse({"final_url":base_url})
        else:
            return JsonResponse({"final_url":"Invalid URL"})
    else:
        form = URLdataForm()

    users = User.objects.all()
    urls = URLdata.objects.all()
    usercount = users.aggregate(Count('username'))
    visitors = urls.aggregate(Sum('visitors'))
    if request.user.is_superuser:
        clickcounts = urls.aggregate(Sum('clicks'))
        linkcounts = urls.aggregate(Count('slug'))
    else:
        urls = URLdata.objects.filter(user=request.user)
        clickcounts = urls.aggregate(Sum('clicks'))
        linkcounts = urls.aggregate(Count('slug'))
    context = {
        'url':urls,
        'clickcounts':clickcounts['clicks__sum'],
        'linkcounts':linkcounts['slug__count'],
        'form':form,
        'visitors':visitors['visitors__sum'],
        'usercount':usercount['username__count'],
    }
    return render(request,"back/home.html",context)

@login_required(login_url=user_login)
def links(request):
    page_number = request.GET.get('page',1)
    if request.user.is_superuser:
        urls = URLdata.objects.all()
        page = Paginator(urls,6)
        page_obj = page.get_page(page_number)
    else:
        urls = URLdata.objects.filter(user=request.user)
        page = Paginator(urls,6)
        page_obj = page.get_page(page_number)
    context = {

        'page_obj':page_obj,
    }
    return render(request,"back/links.html",context)
    

@login_required(login_url=user_login)
def users(request):
    page_number = request.GET.get('page',1)
    users = User.objects.all().filter(is_superuser=False)
    page = Paginator(users,10)
    page_obj = page.get_page(page_number)
    context = {
        'page_obj':page_obj,
        
    }
    return render(request,"back/users.html",context)

@login_required(login_url=user_login)
def delete_user(request,id):
    if request.method == 'POST':
        instance = User.objects.get(id=id)
        instance.delete()
        return redirect(users)
    else:
        return redirect(dashboard)
    return render(request,"back/users.html")

@login_required(login_url=user_login)
def delete_link(request,id):
    instance = URLdata.objects.get(id=id)
    if request.method == 'POST':
        instance.delete()
        return redirect(links)
    else:
        return redirect(dashboard)
    return render(request,"back/links.html")


@login_required(login_url=user_login)
def settings(request):
    context = {}
    return render(request,"back/settings.html",context)

def user_logout(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.user.is_authenticated:
        return redirect(dashboard)
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Welcome ' + user + '! Please Sign In') 
                return redirect(user_login)
        context = {'form':form}
        return render(request, 'back/register.html', context)