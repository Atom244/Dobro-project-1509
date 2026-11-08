from rest_framework import serializers
from .models import Appeal, AppealCategory


class AppealCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppealCategory
        fields = ['id', 'name', 'slug']


class AppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appeal
        fields = ['id', 'public_id', 'category', 'subject', 'description', 'address', 'status', 'created_at', 'updated_at']
        read_only_fields = ['public_id', 'status', 'created_at', 'updated_at']
