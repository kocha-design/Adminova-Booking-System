from django.shortcuts import render

def home(request):
    # Badilisha 'core/home.html' kuwa 'core/landing.html'
    return render(request, 'core/landing.html')