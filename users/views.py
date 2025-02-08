from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def registerUser(request):
    context = {'state': ''}
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            try:
                user = User(username=username, email=email)
                user.set_password(password1)  # Make sure to set the password securely
                user.save()
                return redirect('/login/')
            except Exception as e:
                context['state'] = str(e)  # Convert the exception to string for better display
                return render(request, 'register.html', context)
        else:
            context['state'] = 'Password1 and Password2 are not the same.'
            return render(request, 'register.html', context)
    return render(request, 'register.html', context)


def loginUser(request):
    context = {'state': ''}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)  # Log the user in
            return redirect('home')
        else:
            context['state'] = 'Invalid credentials, please try again.'
            return render(request, 'login.html', context)
    
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
