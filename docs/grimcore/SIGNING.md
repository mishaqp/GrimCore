# GrimCore signing

## Rules

1. The keystore and its passwords are **never** committed, logged, printed in a
 PR or attached to an artifact.
2. Android builds read the signing material from Gradle properties, which the CI
 workflow materialises from GitHub Actions secrets at build time.
3. The same keystore must be used for every GrimCore release, otherwise an
 already installed GrimCore cannot be updated in place.
4. A random debug key is never used for a published APK.

## Property names

| Gradle property | Environment variable | Meaning |
| --- | --- | --- |
| `GRIM_RELEASE_STORE_FILE` | `GRIM_RELEASE_STORE_FILE` | absolute path to the `.jks` |
| `GRIM_RELEASE_STORE_PWD` | `GRIM_RELEASE_STORE_PWD` | keystore password |
| `GRIM_RELEASE_KEY_ALIAS` | `GRIM_RELEASE_KEY_ALIAS` | key alias |
| `GRIM_RELEASE_KEY_PWD` | `GRIM_RELEASE_KEY_PWD` | key password |

If a `GRIM_RELEASE_*` value is missing, `app/build.gradle.kts` falls back to the
upstream `OMNI_RELEASE_*` name. That keeps unmodified upstream workflows working
while GrimCore uses its own secrets.

## GitHub Actions secrets

| Secret | Content |
| --- | --- |
| `GRIM_KEYSTORE_B64` | base64 of the keystore `.jks` (single line, no wrapping) |
| `GRIM_KEYSTORE_PWD` | keystore password |
| `GRIM_KEY_ALIAS` | key alias |
| `GRIM_KEY_PWD` | key password |
| `GRIM_CERT_SHA256` | expected SHA-256 of the signing certificate, lowercase hex |

`GRIM_CERT_SHA256` is optional but recommended: the release job then fails if the
built APK is signed with anything else, which is exactly the failure mode that
silently breaks "install over the previous release".

## Backing up the keystore

The keystore is the only thing that cannot be regenerated. Without it no future
GrimCore APK can update an installed GrimCore. Keep at least two copies off the
repository, for example:

* the owner's own encrypted storage / password manager attachment;
* a private, non-public location reachable only by the owner.

If the keystore is lost, the only recovery path is to publish a new applicationId
(a different app) or uninstall and reinstall, which loses app data.

## Verifying a built APK

```bash
apksigner verify --print-certs GrimCore-v0.1.0-grim.1-arm64-v8a.apk
aapt dump badging GrimCore-v0.1.0-grim.1-arm64-v8a.apk | grep -E 'package|native-code'
sha256sum GrimCore-v0.1.0-grim.1-arm64-v8a.apk
```

The certificate SHA-256 printed by `apksigner` must stay identical across
releases; this is what the CI update-compatibility check asserts.
