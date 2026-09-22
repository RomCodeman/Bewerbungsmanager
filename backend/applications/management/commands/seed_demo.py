from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from django.utils import timezone

from applications.models import Application, Company


DEMO_COMPANIES = [
    {
        "name": "Nordlicht Codewerk Demo GmbH",
        "website": "https://nordlicht-codewerk.example.com",
        "city": "Paderborn",
        "career_url": "https://nordlicht-codewerk.example.com/karriere",
        "notes": "Fiktives Demo-Unternehmen mit Fokus auf Backend-Entwicklung.",
    },
    {
        "name": "TeutoByte Demo Solutions GmbH",
        "website": "https://teutobyte.example.org",
        "city": "Bielefeld",
        "career_url": "https://teutobyte.example.org/jobs",
        "notes": "Fiktives Demo-Unternehmen für Software- und Webentwicklung.",
    },
    {
        "name": "Lippe Digitalwerk Demo UG",
        "website": "https://lippe-digitalwerk.example.net",
        "city": "Detmold",
        "career_url": "",
        "notes": "Initiativbewerbungen sind im Demo-Szenario möglich.",
    },
    {
        "name": "OWL Softwarehaus Demo GmbH",
        "website": "https://owl-softwarehaus.example.com",
        "city": "Gütersloh",
        "career_url": "https://owl-softwarehaus.example.com/careers",
        "notes": "Fiktives Unternehmen mit mehreren Bewerbungen zur Prüfung der 1:n-Beziehung.",
    },
    {
        "name": "WeserCloud Demo Systems GmbH",
        "website": "https://wesercloud.example.org",
        "city": "Minden",
        "career_url": "https://wesercloud.example.org/karriere",
        "notes": "Demo-Datensatz für REST-API- und Follow-up-Szenarien.",
    },
    {
        "name": "Senne Apps Demo GmbH",
        "website": "https://senne-apps.example.net",
        "city": "Hövelhof",
        "career_url": "",
        "notes": "Fiktives kleines App-Team.",
    },
    {
        "name": "Extertal Data Demo GmbH",
        "website": "https://extertal-data.example.com",
        "city": "Lemgo",
        "career_url": "https://extertal-data.example.com/jobs",
        "notes": "Demo-Unternehmen für Full-Stack- und Django-Bewerbungen.",
    },
    {
        "name": "Hermannsweg Tech Demo GmbH",
        "website": "https://hermannsweg-tech.example.org",
        "city": "Detmold",
        "career_url": "https://hermannsweg-tech.example.org/stellen",
        "notes": "Fiktives Unternehmen für Test- und Frontend-Szenarien.",
    },
    {
        "name": "Nethe Softwarelabor Demo GmbH",
        "website": "https://nethe-softwarelabor.example.net",
        "city": "Höxter",
        "career_url": "https://nethe-softwarelabor.example.net/karriere",
        "notes": "Demo-Unternehmen mit mehreren Bewerbungsstatus.",
    },
    {
        "name": "Freiraum Demo GmbH",
        "website": "https://freiraum-demo.example.com",
        "city": "Bad Driburg",
        "career_url": "",
        "notes": "Absichtlich ohne Bewerbung, damit ein erfolgreiches Löschen getestet werden kann.",
    },
]


