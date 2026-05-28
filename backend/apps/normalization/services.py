from datetime import datetime
from decimal import Decimal

from apps.normalization.models import NormalizedActivity

AIRPORT_DISTANCES = {
    ("DEL", "BOM"): 1140,
    ("LHR", "JFK"): 5540,
    ("SFO", "SEA"): 1090,
}

EMISSION_FACTORS = {
    "diesel_liter": Decimal("2.680"),
    "electricity_kwh": Decimal("0.420"),
    "flight_km": Decimal("0.090"),
    "hotel_night": Decimal("15.000"),
}


def _parse_date(value):
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(str(value), fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Invalid date: {value}")


def _normalize_sap(raw):
    qty = Decimal(str(raw.get("MENGE", "0")))
    unit = (raw.get("MEINS") or "").lower()
    if unit == "gallon":
        normalized_qty = qty * Decimal("3.78541")
    elif unit in {"l", "liter", "liters"}:
        normalized_qty = qty
    elif unit == "kg":
        normalized_qty = qty
    else:
        raise ValueError("Missing or unsupported SAP unit")
    return {
        "activity_type": "FUEL_CONSUMPTION",
        "scope": "SCOPE_1",
        "category": "Stationary Combustion",
        "activity_date": _parse_date(raw.get("BUDAT")),
        "quantity": qty,
        "original_unit": unit or "unknown",
        "normalized_unit": "liter" if unit != "kg" else "kg",
        "normalized_quantity": normalized_qty,
        "emission_factor": EMISSION_FACTORS["diesel_liter"],
        "co2e_emissions": normalized_qty * EMISSION_FACTORS["diesel_liter"],
    }


def _normalize_utility(raw):
    qty = Decimal(str(raw.get("kwh", "0")))
    return {
        "activity_type": "ELECTRICITY_PURCHASED",
        "scope": "SCOPE_2",
        "category": "Purchased Electricity",
        "activity_date": _parse_date(raw.get("billing_end")),
        "quantity": qty,
        "original_unit": "kwh",
        "normalized_unit": "kwh",
        "normalized_quantity": qty,
        "emission_factor": EMISSION_FACTORS["electricity_kwh"],
        "co2e_emissions": qty * EMISSION_FACTORS["electricity_kwh"],
    }


def _normalize_travel(raw):
    distance = raw.get("distance_km")
    if distance in (None, ""):
        origin = raw.get("origin_airport")
        dest = raw.get("destination_airport")
        distance = AIRPORT_DISTANCES.get((origin, dest), 800)
    distance = Decimal(str(distance))
    nights = Decimal(str(raw.get("hotel_nights", 0)))
    flight_emissions = distance * EMISSION_FACTORS["flight_km"]
    hotel_emissions = nights * EMISSION_FACTORS["hotel_night"]
    return {
        "activity_type": "BUSINESS_TRAVEL",
        "scope": "SCOPE_3",
        "category": "Business Travel",
        "activity_date": datetime.utcnow().date(),
        "quantity": distance,
        "original_unit": "km",
        "normalized_unit": "km",
        "normalized_quantity": distance,
        "emission_factor": EMISSION_FACTORS["flight_km"],
        "co2e_emissions": flight_emissions + hotel_emissions,
    }


def validate_normalized(raw_row, normalized_data, seen_keys):
    issues = []
    source = raw_row.datasource.source_type
    if source == "UTILITY" and normalized_data["normalized_quantity"] < 0:
        issues.append("negative electricity usage")
    if source == "SAP" and normalized_data["original_unit"] in {"", "unknown"}:
        issues.append("missing units")
    dedupe_key = (source, str(raw_row.raw_json))
    if dedupe_key in seen_keys:
        issues.append("duplicate records")
    seen_keys.add(dedupe_key)
    if source == "SAP" and normalized_data["normalized_quantity"] > Decimal("100000"):
        issues.append("unusually large fuel quantities")
    if source == "TRAVEL":
        if not raw_row.raw_json.get("origin_airport") or not raw_row.raw_json.get("destination_airport"):
            issues.append("missing airport codes")
    return issues


def normalize_raw_record(raw_record, company, seen_keys):
    source_type = raw_record.datasource.source_type
    raw = raw_record.raw_json
    if source_type == "SAP":
        normalized_data = _normalize_sap(raw)
    elif source_type == "UTILITY":
        normalized_data = _normalize_utility(raw)
    elif source_type == "TRAVEL":
        normalized_data = _normalize_travel(raw)
    else:
        raise ValueError(f"Unsupported source type: {source_type}")
    issues = validate_normalized(raw_record, normalized_data, seen_keys)
    status = NormalizedActivity.ReviewStatus.FLAGGED if issues else NormalizedActivity.ReviewStatus.PENDING
    activity = NormalizedActivity.objects.create(
        company=company,
        raw_record=raw_record,
        review_status=status,
        validation_issues=issues,
        **normalized_data,
    )
    return activity
