#!/usr/bin/env python3
"""Apply the Codex (ChatGPT) provider UI and localization patch.

Executed only on GitHub Actions. Every structural replacement is fail-closed so
concurrent localization work cannot be overwritten silently.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, value: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value, encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    value = read(path)
    if old not in value:
        if new in value:
            return
        raise RuntimeError(f"{path}: expected anchor not found: {old[:160]!r}")
    if value.count(old) != 1:
        raise RuntimeError(f"{path}: anchor is not unique: {old[:160]!r}")
    write(path, value.replace(old, new, 1))


SERVICE = "ui/lib/services/model_provider_config_service.dart"
service = read(SERVICE)
if "class ModelProviderAuthMode" not in service:
    service = service.replace(
        "class ModelProviderConfig {\n",
        "abstract final class ModelProviderAuthMode {\n"
        "  static const String apiKey = 'api_key';\n"
        "  static const String codexChatGpt = 'codex_chatgpt';\n"
        "}\n\n"
        "const String codexChatGptModelId = 'gpt-5.3-codex-spark';\n\n"
        "class ModelProviderConfig {\n",
        1,
    )
    service = service.replace(
        "  final String wireApi;\n\n  const ModelProviderConfig({",
        "  final String wireApi;\n"
        "  final String authMode;\n"
        "  final bool acpOnly;\n\n"
        "  bool get isCodexChatGpt =>\n"
        "      authMode == ModelProviderAuthMode.codexChatGpt ||\n"
        "      providerType == ModelProviderAuthMode.codexChatGpt;\n\n"
        "  const ModelProviderConfig({",
        1,
    )
    service = service.replace(
        "    required this.wireApi,\n  });",
        "    required this.wireApi,\n"
        "    this.authMode = ModelProviderAuthMode.apiKey,\n"
        "    this.acpOnly = false,\n"
        "  });",
        1,
    )
    service = service.replace(
        "      wireApi: 'chat_completions',\n    );",
        "      wireApi: 'chat_completions',\n"
        "      authMode: ModelProviderAuthMode.apiKey,\n"
        "      acpOnly: false,\n"
        "    );",
        1,
    )
    service = service.replace(
        "      wireApi: (map['wireApi'] ?? 'chat_completions').toString(),\n    );",
        "      wireApi: (map['wireApi'] ?? 'chat_completions').toString(),\n"
        "      authMode: (map['authMode'] ?? ModelProviderAuthMode.apiKey).toString(),\n"
        "      acpOnly: map['acpOnly'] == true,\n"
        "    );",
        1,
    )
    service = service.replace(
        "  final String wireApi;\n\n  const ModelProviderProfileSummary({",
        "  final String wireApi;\n"
        "  final String authMode;\n"
        "  final bool acpOnly;\n\n"
        "  bool get isCodexChatGpt =>\n"
        "      authMode == ModelProviderAuthMode.codexChatGpt ||\n"
        "      sourceType == ModelProviderAuthMode.codexChatGpt;\n\n"
        "  const ModelProviderProfileSummary({",
        1,
    )
    service = service.replace(
        "    this.wireApi = 'chat_completions',\n  });",
        "    this.wireApi = 'chat_completions',\n"
        "    this.authMode = ModelProviderAuthMode.apiKey,\n"
        "    this.acpOnly = false,\n"
        "  });",
        1,
    )
    service = service.replace(
        "      wireApi: (map?['wireApi'] ?? 'chat_completions').toString(),\n    );",
        "      wireApi: (map?['wireApi'] ?? 'chat_completions').toString(),\n"
        "      authMode: (map?['authMode'] ?? ModelProviderAuthMode.apiKey).toString(),\n"
        "      acpOnly: map?['acpOnly'] == true,\n"
        "    );",
        1,
    )
    service = service.replace(
        "      wireApi: wireApi,\n    );\n  }\n}\n\nclass ModelProviderProfilesPayload",
        "      wireApi: wireApi,\n"
        "      authMode: authMode,\n"
        "      acpOnly: acpOnly,\n"
        "    );\n"
        "  }\n"
        "}\n\n"
        "class ModelProviderProfilesPayload",
        1,
    )
    old_save = """  static Future<ModelProviderProfileSummary> saveProfile({
    String? id,
    required String name,
    required String baseUrl,
    String? apiKey,
    Map<String, String>? customHeaders,
    bool clearApiKey = false,
    bool clearCustomHeaders = false,
    String sourceType = 'custom',
    String protocolType = 'openai_compatible',
    String? wireApi,
  }) async {
    final resolvedWireApi = inferWireApi(
      baseUrl,
      explicitWireApi: wireApi,
      protocolType: protocolType,
    );
    final normalizedCustomHeaders = customHeaders == null
        ? null
        : normalizeCustomHeaders(customHeaders);
    final result = await AssistsMessageService.assistCore
        .invokeMethod<Map<dynamic, dynamic>>('saveModelProviderProfile', {
          if (id != null && id.trim().isNotEmpty) 'id': id.trim(),
          'name': name,
          'baseUrl': baseUrl,
          if (apiKey != null) 'apiKey': apiKey,
          if (apiKey != null) 'replaceApiKey': true,
          if (clearApiKey) 'clearApiKey': true,
          if (normalizedCustomHeaders != null)
            'customHeaders': normalizedCustomHeaders,
          if (normalizedCustomHeaders != null) 'replaceCustomHeaders': true,
          if (clearCustomHeaders) 'clearCustomHeaders': true,
          'sourceType': sourceType,
          'protocolType': protocolType,
          'wireApi': resolvedWireApi,
        });
"""
    new_save = """  static Future<ModelProviderProfileSummary> saveProfile({
    String? id,
    required String name,
    required String baseUrl,
    String? apiKey,
    Map<String, String>? customHeaders,
    bool clearApiKey = false,
    bool clearCustomHeaders = false,
    String sourceType = 'custom',
    String protocolType = 'openai_compatible',
    String? wireApi,
    String? authMode,
  }) async {
    final resolvedAuthMode = authMode ??
        (sourceType == ModelProviderAuthMode.codexChatGpt
            ? ModelProviderAuthMode.codexChatGpt
            : ModelProviderAuthMode.apiKey);
    final isCodexAccount =
        resolvedAuthMode == ModelProviderAuthMode.codexChatGpt;
    final effectiveBaseUrl = isCodexAccount ? '' : baseUrl;
    final effectiveProtocolType = isCodexAccount ? 'codex_acp' : protocolType;
    final resolvedWireApi = isCodexAccount
        ? 'responses'
        : inferWireApi(
            effectiveBaseUrl,
            explicitWireApi: wireApi,
            protocolType: effectiveProtocolType,
          );
    final normalizedCustomHeaders = isCodexAccount || customHeaders == null
        ? null
        : normalizeCustomHeaders(customHeaders);
    final result = await AssistsMessageService.assistCore
        .invokeMethod<Map<dynamic, dynamic>>('saveModelProviderProfile', {
          if (id != null && id.trim().isNotEmpty) 'id': id.trim(),
          'name': name,
          'baseUrl': effectiveBaseUrl,
          if (!isCodexAccount && apiKey != null) 'apiKey': apiKey,
          if (!isCodexAccount && apiKey != null) 'replaceApiKey': true,
          if (clearApiKey || isCodexAccount) 'clearApiKey': true,
          if (normalizedCustomHeaders != null)
            'customHeaders': normalizedCustomHeaders,
          if (normalizedCustomHeaders != null) 'replaceCustomHeaders': true,
          if (clearCustomHeaders || isCodexAccount) 'clearCustomHeaders': true,
          'sourceType': isCodexAccount
              ? ModelProviderAuthMode.codexChatGpt
              : sourceType,
          'protocolType': effectiveProtocolType,
          'wireApi': resolvedWireApi,
          'authMode': resolvedAuthMode,
        });
"""
    if old_save not in service:
        raise RuntimeError("model_provider_config_service.dart: saveProfile anchor changed")
    service = service.replace(old_save, new_save, 1)
    # Account catalog is local and must never fall into HttpController.
    service = service.replace(
        "    final profileSnapshot = targetProfileId == null\n"
        "        ? null\n"
        "        : await _findProfileById(targetProfileId);\n"
        "    final result = await AssistsMessageService.assistCore\n",
        "    final profileSnapshot = targetProfileId == null\n"
        "        ? null\n"
        "        : await _findProfileById(targetProfileId);\n"
        "    if (profileSnapshot?.isCodexChatGpt == true) {\n"
        "      return const <ProviderModelOption>[\n"
        "        ProviderModelOption(\n"
        "          id: codexChatGptModelId,\n"
        "          displayName: codexChatGptModelId,\n"
        "          ownedBy: 'openai',\n"
        "          inputModalities: <String>['text', 'image'],\n"
        "          reasoning: true,\n"
        "          toolCall: true,\n"
        "        ),\n"
        "      ];\n"
        "    }\n"
        "    final result = await AssistsMessageService.assistCore\n",
        1,
    )
    write(SERVICE, service)

ACCOUNT_SERVICE = "ui/lib/services/codex_chatgpt_account_service.dart"
write(ACCOUNT_SERVICE, '''import 'package:ui/services/agent_runtime_service.dart';

enum CodexChatGptAccountState {
  notInstalled,
  installing,
  signedOut,
  waiting,
  signedIn,
  expired,
  cancelled,
  error,
}

class CodexChatGptAccountStatus {
  const CodexChatGptAccountStatus({
    required this.state,
    this.installed = true,
    this.authenticated = false,
    this.verificationUrl,
    this.userCode,
    this.loginId,
    this.message,
  });

  final CodexChatGptAccountState state;
  final bool installed;
  final bool authenticated;
  final String? verificationUrl;
  final String? userCode;
  final String? loginId;
  final String? message;

  bool get isWaiting => state == CodexChatGptAccountState.waiting;

  factory CodexChatGptAccountStatus.fromMap(Map<dynamic, dynamic>? map) {
    final source = map ?? const <dynamic, dynamic>{};
    final rawState = source['state']?.toString().trim().toLowerCase() ?? '';
    final state = switch (rawState) {
      'not_installed' => CodexChatGptAccountState.notInstalled,
      'installing' => CodexChatGptAccountState.installing,
      'waiting' => CodexChatGptAccountState.waiting,
      'signed_in' => CodexChatGptAccountState.signedIn,
      'expired' => CodexChatGptAccountState.expired,
      'cancelled' => CodexChatGptAccountState.cancelled,
      'error' => CodexChatGptAccountState.error,
      _ =>
        source['authenticated'] == true
            ? CodexChatGptAccountState.signedIn
            : CodexChatGptAccountState.signedOut,
    };
    String? allowedString(String key) {
      final value = source[key]?.toString().trim() ?? '';
      return value.isEmpty ? null : value;
    }

    return CodexChatGptAccountStatus(
      state: state,
      installed: source['installed'] != false,
      authenticated: source['authenticated'] == true,
      verificationUrl: allowedString('verificationUrl'),
      userCode: allowedString('userCode'),
      loginId: allowedString('loginId'),
      message: allowedString('message'),
    );
  }

  static const signedOut = CodexChatGptAccountStatus(
    state: CodexChatGptAccountState.signedOut,
  );
  static const installing = CodexChatGptAccountStatus(
    state: CodexChatGptAccountState.installing,
  );
}

abstract final class CodexChatGptAccountService {
  static Future<CodexChatGptAccountStatus> refresh() async {
    return CodexChatGptAccountStatus.fromMap(
      await AgentRuntimeService.readAccount(),
    );
  }

  static Future<CodexChatGptAccountStatus> install() async {
    await AgentRuntimeService.prepareAgent('codex-acp', force: true);
    return refresh();
  }

  static Future<CodexChatGptAccountStatus> login() async {
    return CodexChatGptAccountStatus.fromMap(
      await AgentRuntimeService.startLogin(
        type: CodexLoginType.chatgptDeviceCode,
      ),
    );
  }

  static Future<CodexChatGptAccountStatus> cancel(String? loginId) async {
    return CodexChatGptAccountStatus.fromMap(
      await AgentRuntimeService.cancelLogin(loginId: loginId),
    );
  }

  static Future<CodexChatGptAccountStatus> logout() async {
    return CodexChatGptAccountStatus.fromMap(
      await AgentRuntimeService.logoutAccount(),
    );
  }
}
''')

RUNTIME_SERVICE = "ui/lib/services/agent_runtime_service.dart"
runtime_service = read(RUNTIME_SERVICE)
if "logoutAccount()" not in runtime_service:
    runtime_service = runtime_service.replace(
        "  static Future<Map<String, dynamic>> cancelLogin({String? loginId}) {\n"
        "    return _invokeMap('account/login/cancel', {\n"
        "      if (loginId != null && loginId.trim().isNotEmpty)\n"
        "        'loginId': loginId.trim(),\n"
        "    });\n"
        "  }\n",
        "  static Future<Map<String, dynamic>> cancelLogin({String? loginId}) {\n"
        "    return _invokeMap('account/login/cancel', {\n"
        "      if (loginId != null && loginId.trim().isNotEmpty)\n"
        "        'loginId': loginId.trim(),\n"
        "    });\n"
        "  }\n\n"
        "  static Future<Map<String, dynamic>> logoutAccount() {\n"
        "    return _invokeMap('account/logout');\n"
        "  }\n",
        1,
    )
    write(RUNTIME_SERVICE, runtime_service)

PAGE = "ui/lib/features/home/pages/model_provider_setting/model_provider_setting_page.dart"
page = read(PAGE)
if "CodexChatGptAccountStatus" not in page:
    page = page.replace(
        "import 'package:flutter/material.dart';\n",
        "import 'package:flutter/material.dart';\n"
        "import 'package:flutter/services.dart';\n"
        "import 'package:url_launcher/url_launcher.dart';\n",
        1,
    )
    page = page.replace(
        "import 'package:ui/services/agent_runtime_service.dart';\n",
        "import 'package:ui/services/agent_runtime_service.dart';\n"
        "import 'package:ui/services/codex_chatgpt_account_service.dart';\n",
        1,
    )
    page = page.replace(
        "const List<_ProviderTypeOption> _kProviderTypeOptions = <_ProviderTypeOption>[\n",
        "const List<_ProviderTypeOption> _kProviderTypeOptions = <_ProviderTypeOption>[\n"
        "  _ProviderTypeOption(\n"
        "    value: ModelProviderAuthMode.codexChatGpt,\n"
        "    label: 'Codex (ChatGPT)',\n"
        "    sourceType: ModelProviderAuthMode.codexChatGpt,\n"
        "    protocolType: 'codex_acp',\n"
        "    wireApi: 'responses',\n"
        "  ),\n",
        1,
    )
    page = page.replace(
        "  String _selectedWireApi = 'chat_completions';\n\n  Timer? _autoSaveTimer;\n",
        "  String _selectedWireApi = 'chat_completions';\n"
        "  CodexChatGptAccountStatus _codexAccountStatus =\n"
        "      CodexChatGptAccountStatus.signedOut;\n"
        "  bool _isCodexAccountBusy = false;\n"
        "  bool _isCodexStatusRefreshing = false;\n\n"
        "  Timer? _autoSaveTimer;\n"
        "  Timer? _codexStatusTimer;\n",
        1,
    )
    page = page.replace(
        "  bool get _hasAnyProfileFieldFocus =>\n",
        "  bool get _isCodexChatGpt =>\n"
        "      _selectedSourceType == ModelProviderAuthMode.codexChatGpt ||\n"
        "      _currentProfile?.isCodexChatGpt == true;\n\n"
        "  bool get _hasAnyProfileFieldFocus =>\n",
        1,
    )
    page = page.replace(
        "  String get _selectedProviderValue {\n    final officialProvider",
        "  String get _selectedProviderValue {\n"
        "    if (_isCodexChatGpt) return ModelProviderAuthMode.codexChatGpt;\n"
        "    final officialProvider",
        1,
    )
    page = page.replace(
        "  String get _selectedProviderLabel {\n    final selectedValue = _selectedProviderValue;\n",
        "  String get _selectedProviderLabel {\n"
        "    final selectedValue = _selectedProviderValue;\n"
        "    if (selectedValue == ModelProviderAuthMode.codexChatGpt) {\n"
        "      return context.l10n.modelProviderCodexChatGptName;\n"
        "    }\n",
        1,
    )
    page = page.replace(
        "    _autoSaveTimer?.cancel();\n    unawaited(_persistProfileDraft());\n",
        "    _autoSaveTimer?.cancel();\n"
        "    _codexStatusTimer?.cancel();\n"
        "    unawaited(_persistProfileDraft());\n",
        1,
    )
    # Account profiles are valid with an empty endpoint and no credentials.
    page = page.replace(
        "      final rawBaseUrl = _baseUrlController.text.trim();\n"
        "      final nextBaseUrl =\n"
        "          ModelProviderConfigService.normalizeApiBase(rawBaseUrl) ?? '';\n"
        "      if (rawBaseUrl.isNotEmpty && nextBaseUrl.isEmpty) {\n",
        "      final rawBaseUrl = _isCodexChatGpt\n"
        "          ? ''\n"
        "          : _baseUrlController.text.trim();\n"
        "      final nextBaseUrl =\n"
        "          ModelProviderConfigService.normalizeApiBase(rawBaseUrl) ?? '';\n"
        "      if (!_isCodexChatGpt && rawBaseUrl.isNotEmpty && nextBaseUrl.isEmpty) {\n",
        1,
    )
    page = page.replace(
        "          wireApi: _selectedWireApi,\n        );",
        "          wireApi: _selectedWireApi,\n"
        "          authMode: _isCodexChatGpt\n"
        "              ? ModelProviderAuthMode.codexChatGpt\n"
        "              : ModelProviderAuthMode.apiKey,\n"
        "          clearApiKey: _isCodexChatGpt,\n"
        "          clearCustomHeaders: _isCodexChatGpt,\n"
        "        );",
        1,
    )
    # Refresh account state whenever a Codex profile becomes active.
    page = page.replace(
        "      _customHeadersErrorText = _computeCustomHeadersValidationError();\n    });\n  }\n\n  void _syncController",
        "      _customHeadersErrorText = _computeCustomHeadersValidationError();\n"
        "      if (current.isCodexChatGpt) {\n"
        "        _remoteModels = const <ProviderModelOption>[\n"
        "          ProviderModelOption(\n"
        "            id: codexChatGptModelId,\n"
        "            displayName: codexChatGptModelId,\n"
        "            ownedBy: 'openai',\n"
        "            inputModalities: <String>['text', 'image'],\n"
        "            reasoning: true,\n"
        "            toolCall: true,\n"
        "          ),\n"
        "        ];\n"
        "      }\n"
        "    });\n"
        "    if (current.isCodexChatGpt) {\n"
        "      unawaited(_refreshCodexAccountStatus());\n"
        "    } else {\n"
        "      _codexStatusTimer?.cancel();\n"
        "    }\n"
        "  }\n\n"
        "  void _syncController",
        1,
    )
    page = page.replace(
        "  }) async {\n    if (!profile.configured) return const [];\n",
        "  }) async {\n"
        "    if (profile.isCodexChatGpt) {\n"
        "      return const <ProviderModelOption>[\n"
        "        ProviderModelOption(\n"
        "          id: codexChatGptModelId,\n"
        "          displayName: codexChatGptModelId,\n"
        "          ownedBy: 'openai',\n"
        "          inputModalities: <String>['text', 'image'],\n"
        "          reasoning: true,\n"
        "          toolCall: true,\n"
        "        ),\n"
        "      ];\n"
        "    }\n"
        "    if (!profile.configured) return const [];\n",
        1,
    )
    # Account refresh replaces HTTP model discovery.
    page = page.replace(
        "    final current = _currentProfile;\n"
        "    if (current == null || _isFetchingModels) return;\n"
        "    final baseUrl = _baseUrlController.text.trim();\n\n"
        "    if (baseUrl.isEmpty) {\n",
        "    final current = _currentProfile;\n"
        "    if (current == null || _isFetchingModels) return;\n"
        "    if (_isCodexChatGpt) {\n"
        "      await _refreshCodexAccountStatus(showFailureToast: !silentError);\n"
        "      if (!mounted) return;\n"
        "      setState(() {\n"
        "        _remoteModels = const <ProviderModelOption>[\n"
        "          ProviderModelOption(\n"
        "            id: codexChatGptModelId,\n"
        "            displayName: codexChatGptModelId,\n"
        "            ownedBy: 'openai',\n"
        "            inputModalities: <String>['text', 'image'],\n"
        "            reasoning: true,\n"
        "            toolCall: true,\n"
        "          ),\n"
        "        ];\n"
        "      });\n"
        "      return;\n"
        "    }\n"
        "    final baseUrl = _baseUrlController.text.trim();\n\n"
        "    if (baseUrl.isEmpty) {\n",
        1,
    )
    # Prevent account model mutation and generic chat visibility changes.
    page = page.replace(
        "    if (current == null || current.readOnly) {\n      return;\n    }\n    final modelId = await showDialog<String>(",
        "    if (current == null || current.readOnly || _isCodexChatGpt) {\n"
        "      return;\n"
        "    }\n"
        "    final modelId = await showDialog<String>(",
        1,
    )
    page = page.replace(
        "    if (current == null || _deletingModelIds.contains(item.id)) {\n",
        "    if (current == null ||\n"
        "        _isCodexChatGpt ||\n"
        "        _deletingModelIds.contains(item.id)) {\n",
        1,
    )
    # Special selection persists an ACP-only account profile and clears BYOK secrets.
    page = page.replace(
        "    final isOfficialSelection = selected.baseUrl.isNotEmpty;\n",
        "    final isCodexSelection =\n"
        "        selected.value == ModelProviderAuthMode.codexChatGpt;\n"
        "    final isOfficialSelection = selected.baseUrl.isNotEmpty;\n",
        1,
    )
    page = page.replace(
        "    if (isOfficialSelection) {\n      _syncController(_nameController, selected.providerName);\n      _syncController(_baseUrlController, selected.baseUrl);\n    }\n",
        "    if (isCodexSelection) {\n"
        "      _syncController(\n"
        "        _nameController,\n"
        "        context.l10n.modelProviderCodexChatGptName,\n"
        "      );\n"
        "      _syncController(_baseUrlController, '');\n"
        "      _syncController(_apiKeyController, '');\n"
        "      _replaceCustomHeaderEntries(const <String, String>{});\n"
        "      _apiKeyDirty = true;\n"
        "      _customHeadersDirty = true;\n"
        "    } else if (isOfficialSelection) {\n"
        "      _syncController(_nameController, selected.providerName);\n"
        "      _syncController(_baseUrlController, selected.baseUrl);\n"
        "    }\n",
        1,
    )
    # There are two saveProfile wireApi anchors; replace the selection-specific one by context.
    selection_old = """        sourceType: selected.sourceType,
        protocolType: nextProtocolType,
        wireApi: nextWireApi,
      );
"""
    selection_new = """        sourceType: selected.sourceType,
        protocolType: nextProtocolType,
        wireApi: nextWireApi,
        authMode: isCodexSelection
            ? ModelProviderAuthMode.codexChatGpt
            : ModelProviderAuthMode.apiKey,
        clearApiKey: isCodexSelection,
        clearCustomHeaders: isCodexSelection,
      );
