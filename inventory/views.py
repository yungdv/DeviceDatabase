from django.shortcuts import render
from .models import Hardware

def hardware_list(request):
    hardware = Hardware.objects.all()
    return render(request, 'inventory/hardware_list.html', {'hardware': hardware})
