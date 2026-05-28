from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand

from apps.ingestion.models import Company
from apps.ingestion.services import ingest_csv_and_normalize


class Command(BaseCommand):
    help = "Seed demo companies and ingest sample CSV files"

    def handle(self, *args, **options):
        company, _ = Company.objects.get_or_create(name="Northwind Manufacturing", industry="Industrial")
        sample_dir = Path(__file__).resolve().parents[4] / "sample_data"
        files = [("SAP", "sap_fuel.csv"), ("UTILITY", "utility_electricity.csv"), ("TRAVEL", "travel_concur.csv")]
        for source_type, filename in files:
            path = sample_dir / filename
            with open(path, "rb") as f:
                uploaded = SimpleUploadedFile(name=filename, content=f.read(), content_type="text/csv")
                ingest_csv_and_normalize(
                    company=company,
                    source_type=source_type,
                    uploaded_by="seed-script",
                    uploaded_file=uploaded,
                )
        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully"))
