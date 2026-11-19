from django.core.management.base import BaseCommand
from bookings.models import Service

SERVICES = [
    ("Business Consulting & Corporate Advisory", "business_consulting",
     "Strategic advisory, business planning, compliance and corporate governance support.", 500000),
    ("Administration & HR Support Services", "admin_hr",
     "HR policies, recruitment support, payroll administration and office management.", 300000),
    ("Travel, Ticketing & Corporate Travel Coordination", "travel_ticketing",
     "Flight booking, corporate travel planning and itinerary coordination.", 200000),
    ("Hotel Booking, Airport Transfers & Travel Reservations", "hotel_transfers",
     "Hotel reservations, airport pickups and full travel reservation support.", 150000),
    ("Corporate Catering, Food Supply & Mining Camp Catering", "catering",
     "Daily catering, event food supply and remote camp catering for mining operations.", 400000),
    ("Technology Solutions, Tracking Systems & Data Management", "technology",
     "Fleet tracking, data management systems, and IT solutions for business.", 800000),
    ("Office Supplies, Procurement & Logistics Support Services", "procurement",
     "Office supplies, procurement services, and logistics coordination.", 250000),
    ("Tender Preparation, Business Documentation & Corporate Support", "tender_docs",
     "Tender writing, business documentation and corporate support services.", 350000),
    ("Event Management, Branding & Commercial Support Services", "events_branding",
     "Event planning, branding, and commercial support for businesses.", 600000),
    ("General Trading & Commercial Supply Services", "general_trading",
     "General trading and commercial supply for offices and industrial clients.", 200000),
]

class Command(BaseCommand):
    help = "Seed the 10 Adminova service categories into the database."

    def handle(self, *args, **kwargs):
        created = 0
        for name, category, desc, price in SERVICES:
            _, was_created = Service.objects.get_or_create(
                category=category,
                defaults={'name': name, 'description': desc, 'base_price': price, 'is_active': True}
            )
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Seeded {created} new services."))