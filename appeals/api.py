from rest_framework import permissions, viewsets
from .models import Appeal
from .serializers import AppealSerializer


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


class AppealViewSet(viewsets.ModelViewSet):
    serializer_class = AppealSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Appeal.objects.all()
        return Appeal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
