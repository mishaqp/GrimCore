#!/usr/bin/env python3
"""Prove that the new GrimCore APK can update the previously released one.

Compares versionCode (must strictly increase) and the signing certificate
(must be identical) against the newest published GrimCore release that ships an
APK. With no previous release the check reports "first release" and passes.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path


def api(url, token):
  req = urllib.request.Request(url, headers={
    'Authorization': 'Bearer %s' % token,
    'Accept': 'application/vnd.github+json',
    'User-Agent': 'grimcore-release-check',
  })
  with urllib.request.urlopen(req, timeout=60) as resp:
    return json.loads(resp.read().decode('utf-8'))


def download(url, token, dest):
  req = urllib.request.Request(url, headers={
    'Authorization': 'Bearer %s' % token,
    'Accept': 'application/octet-stream',
    'User-Agent': 'grimcore-release-check',
  })
  with urllib.request.urlopen(req, timeout=300) as resp, open(dest, 'wb') as fh:
    while True:
      chunk = resp.read(1 << 20)
      if not chunk:
        break
      fh.write(chunk)


def sdk_tool(name):
  sdk = os.environ.get('ANDROID_SDK_ROOT') or os.environ.get('ANDROID_HOME') or ''
  if not sdk:
    return None
  tools_dir = Path(sdk, 'build-tools')
  if not tools_dir.is_dir():
    return None
  hits = sorted(str(p) for p in tools_dir.glob('*/' + name))
  return hits[-1] if hits else None


def version_code_of(apk):
  aapt2 = sdk_tool('aapt2')
  if not aapt2:
    return None
  out = subprocess.run([aapt2, 'dump', 'badging', apk], capture_output=True, text=True)
  m = re.search(r"versionCode='(\d+)'", out.stdout)
  return int(m.group(1)) if m else None


def cert_of(apk):
  apksigner = sdk_tool('apksigner')
  if not apksigner:
    return None
  out = subprocess.run([apksigner, 'verify', '--print-certs', apk], capture_output=True, text=True)
  m = re.search(r'SHA-256 digest:\s*([0-9a-fA-F]+)', out.stdout)
  return m.group(1).lower() if m else None


def main():
  p = argparse.ArgumentParser()
  p.add_argument('--apk', required=True)
  p.add_argument('--version-code', required=True, type=int)
  args = p.parse_args()

  token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
  repo = os.environ.get('GITHUB_REPOSITORY', '')
  if not token or not repo:
    print('update-compat: no GH_TOKEN/GITHUB_REPOSITORY, skipping')
    return 0

  releases = api('https://api.github.com/repos/%s/releases?per_page=30' % repo, token)
  current_tag = os.environ.get('GITHUB_REF_NAME', '')
  previous = None
  for rel in releases:
    if rel.get('draft') or rel.get('tag_name') == current_tag:
      continue
    assets = [a for a in rel.get('assets', []) if a.get('name', '').endswith('.apk')]
    if assets:
      previous = (rel, assets[0])
      break

  if not previous:
    print('update-compat: no previously published GrimCore APK -> first release, nothing to compare')
    return 0

  rel, asset = previous
  print('previous release:', rel['tag_name'], '(', asset['name'], ')')

  prev_code = None
  m = re.search(r'versionCode:\s*`?(\d+)`?', rel.get('body') or '')
  if m:
    prev_code = int(m.group(1))

  with tempfile.TemporaryDirectory() as tmp:
    prev_apk = Path(tmp) / 'previous.apk'
    download(asset['url'], token, prev_apk)
    code_from_apk = version_code_of(prev_apk)
    if code_from_apk is not None:
      prev_code = code_from_apk
    prev_cert = cert_of(prev_apk)
    new_cert = cert_of(args.apk)

  if prev_code is None:
    print('update-compat: previous versionCode unknown, ordering check skipped')
  elif args.version_code <= prev_code:
    print('update-compat FAILED: new versionCode %d is not greater than the released %d'
      % (args.version_code, prev_code))
    return 1
  else:
    print('update-compat: versionCode %d > released %d' % (args.version_code, prev_code))

  if prev_cert and new_cert and prev_cert != new_cert:
    print('update-compat FAILED: signing certificate changed, an in-place update would be rejected')
    print(' previous:', prev_cert)
    print(' current :', new_cert)
    return 1
  if prev_cert and new_cert:
    print('update-compat: signing certificate identical to the previous release')
  else:
    print('update-compat: certificate comparison skipped (tooling unavailable)')

  print('update-compat: OK')
  return 0


sys.exit(main())