DEMO_APPLICATIONS = [
    {
        "company": "Nordlicht Codewerk Demo GmbH",
        "position": "Pflichtpraktikum FIAE – Backend",
        "status": Application.Status.APPLIED,
        "application_date_offset": -12,
        "job_url": "https://nordlicht-codewerk.example.com/jobs/fiae-backend",
        "contact_person": "Frau Becker",
        "contact_email": "becker@example.com",
        "next_action": "Nach Bewerbungsstatus fragen",
        "next_action_date_offset": -3,
        "notes": "Bewerbung über das Karriereportal versendet.",
    },
    {
        "company": "Nordlicht Codewerk Demo GmbH",
        "position": "Junior Python Developer",
        "status": Application.Status.PLANNED,
        "application_date_offset": None,
        "job_url": "https://nordlicht-codewerk.example.com/jobs/python-junior",
        "contact_person": "",
        "contact_email": "",
        "next_action": "Stellenanzeige und Anforderungen prüfen",
        "next_action_date_offset": 5,
        "notes": "Noch keine Bewerbung versendet.",
    },
    {
        "company": "TeutoByte Demo Solutions GmbH",
        "position": "Praktikum Softwareentwicklung",
        "status": Application.Status.INTERVIEW,
        "application_date_offset": -18,
        "job_url": "https://teutobyte.example.org/jobs/software-praktikum",
        "contact_person": "Herr Wagner",
        "contact_email": "wagner@example.org",
        "next_action": "Technisches Gespräch vorbereiten",
        "next_action_date_offset": 2,
        "notes": "Einladung zum technischen Gespräch erhalten.",
    },
    {
        "company": "TeutoByte Demo Solutions GmbH",
        "position": "Werkstudent Webentwicklung",
        "status": Application.Status.REJECTED,
        "application_date_offset": -45,
        "job_url": "https://teutobyte.example.org/jobs/webentwicklung",
        "contact_person": "Frau König",
        "contact_email": "koenig@example.org",
        "next_action": "Unterlagen archivieren",
        "next_action_date_offset": -20,
        "notes": "Absage erhalten. Vergangenes Follow-up darf nicht als überfällig zählen.",
    },
    {
        "company": "Lippe Digitalwerk Demo UG",
        "position": "Python Backend Praktikum",
        "status": Application.Status.PLANNED,
        "application_date_offset": None,
        "job_url": "",
        "contact_person": "",
        "contact_email": "",
        "next_action": "Anschreiben fertigstellen",
        "next_action_date_offset": -1,
        "notes": "Geplante Bewerbung ohne Bewerbungsdatum; nächste Aktion ist überfällig.",
    },
    {
        "company": "OWL Softwarehaus Demo GmbH",
        "position": "Pflichtpraktikum Anwendungsentwicklung",
        "status": Application.Status.APPLIED,
        "application_date_offset": -9,
        "job_url": "https://owl-softwarehaus.example.com/jobs/fiae-praktikum",
        "contact_person": "Herr Peters",
        "contact_email": "peters@example.com",
        "next_action": "Follow-up senden",
        "next_action_date_offset": 4,
        "notes": "Bewerbung per E-Mail versendet.",
    },
    {
        "company": "OWL Softwarehaus Demo GmbH",
        "position": "Junior Backend Developer",
        "status": Application.Status.ACCEPTED,
        "application_date_offset": -60,
        "job_url": "https://owl-softwarehaus.example.com/jobs/backend-junior",
        "contact_person": "Frau Sommer",
        "contact_email": "sommer@example.com",
        "next_action": "Vertrag prüfen",
        "next_action_date_offset": -5,
        "notes": "Zusage erhalten. Vergangenes Follow-up darf nicht als überfällig zählen.",
    },
    {
        "company": "WeserCloud Demo Systems GmbH",
        "position": "Praktikum REST-API-Entwicklung",
        "status": Application.Status.APPLIED,
        "application_date_offset": -20,
        "job_url": "https://wesercloud.example.org/jobs/rest-api",
        "contact_person": "Herr Brandt",
        "contact_email": "brandt@example.org",
        "next_action": "Nach Rückmeldung fragen",
        "next_action_date_offset": -7,
        "notes": "Aktive Bewerbung mit überfälligem Follow-up.",
    },
    {
        "company": "Senne Apps Demo GmbH",
        "position": "Frontend Praktikum Angular",
        "status": Application.Status.INTERVIEW,
        "application_date_offset": -14,
        "job_url": "https://senne-apps.example.net/jobs/angular",
        "contact_person": "Frau Neumann",
        "contact_email": "neumann@example.net",
        "next_action": "Portfolio und Projektbeispiele vorbereiten",
        "next_action_date_offset": 1,
        "notes": "Gespräch mit dem Frontend-Team geplant.",
    },
    {
        "company": "Extertal Data Demo GmbH",
        "position": "Praktikum Full-Stack Development",
        "status": Application.Status.APPLIED,
        "application_date_offset": -6,
        "job_url": "https://extertal-data.example.com/jobs/fullstack",
        "contact_person": "Herr Klein",
        "contact_email": "klein@example.com",
        "next_action": "",
        "next_action_date_offset": None,
        "notes": "Aktive Bewerbung ohne geplantes Follow-up.",
    },
    {
        "company": "Extertal Data Demo GmbH",
        "position": "Werkstudent Python/Django",
        "status": Application.Status.REJECTED,
        "application_date_offset": -30,
        "job_url": "https://extertal-data.example.com/jobs/django",
        "contact_person": "Frau Lorenz",
        "contact_email": "lorenz@example.com",
        "next_action": "",
        "next_action_date_offset": None,
        "notes": "Abgeschlossene Bewerbung ohne weitere Aktion.",
    },
    {
        "company": "Hermannsweg Tech Demo GmbH",
        "position": "Praktikum QA & Testautomatisierung",
        "status": Application.Status.ACCEPTED,
        "application_date_offset": -25,
        "job_url": "https://hermannsweg-tech.example.org/jobs/qa",
        "contact_person": "Herr Fischer",
        "contact_email": "fischer@example.org",
        "next_action": "Starttermin bestätigen",
        "next_action_date_offset": 10,
        "notes": "Zusage erhalten.",
    },
    {
        "company": "Hermannsweg Tech Demo GmbH",
        "position": "Praktikum Webentwicklung",
        "status": Application.Status.APPLIED,
        "application_date_offset": -3,
        "job_url": "https://hermannsweg-tech.example.org/jobs/web",
        "contact_person": "Frau Roth",
        "contact_email": "roth@example.org",
        "next_action": "Rückmeldung abwarten",
        "next_action_date_offset": 7,
        "notes": "Frisch versendete Bewerbung.",
    },
    {
        "company": "Nethe Softwarelabor Demo GmbH",
        "position": "FIAE Pflichtpraktikum",
        "status": Application.Status.INTERVIEW,
        "application_date_offset": -11,
        "job_url": "https://nethe-softwarelabor.example.net/jobs/fiae",
        "contact_person": "Herr Hoffmann",
        "contact_email": "hoffmann@example.net",
        "next_action": "Fragen für das Interview vorbereiten",
        "next_action_date_offset": 3,
        "notes": "Erstes Kennenlerngespräch bereits durchgeführt.",
    },
    {
        "company": "Nethe Softwarelabor Demo GmbH",
        "position": "Junior Softwareentwickler",
        "status": Application.Status.PLANNED,
        "application_date_offset": None,
        "job_url": "https://nethe-softwarelabor.example.net/jobs/junior",
        "contact_person": "",
        "contact_email": "",
        "next_action": "Lebenslauf an Stelle anpassen",
        "next_action_date_offset": 14,
        "notes": "Geplante spätere Bewerbung.",
    },
]


