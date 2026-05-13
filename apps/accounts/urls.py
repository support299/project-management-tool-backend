from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClientProfileViewSet, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("clients", ClientProfileViewSet, basename="client")

urlpatterns = [
    path("", include(router.urls)),
]
