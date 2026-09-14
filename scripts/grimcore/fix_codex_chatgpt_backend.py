#!/usr/bin/env python3
"""Small idempotent corrections for the generated account backend and UI."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def patch(path: str, transform) -> None:
    target = ROOT / path
    before = target.read_text(encoding="utf-8")
    after = transform(before)
    if after != before:
        target.write_text(after, encoding="utf-8")


for source in (
    "app/src/main/java/cn/com/omnimind/bot/agent/runtime/AgentDispatchConfiguration.kt",
    "app/src/main/java/cn/com/omnimind/bot/agent/runtime/AgentRuntimeManager.kt",
    "app/src/main/java/cn/com/omnimind/bot/manager/AssistsCoreManager.kt",
):
    patch(
        source,
        lambda value: value.replace(
            "import cn.com.omnimind.baselib.llm.isCodexChatGptAccount\n",
            "",
        ),
    )


def fix_account_manager(value: str) -> str:
    value = re.sub(
        r"; echo \\\\$\? >\$\{quote\(EXIT_PATH\)\}\)",
        "; echo ${'$'}? >${quote(EXIT_PATH)})",
        value,
        count=1,
    )
    value = re.sub(
        r"(?m)^\s*echo \\\\$!\s*$",
        "            echo ${'$'}!",
        value,
        count=1,
    )
    value = re.sub(
        r'(?m)^\s*private const val PATH_PREFIX = .+$',
        r'        private const val PATH_PREFIX = "PATH=\"/root/.npm-global/bin:\$PATH\"; export PATH;"',
        value,
        count=1,
    )
    return value


patch(
    "app/src/main/java/cn/com/omnimind/bot/agent/runtime/CodexChatGptAccountManager.kt",
    fix_account_manager,
)


def fix_provider_type_popup(value: str) -> str:
    marker = "cacheExtent: widget.estimatedHeight,"
    if marker in value:
        return value
    anchor = (
        "          child: ListView.builder(\n"
        "            padding: const EdgeInsets.symmetric(vertical: 8),\n"
        "            itemCount: widget.options.length,\n"
    )
    replacement = (
        "          child: ListView.builder(\n"
        "            cacheExtent: widget.estimatedHeight,\n"
        "            padding: const EdgeInsets.symmetric(vertical: 8),\n"
        "            itemCount: widget.options.length,\n"
    )
    index = value.rfind(anchor)
    if index < 0:
        raise RuntimeError("provider page: provider popup ListView anchor changed")
    return value[:index] + replacement + value[index + len(anchor) :]


# The provider catalog is intentionally scrollable, but it is also short. Keep
# its complete element tree cached so the last protocols remain discoverable by
# semantics/tests after adding Codex as the first entry.
patch(
    "ui/lib/features/home/pages/model_provider_setting/model_provider_setting_page.dart",
    fix_provider_type_popup,
)

# Keep the build scheme comment truthful after incrementing the installable APK.
patch(
    "app/build.gradle.kts",
    lambda value: value.replace(
        "// 0.1.0-grim.3 -> 10003",
        "// 0.1.0-grim.4 -> 10004",
    ),
)

print("Codex ChatGPT backend hotfixes applied")
