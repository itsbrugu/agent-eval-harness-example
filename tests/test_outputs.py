"""
Verifies /app/report.json against the numbered success criteria in instruction.md.
The fixture /app/access.log is fixed and known, so the expected values below
(6 total requests, 3 unique IPs, top path "/index.html") are independently
derived constants, not read from the agent's own output.
"""
import json
from pathlib import Path

REPORT_PATH = Path("/app/report.json")

EXPECTED_TOTAL_REQUESTS = 6
EXPECTED_UNIQUE_IPS = 3
EXPECTED_TOP_PATH = "/index.html"


def _load_report():
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    with open(REPORT_PATH) as f:
        return json.load(f)


def test_report_is_valid_json_object():
    """instruction.md criterion 1: /app/report.json exists and is a valid JSON object."""
    report = _load_report()
    assert isinstance(report, dict), "report.json does not contain a JSON object"


def test_total_requests():
    """instruction.md criterion 2: total_requests equals the number of log lines."""
    report = _load_report()
    assert report.get("total_requests") == EXPECTED_TOTAL_REQUESTS, (
        f"expected total_requests={EXPECTED_TOTAL_REQUESTS}, "
        f"got {report.get('total_requests')!r}"
    )


def test_unique_ips():
    """instruction.md criterion 3: unique_ips equals the number of distinct client IPs."""
    report = _load_report()
    assert report.get("unique_ips") == EXPECTED_UNIQUE_IPS, (
        f"expected unique_ips={EXPECTED_UNIQUE_IPS}, got {report.get('unique_ips')!r}"
    )


def test_top_path():
    """instruction.md criterion 4: top_path equals the most frequently requested path."""
    report = _load_report()
    assert report.get("top_path") == EXPECTED_TOP_PATH, (
        f"expected top_path={EXPECTED_TOP_PATH!r}, got {report.get('top_path')!r}"
    )
