from rest_framework import serializers
from .models import Mockup, MockupTemplate, GeneratedMockup

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

class MockupTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockupTemplate
        fields = [
            "id",
            "name",
            "description",
            "preview_image_url",
        ]

class MockupTemplateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockupTemplate
        fields = [
            "id",
            "psd_path",
            "smart_object_name",
            "bound_width",
            "bound_height",
            "bound_x",
            "bound_y",
        ]

class GeneratedMockupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedMockup
        fields = "__all__"
        read_only_fields = ("user", "created_at")

class AdminMockupTemplateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockupTemplate
        fields = [
            "id",
            "name",
            "description",
            "psd_path",
            "smart_object_name",
            "preview_image_url",
        ]
        read_only_fields = ("id",)