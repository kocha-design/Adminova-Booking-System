from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Service, Booking
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import io

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
    
    # Chukua bookings zote, lakini panga kwa status
    all_bookings = Booking.objects.all().order_by('-created_at')
    
    # Hesabu kwa ajili ya muhtasari (Summary Cards)
    pending_count = Booking.objects.filter(status='pending').count()
    confirmed_count = Booking.objects.filter(status='confirmed').count()
    rejected_count = Booking.objects.filter(status='rejected').count()
    
    context = {
        'bookings': all_bookings,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'rejected_count': rejected_count,
    }
    return render(request, 'bookings/admin_dashboard.html', context)

@login_required
def update_booking_status(request, booking_id):
    if not request.user.is_company_staff():
        messages.error(request, "Access denied.")
        return redirect('core:home')

    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        quoted_price = request.POST.get('quoted_price')
        admin_notes = request.POST.get('admin_notes', '')

        if new_status in dict(Booking.STATUS_CHOICES):
            booking.status = new_status
            if quoted_price:
                booking.quoted_price = quoted_price
            if admin_notes:
                booking.admin_notes = admin_notes
            booking.save()
            messages.success(request, f"Booking #{booking.id} updated successfully.")

    return redirect('bookings:admin_dashboard')

# 1. View ya Kuonyesha Huduma Zote kwa Admin
@login_required
def manage_services(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('bookings:my_bookings')
    
    # Chukua huduma zote (zilizofichwa na zilizo hai)
    services = Service.objects.all().order_by('category')
    return render(request, 'bookings/manage_services.html', {'services': services})


# 2. View ya Kuongeza au Kurekebisha Huduma
@login_required
def service_form(request, service_id=None):
    if not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('bookings:my_bookings')

    # Kama service_id imetolewa, tuna-edit. Kama haipo, tunaunda mpya.
    if service_id:
        service = get_object_or_404(Service, id=service_id)
    else:
        service = None

    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        description = request.POST.get('description')
        base_price = request.POST.get('base_price') or None
        is_active = request.POST.get('is_active') == 'on'

        if service:
            # Update iliyopo
            service.name = name
            service.category = category
            service.description = description
            service.base_price = base_price
            service.is_active = is_active
            service.save()
            messages.success(request, f"Service '{name}' updated successfully.")
        else:
            # Tengeneza mpya
            Service.objects.create(
                name=name,
                category=category,
                description=description,
                base_price=base_price,
                is_active=is_active
            )
            messages.success(request, f"Service '{name}' created successfully.")

        return redirect('bookings:manage_services')

    return render(request, 'bookings/service_form.html', {'service': service})


# 3. View ya Kufuta Huduma
@login_required
def delete_service(request, service_id):
    if not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('bookings:my_bookings')

    service = get_object_or_404(Service, id=service_id)
    service_name = service.name
    service.delete()
    messages.success(request, f"Service '{service_name}' deleted successfully.")
    return redirect('bookings:manage_services')

# 1. PDF ya Quotation
@login_required
def download_quotation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Ruhusu tu kama ni mmiliki au ni staff
    if booking.customer != request.user and not request.user.is_company_staff():
        messages.error(request, "Access denied.")
        return redirect('bookings:my_bookings')

    # Ruhusu tu kama booking imekubaliwa au ina bei
    if booking.status not in ['confirmed', 'in_progress', 'completed'] or not booking.quoted_price:
        messages.error(request, "Quotation is only available for confirmed bookings with a set price.")
        return redirect('bookings:my_bookings')

    html_string = render_to_string('bookings/pdf/quotation.html', {'booking': booking})
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Quotation_{booking.id}.pdf"'
    return response


# 2. PDF ya Receipt
@login_required
def download_receipt(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.customer != request.user and not request.user.is_company_staff():
        messages.error(request, "Access denied.")
        return redirect('bookings:my_bookings')

    if booking.status != 'completed':
        messages.error(request, "Receipt is only available for completed bookings.")
        return redirect('bookings:my_bookings')

    html_string = render_to_string('bookings/pdf/receipt.html', {'booking': booking})
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Receipt_{booking.id}.pdf"'
    return response


# 3. PDF ya Confirmation
@login_required
def download_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.customer != request.user and not request.user.is_company_staff():
        messages.error(request, "Access denied.")
        return redirect('bookings:my_bookings')

    if booking.status not in ['confirmed', 'in_progress', 'completed']:
        messages.error(request, "Confirmation is only available for confirmed bookings.")
        return redirect('bookings:my_bookings')

    html_string = render_to_string('bookings/pdf/confirmation.html', {'booking': booking})
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Confirmation_{booking.id}.pdf"'
    return response