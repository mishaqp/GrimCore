#!/usr/bin/env python3
"""Read GrimCore versionName / versionCode out of app/build.gradle.kts.

Usage: read_version.py versionName | versionCode
"""
import re
import sys
from pathlib import Path

GRADLE = Path('app/build.gradle.kts')
VERSION_NAME_RE = re.compile(r'versionName\s*=\s*"([^"]+)"')


def read_text() -> str:
  if not GRADLE.is_file():
    raise SystemExit('app/build.gradle.kts not found; run from the repository root')
  return GRADLE.read_text(encoding='utf-8')


def read_version_name() -> str:
  m = VERSION_NAME_RE.search(read_text())
  if not m:
    raise SystemExit('versionName not found in app/build.gradle.kts')
  return m.group(1)


def read_version_code() -> int:
  tail = read_text()[VERSION_NAME_RE.search(read_text()).end():] if False else read_text()
  m = re.search(r'versionCode\s*=\s*(\d+)', read_text())
  if not m:
    raise SystemExit('versionCode not found in app/build.gradle.kts')
  return int(m.group(1))


def expected_version_code(version_name: str) -> int:
  # major * 1000000 + minor * 10000 + patch * 100 + grim
  m = re.match(r'^(\d+)\.(\d+)\.(\d+)-grim\.(\d+)$', version_name)
  if not m:
    raise SystemExit('versionName does not follow the GrimCore scheme: ' + version_name)
  major, minor, patch, grim = (int(v) for v in m.groups())
  return major * 1000000 + minor * 10000 + patch * 100 + grim


if __name__ == '__main__':
  if len(sys.argv) != 2 or sys.argv[1] not in ('versionName', 'versionCode'):
    raise SystemExit('usage: read_version.py versionName|versionCode')
  print(read_version_name() if sys.argv[1] == 'versionName' else read_version_code())
