import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings

def generate_mockup_via_node(template, design_file, options):
    url = f"{settings.NODE_MOCKUP_ENGINE_URL}/api/generate"

    response = requests.post(
        url,
        files={"design": design_file},
        data={
            "psd_path": template.psd_path,
            "smart_object_name": template.smart_object_name,
            "export_quality": options["export_quality"],
            "watermark": options["watermark"],
        },
        timeout=120,
    )

    if response.status_code != 200:
        raise Exception(f"Node error: {response.text}")

    # 🔥 Response is image bytes
    filename = f"{template.id}.png"

    django_file = ContentFile(response.content)

    saved_path = default_storage.save(
        f"mockups/generated/{filename}",
        django_file,
    )

    return default_storage.url(saved_path)