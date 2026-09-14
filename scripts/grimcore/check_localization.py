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
import xml.etree.ElementTree as ET
from pathlib import Path

L10N = Path('ui/lib/l10n')
GENERATED = L10N / 'generated'
ARB = {'zh': L10N / 'app_zh.arb', 'en': L10N / 'app_en.arb', 'ru': L10N / 'app_ru.arb'}
ANDROID_RESOURCE_CATALOGS = (
    Path('app/src/main/res'),
    Path('assists/src/main/res'),
    Path('baselib/src/main/res'),
    Path('accessibility/src/main/res'),
)
CJK = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]')
# The language picker intentionally lists every language in its own script.
CJK_ALLOWED = {'languageZhHans'}
PLACEHOLDER = re.compile(r'\{[^}]*\}')
ANDROID_PLACEHOLDER = re.compile(r'%(?:\d+\$)?[A-Za-z]')
GENERATED_DECLARATION = re.compile(
    r'(?m)^  String(?P<getter> get)? (?P<name>[A-Za-z_]\w*)'
    r'(?:\((?P<params>[^)]*)\))?')

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
  result = {}
  for match in GENERATED_DECLARATION.finditer(text):
    params = re.sub(r'\s+', ' ', match.group('params') or '').strip()
    result[match.group('name')] = ('getter' if match.group('getter') else params)
  return result


def generated_member_blocks(text):
  """Returns each generated getter/method body without adjacent members."""
  declarations = list(GENERATED_DECLARATION.finditer(text))
  return {
      declaration.group('name'): text[
          declaration.start():
          declarations[index + 1].start()
          if index + 1 < len(declarations) else len(text)]
      for index, declaration in enumerate(declarations)
  }


def stale_generated_keys(text, messages):
  """Finds ARB values missing from their corresponding generated member."""
  blocks = generated_member_blocks(text)
  return [
      key for key, value in messages.items()
      if key not in blocks or dart_message_literal(value) not in blocks[key]
  ]


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
      messages = {key: arbs[locale][key] for key in template}
      for key in stale_generated_keys(text, messages):
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
      exact_en_start = legacy_text.index('_exactEn =')
      exact_ru_start = legacy_text.index('_exactRu =')
      regex_en_start = legacy_text.index('_regexEn =')
      regex_ru_start = legacy_text.index('_regexRu =')
      en_block = legacy_text[exact_en_start:exact_ru_start]
      ru_block = legacy_text[exact_ru_start:regex_en_start]
      regex_en_block = legacy_text[
          regex_en_start:regex_ru_start]
      regex_ru_block = legacy_text[
          regex_ru_start:legacy_text.index(
              'static void setResolvedLocale')]
      en_entries = extract_dart_string_map(en_block)
      ru_entries = extract_dart_string_map(ru_block)
      en_keys = list(en_entries)
      en_key_set = set(en_entries)
      ru_key_set = set(ru_entries)
      if en_key_set != ru_key_set:
        errors.append('legacy localizer: %d en literals vs %d ru literals'
            % (len(en_key_set), len(ru_key_set)))
        missing_ru = [key for key in en_keys if key not in ru_key_set]
        if missing_ru:
          errors.append('legacy localizer: no Russian for %s'
              % ', '.join(missing_ru[:10]))
        missing_en = sorted(ru_key_set - en_key_set)
        if missing_en:
          errors.append('legacy localizer: no English for %s'
              % ', '.join(missing_en[:10]))
      for value in ru_entries.values():
        if CJK.search(value):
          errors.append('legacy localizer: Chinese left in the Russian value: %s' % value[:40])
      regex_en = extract_dart_regexp_patterns(regex_en_block)
      regex_ru = extract_dart_regexp_patterns(regex_ru_block, russian=True)
      if regex_en != regex_ru:
        errors.append('legacy localizer: English and Russian regex coverage differs')
      check_legacy_call_coverage(
          Path('ui/lib'), ru_entries, compile_dart_regexps(regex_ru))

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

  # Android resources. Every module with a user-facing Chinese default
  # catalog must provide complete English and Russian overlays; otherwise a
  # library resource silently falls back to Chinese even when the app is RU.
  for resource_dir in ANDROID_RESOURCE_CATALOGS:
    default_path = resource_dir / 'values/strings.xml'
    en_path = resource_dir / 'values-en/strings.xml'
    ru_path = resource_dir / 'values-ru/strings.xml'
    default_strings = load_android_strings(default_path)
    en_strings = load_android_strings(en_path)
    ru_strings = load_android_strings(ru_path)
    if default_strings is None or en_strings is None or ru_strings is None:
      continue
    default_keys = set(default_strings)
    for locale, path, values in (
        ('en', en_path, en_strings),
        ('ru', ru_path, ru_strings)):
      actual_keys = set(values)
      if actual_keys != default_keys:
        missing = sorted(default_keys - actual_keys)
        extra = sorted(actual_keys - default_keys)
        errors.append('%s does not mirror %s (missing=%s, extra=%s)'
            % (path, default_path, ', '.join(missing[:10]), ', '.join(extra[:10])))
      for key in sorted(default_keys & actual_keys):
        value = values[key]
        if not value.strip():
          errors.append('%s: empty Android string %s' % (path, key))
        expected = sorted(ANDROID_PLACEHOLDER.findall(default_strings[key]))
        actual = sorted(ANDROID_PLACEHOLDER.findall(value))
        if expected != actual:
          errors.append('%s: placeholder mismatch for %s (%s != %s)'
              % (path, key, expected, actual))
      if locale == 'ru' and CJK.search(path.read_text(encoding='utf-8')):
        errors.append('%s still contains Chinese text' % path)

  return report()


