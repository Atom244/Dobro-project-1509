from rest_framework import permissions, viewsets
from .models import Appeal, AppealStatusHistory
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
        appeal = serializer.save(user=self.request.user)
        AppealStatusHistory.objects.create(appeal=appeal, new_status=appeal.status, comment='Обращение зарегистрировано через API')

    def perform_update(self, serializer):
        appeal = self.get_object()
        old_status = appeal.status
        appeal = serializer.save()
        if old_status != appeal.status:
            AppealStatusHistory.objects.create(appeal=appeal, old_status=old_status, new_status=appeal.status, comment='Статус изменён через API')
