from django.shortcuts import render,redirect
from .models import Receipe

from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth import login,logout,authenticate



from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/api/login/")
def receipes(request):
    if request.method=='POST':
        data=request.POST
        receipe_image=request.FILES.get('receipe_image')
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')

        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image
        )

        return redirect('/api/receipes/')
    
    queryset=Receipe.objects.all()

    if request.GET.get('search'):
        queryset=queryset.filter(receipe_name__icontains=request.GET.get('search'))
    
    # queryset=Receipe.objects.all()
    context={'receipes':queryset}

    return render(request,'receipes.html',context)


@login_required(login_url="/api/login/")
def delete_receipe(request,id):
    queryset=Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('/api/receipes/')


@login_required(login_url="/api/login/")
def update_receipe(request,id):
    queryset=Receipe.objects.get(id=id)

    if request.method=='POST':
        data=request.POST
        receipe_image=request.FILES.get('receipe_image')
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')

        queryset.receipe_name=receipe_name
        queryset.receipe_description=receipe_description
        if receipe_image:
            queryset.receipe_image=receipe_image

        queryset.save()
        return redirect('/api/receipes/')

    context={'receipe':queryset}
    return render(request,'update_receipe.html',context)
    # return 


def register(request):

    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')

        user=User.objects.filter(username=username)
        if user.exists():
            messages.add_message(request, messages.INFO, "Username already exists")
            return redirect('/api/register/')

        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )

        user.set_password(password)
        user.save()

        messages.add_message(request, messages.INFO, "Account created successfully")
        return redirect('/api/register/')
    return render(request,'register.html')



def login_page(request):
     if request.method=="POST":
        
        username=request.POST.get('username')
        password=request.POST.get('password')
        

        user=User.objects.filter(username=username)
        if not user.exists:
            messages.add_message(request, messages.INFO, "Not registered")
            return redirect('/api/login/')

        user=authenticate(username=username,password=password)

        if user is None:
            messages.add_message(request, messages.INFO, "Credentials are not correct")
        else:
            login(request,user)
            return redirect('/api/receipes/')
    
     return render(request,'login.html')


def logout_page(request):
    logout(request)
    return redirect('/api/login/')