def load_text(path):
  if not path.is_file():
    errors.append('missing generated file: %s' % path)
    return None
  return path.read_text(encoding='utf-8')


def load_android_strings(path):
  if not path.is_file():
    errors.append('missing Android resource file: %s' % path)
    return None
  try:
    root = ET.parse(path).getroot()
  except ET.ParseError as error:
    errors.append('invalid Android resource XML %s: %s' % (path, error))
    return None
  return {
      element.attrib['name']: ''.join(element.itertext())
      for element in root
      if element.tag == 'string' and 'name' in element.attrib
  }


def _skip_dart_line_comment(text, start):
  end = text.find('\n', start + 2)
  return len(text) if end == -1 else end


def _skip_dart_block_comment(text, start):
  depth = 1
  cursor = start + 2
  while cursor < len(text) and depth:
    if text.startswith('/*', cursor):
      depth += 1
      cursor += 2
    elif text.startswith('*/', cursor):
      depth -= 1
      cursor += 2
    else:
      cursor += 1
  return cursor


def _dart_quote_at(text, start):
  raw = (text[start:start + 1] in ('r', 'R') and
      text[start + 1:start + 2] in ("'", '"') and
      (start == 0 or not (text[start - 1].isalnum() or text[start - 1] == '_')))
  quote_start = start + 1 if raw else start
  quote = text[quote_start:quote_start + 1]
  if quote not in ("'", '"'):
    return None
  triple = text.startswith(quote * 3, quote_start)
  return raw, quote_start, quote, 3 if triple else 1


def _skip_dart_quoted_source(text, start):
  quote_info = _dart_quote_at(text, start)
  if quote_info is None:
    return start + 1
  raw, quote_start, quote, quote_width = quote_info
  closing = quote * quote_width
  cursor = quote_start + quote_width
  while cursor < len(text):
    if text.startswith(closing, cursor):
      return cursor + quote_width
    if not raw and text[cursor] == '\\':
      cursor += 2
      continue
    if not raw and text.startswith('${', cursor):
      cursor = _skip_dart_braced_expression(text, cursor + 2)
      continue
    cursor += 1
  return len(text)


def _skip_dart_braced_expression(text, start):
  depth = 1
  cursor = start
  while cursor < len(text) and depth:
    if text.startswith('//', cursor):
      cursor = _skip_dart_line_comment(text, cursor)
      continue
    if text.startswith('/*', cursor):
      cursor = _skip_dart_block_comment(text, cursor)
      continue
    if _dart_quote_at(text, cursor) is not None:
      cursor = _skip_dart_quoted_source(text, cursor)
      continue
    if text[cursor] == '{':
      depth += 1
    elif text[cursor] == '}':
      depth -= 1
    cursor += 1
  return cursor


