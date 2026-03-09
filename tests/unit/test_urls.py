import pytest
from nova.utils.urls import normalize_google_sheet_url


def test_normalize_google_sheet_url_strips_usp_sharing():
    url = "https://docs.google.com/spreadsheets/d/1JQ7sfe/edit?usp=sharing"
    assert normalize_google_sheet_url(url) == "https://docs.google.com/spreadsheets/d/1JQ7sfe/edit"


def test_normalize_google_sheet_url_strips_query_and_fragment():
    url = "https://docs.google.com/spreadsheets/d/123/edit?foo=bar#sheet"
    assert normalize_google_sheet_url(url) == "https://docs.google.com/spreadsheets/d/123/edit"


def test_normalize_google_sheet_url_unchanged_when_clean():
    url = "https://docs.google.com/spreadsheets/d/123/edit"
    assert normalize_google_sheet_url(url) == url
