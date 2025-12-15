from django.db import models
from django.conf import settings

# Create your models here.

class Mockup(models.Model):
    STATUS_CHOICES = (
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    EXPORT_TYPE_CHOICES = (
        ("sd", "Standard"),
        ("hd", "High Definition"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mockups"
    )

    export_type = models.CharField(
        max_length=10,
        choices=EXPORT_TYPE_CHOICES,
        default="sd"
    )

    watermark_applied = models.BooleanField(default=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="processing"
    )

    file_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} | {self.export_type} | {self.status}"