from django.conf import settings


def space_name(request):
    return {
        "space_name": settings.VCAP_APPLICATION.get("space_name", "unknown"),
    }
