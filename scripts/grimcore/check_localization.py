#!/usr/bin/env python3
"""GrimCore localization contract.

* app_zh.arb is the template: en and ru must carry every key.
* placeholders ({name}, {count}, ...) must survive translation.
* the Russian locale must not leak Chinese text (the "half-translated UI"
  failure mode) and must not be empty.
* Android resource values-ru/strings.xml must mirror values/strings.xml.
"""
import json
import re
import sys
from pathlib import Path

L10N = Path('ui/lib/l10n')
ARB = {'zh': L10N / 'app_zh.arb', 'en': L10N / 'app_en.arb', 'ru': L10N / 'app_ru.arb'}
RES = Path('app/src/main/res')
CJK = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]')
# The language picker intentionally lists every language in its own script.
CJK_ALLOWED = {'languageZhHans'}
PLACEHOLDER = re.compile(r'\{[^}]*\}')

errors = []


def load(path):
  if not path.is_file():
    errors.append('missing file: %s' % path)
    return None
  return json.loads(path.read_text(encoding='utf-8'))


def user_keys(data):
  return [k for k in data if not k.startswith('@')]


def main():
  arbs = {loc: load(p) for loc, p in ARB.items()}
  if any(v is None for v in arbs.values()):
    return report()
  template = user_keys(arbs['zh'])
  for loc in ('en', 'ru'):
    keys = user_keys(arbs[loc])
    missing = [k for k in template if k not in keys]
    extra = [k for k in keys if k not in template]
    if missing:
      errors.append('%s is missing %d key(s): %s' % (loc, len(missing), ', '.join(missing[:10])))
    if extra:
      errors.append('%s has %d key(s) that are not in the template: %s' % (loc, len(extra), ', '.join(extra[:10])))

  for key in template:
    for loc in ('en', 'ru'):
      value = arbs[loc].get(key)
      if not isinstance(value, str) or not value.strip():
        errors.append('%s: empty value for %s' % (loc, key))
        continue
      expected = sorted(PLACEHOLDER.findall(arbs['zh'].get(key, '')))
      actual = sorted(PLACEHOLDER.findall(value))
      if expected != actual:
        errors.append('%s: placeholder mismatch for %s (%s != %s)' % (loc, key, expected, actual))

  for key, value in arbs['ru'].items():
    if key.startswith('@'):
      continue
    if CJK.search(value) and key not in CJK_ALLOWED:
      errors.append('ru: Chinese text left in %s: %s' % (key, value[:40]))

  # Android resources
  default = RES / 'values/strings.xml'
  en_res = RES / 'values-en/strings.xml'
  ru_res = RES / 'values-ru/strings.xml'
  if not ru_res.is_file():
    errors.append('missing Android resource file: %s' % ru_res)
  else:
    name_re = re.compile(r'<string name="([^"]+)"')
    d = name_re.findall(default.read_text(encoding='utf-8'))
    e = name_re.findall(en_res.read_text(encoding='utf-8'))
    r = name_re.findall(ru_res.read_text(encoding='utf-8'))
    if sorted(d) != sorted(r):
      errors.append('values-ru/strings.xml does not mirror values/strings.xml')
    if sorted(d) != sorted(e):
      errors.append('values-en/strings.xml does not mirror values/strings.xml')
    ru_text = ru_res.read_text(encoding='utf-8')
    if CJK.search(ru_text):
      errors.append('values-ru/strings.xml still contains Chinese text')

  return report()


def report():
  if errors:
    print('GrimCore localization check FAILED:')
    for e in errors[:40]:
      print(' -', e)
    if len(errors) > 40:
      print(' ... and %d more' % (len(errors) - 40))
    return 1
  print('GrimCore localization check passed')
  return 0


sys.exit(main())
