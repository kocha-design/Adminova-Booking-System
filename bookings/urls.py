from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/update/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
        # URLs za Kusimamia Huduma
    path('manage-services/', views.manage_services, name='manage_services'),
    path('manage-services/create/', views.service_form, name='create_service'),
    path('manage-services/edit/<int:service_id>/', views.service_form, name='edit_service'),
    path('manage-services/delete/<int:service_id>/', views.delete_service, name='delete_service'),
]