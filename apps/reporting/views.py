from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.projects.models import Project
from apps.tasks.models import Task
from apps.tickets.models import Ticket


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        projects = Project.objects.all()
        tasks = Task.objects.all()
        tickets = Ticket.objects.all()

        if user.role == User.Role.CLIENT:
            projects = projects.filter(client__user=user)
            tasks = tasks.filter(project__client__user=user)
            tickets = tickets.filter(client__user=user)
        elif user.role == User.Role.TEAM_MEMBER:
            projects = projects.filter(memberships__user=user).distinct()
            tasks = tasks.filter(project__memberships__user=user).distinct()
            tickets = tickets.filter(project__memberships__user=user).distinct()

        return Response(
            {
                "total_projects": projects.count(),
                "pending_tasks": tasks.exclude(status=Task.Status.COMPLETED).count(),
                "completed_tasks": tasks.filter(status=Task.Status.COMPLETED).count(),
                "team_workload": tasks.exclude(status=Task.Status.COMPLETED).values("assignee").distinct().count(),
                "client_ticket_count": tickets.count(),
            }
        )
