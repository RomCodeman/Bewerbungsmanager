from django.db import models


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    career_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Application(models.Model):
    class Status(models.TextChoices):
        PLANNED = "PLANNED", "Geplant"
        APPLIED = "APPLIED", "Beworben"
        INTERVIEW = "INTERVIEW", "Interview"
        ACCEPTED = "ACCEPTED", "Zusage"
        REJECTED = "REJECTED", "Absage"

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="applications",
    )

    position = models.CharField(max_length=200)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNED,
    )

    application_date = models.DateField(
        blank=True,
        null=True,
    )

    job_url = models.URLField(blank=True)

    contact_person = models.CharField(
        max_length=200,
        blank=True,
    )

    contact_email = models.EmailField(blank=True)

    next_action = models.CharField(
        max_length=255,
        blank=True,
    )

    next_action_date = models.DateField(
        blank=True,
        null=True,
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.company.name} – {self.position}"
