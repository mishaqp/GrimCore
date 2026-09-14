import 'package:flutter_test/flutter_test.dart';
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
