#!/usr/bin/env python3
"""GrimCore secret hygiene.

The keystore, its passwords and any API key must never enter the repository.
This is a narrow, deterministic check that complements gitleaks: it looks for
the exact artifacts GrimCore depends on plus a few high-signal token shapes.
"""
import re
import sys
from pathlib import Path

ROOT = Path('.')
SKIP_DIRS = {'.git', 'build', '.dart_tool', '.gradle', 'node_modules', 'artifacts'}
FORBIDDEN_SUFFIXES = ('.jks', '.keystore', '.p12', '.pfx', '.pem', '.key')
TEXT_SUFFIXES = {
  '.py', '.sh', '.kt', '.kts', '.dart', '.arb', '.xml', '.json', '.yml', '.yaml',
  '.gradle', '.properties', '.toml', '.md', '.txt', '.cfg', '.ini', '.env',
}
PATTERNS = [
  ('private key block', re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----')),
  ('github token', re.compile(r'gh[pousr]_[A-Za-z0-9]{36}')),
  ('openai style key', re.compile(r'\bsk-[A-Za-z0-9]{32,}\b')),
  ('google api key', re.compile(r'\bAIza[0-9A-Za-z_\-]{35}\b')),
  ('inline keystore base64', re.compile(r'(KEYSTORE_B64|KEYSTORE)\s*[:=]\s*"?[A-Za-z0-9+/]{200,}')),
]
ALLOWED_HINTS = ('example', 'EXAMPLE', 'redacted', 'placeholder', 'your-token', 'xxxx')

errors = []
scanned = 0


def scan_file(path: Path):
  global scanned
  text = path.read_text(encoding='utf-8', errors='ignore')
  scanned += 1
  for label, rx in PATTERNS:
    m = rx.search(text)
    if m:
      line = text[:m.start()].count('\n') + 1
      snippet = text[max(0, m.start() - 20):m.end() + 20].replace('\n', ' ')
      if any(h in snippet for h in ALLOWED_HINTS):
       continue
      errors.append('%s:%d looks like a %s' % (path, line, label))


def main():
  if not (ROOT / 'app/build.gradle.kts').is_file():
    raise SystemExit('run from the repository root')
  for path in sorted(ROOT.rglob('*')):
    if not path.is_file():
      continue
    if any(part in SKIP_DIRS for part in path.parts):
      continue
    if path.suffix.lower() in FORBIDDEN_SUFFIXES:
      errors.append('forbidden signing/key material in the repository: %s' % path)
      continue
    if path.suffix.lower() not in TEXT_SUFFIXES:
      continue
    try:
      if path.stat().st_size > 512 * 1024:
        continue
    except OSError:
      continue
    scan_file(path)

  gradle_props = ROOT / 'gradle.properties'
  if gradle_props.is_file():
    props = gradle_props.read_text(encoding='utf-8', errors='ignore')
    for name in ('GRIM_RELEASE', 'OMNI_RELEASE'):
      if re.search(name + r'(STORE_PWD|KEY_PWD)\s*=\s*\S', props):
        errors.append('gradle.properties must not contain %s*_PWD values' % name)

  if errors:
    print('GrimCore secret check FAILED:')
    for e in errors:
      print(' -', e)
    return 1
  print('GrimCore secret check passed (%d text files scanned)' % scanned)
  return 0


sys.exit(main())
