from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.db.models.deletion import ProtectedError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Application, Company


# Create your tests here.
class ApplicationModelTests(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Beispiel GmbH",
            city="Paderborn",
        )

    def test_company_can_have_multiple_applications(self):
        Application.objects.create(
            company=self.company,
            position="Pflichtpraktikum FIAE",
            status=Application.Status.APPLIED,
        )

        Application.objects.create(
            company=self.company,
            position="Junior Python Developer",
            status=Application.Status.PLANNED,
        )

        self.assertEqual(
            self.company.applications.count(),
            2,
        )

    def test_company_with_applications_cannot_be_deleted(self):
        Application.objects.create(
            company=self.company,
            position="Pflichtpraktikum FIAE",
            status=Application.Status.APPLIED,
        )

        with self.assertRaises(ProtectedError):
            self.company.delete()

    def test_company_with_application_cannot_be_deleted_via_api(self):
        Application.objects.create(
            company=self.company,
            position="Pflichtpraktikum FIAE",
            status=Application.Status.APPLIED,
        )

        response = self.client.delete(
            reverse(
                "company-detail",
                args=[self.company.id],
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT,
        )

        self.assertIn(
            "detail",
            response.data,
        )


class ApplicationAPITests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Beispiel GmbH",
            city="Paderborn",
        )

        self.application = Application.objects.create(
            company=self.company,
            position="Pflichtpraktikum FIAE",
            status=Application.Status.APPLIED,
            application_date="2026-09-20",
        )

        self.interview_application = Application.objects.create(
            company=self.company,
            position="Backend Developer",
            status=Application.Status.INTERVIEW,
            application_date="2026-09-15",
        )

    def test_create_application(self):
        data = {
            "company": self.company.id,
            "position": "Junior Python Developer",
            "status": Application.Status.APPLIED,
            "application_date": "2026-09-21",
        }

        response = self.client.post(
            reverse("application-list"),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["status_display"],
            "Beworben",
        )

    def test_planned_application_with_date_is_rejected(self):
        data = {
            "company": self.company.id,
            "position": "Werkstudent Softwareentwicklung",
            "status": Application.Status.PLANNED,
            "application_date": "2026-09-22",
        }

        response = self.client.post(
            reverse("application-list"),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "application_date",
            response.data,
        )

    def test_filter_applications_by_status(self):
        response = self.client.get(
            reverse("application-list"),
            {
                "status": Application.Status.APPLIED,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)

        self.assertEqual(
            response.data[0]["status"],
            Application.Status.APPLIED,
        )

    def test_search_companies_by_city(self):
        Company.objects.create(
            name="Andere GmbH",
            city="Bielefeld",
        )

        response = self.client.get(
            reverse("company-list"),
            {
                "search": "Paderborn",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 1)

        self.assertEqual(
            response.data[0]["name"],
            "Beispiel GmbH",
        )


class DashboardAPITests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Dashboard GmbH",
        )

        Application.objects.create(
            company=self.company,
            position="Python Praktikum",
            status=Application.Status.APPLIED,
            application_date=timezone.localdate(),
            next_action="Nachfragen",
            next_action_date=(timezone.localdate() - timedelta(days=1)),
        )

        Application.objects.create(
            company=self.company,
            position="Backend Praktikum",
            status=Application.Status.INTERVIEW,
            application_date=timezone.localdate(),
        )

    def test_dashboard_returns_statistics(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["applications_total"],
            2,
        )

        self.assertEqual(
            response.data["by_status"]["APPLIED"],
            1,
        )

        self.assertEqual(
            response.data["by_status"]["INTERVIEW"],
            1,
        )

        self.assertEqual(
            response.data["overdue_follow_ups"],
            1,
        )
