from __future__ import annotations

import argparse
from pathlib import Path

from .github_audit import audit_repository, render_json, render_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wv", description="WorkVault local-first provenance tools")
    sub = parser.add_subparsers(dest="command", required=True)

    audit = sub.add_parser("github-audit", help="scan a local repository for risky runtime/session traces")
    audit.add_argument("path", nargs="?", default=".", help="repository path (default: current directory)")
    audit.add_argument("--json", action="store_true", dest="as_json", help="emit machine-readable JSON")
    audit.add_argument("--max-bytes", type=int, default=2_000_000, help="maximum text file size to inspect")
    audit.add_argument("--fail-on", choices=["review", "private", "secret"], help="return non-zero when this risk threshold is met")
    return parser


def _exit_code(findings, threshold: str | None) -> int:
    if not threshold:
        return 0
    severity = {"REVIEW": 1, "PRIVATE_REFERENCE": 2, "SECRET_ROTATE": 3}
    target = {"review": 1, "private": 2, "secret": 3}[threshold]
    return 2 if any(severity.get(item.classification, 0) >= target for item in findings) else 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "github-audit":
        root = Path(args.path).expanduser()
        findings = audit_repository(root, max_bytes=args.max_bytes)
        print(render_json(findings) if args.as_json else render_text(findings))
        return _exit_code(findings, args.fail_on)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
