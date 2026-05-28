# Source Realism Notes

This prototype mimics common enterprise export patterns:

- SAP fuel/procurement exports with operational columns (`BUKRS`, `WERKS`, `MATNR`, `MENGE`, `MEINS`, `BUDAT`).
- Utility billing exports with period boundaries and meter-level usage.
- Travel exports with itinerary fields and optional missing distance.

Sample files intentionally include:

- mixed date formats
- inconsistent units
- missing fields
- outlier usage values

These reflect common data quality issues analysts handle in emissions workflows.

# What Would Break in Production

- Static emission factors should be replaced with versioned regional factor tables.
- Duplicate detection via raw JSON matching is simplistic for large-scale ingestion.
- Synchronous processing should move to async workers for large files.
