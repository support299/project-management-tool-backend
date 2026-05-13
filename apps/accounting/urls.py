from django.http import JsonResponse
from django.urls import path


def health(request):
    return JsonResponse({"status": "accounting-ready"})


urlpatterns = [
    path("health/", health, name="accounting-health"),
]
