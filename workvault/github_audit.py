from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

SENSITIVE_PATH_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("PRIVATE_REFERENCE", re.compile(r"(^|/)(\.codex-history|\.specstory|Session-History|Session-History-Archive)(/|$)", re.I)),
    ("PRIVATE_REFERENCE", re.compile(r"(^|/)(\.claude|\.qwen|\.gemini|\.cursor|\.poolside|\.private-journal)(/|$)", re.I)),
    ("PRIVATE_REFERENCE", re.compile(r"(conversation[-_ ]?export|gemini-conversation|full-conversation|this-session-is-being-continued)", re.I)),
    ("SECRET_ROTATE", re.compile(r"(^|/)(\.env(?:\..*)?|oauth_creds\.json|credentials?\.json|\.auth[^/]*)$", re.I)),
    ("REVIEW", re.compile(r"(^|/)(logs?|debug|tmp|temp|backups?)(/|$)", re.I)),
)

SECRET_CONTENT_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("OPENAI_API_KEY", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("GITHUB_TOKEN", re.compile(r"\bgh[opsu]_[A-Za-z0-9]{20,}\b")),
    ("AWS_ACCESS_KEY", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("PRIVATE_KEY", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("GENERIC_SECRET_ASSIGNMENT", re.compile(r"(?i)\b(api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+\-=]{12,}")),
)

TEXT_SUFFIXES = {
    ".txt", ".md", ".json", ".jsonl", ".toml", ".yaml", ".yml", ".ini", ".cfg",
    ".conf", ".env", ".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".zsh", ".bash",
    ".fish", ".ps1", ".csv", ".xml", ".html", ".htm",
}

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__"}


@dataclass(frozen=True)
class Finding:
    path: str
    classification: str
    reason: str
    rule: str
    line: int | None = None


def classify_path(relative_path: str) -> Finding | None:
    normalized = relative_path.replace("\\", "/")
    for classification, pattern in SENSITIVE_PATH_RULES:
        if pattern.search(normalized):
            return Finding(normalized, classification, "sensitive path pattern", pattern.pattern)
    return None


def scan_text(relative_path: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for name, pattern in SECRET_CONTENT_RULES:
            if pattern.search(line):
                findings.append(Finding(relative_path, "SECRET_ROTATE", "secret-like content", name, line_number))
    return findings


def _looks_textual(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name.startswith(".env")


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def audit_repository(root: str | Path, max_bytes: int = 2_000_000) -> list[Finding]:
    root_path = Path(root).expanduser().resolve()
    findings: list[Finding] = []
    seen: set[tuple[str, str, str, int | None]] = set()

    for path in iter_files(root_path):
        relative = path.relative_to(root_path).as_posix()
        path_finding = classify_path(relative)
        if path_finding:
            key = (path_finding.path, path_finding.classification, path_finding.rule, path_finding.line)
            if key not in seen:
                findings.append(path_finding)
                seen.add(key)

        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size > max_bytes or not _looks_textual(path):
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for finding in scan_text(relative, text):
            key = (finding.path, finding.classification, finding.rule, finding.line)
            if key not in seen:
                findings.append(finding)
                seen.add(key)

    priority = {"SECRET_ROTATE": 0, "PRIVATE_REFERENCE": 1, "REVIEW": 2, "SAFE_PUBLIC": 3}
    return sorted(findings, key=lambda item: (priority.get(item.classification, 99), item.path, item.line or 0))


def render_json(findings: Iterable[Finding]) -> str:
    return json.dumps([asdict(item) for item in findings], indent=2)


def render_text(findings: Iterable[Finding]) -> str:
    rows = list(findings)
    if not rows:
        return "No sensitive repository signals found."
    lines = ["CLASSIFICATION\tPATH\tLINE\tREASON/RULE"]
    for item in rows:
        line = "" if item.line is None else str(item.line)
        lines.append(f"{item.classification}\t{item.path}\t{line}\t{item.reason}: {item.rule}")
    return "\n".join(lines)
