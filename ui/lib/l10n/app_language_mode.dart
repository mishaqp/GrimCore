import 'dart:ui';

/// Languages GrimCore can run in. Order matters: it is the order of the
/// picker in settings.
enum AppLanguageMode {
  system('system'),
  zhHans('zhHans'),
  en('en'),
  ru('ru');

  const AppLanguageMode(this.storageValue);

  final String storageValue;

  static AppLanguageMode fromStorageValue(String? raw) {
    final normalized = raw?.trim();
    return AppLanguageMode.values.firstWhere(
      (mode) => mode.storageValue == normalized,
      orElse: () => AppLanguageMode.system,
    );
  }
}

class ResolvedAppLocale {
  const ResolvedAppLocale({
    required this.mode,
    required this.systemLocale,
    required this.locale,
  });

  final AppLanguageMode mode;
  final Locale systemLocale;
  final Locale locale;

  bool get isEnglish => locale.languageCode == 'en';
  bool get isChinese => locale.languageCode == 'zh';
  bool get isRussian => locale.languageCode == 'ru';

  /// GrimCore branding is locale independent: the upstream fork used to
  /// switch between an English and a Chinese brand name here.
  String get brandName => 'GrimCore';
}

ResolvedAppLocale resolveAppLocale({
  required AppLanguageMode mode,
  required Locale systemLocale,
}) {
  final normalizedSystemLocale = _normalizeSupportedLocale(systemLocale);
  final resolvedLocale = switch (mode) {
    AppLanguageMode.system => normalizedSystemLocale,
    AppLanguageMode.zhHans => const Locale('zh', 'CN'),
    AppLanguageMode.en => const Locale('en', 'US'),
    AppLanguageMode.ru => const Locale('ru', 'RU'),
  };

  return ResolvedAppLocale(
    mode: mode,
    systemLocale: normalizedSystemLocale,
    locale: resolvedLocale,
  );
}

Locale _normalizeSupportedLocale(Locale locale) {
  switch (locale.languageCode.toLowerCase()) {
    case 'zh':
      return const Locale('zh', 'CN');
    case 'ru':
      return const Locale('ru', 'RU');
    default:
      return const Locale('en', 'US');
  }
}
