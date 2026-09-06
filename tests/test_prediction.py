from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.prediction import predict_case, validate_case


VALID_CASE = ("Female", 72, 2, 28, 1400, 0.755, 1.250)


def test_valid_case_returns_expected_fields():
    result = predict_case(*VALID_CASE)
    assert result["model"] == "Soft Voting Ensemble"
    assert result["category"] in {"CDR = 0", "CDR > 0"}
    assert 0.0 <= result["probability"] <= 1.0
    assert result["threshold"] == 0.5


@pytest.mark.parametrize(
    "case",
    [
        ("Female", 33, 1, 14, 1123, 0.644, 0.881),
        ("Male", 96, 5, 30, 1992, 0.847, 1.563),
    ],
)
def test_boundary_values_are_accepted(case):
    frame = validate_case(*case)
    assert frame.shape == (1, 7)


@pytest.mark.parametrize(
    ("index", "value", "message"),
    [
        (0, None, "Sex must be selected"),
        (1, None, "Age is required"),
        (1, 32, "Age must be between 33 and 96"),
        (2, 6, "Socioeconomic status (SES) must be between 1 and 5"),
        (3, 13, "MMSE score must be between 14 and 30"),
        (4, 2000, "Estimated total intracranial volume"),
        (5, 0.9, "Normalised whole-brain volume"),
        (6, float("nan"), "Atlas scaling factor (ASF) must be a finite number"),
    ],
)
def test_invalid_values_are_rejected(index, value, message):
    case = list(VALID_CASE)
    case[index] = value
    with pytest.raises(ValueError, match=r".*") as caught:
        validate_case(*case)
    assert message in str(caught.value)


def test_whole_number_fields_reject_decimals():
    with pytest.raises(ValueError, match="Age must be entered as a whole number"):
        validate_case("Female", 74.5, 2, 29, 1344, 0.743, 1.306)


def test_predictions_are_deterministic():
    first = predict_case(*VALID_CASE)
    second = predict_case(*VALID_CASE)
    assert first == second


def test_numeric_text_entries_are_accepted():
    result = predict_case("Female", "72", "2", "28", "1400", "0.755", "1.250")
    assert result["category"] in {"CDR = 0", "CDR > 0"}


def test_non_numeric_text_is_rejected_cleanly():
    with pytest.raises(ValueError, match="Age is required and must be numeric"):
        predict_case("Female", "not an age", "2", "28", "1400", "0.755", "1.250")
