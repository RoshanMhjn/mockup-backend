from rest_framework import serializers
from .models import Mockup

class MockupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mockup
        fields = [
            "id",
            "export_type",
            "watermark_applied",
            "status",
            "file_url",
            "created_at",
        ]
        read_only_fields = fields
