from django.shortcuts import render
from .models import Product, SiteSettings

# Create your views here.

def home(request):
    products = Product.objects.filter(is_active=True)
    settings, created = SiteSettings.objects.get_or_create(id=1)
    
    context = {
        'products': products,
        'settings': settings,
    }
    return render(request, 'home.html', context)

def checkout(request):
    settings, created = SiteSettings.objects.get_or_create(id=1)
    context = {
        'settings': settings,
    }
    return render(request, 'checkout.html', context)