def _decode_dart_escape(text, start):
  """Returns (decoded character, next cursor) for a non-raw Dart escape."""
  if start + 1 >= len(text):
    return '\\', start + 1
  escaped = text[start + 1]
  if escaped == 'u':
    if text[start + 2:start + 3] == '{':
      end = text.find('}', start + 3)
      if end != -1:
        try:
          return chr(int(text[start + 3:end], 16)), end + 1
        except ValueError:
          pass
    digits = text[start + 2:start + 6]
    if len(digits) == 4 and all(c in '0123456789abcdefABCDEF' for c in digits):
      return chr(int(digits, 16)), start + 6
  if escaped == 'x':
    digits = text[start + 2:start + 4]
    if len(digits) == 2 and all(c in '0123456789abcdefABCDEF' for c in digits):
      return chr(int(digits, 16)), start + 4
  replacements = {
      'n': '\n', 'r': '\r', 't': '\t', 'b': '\b', 'f': '\f',
      'v': '\v', '\\': '\\', "'": "'", '"': '"', '$': '$'}
  return replacements.get(escaped, escaped), start + 2


def _interpolation_sample(expression):
  expression = expression.lower()
  numeric_hint = re.compile(
      r'(?:count|seconds?|minutes?|hours?|days?|months?|years?|index|'
      r'length|round|number|total|changedfiles|messagecount|\.in[a-z]+)')
  return '1' if numeric_hint.search(expression) else 'X'


def dart_string_literals(text):
  """Lexes Dart strings, decoding escapes and sampling interpolations.

  This intentionally stays dependency-free because the localization contract
  runs before Flutter is installed in the lightweight CI job.
  """
  strings = []
  ignored = []
  cursor = 0
  while cursor < len(text):
    if text.startswith('//', cursor):
      end = _skip_dart_line_comment(text, cursor)
      ignored.append((cursor, end))
      cursor = end
      continue
    if text.startswith('/*', cursor):
      end = _skip_dart_block_comment(text, cursor)
      ignored.append((cursor, end))
      cursor = end
      continue
    quote_info = _dart_quote_at(text, cursor)
    if quote_info is None:
      cursor += 1
      continue
    start = cursor
    raw, quote_start, quote, quote_width = quote_info
    closing = quote * quote_width
    cursor = quote_start + quote_width
    value = []
    sample = []
    interpolated = False
    while cursor < len(text):
      if text.startswith(closing, cursor):
        cursor += quote_width
        break
      if raw:
        value.append(text[cursor])
        sample.append(text[cursor])
        cursor += 1
        continue
      if text[cursor] == '\\':
        decoded, cursor = _decode_dart_escape(text, cursor)
        value.append(decoded)
        sample.append(decoded)
        continue
      if text.startswith('${', cursor):
        expression_start = cursor + 2
        end = _skip_dart_braced_expression(text, expression_start)
        expression = text[expression_start:max(expression_start, end - 1)]
        marker = _interpolation_sample(expression)
        value.append(marker)
        sample.append(marker)
        interpolated = True
        cursor = end
        continue
      if text[cursor] == '$':
        match = re.match(r'\$([A-Za-z_]\w*)', text[cursor:])
        if match:
          marker = _interpolation_sample(match.group(1))
          value.append(marker)
          sample.append(marker)
          interpolated = True
          cursor += len(match.group(0))
          continue
      value.append(text[cursor])
      sample.append(text[cursor])
      cursor += 1
    strings.append({
        'start': start,
        'end': cursor,
        'value': ''.join(value),
        'sample': ''.join(sample),
        'interpolated': interpolated,
        'source': text[start:cursor],
    })
    ignored.append((start, cursor))
  return strings, sorted(ignored)


def _offset_is_ignored(offset, spans):
  for start, end in spans:
    if start > offset:
      return False
    if start <= offset < end:
      return True
  return False


