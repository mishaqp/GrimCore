# GrimCore

Personal, independently versioned Android build of the OmniBot agent.

GrimCore is a **fork**, not a rewrite. It takes the upstream OmniBot code base at
tag `v0.6.2.3`, re-brands the user-facing surface, adds a Russian localization and
ships its own version, signing and CI/CD scheme. All agent functionality —
conversation, ACP harnesses (Codex CLI, Claude Code, Kimi Code, OpenCode,
DeepSeek Harness), the embedded Alpine/PRoot terminal, MCP server and tools,
skills, subagents, workspace, memory, browser control, WebChat, device control
through Shizuku and the Android permission architecture — comes from upstream and
is intentionally left intact.

* Package ID: `com.mishaqp.grimcore`
* First release: `v0.1.0-grim.1` (`versionCode` ~10001)
* ABI in the user APK: `arm64-v8a` only
* Assistant name: **Grim**

Upstream feature documentation: https://omnimind-ai.github.io/OmniBot-Docs/

## Why this fork exists

* Independent versioning and an independent, permanently signed release channel.
* Russian localization of the interface, terminal, ACP settings, MCP, skills,
 memory, browser, schedules, permissions and onboarding.
* A dark monochrome "cyberpunk" theme (near-black background, graphite surfaces,
 white text, muted red accent) with an original GrimCore vector mark.
* BYOK by default: your own OpenAI-compatible providers, no mandatory cloud
 account.

## Status

This is a bootstrap release. Read `docs/grimcore/BASELINE.md` for the exact
upstream baseline and `docs/grimcore/REPORT.md` for what is verified by code, by
CI, by emulator and what still needs a physical device.

## Building

The upstream build graph is unchanged.

```bash
# debug APK
./gradlew :app:assembleDevelopStandardDebug -Ptarget=lib/main_standard.dart

# arm64-v8a release APK (needs the GRIM_RELEASE_* signing properties)
./gradlew :app:assembleProductionStandardRelease \
 -Ptarget=lib/main_standard.dart \
 -PgrimAbiArm64Only=true
```

Signing secrets are read from Gradle properties / environment variables, never
from the repository: `GRIM_RELEASE_STORE_FILE`, `GRIM_RELEASE_STORE_PWD`,
`GRIM_RELEASE_KEY_ALIAS`, `GRIM_RELEASE_KEY_PWD`. If they are absent the
`OMNI_RELEASE_*` names are used as a fallback so that unmodified upstream flows
keep working. See `docs/grimcore/SIGNING.md`.

## License and attribution

Upstream OmniBot is under a segmented dual license: AGPL-3.0 for non-commercial,
personal, educational and research use, and a commercial license otherwise.
GrimCore is used for personal, non-commercial purposes only and is therefore
distributed under the upstream AGPL-3.0 terms.

The upstream `LICENSE` file is kept verbatim. See `NOTICE` for the full
attribution, the exact baseline commit and the trademark statement. GrimCore is
not affiliated with, endorsed by, or supported by the OmniBot/OmniMind authors.
