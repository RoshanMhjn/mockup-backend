from django.core.files.base import File
from django.core.files.storage import default_storage
import os


def store_generated_mockup(local_path, filename):
    """
    Stores generated mockup using Django storage
    (local / MinIO / S3)
    """
    with open(local_path, "rb") as f:
        django_file = File(f)
        saved_path = default_storage.save(
            f"mockups/generated/{filename}",
            django_file,
        )

    return default_storage.url(saved_path)
