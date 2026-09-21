from .models import Application, Company
from .serializers import ApplicationSerializer, CompanySerializer

import logging

from django.db.models.deletion import ProtectedError
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from django.db.models import Count
from django.utils import timezone

from rest_framework.views import APIView

logger = logging.getLogger(__name__)


# Create your views here.
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "city"]

    def destroy(self, request, *args, **kwargs):
        company = self.get_object()

        try:
            self.perform_destroy(company)
        except ProtectedError:
            logger.warning(
                "Blocked deletion of company id=%s because applications exist",
                company.pk,
            )

            return Response(
                {
                    "detail": (
                        "Das Unternehmen kann nicht gelöscht werden, "
                        "solange Bewerbungen damit verknüpft sind."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.select_related("company").all()
    serializer_class = ApplicationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "position",
        "company__name",
        "contact_person",
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.query_params.get("status")

        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def perform_update(self, serializer):
        previous_status = serializer.instance.status
        application = serializer.save()

        if previous_status != application.status:
            logger.info(
                "Application id=%s status changed from %s to %s",
                application.pk,
                previous_status,
                application.status,
            )


class DashboardView(APIView):
    def get(self, request):
        status_counts = {status: 0 for status, _ in Application.Status.choices}

        grouped_statuses = Application.objects.values("status").annotate(
            total=Count("id")
        )

        for item in grouped_statuses:
            status_counts[item["status"]] = item["total"]

        overdue_follow_ups = (
            Application.objects.filter(
                next_action_date__lt=timezone.localdate(),
            )
            .exclude(
                status__in=[
                    Application.Status.ACCEPTED,
                    Application.Status.REJECTED,
                ]
            )
            .count()
        )

        return Response(
            {
                "companies_total": Company.objects.count(),
                "applications_total": sum(status_counts.values()),
                "by_status": status_counts,
                "overdue_follow_ups": overdue_follow_ups,
            }
        )
