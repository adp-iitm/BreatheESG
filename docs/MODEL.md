# Data Model

The MVP separates immutable ingestion data from normalized ESG activities.

- `Company`: tenant boundary for multi-company data.
- `DataSource`: one uploaded source file with source type, uploader, and timestamp.
- `RawRecord`: exact original CSV row, row number, processing status, and parsing error if any.
- `NormalizedActivity`: queryable ESG activity used by analysts. Each row points to exactly one `RawRecord`.
- `AuditLog`: immutable review action history (approve/reject with before/after values).

# Normalization Flow

1. Analyst uploads a CSV and chooses `SAP`, `UTILITY`, or `TRAVEL`.
2. System creates a `DataSource` row.
3. Every CSV line is stored as a `RawRecord` before transformation.
4. Normalizer maps source-specific fields into `NormalizedActivity`.
5. Validation marks suspicious records as `FLAGGED`.
6. Processing status on `RawRecord` becomes `NORMALIZED` or `FAILED`.

# Audit Strategy

- Approved activities are `locked=True` to prevent edits.
- Every approve/reject action writes to `AuditLog`.
- Normalized rows remain traceable to source file and raw payload.

# Multi-Tenancy

- `Company` foreign keys on `DataSource` and `NormalizedActivity` partition records.
- API requests can be scoped per company (MVP currently accepts `company_id` on upload).

# Source Tracking

- `DataSource.source_type` tracks SAP/UTILITY/TRAVEL lineage.
- `DataSource.uploaded_at` and `uploaded_by` preserve ingestion context.
- `RawRecord.row_number` links back to exact row location in source file.
