from .models import Application, Company
from .serializers import ApplicationSerializer, CompanySerializer

import logging

from django.db.models.deletion import ProtectedError
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

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
