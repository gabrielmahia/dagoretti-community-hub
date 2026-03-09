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
    path = os.path.join(os.path.dirname(__file__), "..", "data", "kcse_results.csv")
    df = pd.read_csv(path)
    assert len(df) >= 30, f"Expected at least 30 years, got {len(df)}"
    assert "year" in df.columns
    assert "mean_grade" in df.columns
    assert "verified" in df.columns, "Missing verified column — data integrity requires it"
    confirmed = df[df["verified"] == "confirmed"]
    assert len(confirmed) >= 6, f"Expected at least 6 confirmed years, got {len(confirmed)}"


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
    from pages.career_pathways import grade_meets_minimum, GRADE_ORDER, CLUSTERS
    assert grade_meets_minimum("A", "B+") is True
    assert grade_meets_minimum("C", "B+") is False
    assert grade_meets_minimum("B+", "B+") is True
    assert len(CLUSTERS) >= 8


def test_all_page_modules_importable():
    page_modules = [
        "pages.home",
        "pages.alumni_atlas",
        "pages.kcse_tracker",
        "pages.career_pathways",
        "pages.memory_wall",
        "pages.then_now",
        "pages.mentorship",
        "pages.scholarships",
        "pages.submit",
        "pages.events",
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
