from django.shortcuts import render
from .models import Parking


def map_view(request):
    qs = Parking.objects.all()
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(address__icontains=q)
    if request.GET.get('accessible') or request.GET.get('special'):
        qs = qs.filter(accessible_spaces__gt=0)
    if request.GET.get('free'):
        qs = qs.filter(paid=False)
    if request.GET.get('paid'):
        qs = qs.filter(paid=True)
    if request.GET.get('open24'):
        qs = qs.filter(open_24h=True)
    return render(request, 'parking/map.html', {'parkings': qs, 'q': q})
