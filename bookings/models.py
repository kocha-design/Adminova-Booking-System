from django.db import models
from django.conf import settings

class Service(models.Model):
    SERVICE_CATEGORIES = [
        ('business_consulting', 'Business Consulting & Corporate Advisory'),
        ('admin_hr', 'Administration & Human Resource Support Services'),
        ('travel_ticketing', 'Travel, Ticketing & Corporate Travel Coordination'),
        ('hotel_transfers', 'Hotel Booking, Airport Transfers & Travel Reservations'),
        ('catering', 'Corporate Catering, Food Supply & Mining Camp Catering'),
        ('technology', 'Technology Solutions, Tracking Systems & Data Management'),
        ('procurement', 'Office Supplies, Procurement & Logistics Support'),
        ('tender_docs', 'Tender Preparation, Business Documentation & Corporate Support'),
        ('events_branding', 'Event Management, Branding & Commercial Support'),
        ('general_trading', 'General Trading & Commercial Supply Services'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=SERVICE_CATEGORIES)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'), # Ongeza hii
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    details = models.TextField(help_text="Customer's specific requirements")
    preferred_date = models.DateField(null=True, blank=True)
    quoted_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.service.name} by {self.customer.username}"