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
    eager = (
        "          child: ListView(\n"
        "            padding: const EdgeInsets.symmetric(vertical: 8),\n"
        "            children: List<Widget>.generate(\n"
        "              widget.options.length,\n"
        "              (index) => _buildProtocolTile(widget.options[index]),\n"
        "            ),\n"
        "          ),\n"
    )
    if eager in value:
        return value

    lazy_variants = (
        (
            "          child: ListView.builder(\n"
            "            cacheExtent: widget.estimatedHeight,\n"
            "            padding: const EdgeInsets.symmetric(vertical: 8),\n"
            "            itemCount: widget.options.length,\n"
            "            itemBuilder: (context, index) {\n"
            "              return _buildProtocolTile(widget.options[index]);\n"
            "            },\n"
            "          ),\n"
        ),
        (
            "          child: ListView.builder(\n"
            "            padding: const EdgeInsets.symmetric(vertical: 8),\n"
            "            itemCount: widget.options.length,\n"
            "            itemBuilder: (context, index) {\n"
            "              return _buildProtocolTile(widget.options[index]);\n"
            "            },\n"
            "          ),\n"
        ),
    )
    for lazy in lazy_variants:
        if lazy in value:
            return value.replace(lazy, eager, 1)
    raise RuntimeError("provider page: provider popup ListView anchor changed")


# The catalog remains height-limited and scrollable, but its short list is built
# eagerly. This keeps every protocol reachable through semantics and widget
# tests after inserting Codex at the beginning of the menu.
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
