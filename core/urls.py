from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    # Kama ulikuwa na path('welcome/', ...), inafaa pia
]