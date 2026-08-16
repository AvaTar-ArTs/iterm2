from pathlib import Path

from workvault.github_audit import audit_repository, classify_path, scan_text


def test_classifies_session_history():
    finding = classify_path(".codex-history/session.md")
    assert finding is not None
    assert finding.classification == "PRIVATE_REFERENCE"


def test_detects_secret_like_content_without_echoing_secret():
    findings = scan_text("config.txt", "OPENAI_API_KEY=sk-proj-abcdefghijklmnopqrstuvwxyz123456")
    assert findings
    assert findings[0].classification == "SECRET_ROTATE"
    assert "abcdefghijklmnopqrstuvwxyz" not in findings[0].reason


def test_repository_audit(tmp_path: Path):
    history = tmp_path / ".specstory" / "debug"
    history.mkdir(parents=True)
    (history / "event.json").write_text('{"ok": true}', encoding="utf-8")
    (tmp_path / "safe.md").write_text("hello", encoding="utf-8")

    findings = audit_repository(tmp_path)
    assert any(item.classification == "PRIVATE_REFERENCE" for item in findings)
    assert all(item.path != "safe.md" for item in findings)
