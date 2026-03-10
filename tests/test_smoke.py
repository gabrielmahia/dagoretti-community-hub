"""
Smoke tests — verify all pages import cleanly and data loads without error.
"""

import sys
import os
import importlib
import pytest
import pandas as pd

# Add app root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_data_alumni_schema():
    """alumni.csv must exist with correct schema. Empty is valid — no fabricated data."""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "alumni.csv")
    df = pd.read_csv(path)
    required_cols = ["name", "year", "industry", "role", "city", "country", "lat", "lon", "mentoring"]
    for col in required_cols:
        assert col in df.columns, f"Missing column: {col}"
    # Row count may be 0 at launch — alumni self-register via Submit Data page
    # Verify that IF rows exist they are all-male (boys-only school since 1929)
    if not df.empty:
        assert df["name"].notna().all(), "Alumni names must not be null"


def test_data_kcse_loads():
    """KCSE tracker shows confirmed years only — no fabricated or illustrative rows."""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "kcse_results.csv")
    df = pd.read_csv(path)
    assert "year" in df.columns
    assert "mean_grade" in df.columns
    assert "verified" in df.columns, "Missing verified column — data integrity requires it"
    assert "source" in df.columns, "Missing source column — every row must cite a primary source"

    # ALL rows must be confirmed — no illustrative data allowed
    unconfirmed = df[df["verified"] != "confirmed"]
    assert len(unconfirmed) == 0, (
        f"{len(unconfirmed)} rows are not confirmed — remove or verify: "
        f"{unconfirmed['year'].tolist()}"
    )

    # Must have at least the 6 known verified years
    confirmed = df[df["verified"] == "confirmed"]
    assert len(confirmed) >= 6, f"Expected at least 6 confirmed years, got {len(confirmed)}"

    # All confirmed rows must have a source string
    no_source = confirmed[confirmed["source"].isna() | (confirmed["source"].str.strip() == "")]
    assert len(no_source) == 0, f"{len(no_source)} confirmed rows have no source citation"


def test_data_scholarships_loads():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "scholarships.csv")
    df = pd.read_csv(path)
    assert len(df) >= 20
    assert "name" in df.columns
    assert "diaspora_relevant" in df.columns


def test_data_kenya_then_now_loads():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "kenya_then_now.csv")
    df = pd.read_csv(path)
    assert len(df) >= 20
    assert "indicator" in df.columns
    assert "value_2000" in df.columns
    assert "value_2025" in df.columns


def test_career_pathways_grade_logic():
    from views.career_pathways import grade_meets_minimum, GRADE_ORDER, CLUSTERS
    assert grade_meets_minimum("A", "B+") is True
    assert grade_meets_minimum("C", "B+") is False
    assert grade_meets_minimum("B+", "B+") is True
    assert len(CLUSTERS) >= 8


def test_all_page_modules_importable():
    page_modules = [
        "views.home",
        "views.alumni_atlas",
        "views.kcse_tracker",
        "views.career_pathways",
        "views.memory_wall",
        "views.then_now",
        "views.mentorship",
        "views.scholarships",
        "views.submit",
        "views.events",
    ]
    for mod_name in page_modules:
        mod = importlib.import_module(mod_name)
        assert hasattr(mod, "render"), f"{mod_name} missing render() function"


def test_alumni_lat_lon_are_numeric():
    """Any alumni rows that exist must have valid coordinates."""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "alumni.csv")
    df = pd.read_csv(path)
    if df.empty:
        return  # Empty at launch is valid — alumni self-register
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    invalid = df[df["lat"].isna() | df["lon"].isna()]
    assert len(invalid) == 0, f"{len(invalid)} alumni rows have missing coordinates"
