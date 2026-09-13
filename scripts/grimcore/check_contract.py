#!/usr/bin/env python3
"""GrimCore app-identity contract.

Fails the build when the fork identity is broken: wrong applicationId, wrong
version scheme, an accidental x86_64 in the user APK, a lost manifest
authority, a namespace rewrite, or a removed attribution file.
"""
import re
import sys
from pathlib import Path

ROOT = Path('.')
GRADLE = ROOT / 'app/build.gradle.kts'
MANIFEST = ROOT / 'app/src/main/AndroidManifest.xml'

EXPECTED_APPLICATION_ID = 'com.mishaqp.grimcore'
EXPECTED_NAMESPACE = 'cn.com.omnimind.bot'
VERSION_SCHEME = re.compile(r'^(\d+)\.(\d+)\.(\d+)-grim\.(\d+)$')

errors = []
notes = []


def check(condition, message):
  if not condition:
    errors.append(message)


def gradle_text():
  return GRADLE.read_text(encoding='utf-8')


def main():
  text = gradle_text()

  # 1. applicationId
  check('applicationId = "%s"' % EXPECTED_APPLICATION_ID in text,
    'app/build.gradle.kts must set applicationId = "%s"' % EXPECTED_APPLICATION_ID)

  # 2. namespace must stay untouched: Room migrations, ProGuard rules,
  #    JNI symbol names and all Kotlin packages depend on it.
  check('namespace = "%s"' % EXPECTED_NAMESPACE in text,
    'app/build.gradle.kts namespace must stay "%s"' % EXPECTED_NAMESPACE)
  check(text.count(EXPECTED_NAMESPACE) == 1,
    '"%s" must appear exactly once in app/build.gradle.kts (the namespace)' % EXPECTED_NAMESPACE)

  # 3. version scheme
  m = re.search(r'versionName\s*=\s*"([^"]+)"', text)
  check(m is not None, 'versionName not found')
  name = m.group(1) if m else ''
  vm = VERSION_SCHEME.match(name)
  check(vm is not None, 'versionName "%s" must match MAJOR.MINOR.PATCH-grim.N' % name)
  m = re.search(r'versionCode\s*=\s*(\d+)', text)
  check(m is not None, 'versionCode not found')
  if vm and m:
    expected = (int(vm.group(1)) * 1000000 + int(vm.group(2)) * 10000
      + int(vm.group(3)) * 100 + int(vm.group(4)))
    check(int(m.group(1)) == expected,
      'versionCode %s does not match the scheme value %d for %s' % (m.group(1), expected, name))

  # 4. the user APK is arm64-v8a only
  ndk = re.search(r'ndk \{(.*?)\n {8}\}', text, re.S)
  check(ndk is not None, 'ndk abiFilters block not found')
  if ndk:
    block = ndk.group(1)
    # comments explain the rule; only real code counts for the ordering check
    code_lines = [l for l in block.split('\n') if not l.strip().startswith('//')]
    code = '\n'.join(code_lines)
    check('abiFilters.add("arm64-v8a")' in code,
      'the arm64-only branch must add exactly arm64-v8a')
    check('else' in code and 'x86_64' in code,
      'x86_64 must stay available only behind the grimAbiArm64Only=false branch')
    if 'else' in code and 'x86_64' in code:
      check(code.index('else') < code.index('x86_64'),
        'x86_64 must only appear inside the else branch')

  # 5. no testOnly user APK
  manifest = MANIFEST.read_text(encoding='utf-8')
  check('testOnly' not in manifest, 'AndroidManifest.xml must not declare testOnly')
  check('testOnly' not in text, 'app/build.gradle.kts must not declare testOnly')

  # 6. authorities follow one applicationId
  check('${applicationId}.fileprovider' in manifest,
    'FileProvider authority must use ${applicationId}')
  check('${applicationId}.shizuku' in manifest,
    'ShizukuProvider authority must use ${applicationId}')

  # 7. attribution stays
  check((ROOT / 'LICENSE').is_file(), 'LICENSE must stay in the repository')
  check((ROOT / 'NOTICE').is_file(), 'NOTICE must stay in the repository')
  notice = (ROOT / 'NOTICE').read_text(encoding='utf-8')
  check('omnimind-ai/OmniBot' in notice, 'NOTICE must name the upstream project')
  check('v0.6.2.3' in notice, 'NOTICE must record the upstream baseline tag')

  # 8. release workflow targets arm64-v8a
  rel = ROOT / '.github/workflows/grimcore-release.yml'
  check(rel.is_file(), '.github/workflows/grimcore-release.yml is missing')
  if rel.is_file():
    rtext = rel.read_text(encoding='utf-8')
    check('grimAbiArm64Only=true' in rtext, 'the release workflow must pass -PgrimAbiArm64Only=true')
    check('arm64-v8a' in rtext, 'the release workflow must verify the arm64-v8a ABI')

  for note in notes:
    print('note:', note)
  if errors:
    print('GrimCore contract check FAILED:')
    for e in errors:
      print(' -', e)
    return 1
  print('GrimCore contract check passed')
  print(' applicationId:', EXPECTED_APPLICATION_ID)
  print(' namespace    :', EXPECTED_NAMESPACE)
  print(' version      :', name, '/', m.group(1) if m else '?')
  return 0


sys.exit(main())
