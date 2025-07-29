# tests/test_wordlist.py

import datetime
import string

import pytest

from advanced_password_tool.core.wordlist import (
    generate_custom_wordlist,
    leet_transform,
    case_variants,
    append_years,
    DEFAULT_LEET,
)

def test_case_variants():
    variants = case_variants("TestWord")
    assert "Testword".lower() in variants or "TestWord".capitalize() in variants
    assert "TESTWORD" in variants
    assert "testword" in variants

def test_leet_transform_single():
    variants = leet_transform("easy", leet_map={'e':'3', 'a':'4'})
    assert "easy" in variants
    assert "34sy" in variants or "e4sy" in variants

def test_append_years_full_and_short():
    base = {"foo"}
    year = 2021
    variants = append_years(base, start=year, end=year)
    assert "foo2021" in variants
    assert "foo21" in variants

def test_generate_custom_wordlist_basic():
    cfg = {"leet": False, "casing": True, "years": False, "year_range":[2000,2000], "symbols": []}
    wl = generate_custom_wordlist(["apple"], cfg)
    assert "apple" in wl
    assert "Apple" in wl or "APPLE" in wl

def test_with_leet_and_symbols_and_years():
    cfg = {
        "leet": True,
        "casing": True,
        "years": True,
        "year_range": [2020, 2021],
        "symbols": ['!', '@'],
    }
    inputs = ["banana"]
    wl = generate_custom_wordlist(inputs, cfg)
    # basic presence
    assert any(w.startswith("banana") for w in wl)
    # symbol variants
    assert any(w.endswith("!") or w.startswith("!") for w in wl)
    # year appended
    assert any(w.endswith("20") or w.endswith("2021") for w in wl)
    # combo of variants exists (two-word concatenation)
    # pick any two distinct entries
    if len(wl) >= 2:
        combinations = [a + b for a in wl for b in wl if a != b]
        assert any(combo in wl for combo in combinations)

def test_uniqueness_and_sorted():
    cfg = {"leet": False, "casing": False, "years
