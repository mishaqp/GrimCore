import 'package:flutter/material.dart';
import 'package:ui/l10n/generated/app_localizations.dart';
import 'package:ui/l10n/generated/app_localizations_en.dart';
import 'package:ui/l10n/generated/app_localizations_ru.dart';
import 'package:ui/l10n/generated/app_localizations_zh.dart';
import 'package:ui/l10n/legacy_text_localizer.dart';

extension AppL10nBuildContextX on BuildContext {
  AppLocalizations get l10n {
    final localized = AppLocalizations.of(this);
    if (localized != null) return localized;
    return switch (Localizations.maybeLocaleOf(this)?.languageCode) {
      'en' => AppLocalizationsEn(),
      'ru' => AppLocalizationsRu(),
      _ => AppLocalizationsZh(),
    };
  }

  String trLegacy(String text) {
    final resolvedLocale = AppLocalizations.of(this) == null
        ? Localizations.maybeLocaleOf(this) ?? const Locale('en')
        : Localizations.localeOf(this);
    return LegacyTextLocalizer.localize(text, locale: resolvedLocale);
  }
}
