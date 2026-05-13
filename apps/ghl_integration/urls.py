from django.http import JsonResponse
from django.urls import path


def health(request):
    return JsonResponse({"status": "ghl-integration-ready"})

urlpatterns = [
    path("health/", health, name="ghl-health"),
]
