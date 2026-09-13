import 'package:flutter/widgets.dart';
import 'package:ui/l10n/legacy_text_localizer.dart';

/// Whether the active locale should show English onboarding copy.
bool onboardingIsEnglish(BuildContext context) =>
    Localizations.localeOf(context).languageCode.toLowerCase() == 'en';

/// Picks the Chinese or English copy for the current locale.
String onbTr(BuildContext context, String zh, String en) =>
    LegacyTextLocalizer.pick(en, zh, locale: Localizations.localeOf(context));

/// Signature for the localization resolver passed into controllers.
typedef OnboardingTranslator = String Function(String zh, String en);
