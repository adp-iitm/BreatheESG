# Key Decisions

- Chose CSV upload for all sources to keep ingestion realistic but MVP-sized.
- Modeled raw and normalized tables separately to guarantee replay/debug/audit value.
- Used synchronous ingestion and normalization in a single request for clarity (no queue complexity).
- Added a lightweight service layer (`ingestion.services`, `normalization.services`) to keep views thin.

# Simplifications

- No auth/RBAC beyond uploader string fields.
- Static emission factors and airport distance map for deterministic demo behavior.
- Basic filtering and dashboard aggregates only; no advanced analytics or charting.

# Why CSV Ingestion

- Enterprise exports from SAP, utility portals, and travel tools commonly produce CSV.
- CSV is practical for a prototype while preserving realistic parser/validation behavior.

# Why These Source Formats

- SAP sample includes German-style headers/date variants and mixed units.
- Utility sample includes off-cycle billing periods and cost/tariff fields.
- Travel sample mirrors Concur-style exports with optional missing distance.
