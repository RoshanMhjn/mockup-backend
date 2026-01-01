from django.contrib import admin
from .models import MockupTemplate, GeneratedMockup, Mockup

@admin.register(MockupTemplate)
class MockupTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "smart_object_name",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = ("name", "smart_object_name")


@admin.register(GeneratedMockup)
class GeneratedMockupAdmin(admin.ModelAdmin):
    list_display = ("user", "template", "created_at")
    search_fields = ("user__email", "template__name")


@admin.register(Mockup)
class MockupAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "export_type", "created_at")
    list_filter = ("status", "export_type")
