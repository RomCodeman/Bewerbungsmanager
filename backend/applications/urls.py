from rest_framework.routers import DefaultRouter

from .views import ApplicationViewSet, CompanyViewSet

from django.urls import path

from .views import (
    ApplicationViewSet,
    CompanyViewSet,
    DashboardView,
)

router = DefaultRouter()

router.register(
    "companies",
    CompanyViewSet,
    basename="company",
)

router.register(
    "applications",
    ApplicationViewSet,
    basename="application",
)

urlpatterns = [
    path(
        "dashboard/",
        DashboardView.as_view(),
        name="dashboard",
    ),
    *router.urls,
]
