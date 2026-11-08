from app.core.log_redact import redact_for_log, redact_subprocess_stderr


def test_redact_for_log_truncates() -> None:
    assert redact_for_log("abc", max_len=10) == "abc"
    long = "x" * 100
    out = redact_for_log(long, max_len=20)
    assert len(out) == 20
    assert out.endswith("...")


def test_redact_subprocess_stderr_empty() -> None:
    assert redact_subprocess_stderr(b"") == "(vacío)"
