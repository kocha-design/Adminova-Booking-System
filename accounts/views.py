from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import CustomUser

def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role', 'customer')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'accounts/register.html')

        user = CustomUser.objects.create_user(
            username=username, email=email, password=password1, role=role
        )
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect('core:home')

    return render(request, 'accounts/register.html')