from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Service, Booking

def service_list(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'bookings/service_list.html', {'services': services})

@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id, is_active=True)
    if request.user.role != 'customer':
        messages.error(request, "Only customers can make bookings.")
        return redirect('bookings:service_list')
    
    if request.method == 'POST':
        details = request.POST.get('details')
        preferred_date = request.POST.get('preferred_date') or None
        booking = Booking.objects.create(
            customer=request.user,
            service=service,
            details=details,
            preferred_date=preferred_date
        )
        messages.success(request, f"Booking #{booking.id} submitted successfully!")
        return redirect('bookings:my_bookings')
    
    return render(request, 'bookings/book_service.html', {'service': service})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def admin_dashboard(request):
    if not request.user.is_company_staff():
        messages.error(request, "Access denied.")
        return redirect('core:home')
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'bookings/admin_dashboard.html', {'bookings': bookings})