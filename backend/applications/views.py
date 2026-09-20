from rest_framework import filters, viewsets

from .models import Application, Company
from .serializers import ApplicationSerializer, CompanySerializer


# Create your views here.
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "city"]


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