#!/usr/bin/env bash
# GrimCore APK verification: package id, version, ABI, signature, checksum.
#
# usage: verify_apk.sh --apk PATH --package ID --version-name NAME \
#                      --version-code CODE --abi arm64-v8a
set -euo pipefail

APK=""
EXPECTED_PACKAGE=""
EXPECTED_VERSION_NAME=""
EXPECTED_VERSION_CODE=""
EXPECTED_ABI="arm64-v8a"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apk) APK="$2"; shift 2 ;;
    --package) EXPECTED_PACKAGE="$2"; shift 2 ;;
    --version-name) EXPECTED_VERSION_NAME="$2"; shift 2 ;;
    --version-code) EXPECTED_VERSION_CODE="$2"; shift 2 ;;
    --abi) EXPECTED_ABI="$2"; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

fail() { echo "verify_apk: $*" >&2; exit 1; }

[[ -n "${APK}" ]] || fail "--apk is required"
[[ -f "${APK}" ]] || fail "APK not found: ${APK}"

SDK="${ANDROID_SDK_ROOT:-${ANDROID_HOME:-}}"
[[ -n "${SDK}" ]] || fail "ANDROID_SDK_ROOT / ANDROID_HOME is not set"

AAPT2="$(find "${SDK}/build-tools" -maxdepth 2 -name aapt2 2>/dev/null | sort | tail -n 1 || true)"
APKSIGNER="$(find "${SDK}/build-tools" -maxdepth 2 -name apksigner 2>/dev/null | sort | tail -n 1 || true)"
[[ -n "${AAPT2}" ]] || fail "aapt2 not found under ${SDK}/build-tools"
[[ -n "${APKSIGNER}" ]] || fail "apksigner not found under ${SDK}/build-tools"

BADGING="$("${AAPT2}" dump badging "${APK}")"

pkg_line="$(printf '%s\n' "${BADGING}" | grep -m1 '^package:')"
echo "package line: ${pkg_line}"
echo "${pkg_line}" | grep -q "name='${EXPECTED_PACKAGE}'" \
  || fail "package id mismatch (expected ${EXPECTED_PACKAGE})"
echo "${pkg_line}" | grep -q "versionCode='${EXPECTED_VERSION_CODE}'" \
  || fail "versionCode mismatch (expected ${EXPECTED_VERSION_CODE})"
echo "${pkg_line}" | grep -q "versionName='${EXPECTED_VERSION_NAME}'" \
  || fail "versionName mismatch (expected ${EXPECTED_VERSION_NAME})"

native="$(printf '%s\n' "${BADGING}" | grep -m1 '^native-code:' || true)"
echo "native-code: ${native}"
[[ -n "${native}" ]] || fail "APK contains no native code"
echo "${native}" | grep -q "'${EXPECTED_ABI}'" || fail "ABI ${EXPECTED_ABI} missing"
if [[ "${EXPECTED_ABI}" == "arm64-v8a" ]]; then
  echo "${native}" | grep -q "'x86_64'" && fail "x86_64 must not be part of the user APK"
fi

signature="$("${APKSIGNER}" verify --print-certs "${APK}")"
cert_sha="$(printf '%s\n' "${signature}" | grep -m1 'SHA-256 digest:' | awk '{print $NF}' | tr 'A-F' 'a-f')"
[[ -n "${cert_sha}" ]] || fail "could not read the signing certificate"
echo "signer certificate SHA-256: ${cert_sha}"
if [[ -n "${GRIM_CERT_SHA256:-}" ]]; then
  expected_cert="$(printf '%s' "${GRIM_CERT_SHA256}" | tr 'A-F' 'a-f')"
  [[ "${cert_sha}" == "${expected_cert}" ]] || fail "signing certificate changed: ${cert_sha} != ${expected_cert}"
  echo "signing certificate matches GRIM_CERT_SHA256"
else
  echo "note: GRIM_CERT_SHA256 is not set, certificate pinning skipped"
fi

sha256sum "${APK}"
echo "verify_apk: OK"
