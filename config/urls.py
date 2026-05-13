from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/accounts/", include("apps.accounts.urls")),
    path("api/v1/projects/", include("apps.projects.urls")),
    path("api/v1/tasks/", include("apps.tasks.urls")),
    path("api/v1/tickets/", include("apps.tickets.urls")),
    path("api/v1/notifications/", include("apps.notifications.urls")),
    path("api/v1/ghl/", include("apps.ghl_integration.urls")),
    path("api/v1/reporting/", include("apps.reporting.urls")),
    path("api/v1/accounting/", include("apps.accounting.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
