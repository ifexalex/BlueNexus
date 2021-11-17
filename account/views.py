from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password
from account.form import RegisterForm
from account.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def Register(request):
    
    if request.method == 'POST':
        
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = make_password(form.cleaned_data['password'])
            username = email.split('@')[0]
            
            user = User.objects.create(
                username=username, 
                first_name=first_name, 
                last_name=last_name, 
                email=email, 
                password=password,
            )
            
            user.save()
            messages.success(request,'Registration successful')
            redirect('login')
    else:
    
        form = RegisterForm()
    
    context = {
        'form': form,
    }
    return render(request, 'account/register.html',context)
    

def Login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request,'invalid login credentials')
            return redirect('login')
    return render(request, 'account/login.html',)

@login_required(login_url='login')
def Logout(request):

    logout(request)
    messages.success(request,'Logged out successfully')
    return redirect('login')
    