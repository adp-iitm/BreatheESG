import csv
from io import StringIO

from django.db import transaction

from apps.ingestion.models import DataSource, RawRecord
from apps.normalization.services import normalize_raw_record


def _decode_csv_payload(file_bytes):
    # Real-world exports are often UTF-8, UTF-8 BOM, CP1252, or Latin-1.
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return file_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("Unable to decode CSV file. Please upload UTF-8, CP1252, or Latin-1 encoded CSV.")


@transaction.atomic
def ingest_csv_and_normalize(*, company, source_type, uploaded_by, uploaded_file):
    datasource = DataSource.objects.create(
        company=company,
        source_type=source_type,
        ingestion_method="CSV_UPLOAD",
        original_filename=uploaded_file.name,
        uploaded_by=uploaded_by,
    )
    file_bytes = uploaded_file.read()
    decoded = _decode_csv_payload(file_bytes)
    reader = csv.DictReader(StringIO(decoded))
    if not reader.fieldnames:
        raise ValueError("CSV header row is missing or unreadable.")
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
