from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProjectAttachmentViewSet, ProjectMemberViewSet, ProjectViewSet

router = DefaultRouter()
router.register("members", ProjectMemberViewSet, basename="project-member")
router.register("attachments", ProjectAttachmentViewSet, basename="project-attachment")

project_list = ProjectViewSet.as_view({"get": "list", "post": "create"})
project_detail = ProjectViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path("", project_list, name="project-list"),
    path("<int:pk>/", project_detail, name="project-detail"),
    path("", include(router.urls)),
]
