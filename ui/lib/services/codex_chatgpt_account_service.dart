import 'package:ui/services/agent_runtime_service.dart';

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
