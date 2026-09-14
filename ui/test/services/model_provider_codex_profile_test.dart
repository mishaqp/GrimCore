import 'package:flutter_test/flutter_test.dart';
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
