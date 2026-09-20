from rest_framework import serializers

from .models import Application, Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company

        fields = [
            "id",
            "name",
            "website",
            "city",
            "career_url",
            "notes",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:

        model = Application

        fields = [
            "id",
            "company",
            "position",
            "status",
            "status_display",
            "application_date",
            "job_url",
            "contact_person",
            "contact_email",
            "next_action",
            "next_action_date",
            "notes",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        status = attrs.get(
            "status",
            getattr(self.instance, "status", Application.Status.PLANNED),
        )

        application_date = attrs.get(
            "application_date",
            getattr(self.instance, "application_date", None),
        )

        if status == Application.Status.PLANNED and application_date:
            raise serializers.ValidationError(
                {
                    "application_date": (
                        "Für eine geplante Bewerbung darf kein Bewerbungsdatum gesetzt sein."
                    )
                }
            )

        return attrs
