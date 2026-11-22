from app.core.learning_catalog import LESSONS
from app.core.scan_context_for_learning import format_practice_context, last_record
from app.core.scan_history import ScanRecord, append_record, clear_history


def setup_function():
    clear_history()


def teardown_function():
    clear_history()


def test_format_without_scans():
    lesson = LESSONS[0]
    text = format_practice_context(lesson)
    assert "Sin escaneos" in text
    assert lesson.practice_kind in text


def test_format_with_discovery_scan():
    lesson = LESSONS[0]
    append_record(
        ScanRecord(
            kind="discovery",
            target="192.168.1.0/24",
            summary="2 hosts",
            payload=[{"ip": "192.168.1.10", "mac": "aa", "hostname": "", "methods": ["arp"]}],
        )
    )
    text = format_practice_context(lesson)
    assert "192.168.1.10" in text
    assert last_record("discovery") is not None