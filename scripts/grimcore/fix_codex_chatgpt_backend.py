#!/usr/bin/env python3
"""Small idempotent corrections for the generated account backend and UI."""
from pathlib import Path

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



def fix_provider_type_popup(value: str) -> str:
    switch_height = "const double _kProviderSwitchPopupMaxHeight = 320;\n"
    protocol_height_420 = "const double _kProviderTypePopupMaxHeight = 420;\n"
    protocol_height_320 = "const double _kProviderTypePopupMaxHeight = 320;\n"
    if protocol_height_420 in value:
        value = value.replace(protocol_height_420, protocol_height_320, 1)
    elif protocol_height_320 not in value:
        if switch_height not in value:
            raise RuntimeError("provider page: popup height constant anchor changed")
        value = value.replace(
            switch_height,
            switch_height + protocol_height_320,
            1,
        )

    shared_height = (
        "final estimatedHeight = (_kProviderTypeOptions.length * 48 + 24)\n"
        "        .clamp(120.0, _kProviderSwitchPopupMaxHeight)\n"
    )
    dedicated_height = (
        "final estimatedHeight = (_kProviderTypeOptions.length * 48 + 24)\n"
        "        .clamp(120.0, _kProviderTypePopupMaxHeight)\n"
    )
    if shared_height in value:
        value = value.replace(shared_height, dedicated_height, 1)
    elif dedicated_height not in value:
        raise RuntimeError("provider page: protocol popup height anchor changed")

    state_marker = (
        "class _ProviderTypePopupEntryState "
        "extends State<_ProviderTypePopupEntry> {"
    )
    head, separator, state = value.partition(state_marker)
    if not separator:
        raise RuntimeError("provider page: provider popup state anchor changed")

    stable_key = (
        "      key: ValueKey<String>("
        "'provider-protocol-option-${option.value}'),\n"
    )
    tile_anchor = (
        "    return Padding(\n"
        "      padding: const EdgeInsets.fromLTRB(10, 2, 10, 2),\n"
    )
    if stable_key not in state:
        if tile_anchor not in state:
            raise RuntimeError("provider page: provider option tile anchor changed")
        state = state.replace(
            tile_anchor,
            "    return Padding(\n" + stable_key
            + "      padding: const EdgeInsets.fromLTRB(10, 2, 10, 2),\n",
            1,
        )

    lazy = (
        "          child: ListView.builder(\n"
        "            padding: const EdgeInsets.symmetric(vertical: 8),\n"
        "            itemCount: widget.options.length,\n"
        "            itemBuilder: (context, index) {\n"
        "              return _buildProtocolTile(widget.options[index]);\n"
        "            },\n"
        "          ),\n"
    )
    eager = (
        "          child: ListView(\n"
        "            padding: const EdgeInsets.symmetric(vertical: 8),\n"
        "            children: List<Widget>.generate(\n"
        "              widget.options.length,\n"
        "              (index) => _buildProtocolTile(widget.options[index]),\n"
        "            ),\n"
        "          ),\n"
    )
    cached = (
        "          child: ListView.builder(\n"
        "            cacheExtent: widget.estimatedHeight,\n"
        "            padding: const EdgeInsets.symmetric(vertical: 8),\n"
        "            itemCount: widget.options.length,\n"
        "            itemBuilder: (context, index) {\n"
        "              return _buildProtocolTile(widget.options[index]);\n"
        "            },\n"
        "          ),\n"
    )
    if lazy not in state:
        for previous in (eager, cached):
            if previous in state:
                state = state.replace(previous, lazy, 1)
                break
        else:
            raise RuntimeError("provider page: provider popup list anchor changed")
    return head + separator + state


# Keep the protocol menu compact and scrollable as its catalog grows. Stable
# value keys let tests and accessibility locate an off-screen option after a
# real scroll instead of coupling correctness to a fixed popup height.
patch(
    "ui/lib/features/home/pages/model_provider_setting/model_provider_setting_page.dart",
    fix_provider_type_popup,
)

# Keep the build scheme comment truthful after incrementing the installable APK.
patch(
    "app/build.gradle.kts",
    lambda value: value.replace(
        "// 0.1.0-grim.3 -> 10003",
        "// 0.1.0-grim.5 -> 10005",
    ),
)

print("Codex ChatGPT backend hotfixes applied")
