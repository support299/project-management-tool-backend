from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TaskAttachmentViewSet, TaskViewSet

router = DefaultRouter()
router.register("attachments", TaskAttachmentViewSet, basename="task-attachment")

task_list = TaskViewSet.as_view({"get": "list", "post": "create"})
task_detail = TaskViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path("", task_list, name="task-list"),
    path("<int:pk>/", task_detail, name="task-detail"),
    path("", include(router.urls)),
]
