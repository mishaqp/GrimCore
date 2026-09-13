import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ui/l10n/legacy_text_localizer.dart';
import 'package:ui/widgets/omnibot_error_widget.dart';

void main() {
  tearDown(LegacyTextLocalizer.clearResolvedLocale);

  testWidgets('global fallback replaces Flutter error widget', (tester) async {
    LegacyTextLocalizer.setResolvedLocale(const Locale('ru'));
    final originalBuilder = ErrorWidget.builder;
    addTearDown(() => ErrorWidget.builder = originalBuilder);
    installOmnibotErrorWidget();
    late final Widget fallback;
    try {
      fallback = ErrorWidget.builder(
        FlutterErrorDetails(exception: StateError('test rendering failure')),
      );
    } finally {
      ErrorWidget.builder = originalBuilder;
    }

    await tester.pumpWidget(MaterialApp(home: fallback));

    expect(find.byType(OmnibotSafeErrorWidget), findsOneWidget);
    expect(find.text('Содержимое временно недоступно'), findsOneWidget);
  });

  for (final (locale, message) in const <(Locale, String)>[
    (Locale('en'), 'Content is temporarily unavailable'),
    (Locale('zh'), '内容暂时无法显示'),
    (Locale('ru'), 'Содержимое временно недоступно'),
  ]) {
    testWidgets('safe error widget uses ${locale.languageCode} locale', (
      tester,
    ) async {
      LegacyTextLocalizer.setResolvedLocale(locale);
      await tester.pumpWidget(
        const MaterialApp(home: OmnibotSafeErrorWidget()),
      );

      expect(find.text(message), findsOneWidget);
      expect(tester.takeException(), isNull);
    });
  }
}