"""
    if selection_old not in page:
        raise RuntimeError("provider page: provider selection save anchor changed")
    page = page.replace(selection_old, selection_new, 1)
    page = page.replace(
        "      _apiKeyDirty = false;\n      _customHeadersDirty = false;\n    } catch (_) {",
        "      _apiKeyDirty = false;\n"
        "      _customHeadersDirty = false;\n"
        "      if (isCodexSelection) {\n"
        "        setState(() {\n"
        "          _remoteModels = const <ProviderModelOption>[\n"
        "            ProviderModelOption(\n"
        "              id: codexChatGptModelId,\n"
        "              displayName: codexChatGptModelId,\n"
        "              ownedBy: 'openai',\n"
        "              inputModalities: <String>['text', 'image'],\n"
        "              reasoning: true,\n"
        "              toolCall: true,\n"
        "            ),\n"
        "          ];\n"
        "        });\n"
        "        await _refreshCodexAccountStatus();\n"
        "      }\n"
        "    } catch (_) {",
        1,
    )
    # Localized provider label in menu sizing and rendering.
    page = page.replace(
        "      _kProviderTypeOptions.map((option) => option.label),\n",
        "      _kProviderTypeOptions.map(\n"
        "        (option) => option.value == ModelProviderAuthMode.codexChatGpt\n"
        "            ? context.l10n.modelProviderCodexChatGptName\n"
        "            : option.label,\n"
        "      ),\n",
        1,
    )
    popup_anchor = """                child: Text(
                  option.label,
                  maxLines: 1,
"""
    popup_replace = """                child: Text(
                  option.value == ModelProviderAuthMode.codexChatGpt
                      ? context.l10n.modelProviderCodexChatGptName
                      : option.label,
                  maxLines: 1,
"""
    # First occurrence belongs to the generic selection popup; replace last occurrence only.
    popup_index = page.rfind(popup_anchor)
    if popup_index < 0:
        raise RuntimeError("provider page: provider popup label anchor changed")
    page = page[:popup_index] + popup_replace + page[popup_index + len(popup_anchor):]

    # Insert account lifecycle methods before the card builder.
    account_methods = '''  void _scheduleCodexStatusPolling() {
    _codexStatusTimer?.cancel();
    if (!_isCodexChatGpt || !_codexAccountStatus.isWaiting) return;
    _codexStatusTimer = Timer.periodic(const Duration(seconds: 2), (_) {
      if (!mounted ||
          !_isCodexChatGpt ||
          _isCodexAccountBusy ||
          _isCodexStatusRefreshing) {
        return;
      }
      unawaited(_refreshCodexAccountStatus());
    });
  }

  Future<void> _refreshCodexAccountStatus({
    bool showFailureToast = false,
  }) async {
    if (!_isCodexChatGpt ||
        _isCodexAccountBusy ||
        _isCodexStatusRefreshing) {
      return;
    }
    _isCodexStatusRefreshing = true;
    try {
      final status = await CodexChatGptAccountService.refresh();
      if (!mounted || !_isCodexChatGpt) return;
      setState(() => _codexAccountStatus = status);
      _scheduleCodexStatusPolling();
    } catch (_) {
      if (!mounted) return;
      setState(() {
        _codexAccountStatus = const CodexChatGptAccountStatus(
          state: CodexChatGptAccountState.error,
        );
      });
      if (showFailureToast) {
        showToast(
          context.l10n.modelProviderCodexStatusFailed,
          type: ToastType.error,
        );
      }
    } finally {
      _isCodexStatusRefreshing = false;
    }
  }

  Future<void> _runCodexAccountAction(
    Future<CodexChatGptAccountStatus> Function() action, {
    required String failureMessage,
  }) async {
    if (_isCodexAccountBusy) return;
    setState(() => _isCodexAccountBusy = true);
    try {
      final status = await action();
      if (!mounted || !_isCodexChatGpt) return;
      setState(() => _codexAccountStatus = status);
      _scheduleCodexStatusPolling();
    } catch (_) {
      if (!mounted) return;
      showToast(failureMessage, type: ToastType.error);
      setState(() {
        _codexAccountStatus = const CodexChatGptAccountStatus(
          state: CodexChatGptAccountState.error,
        );
      });
    } finally {
      if (mounted) setState(() => _isCodexAccountBusy = false);
    }
  }

  Future<void> _installCodex() async {
    if (_isCodexAccountBusy) return;
    setState(() {
      _isCodexAccountBusy = true;
      _codexAccountStatus = CodexChatGptAccountStatus.installing;
    });
    try {
      final status = await CodexChatGptAccountService.install();
      if (!mounted || !_isCodexChatGpt) return;
      setState(() => _codexAccountStatus = status);
    } catch (_) {
      if (!mounted) return;
      setState(() {
        _codexAccountStatus = const CodexChatGptAccountStatus(
          state: CodexChatGptAccountState.error,
        );
      });
      showToast(
        context.l10n.modelProviderCodexInstallFailed,
        type: ToastType.error,
      );
    } finally {
      if (mounted) setState(() => _isCodexAccountBusy = false);
    }
  }

  Future<void> _copyCodexDeviceCode() async {
    final code = _codexAccountStatus.userCode;
    if (code == null || code.isEmpty) return;
    await Clipboard.setData(ClipboardData(text: code));
    if (mounted) {
      showToast(
        context.l10n.modelProviderCodexCodeCopied,
        type: ToastType.success,
      );
    }
  }

  Future<void> _openCodexVerificationUrl() async {
    final raw = _codexAccountStatus.verificationUrl;
    final uri = raw == null ? null : Uri.tryParse(raw);
    if (uri == null ||
        !await launchUrl(uri, mode: LaunchMode.externalApplication)) {
      if (mounted) {
        showToast(
          context.l10n.modelProviderCodexBrowserFailed,
          type: ToastType.error,
        );
      }
    }
  }

  String _codexStatusLabel() {
    return switch (_codexAccountStatus.state) {
      CodexChatGptAccountState.notInstalled =>
        context.l10n.modelProviderCodexNotInstalled,
      CodexChatGptAccountState.installing =>
        context.l10n.modelProviderCodexInstalling,
      CodexChatGptAccountState.signedOut =>
        context.l10n.modelProviderCodexSignedOut,
      CodexChatGptAccountState.waiting =>
        context.l10n.modelProviderCodexWaiting,
      CodexChatGptAccountState.signedIn =>
        context.l10n.modelProviderCodexSignedIn,
      CodexChatGptAccountState.expired =>
        context.l10n.modelProviderCodexExpired,
      CodexChatGptAccountState.cancelled =>
        context.l10n.modelProviderCodexCancelled,
      CodexChatGptAccountState.error => context.l10n.modelProviderCodexError,
    };
  }

  Widget _buildCodexAccountCard() {
    final status = _codexAccountStatus;
    final waiting = status.state == CodexChatGptAccountState.waiting;
    final signedIn = status.state == CodexChatGptAccountState.signedIn;
    final notInstalled = status.state == CodexChatGptAccountState.notInstalled;
    final installing = status.state == CodexChatGptAccountState.installing;
    final diagnosticMessage = status.message;
    return Container(
      key: const Key('codex-chatgpt-account-card'),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: context.omniPalette.surfaceSecondary,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: context.omniPalette.borderSubtle),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                signedIn ? LucideIcons.circleCheck : LucideIcons.logIn,
                size: 20,
                color: signedIn
                    ? context.omniPalette.accentPrimary
                    : _secondaryTextColor,
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Text(
                  _codexStatusLabel(),
                  style: TextStyle(
                    color: _primaryTextColor,
                    fontSize: 14,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
              if (_isCodexAccountBusy)
                const SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(strokeWidth: 2),
                ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            context.l10n.modelProviderCodexDescription,
            style: TextStyle(color: _secondaryTextColor, fontSize: 12),
          ),
          if (diagnosticMessage != null) ...[
            const SizedBox(height: 12),
            SelectableText(
              diagnosticMessage,
              key: const Key('codex-chatgpt-error-message'),
              style: TextStyle(
                color: Theme.of(context).colorScheme.error,
                fontSize: 12,
              ),
            ),
          ],
          if (waiting) ...[
            const SizedBox(height: 14),
            Text(
              context.l10n.modelProviderCodexDeviceInstructions,
              style: TextStyle(color: _secondaryTextColor, fontSize: 12),
            ),
            if (status.verificationUrl != null) ...[
              const SizedBox(height: 10),
              Text(
                context.l10n.modelProviderCodexVerificationUrl,
                style: TextStyle(color: _tertiaryTextColor, fontSize: 11),
              ),
              SelectableText(
                status.verificationUrl!,
                key: const Key('codex-chatgpt-verification-url'),
                style: TextStyle(color: _primaryTextColor, fontSize: 13),
              ),
            ],
            if (status.userCode != null) ...[
              const SizedBox(height: 10),
              Text(
                context.l10n.modelProviderCodexDeviceCode,
                style: TextStyle(color: _tertiaryTextColor, fontSize: 11),
              ),
              SelectableText(
                status.userCode!,
                key: const Key('codex-chatgpt-device-code'),
                style: TextStyle(
                  color: _primaryTextColor,
                  fontSize: 20,
                  fontWeight: FontWeight.w700,
                  letterSpacing: 1.5,
                ),
              ),
            ],
          ],
          const SizedBox(height: 14),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              if (notInstalled)
                FilledButton.icon(
                  key: const Key('codex-chatgpt-install-button'),
                  onPressed: _isCodexAccountBusy ? null : _installCodex,
                  icon: const Icon(LucideIcons.download, size: 17),
                  label: Text(context.l10n.modelProviderCodexInstall),
                )
              else if (!signedIn && !waiting && !installing)
                FilledButton.icon(
                  key: const Key('codex-chatgpt-login-button'),
                  onPressed: _isCodexAccountBusy
                      ? null
                      : () => _runCodexAccountAction(
                          CodexChatGptAccountService.login,
                          failureMessage:
                              context.l10n.modelProviderCodexLoginFailed,
                        ),
                  icon: const Icon(LucideIcons.logIn, size: 17),
                  label: Text(context.l10n.modelProviderCodexLogin),
                ),
              if (waiting && status.userCode != null)
                OutlinedButton.icon(
                  onPressed: _copyCodexDeviceCode,
                  icon: const Icon(LucideIcons.copy, size: 17),
                  label: Text(context.l10n.modelProviderCodexCopyCode),
                ),
              if (waiting && status.verificationUrl != null)
                OutlinedButton.icon(
                  onPressed: _openCodexVerificationUrl,
                  icon: const Icon(LucideIcons.externalLink, size: 17),
                  label: Text(context.l10n.modelProviderCodexOpenBrowser),
                ),
              if (waiting)
                TextButton(
                  onPressed: _isCodexAccountBusy
                      ? null
                      : () => _runCodexAccountAction(
                          () =>
                              CodexChatGptAccountService.cancel(status.loginId),
                          failureMessage:
                              context.l10n.modelProviderCodexStatusFailed,
                        ),
                  child: Text(context.l10n.modelProviderCodexCancelLogin),
                ),
              if (!notInstalled && !installing)
                TextButton(
                  onPressed: _isCodexAccountBusy
                      ? null
                      : () =>
                            _refreshCodexAccountStatus(showFailureToast: true),
                  child: Text(context.l10n.modelProviderCodexCheckStatus),
                ),
              if (signedIn)
                TextButton(
                  key: const Key('codex-chatgpt-logout-button'),
                  onPressed: _isCodexAccountBusy
                      ? null
                      : () => _runCodexAccountAction(
                          CodexChatGptAccountService.logout,
                          failureMessage:
                              context.l10n.modelProviderCodexLogoutFailed,
                        ),
                  child: Text(context.l10n.modelProviderCodexLogout),
                ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            context.l10n.modelProviderCodexModelNote,
            style: TextStyle(color: _tertiaryTextColor, fontSize: 11),
          ),
        ],
      ),
    );
  }

'''
    builder_anchor = "  Widget _buildCard({required Widget child}) {\n"
    if builder_anchor not in page:
        raise RuntimeError("provider page: card builder anchor changed")
    page = page.replace(builder_anchor, account_methods + builder_anchor, 1)

    # Hide BYOK-only fields and render the account card instead.
    fields_old = """                        const SizedBox(height: 12),
                        TextField(
                          controller: _baseUrlController,
                          focusNode: _baseUrlFocusNode,
                          enabled: !(_currentProfile?.readOnly ?? false),
                          style: context.omniInputTextStyle,
                          decoration: _buildInputDecoration(
                            label: 'Base URL',
                            hint: context.l10n.modelProviderBaseUrlHint,
                          ),
                        ),
                        const SizedBox(height: 8),
                        ValueListenableBuilder<TextEditingValue>(
                          valueListenable: _baseUrlController,
                          builder: (context, value, child) {
                            final url = _buildBaseUrlHelperText(value.text);
                            if (url == null) {
                              return const SizedBox.shrink();
                            }
                            return Text(
                              url,
                              style: TextStyle(
                                color: _tertiaryTextColor,
                                fontSize: 12,
                                fontFamily: 'PingFang SC',
                              ),
                            );
                          },
                        ),
                        if (_selectedProviderValue == 'openai_compatible') ...[
                          const SizedBox(height: 12),
                          _buildWireApiField(),
                        ],
                        const SizedBox(height: 14),
                        TextField(
                          controller: _apiKeyController,
                          focusNode: _apiKeyFocusNode,
                          enabled: !(_currentProfile?.readOnly ?? false),
                          style: context.omniInputTextStyle,
                          obscureText: _obscureApiKey,
                          decoration: _buildInputDecoration(
                            label: 'API Key',
                            hint: 'e.g., sk-xxxx',
                            suffixIcon: IconButton(
                              key: const Key(
                                'provider-api-key-visibility-button',
                              ),
                              splashRadius: 18,
                              onPressed: () {
                                setState(() {
                                  _obscureApiKey = !_obscureApiKey;
                                });
                              },
                              icon: Icon(
                                _obscureApiKey
                                    ? LucideIcons.eyeOff
                                    : LucideIcons.eye,
                                color: _tertiaryTextColor,
                                size: 18,
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          context.l10n.modelProviderApiKeyHint,
                          style: TextStyle(
                            color: _tertiaryTextColor,
                            fontSize: 12,
                            fontFamily: 'PingFang SC',
                          ),
                        ),
                        const SizedBox(height: 16),
                        _buildCustomHeadersEditor(),
"""
    fields_new = """                        const SizedBox(height: 12),
                        if (_isCodexChatGpt)
                          _buildCodexAccountCard()
                        else ...[
                          TextField(
                            controller: _baseUrlController,
                            focusNode: _baseUrlFocusNode,
                            enabled: !(_currentProfile?.readOnly ?? false),
                            style: context.omniInputTextStyle,
                            decoration: _buildInputDecoration(
                              label: 'Base URL',
                              hint: context.l10n.modelProviderBaseUrlHint,
                            ),
                          ),
                          const SizedBox(height: 8),
                          ValueListenableBuilder<TextEditingValue>(
                            valueListenable: _baseUrlController,
                            builder: (context, value, child) {
                              final url = _buildBaseUrlHelperText(value.text);
                              if (url == null) {
                                return const SizedBox.shrink();
                              }
                              return Text(
                                url,
                                style: TextStyle(
                                  color: _tertiaryTextColor,
                                  fontSize: 12,
                                  fontFamily: 'PingFang SC',
                                ),
                              );
                            },
                          ),
                          if (_selectedProviderValue == 'openai_compatible') ...[
                            const SizedBox(height: 12),
                            _buildWireApiField(),
                          ],
                          const SizedBox(height: 14),
                          TextField(
                            controller: _apiKeyController,
                            focusNode: _apiKeyFocusNode,
                            enabled: !(_currentProfile?.readOnly ?? false),
                            style: context.omniInputTextStyle,
                            obscureText: _obscureApiKey,
                            decoration: _buildInputDecoration(
                              label: 'API Key',
                              hint: 'e.g., sk-xxxx',
                              suffixIcon: IconButton(
                                key: const Key(
                                  'provider-api-key-visibility-button',
                                ),
                                splashRadius: 18,
                                onPressed: () {
                                  setState(() {
                                    _obscureApiKey = !_obscureApiKey;
                                  });
                                },
                                icon: Icon(
                                  _obscureApiKey
                                      ? LucideIcons.eyeOff
                                      : LucideIcons.eye,
                                  color: _tertiaryTextColor,
                                  size: 18,
                                ),
                              ),
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            context.l10n.modelProviderApiKeyHint,
                            style: TextStyle(
                              color: _tertiaryTextColor,
                              fontSize: 12,
                              fontFamily: 'PingFang SC',
                            ),
                          ),
                          const SizedBox(height: 16),
                          _buildCustomHeadersEditor(),
                        ],
"""
    if fields_old not in page:
        raise RuntimeError("provider page: BYOK fields anchor changed")
    page = page.replace(fields_old, fields_new, 1)
    page = page.replace(
        "                              onPressed: _currentProfile?.readOnly == true\n"
        "                                  ? null\n"
        "                                  : _promptAddModel,\n",
        "                              onPressed:\n"
        "                                  _currentProfile?.readOnly == true ||\n"
        "                                      _isCodexChatGpt\n"
        "                                  ? null\n"
        "                                  : _promptAddModel,\n",
        1,
    )
    page = page.replace(
        "                                  onPressed: _currentProfile == null\n"
        "                                      ? null\n",
        "                                  onPressed:\n"
        "                                      _currentProfile == null ||\n"
        "                                          _isCodexChatGpt\n"
        "                                      ? null\n",
        1,
    )
    write(PAGE, page)

# Localized strings. Product/model identifiers remain stable; every new
# explanatory/action/status string is in ARB and generated by Flutter.
translations = {
    "app_en.arb": {
        "modelProviderCodexChatGptName": "Codex (ChatGPT)",
        "modelProviderCodexDescription": "Uses the official Codex CLI device sign-in and the existing Codex ACP runtime. No API key is stored.",
        "modelProviderCodexNotInstalled": "Codex is not installed",
        "modelProviderCodexInstalling": "Installing Codex…",
        "modelProviderCodexSignedOut": "Not signed in",
        "modelProviderCodexWaiting": "Waiting for ChatGPT sign-in",
        "modelProviderCodexSignedIn": "Signed in with ChatGPT",
        "modelProviderCodexExpired": "The sign-in code expired",
        "modelProviderCodexCancelled": "Sign-in was cancelled",
        "modelProviderCodexError": "Codex sign-in error",
        "modelProviderCodexInstall": "Install Codex",
        "modelProviderCodexLogin": "Sign in with ChatGPT",
        "modelProviderCodexCheckStatus": "Check status",
        "modelProviderCodexLogout": "Sign out",
        "modelProviderCodexCancelLogin": "Cancel sign-in",
        "modelProviderCodexCopyCode": "Copy code",
        "modelProviderCodexOpenBrowser": "Open browser",
        "modelProviderCodexDeviceInstructions": "Open the official page, sign in to ChatGPT, and enter the one-time code. Tokens are never shown in the app.",
        "modelProviderCodexVerificationUrl": "Official sign-in page",
        "modelProviderCodexDeviceCode": "One-time code",
        "modelProviderCodexModelNote": "Model: gpt-5.3-codex-spark. If your account does not have access, Codex will return the real plan or rollout error without switching models.",
        "modelProviderCodexCodeCopied": "Code copied",
        "modelProviderCodexBrowserFailed": "Could not open the browser",
        "modelProviderCodexInstallFailed": "Could not install Codex",
        "modelProviderCodexLoginFailed": "Could not start ChatGPT sign-in",
        "modelProviderCodexLogoutFailed": "Could not sign out of Codex",
        "modelProviderCodexStatusFailed": "Could not check Codex sign-in status"
    },
    "app_ru.arb": {
        "modelProviderCodexChatGptName": "Codex (ChatGPT)",
        "modelProviderCodexDescription": "Использует официальный вход Codex CLI по коду устройства и существующий Codex ACP runtime. API-ключ не сохраняется.",
        "modelProviderCodexNotInstalled": "Codex не установлен",
        "modelProviderCodexInstalling": "Установка Codex…",
        "modelProviderCodexSignedOut": "Вход не выполнен",
        "modelProviderCodexWaiting": "Ожидание входа через ChatGPT",
        "modelProviderCodexSignedIn": "Вход через ChatGPT выполнен",
        "modelProviderCodexExpired": "Код входа истёк",
        "modelProviderCodexCancelled": "Вход отменён",
        "modelProviderCodexError": "Ошибка входа Codex",
        "modelProviderCodexInstall": "Установить Codex",
        "modelProviderCodexLogin": "Войти через ChatGPT",
        "modelProviderCodexCheckStatus": "Проверить статус",
        "modelProviderCodexLogout": "Выйти",
        "modelProviderCodexCancelLogin": "Отменить вход",
        "modelProviderCodexCopyCode": "Копировать код",
        "modelProviderCodexOpenBrowser": "Открыть браузер",
        "modelProviderCodexDeviceInstructions": "Откройте официальную страницу, войдите в ChatGPT и введите одноразовый код. Токены никогда не показываются в приложении.",
        "modelProviderCodexVerificationUrl": "Официальная страница входа",
        "modelProviderCodexDeviceCode": "Одноразовый код",
        "modelProviderCodexModelNote": "Модель: gpt-5.3-codex-spark. Если она недоступна вашему тарифу, Codex покажет реальную ошибку тарифа или rollout без подмены модели.",
        "modelProviderCodexCodeCopied": "Код скопирован",
        "modelProviderCodexBrowserFailed": "Не удалось открыть браузер",
        "modelProviderCodexInstallFailed": "Не удалось установить Codex",
        "modelProviderCodexLoginFailed": "Не удалось запустить вход через ChatGPT",
        "modelProviderCodexLogoutFailed": "Не удалось выйти из Codex",
        "modelProviderCodexStatusFailed": "Не удалось проверить статус входа Codex"
    },
    "app_zh.arb": {
        "modelProviderCodexChatGptName": "Codex (ChatGPT)",
        "modelProviderCodexDescription": "使用官方 Codex CLI 设备登录和现有 Codex ACP 运行时，不保存 API Key。",
        "modelProviderCodexNotInstalled": "Codex 尚未安装",
        "modelProviderCodexInstalling": "正在安装 Codex…",
        "modelProviderCodexSignedOut": "尚未登录",
        "modelProviderCodexWaiting": "等待 ChatGPT 登录",
        "modelProviderCodexSignedIn": "已通过 ChatGPT 登录",
        "modelProviderCodexExpired": "登录代码已过期",
        "modelProviderCodexCancelled": "登录已取消",
        "modelProviderCodexError": "Codex 登录错误",
        "modelProviderCodexInstall": "安装 Codex",
        "modelProviderCodexLogin": "通过 ChatGPT 登录",
        "modelProviderCodexCheckStatus": "检查状态",
        "modelProviderCodexLogout": "退出登录",
        "modelProviderCodexCancelLogin": "取消登录",
        "modelProviderCodexCopyCode": "复制代码",
        "modelProviderCodexOpenBrowser": "打开浏览器",
        "modelProviderCodexDeviceInstructions": "打开官方页面，登录 ChatGPT 并输入一次性代码。应用不会显示令牌。",
        "modelProviderCodexVerificationUrl": "官方登录页面",
        "modelProviderCodexDeviceCode": "一次性代码",
        "modelProviderCodexModelNote": "模型：gpt-5.3-codex-spark。若账户无权限，Codex 会显示真实套餐或灰度错误，不会切换模型。",
        "modelProviderCodexCodeCopied": "代码已复制",
        "modelProviderCodexBrowserFailed": "无法打开浏览器",
        "modelProviderCodexInstallFailed": "无法安装 Codex",
        "modelProviderCodexLoginFailed": "无法启动 ChatGPT 登录",
        "modelProviderCodexLogoutFailed": "无法退出 Codex",
        "modelProviderCodexStatusFailed": "无法检查 Codex 登录状态"
    },
}
for filename, values in translations.items():
    path = f"ui/lib/l10n/{filename}"
    data = json.loads(read(path))
    data.update(values)
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")

write("ui/test/services/codex_chatgpt_account_service_test.dart", '''import 'package:flutter_test/flutter_test.dart';
import 'package:ui/services/codex_chatgpt_account_service.dart';

void main() {
  test('legacy or missing state is safely signed out', () {
    final status = CodexChatGptAccountStatus.fromMap(const <String, dynamic>{});
    expect(status.state, CodexChatGptAccountState.signedOut);
    expect(status.authenticated, isFalse);
    expect(status.message, isNull);
  });

  test('device flow exposes only URL, code and opaque login id', () {
    final status = CodexChatGptAccountStatus.fromMap(const <String, dynamic>{
      'state': 'waiting',
      'verificationUrl': 'https://auth.openai.com/codex/device',
      'userCode': 'ABCD-EFGH',
      'loginId': 'opaque-id',
      'access_token': 'must-not-be-projected',
      'authJson': '{secret}',
    });
    expect(status.state, CodexChatGptAccountState.waiting);
    expect(status.verificationUrl, 'https://auth.openai.com/codex/device');
    expect(status.userCode, 'ABCD-EFGH');
    expect(status.loginId, 'opaque-id');
    expect(status.message, isNull);
    expect(status.toString(), isNot(contains('must-not-be-projected')));
    expect(status.toString(), isNot(contains('{secret}')));
  });

  test('safe native diagnostic remains available for the error card', () {
    final status = CodexChatGptAccountStatus.fromMap(const <String, dynamic>{
      'state': 'error',
      'message': 'device code login is not enabled for this Codex server',
    });
    expect(status.state, CodexChatGptAccountState.error);
    expect(
      status.message,
      'device code login is not enabled for this Codex server',
    );
  });

  test('expired and authenticated statuses remain distinct', () {
    final expired = CodexChatGptAccountStatus.fromMap(const <String, dynamic>{
      'state': 'expired',
      'message': 'Device code expired. Start sign-in again.',
    });
    final signedIn = CodexChatGptAccountStatus.fromMap(const <String, dynamic>{
      'state': 'signed_in',
      'authenticated': true,
    });
    expect(expired.state, CodexChatGptAccountState.expired);
    expect(expired.message, isNotEmpty);
    expect(signedIn.state, CodexChatGptAccountState.signedIn);
    expect(signedIn.authenticated, isTrue);
  });
}
''')

write("ui/test/services/model_provider_codex_profile_test.dart", '''import 'package:flutter_test/flutter_test.dart';
import 'package:ui/services/model_provider_config_service.dart';

void main() {
  test('old profiles default to API-key auth mode', () {
    final profile = ModelProviderProfileSummary.fromMap(const <String, dynamic>{
      'id': 'legacy',
      'name': 'Legacy',
      'sourceType': 'custom',
    });
    expect(profile.authMode, ModelProviderAuthMode.apiKey);
    expect(profile.isCodexChatGpt, isFalse);
  });

  test('Codex ChatGPT profile is ACP-only without URL or key', () {
    final profile = ModelProviderProfileSummary.fromMap(const <String, dynamic>{
      'id': 'codex-chatgpt',
      'name': 'Codex (ChatGPT)',
      'sourceType': 'codex_chatgpt',
      'authMode': 'codex_chatgpt',
      'protocolType': 'codex_acp',
      'baseUrl': '',
      'apiKey': '',
      'configured': true,
      'acpOnly': true,
    });
    expect(profile.isCodexChatGpt, isTrue);
    expect(profile.baseUrl, isEmpty);
    expect(profile.apiKey, isEmpty);
    expect(profile.acpOnly, isTrue);
    expect(codexChatGptModelId, 'gpt-5.3-codex-spark');
  });
}
''')

print("Codex ChatGPT UI patch applied")
