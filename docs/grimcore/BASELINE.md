# GrimCore — baseline record

Recorded at bootstrap time. Every value below was read from the GitHub REST API
on 2026-09-13, not from the README.

## Upstream

| Field | Value |
| --- | --- |
| Repository | `omnimind-ai/OmniBot` |
| Default branch | `main` |
| HEAD of `main` | `54aeae8046a4f3bcf0fccc1ca30713722a81d863` (2026-09-11, PR #530) |
| Latest published tag | `v0.6.2.3` = `11a380d72bd1385422c3d8ec9e521a895d22bb8d` (2026-09-10) |
| Latest non-prerelease release | `v0.6.2` = `2bd4e07793e3d47af65c9255757e473dc989ea15` (2026-09-07) |
| License | `NOASSERTION` — segmented dual license, AGPL-3.0 + commercial (see `LICENSE`) |
| Size | ~515 MB (`size` = 514944 KB) |
| Stars / forks | 1982 /139 |

## Why `v0.6.2.3` and not `main`

* `main` moved to `54aeae8` on 2026-09-11. That commit has **no** CI run: the
 `Pull Request CI` workflow only triggers on `pull_request` and
 `workflow_dispatch`, so pushes to `main` (including the `Sync models.dev
 catalog` bot commits) never produce a CI status.
* The last *push-triggered* green `Pull Request CI` run on `main` is
 `8203f5a428e1` from 2026-08-27 — i.e. six weeks of `main` history has no
 green CI signal on its own HEAD.
* `v0.6.2.3` is the latest published release tag **and** has a green
 `Release APK` workflow run (2026-09-10T16:11:36Z) that produced the
 distributed APK.

Therefore the GrimCore working branch starts from the `v0.6.2.3` commit.

To keep the pull-request diff limited to GrimCore changes, upstream `main`
(`54aeae8`) is merged into the branch as the second parent of the bootstrap
commit. `main` is exactly `v0.6.2.3` +1 commit (PR #530, a UI perf fix), so the
resulting tree equals upstream `main` while the tag remains recorded in history.

## Fork facts

| Field | Value |
| --- | --- |
| Fork | `mishaqp/GrimCore` |
| Fork parent | `omnimind-ai/OmniBot` (fork link preserved) |
| Created | 2026-09-13 |
| Default branch | `main` (upstream, untouched) |
| Working branch | `bootstrap/grimcore-v0.1.0` |
| Bootstrap commit | `ebff010c0c97db110bee1125456f0fd326b87c15` |

The stale, custom-commit-free fork `mishaqp/OmniBot-ru` was removed with the
owner's explicit confirmation in order to free the single per-network fork slot
(GitHub allows one fork of a given repository per account).

## Upstream CI inventory (as found)

The upstream tree contained `release.yml`, `sync-models-dev.yml`, and
`sync-to-cnb.yml` alongside `ci.yml`. The fork retires those workflows and the
Cloudflare update Worker; GrimCore updates are served only from its GitHub
Release assets.

`ci.yml` runs: gitleaks secret scan, Gradle wrapper validation, `flutter test`,
`flutter analyze`, then
`./gradlew :app:testDevelopStandardDebugUnitTest :app:lintDevelopStandardDebug
:app:assembleDevelopStandardDebug -Ptarget=lib/main_standard.dart`.

Toolchain pinned by upstream: JDK21, Flutter3.47.2, Node22, pnpm10.28.0,
Android platform37.0, NDK28.2.13676358.

The retired upstream release pipeline required `RELEASE_KEYSTORE`,
`RELEASE_PASSWORD`, and `RELEASE_KEY_ALIAS`. Those secrets do not exist in the
fork and must not exist — GrimCore has its own keystore and its own secrets
(`GRIM_*`).

## Upstream build facts

| Field | Upstream value | GrimCore value |
| --- | --- | --- |
| `applicationId` / `namespace` (app module) | `cn.com.omnimind.bot` | `com.mishaqp.grimcore` (applicationId) / namespace kept |
| `versionCode` | 15 | 10001 |
| `versionName` | `0.6.2.3` | `0.1.0-grim.1` |
| ABIs | `arm64-v8a`, `x86_64` | `arm64-v8a` for user builds |
| Flavors | `version` × `edition` (`develop`/`production` × `standard`) | unchanged |
| `minSdk` / `targetSdk` / `compileSdk` | 29 /36 /37 | unchanged |
| Signing | `OMNI_RELEASE_*` Gradle properties | `GRIM_RELEASE_*` (falls back to `OMNI_RELEASE_*`) |
