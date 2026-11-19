from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

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

@login_required
def profile_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        
        request.user.phone = phone
        request.user.email = email
        request.user.save()
        
        messages.success(request, "Profile updated successfully!")
        return redirect('accounts:profile')
        
    return render(request, 'accounts/profile.html')

# 1. View ya Kuonyesha Watumiaji Wote
@login_required
def manage_users(request):
    # Hakikisha ni Super Admin tu anayeweza kuingia
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Only Super Admins can manage users.")
        return redirect('bookings:my_bookings')
    
    # Toa watumiaji wote isipokuwa yeye mwenyewe (Brian)
    users = CustomUser.objects.exclude(id=request.user.id).order_by('-date_joined')
    
    return render(request, 'accounts/manage_users.html', {'users': users})


# 2. View ya Kubadilisha Role ya Mtumiaji
@login_required
def update_user_role(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('bookings:my_bookings')

    if request.method == 'POST':
        target_user = get_object_or_404(CustomUser, id=user_id)
        new_role = request.POST.get('role')
        
        if new_role in dict(CustomUser.ROLE_CHOICES):
            target_user.role = new_role
            # Kama ni Admin, mpe na staff status ili aweze kuingia Django Admin
            if new_role == 'admin':
                target_user.is_staff = True
            else:
                target_user.is_staff = False
                
            target_user.save()
            messages.success(request, f"{target_user.username}'s role has been updated to {target_user.get_role_display()}.")
        
    return redirect('accounts:manage_users')

# 1. View ya Kuonyesha Fomu ya Kuunda Worker
@login_required
def create_worker(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Only Super Admins can create workers.")
        return redirect('bookings:my_bookings')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role', 'worker')
        password = request.POST.get('password')

        # Kagua kama username tayari ipo
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'accounts/create_worker.html')

        # Tengeneza mtumiaji mpya
        new_user = CustomUser.objects.create_user(
            username=username,
            email=email,
            phone=phone,
            password=password,
            role=role
        )
        # Kama ni admin, mpe staff status
        if role == 'admin':
            new_user.is_staff = True
            new_user.save()

        messages.success(request, f"Worker '{username}' created successfully! Give them the password: {password}")
        return redirect('accounts:manage_users')

    return render(request, 'accounts/create_worker.html')