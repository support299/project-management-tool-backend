from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TicketCommentViewSet, TicketViewSet

router = DefaultRouter()
router.register("comments", TicketCommentViewSet, basename="ticket-comment")

ticket_list = TicketViewSet.as_view({"get": "list", "post": "create"})
ticket_detail = TicketViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path("", ticket_list, name="ticket-list"),
    path("<int:pk>/", ticket_detail, name="ticket-detail"),
    path("", include(router.urls)),
]