class Command(BaseCommand):
    help = (
        "Erstellt einen reproduzierbaren Demo-Datensatz mit 10 fiktiven "
        "Unternehmen und 15 Bewerbungen. Vorhandene Demo-Daten werden ersetzt."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        today = timezone.localdate()
        demo_names = [company["name"] for company in DEMO_COMPANIES]

        existing_demo_companies = Company.objects.filter(name__in=demo_names)
        Application.objects.filter(company__in=existing_demo_companies).delete()
        existing_demo_companies.delete()

        companies = {}
        for company_data in DEMO_COMPANIES:
            company = Company.objects.create(**company_data)
            companies[company.name] = company

        for application_data in DEMO_APPLICATIONS:
            company_name = application_data["company"]
            application_date_offset = application_data["application_date_offset"]
            next_action_date_offset = application_data["next_action_date_offset"]

            Application.objects.create(
                company=companies[company_name],
                position=application_data["position"],
                status=application_data["status"],
                application_date=(
                    today + timedelta(days=application_date_offset)
                    if application_date_offset is not None
                    else None
                ),
                job_url=application_data["job_url"],
                contact_person=application_data["contact_person"],
                contact_email=application_data["contact_email"],
                next_action=application_data["next_action"],
                next_action_date=(
                    today + timedelta(days=next_action_date_offset)
                    if next_action_date_offset is not None
                    else None
                ),
                notes=application_data["notes"],
            )

        status_counts = {
            status_value: 0 for status_value, _ in Application.Status.choices
        }

        for item in (
            Application.objects.filter(company__name__in=demo_names)
            .values("status")
            .annotate(total=Count("id"))
        ):
            status_counts[item["status"]] = item["total"]

        overdue_follow_ups = (
            Application.objects.filter(
                company__name__in=demo_names,
                next_action_date__lt=today,
            )
            .exclude(
                status__in=[
                    Application.Status.ACCEPTED,
                    Application.Status.REJECTED,
                ]
            )
            .count()
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo-Daten erstellt: 10 Unternehmen, 15 Bewerbungen."
            )
        )
        self.stdout.write(
            "Status: "
            f"PLANNED={status_counts[Application.Status.PLANNED]}, "
            f"APPLIED={status_counts[Application.Status.APPLIED]}, "
            f"INTERVIEW={status_counts[Application.Status.INTERVIEW]}, "
            f"ACCEPTED={status_counts[Application.Status.ACCEPTED]}, "
            f"REJECTED={status_counts[Application.Status.REJECTED]}"
        )
        self.stdout.write(f"Überfällige Follow-ups: {overdue_follow_ups}")
        self.stdout.write(
            "Freiraum Demo GmbH hat absichtlich keine Bewerbung und kann gelöscht werden."
        )
