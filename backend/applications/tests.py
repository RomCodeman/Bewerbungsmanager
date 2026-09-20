from django.test import TestCase
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
