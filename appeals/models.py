from django.conf import settings
from django.db import models


class AppealCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=130, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория обращения'
        verbose_name_plural = 'Категории обращений'

    def __str__(self):
        return self.name


class Appeal(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Новое'
        ACCEPTED = 'accepted', 'Принято'
        IN_PROGRESS = 'in_progress', 'В работе'
        INFO = 'info', 'Требуется дополнительная информация'
        RESOLVED = 'resolved', 'Решено'
        CLOSED = 'closed', 'Закрыто'

    public_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appeals')
    category = models.ForeignKey(AppealCategory, on_delete=models.PROTECT, related_name='appeals')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=300, blank=True)
    attachment = models.FileField(upload_to='appeals/%Y/%m/', blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.public_id:
            super().save(*args, **kwargs)
            self.public_id = f'SPB-{self.created_at.year}-{self.pk:06d}'
            return super().save(update_fields=['public_id'])
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.public_id}: {self.subject}'


class AppealStatusHistory(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20, choices=Appeal.Status.choices)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.appeal.public_id}: {self.get_new_status_display()}'
