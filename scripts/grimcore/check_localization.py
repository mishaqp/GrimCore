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
GENERATED = L10N / 'generated'
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


def generated_api(text, root=False):
  if root:
    text = text.split('class _AppLocalizationsDelegate', 1)[0]
  declaration = re.compile(
      r'(?m)^  String(?P<getter> get)? (?P<name>[A-Za-z_]\w*)'
      r'(?:\((?P<params>[^)]*)\))?')
  result = {}
  for match in declaration.finditer(text):
    params = re.sub(r'\s+', ' ', match.group('params') or '').strip()
    result[match.group('name')] = ('getter' if match.group('getter') else params)
  return result


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

  # Generated sources are tracked. Keep them synchronized so a clean checkout
  # can analyze and build without relying on an implicit pub-get side effect.
  expected_generated_keys = set(template)
  root_generated = GENERATED / 'app_localizations.dart'
  root_text = load_text(root_generated)
  if root_text is not None:
    root_api = generated_api(root_text, root=True)
    report_key_drift(root_generated, expected_generated_keys, set(root_api))
    for locale, class_name in (
        ('en', 'AppLocalizationsEn'),
        ('ru', 'AppLocalizationsRu'),
        ('zh', 'AppLocalizationsZh')):
      if "Locale('%s')" % locale not in root_text:
        errors.append('%s: supportedLocales is missing %s' % (root_generated, locale))
      if "case '%s':" % locale not in root_text:
        errors.append('%s: locale lookup is missing %s' % (root_generated, locale))
      if '%s()' % class_name not in root_text:
        errors.append('%s: locale lookup is missing %s' % (root_generated, class_name))
  for locale in ('en', 'ru', 'zh'):
    generated = GENERATED / ('app_localizations_%s.dart' % locale)
    text = load_text(generated)
    if text is not None:
      api = generated_api(text)
      report_key_drift(generated, expected_generated_keys, set(api))
      if root_text is not None:
        report_signature_drift(generated, root_api, api)
      for key in template:
        expected_literal = dart_message_literal(arbs[locale][key])
        if expected_literal not in text:
          errors.append('%s has stale generated text for %s'
              % (generated, key))

  # The legacy literal localizer must cover Russian as well: it is what turns the
  # remaining hard-coded Chinese literals on user-facing screens into Russian.
  legacy = L10N / 'legacy_text_localizer.dart'
  if not legacy.is_file():
    errors.append('missing file: %s' % legacy)
  else:
    legacy_text = legacy.read_text(encoding='utf-8')
    for table in ('_exactEn', '_exactRu', '_regexEn', '_regexRu'):
      if table not in legacy_text:
        errors.append('legacy_text_localizer.dart is missing %s' % table)
    if all(table in legacy_text for table in
        ('_exactEn', '_exactRu', '_regexEn', '_regexRu')):
      en_block = legacy_text[legacy_text.index('_exactEn'):legacy_text.index('_exactRu')]
      ru_block = legacy_text[legacy_text.index('_exactRu'):legacy_text.index('_regexEn')]
      key_re = re.compile('(?m)^    \'(.+?)\':')
      en_keys = key_re.findall(en_block)
      ru_keys = set(key_re.findall(ru_block))
      if len(en_keys) != len(ru_keys):
        errors.append('legacy localizer: %d en literals vs %d ru literals'
            % (len(en_keys), len(ru_keys)))
        missing_keys = [k for k in en_keys if k not in ru_keys]
        if missing_keys:
          errors.append('legacy localizer: no Russian for %s' % ', '.join(missing_keys[:10]))
      ru_values = re.findall(r"(?m)^    '.+?': '(.*)',", ru_block)
      for value in ru_values:
        if CJK.search(value):
          errors.append('legacy localizer: Chinese left in the Russian value: %s' % value[:40])

  # Do not allow new two-language helpers to silently send Russian users to
  # the Chinese branch. Existing call sites must use pick/pickForEnglishFlag.
  legacy_ternary = re.compile(
      r'(?:LegacyTextLocalizer\.isEnglish|_?isEnglish|_?english|en)\s*'
      r'\?\s*(?:r)?(?:\'(?:\\.|[^\'\\])*\'|"(?:\\.|[^"\\])*")\s*'
      r':\s*(?:r)?(?:\'(?:\\.|[^\'\\])*[\u3400-\u9fff](?:\\.|[^\'\\])*\'|'
      r'"(?:\\.|[^"\\])*[\u3400-\u9fff](?:\\.|[^"\\])*")',
      re.DOTALL)
  for dart_file in (Path('ui/lib')).rglob('*.dart'):
    dart_text = dart_file.read_text(encoding='utf-8')
    if legacy_ternary.search(dart_text):
      errors.append('%s: legacy EN/ZH ternary bypasses Russian fallback' % dart_file)
    # Nested ternaries and computed branches do not match the literal-only
    # expression above. Catch language flags that still lead to a quoted CJK
    # branch unless the surrounding code has an explicit Russian branch.
    language_branch = re.compile(
        r'(?:LegacyTextLocalizer\.isEnglish|_?isEnglish|_?english)\s*\?')
    quoted_cjk = re.compile(
        r'''(?:r)?(?:'(?:\\.|[^'\\])*[\u3400-\u9fff](?:\\.|[^'\\])*'|'''
        r'''"(?:\\.|[^"\\])*[\u3400-\u9fff](?:\\.|[^"\\])*")''')
    for match in language_branch.finditer(dart_text):
      branch = dart_text[match.start():match.start() + 360]
      if not quoted_cjk.search(branch):
        continue
      prefix = dart_text[max(0, match.start() - 320):match.start()]
      if 'isRussian' not in prefix:
        line = dart_text.count('\n', 0, match.start()) + 1
        errors.append('%s:%d: nested EN/ZH branch bypasses Russian fallback'
            % (dart_file, line))

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


def load_text(path):
  if not path.is_file():
    errors.append('missing generated file: %s' % path)
    return None
  return path.read_text(encoding='utf-8')


def report_key_drift(path, expected, actual):
  missing = sorted(expected - actual)
  extra = sorted(actual - expected)
  if missing:
    errors.append('%s is missing %d generated key(s): %s'
        % (path, len(missing), ', '.join(missing[:10])))
  if extra:
    errors.append('%s has %d unexpected generated key(s): %s'
        % (path, len(extra), ', '.join(extra[:10])))


def report_signature_drift(path, expected, actual):
  for key in sorted(set(expected) & set(actual)):
    if expected[key] != actual[key]:
      errors.append('%s has a signature mismatch for %s (%s != %s)'
          % (path, key, expected[key], actual[key]))


def dart_message_literal(value):
  placeholders = {}

  def reserve_placeholder(match):
    marker = '__GRIMCORE_PLACEHOLDER_%d__' % len(placeholders)
    placeholders[marker] = '$' + match.group(0)[1:-1]
    return marker

  escaped = PLACEHOLDER.sub(reserve_placeholder, value)
  escaped = (escaped.replace('\\', '\\\\')
      .replace("'", "\\'")
      .replace('"', '\\"')
      .replace('\n', '\\n')
      .replace('\r', '\\r')
      .replace('\t', '\\t'))
  for marker, replacement in placeholders.items():
    escaped = escaped.replace(marker, replacement)
  return "'%s'" % escaped


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