def _first_dart_argument_end(text, start, ignored_by_start):
  stack = []
  cursor = start
  while cursor < len(text):
    ignored_end = ignored_by_start.get(cursor)
    if ignored_end is not None:
      cursor = ignored_end
      continue
    char = text[cursor]
    if char in '([{':
      stack.append(char)
    elif char in ')]}':
      if not stack:
        return cursor
      stack.pop()
    elif char == ',' and not stack:
      return cursor
    cursor += 1
  return len(text)


def extract_dart_string_map(block):
  strings, _ = dart_string_literals(block)
  result = {}
  for index, item in enumerate(strings):
    cursor = item['end']
    while cursor < len(block) and block[cursor].isspace():
      cursor += 1
    if cursor >= len(block) or block[cursor] != ':':
      continue
    for value in strings[index + 1:]:
      if value['start'] > cursor:
        result[item['value']] = value['value']
        break
  return result


def extract_dart_regexp_patterns(block, russian=False):
  strings, ignored = dart_string_literals(block)
  pattern_starts = set()
  patterns = []
  for match in re.finditer(r'\bRegExp\s*\(', block):
    if _offset_is_ignored(match.start(), ignored):
      continue
    pattern = next((item for item in strings if item['start'] >= match.end()), None)
    if pattern is None:
      continue
    pattern_starts.add(pattern['start'])
    patterns.append(pattern['value'])
  if russian:
    for item in strings:
      if item['start'] not in pattern_starts and CJK.search(item['value']):
        errors.append(
            'legacy localizer: Chinese left in a Russian regex result: %s'
            % item['value'][:40])
  return patterns


def compile_dart_regexps(patterns):
  compiled = []
  for pattern in patterns:
    try:
      compiled.append(re.compile(pattern.replace('\\/', '/')))
    except re.error as error:
      errors.append('legacy localizer: unsupported regex %s: %s'
          % (pattern, error))
  return compiled


def check_legacy_call_coverage(root, ru_entries, ru_regexps):
  call_pattern = re.compile(
      r'(?<!\w)(?:LegacyTextLocalizer\s*\.\s*localize|trLegacy)\s*\(')
  for dart_file in root.rglob('*.dart'):
    if dart_file.parent == L10N or GENERATED in dart_file.parents:
      continue
    text = dart_file.read_text(encoding='utf-8')
    strings, ignored = dart_string_literals(text)
    ignored_by_start = {start: end for start, end in ignored}
    for call in call_pattern.finditer(text):
      if _offset_is_ignored(call.start(), ignored):
        continue
      argument_start = call.end()
      argument_end = _first_dart_argument_end(
          text, argument_start, ignored_by_start)
      for item in strings:
        if item['start'] < argument_start or item['end'] > argument_end:
          continue
        if not CJK.search(item['value']):
          continue
        sample = item['sample']
        covered = (not item['interpolated'] and item['value'] in ru_entries)
        if not covered:
          covered = any(pattern.fullmatch(sample) for pattern in ru_regexps)
        if covered:
          continue
        line = text.count('\n', 0, item['start']) + 1
        errors.append(
            '%s:%d: localize/trLegacy has no Russian coverage for %s'
            % (dart_file, line, item['source'][:80]))


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


def self_test():
  # Both swapped values still occur in the file, so the former global
  # substring check would accept this fixture. Member-scoped validation must
  # attribute each value to its own getter/method and reject the swap.
  fixture = """class Fixture {
  String get alpha => 'Beta';

  String get beta =>
      'Alpha';

  String greeting(Object name) {
    return 'Hello $name';
  }
}
"""
  messages = {
      'alpha': 'Alpha',
      'beta': 'Beta',
      'greeting': 'Hello {name}',
      'missing': 'Absent',
  }
  actual = stale_generated_keys(fixture, messages)
  expected = ['alpha', 'beta', 'missing']
  if actual != expected:
    print('GrimCore localization self-test FAILED: %s != %s'
        % (actual, expected))
    return 1
  print('GrimCore localization self-test passed')
  return 0


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


if __name__ == '__main__':
  if sys.argv[1:] == ['--self-test']:
    sys.exit(self_test())
  if sys.argv[1:]:
    print('usage: check_localization.py [--self-test]', file=sys.stderr)
    sys.exit(2)
  sys.exit(main())
