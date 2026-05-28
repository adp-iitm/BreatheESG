import csv
from io import StringIO

from django.db import transaction

from apps.ingestion.models import DataSource, RawRecord
from apps.normalization.services import normalize_raw_record


@transaction.atomic
def ingest_csv_and_normalize(*, company, source_type, uploaded_by, uploaded_file):
    datasource = DataSource.objects.create(
        company=company,
        source_type=source_type,
        ingestion_method="CSV_UPLOAD",
        original_filename=uploaded_file.name,
        uploaded_by=uploaded_by,
    )
    decoded = uploaded_file.read().decode("utf-8-sig")
    reader = csv.DictReader(StringIO(decoded))
    seen_keys = set()
    for row_number, row in enumerate(reader, start=2):
        raw = RawRecord.objects.create(
            datasource=datasource,
            row_number=row_number,
            raw_json=row,
            processing_status=RawRecord.ProcessingStatus.PENDING,
        )
        try:
            normalize_raw_record(raw, company, seen_keys)
            raw.processing_status = RawRecord.ProcessingStatus.NORMALIZED
            raw.error_message = ""
        except Exception as exc:
            raw.processing_status = RawRecord.ProcessingStatus.FAILED
            raw.error_message = str(exc)
        raw.save(update_fields=["processing_status", "error_message"])
    return datasource
