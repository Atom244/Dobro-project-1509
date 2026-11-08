from django.contrib import admin
from .models import Appeal, AppealCategory, AppealStatusHistory


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ['public_id', 'subject', 'user', 'category', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['public_id', 'subject', 'description', 'user__username']
    readonly_fields = ['public_id', 'created_at', 'updated_at']

    def save_model(self, request, obj, form, change):
        old = None
        if change:
            old = Appeal.objects.get(pk=obj.pk).status
        super().save_model(request, obj, form, change)
        if not change or old != obj.status:
            AppealStatusHistory.objects.create(appeal=obj, old_status=old or '', new_status=obj.status)


admin.site.register(AppealCategory)
admin.site.register(AppealStatusHistory)
