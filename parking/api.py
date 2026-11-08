from rest_framework import viewsets
from .models import Parking
from .serializers import ParkingSerializer


class ParkingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get('accessible'):
            qs = qs.filter(accessible_spaces__gt=0)
        if self.request.query_params.get('free'):
            qs = qs.filter(paid=False)
        return qs
