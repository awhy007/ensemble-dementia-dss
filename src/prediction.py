"""Validated prediction logic for the research prototype.

The model bundle is trusted project output created by the final modelling
notebook. Do not use this module to load model files from untrusted sources.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "selected_model_bundle.joblib"

FEATURES = ["M/F", "Age", "SES", "MMSE", "eTIV", "nWBV", "ASF"]
NUMERIC_RULES = {
    "Age": (33.0, 96.0, True),
    "SES": (1.0, 5.0, True),
    "MMSE": (14.0, 30.0, True),
    "eTIV": (1123.0, 1992.0, False),
    "nWBV": (0.644, 0.847, False),
    "ASF": (0.881, 1.563, False),
}
DISPLAY_NAMES = {
    "Age": "Age",
    "SES": "Socioeconomic status (SES)",
    "MMSE": "MMSE score",
    "eTIV": "Estimated total intracranial volume (eTIV)",
    "nWBV": "Normalised whole-brain volume (nWBV)",
    "ASF": "Atlas scaling factor (ASF)",
}


@lru_cache(maxsize=1)
def load_bundle(model_path: str | Path = DEFAULT_MODEL_PATH) -> dict[str, Any]:
    """Load and check the trusted model bundle once per process."""
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(f"Model bundle not found: {path}")

    bundle = joblib.load(path)
    required = {"type", "name", "features", "threshold"}
    if not isinstance(bundle, dict) or not required.issubset(bundle):
        raise ValueError("The model bundle does not have the expected project structure.")
    if bundle["features"] != FEATURES:
        raise ValueError("The model feature order does not match the prototype.")
    if bundle["type"] != "soft_voting" or "models" not in bundle:
        raise ValueError("The locked project model is expected to be a soft-voting ensemble.")
    return bundle


def _validated_number(field: str, value: Any) -> float:
    label = DISPLAY_NAMES[field]
    if value is None or isinstance(value, bool):
        raise ValueError(f"{label} is required and must be numeric.")

    if isinstance(value, str):
        value = value.strip()
        if not value:
            raise ValueError(f"{label} is required and must be numeric.")

    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{label} is required and must be numeric.") from None

    if not np.isfinite(number):
        raise ValueError(f"{label} must be a finite number.")

    minimum, maximum, integer_only = NUMERIC_RULES[field]
    if number < minimum or number > maximum:
        raise ValueError(f"{label} must be between {minimum:g} and {maximum:g}.")
    if integer_only and not number.is_integer():
        raise ValueError(f"{label} must be entered as a whole number.")
    return number


def validate_case(
    sex: str,
    age: Any,
    ses: Any,
    mmse: Any,
    etiv: Any,
    nwbv: Any,
    asf: Any,
) -> pd.DataFrame:
    """Validate one fictional case and return fields expected by the model."""
    sex_codes = {"Female": "F", "Male": "M"}
    if sex not in sex_codes:
        raise ValueError("Sex must be selected as Female or Male.")

    values = {
        "M/F": sex_codes[sex],
        "Age": _validated_number("Age", age),
        "SES": _validated_number("SES", ses),
        "MMSE": _validated_number("MMSE", mmse),
        "eTIV": _validated_number("eTIV", etiv),
        "nWBV": _validated_number("nWBV", nwbv),
        "ASF": _validated_number("ASF", asf),
    }
    return pd.DataFrame([values], columns=FEATURES)


def predict_case(
    sex: str,
    age: Any,
    ses: Any,
    mmse: Any,
    etiv: Any,
    nwbv: Any,
    asf: Any,
    *,
    model_path: str | Path = DEFAULT_MODEL_PATH,
) -> dict[str, Any]:
    """Return the soft-voting result for one validated fictional case."""
    case = validate_case(sex, age, ses, mmse, etiv, nwbv, asf)
    bundle = load_bundle(model_path)

    probabilities = np.array(
        [model.predict_proba(case)[:, 1][0] for model in bundle["models"].values()],
        dtype=float,
    )
    probability = float(probabilities.mean())
    threshold = float(bundle["threshold"])
    positive = probability >= threshold

    return {
        "model": bundle["name"],
        "category": "CDR > 0" if positive else "CDR = 0",
        "category_explanation": (
            "recorded cognitive impairment or dementia category"
            if positive
            else "no recorded cognitive impairment category"
        ),
        "probability": probability,
        "threshold": threshold,
    }
