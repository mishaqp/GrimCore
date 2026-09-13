import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ui/l10n/l10n.dart';
import 'package:ui/l10n/legacy_text_localizer.dart';

void main() {
  tearDown(LegacyTextLocalizer.clearResolvedLocale);

  test('uses active locale override for legacy translations', () {
    LegacyTextLocalizer.setResolvedLocale(const Locale('zh'));
    expect(LegacyTextLocalizer.localize('设置'), '设置');

    LegacyTextLocalizer.setResolvedLocale(const Locale('en'));
    expect(LegacyTextLocalizer.localize('设置'), 'Settings');
  });

  group('pick', () {
    test('returns the requested English or Chinese branch', () {
      expect(
        LegacyTextLocalizer.pick('Settings', '设置', locale: const Locale('en')),
        'Settings',
      );
      expect(
        LegacyTextLocalizer.pick('Settings', '设置', locale: const Locale('zh')),
        '设置',
      );
    });

    test('uses a known Russian translation', () {
      expect(
        LegacyTextLocalizer.pick('Settings', '设置', locale: const Locale('ru')),
        'Настройки',
      );
    });

    test('prefers an explicit Russian branch', () {
      expect(
        LegacyTextLocalizer.pick(
          'Open workspace',
          '打开工作区',
          ru: 'Открыть рабочую область',
          locale: const Locale('ru'),
        ),
        'Открыть рабочую область',
      );
    });

    test(
      'falls back to English instead of Chinese for unknown Russian text',
      () {
        expect(
          LegacyTextLocalizer.pick(
            'New copy without a Russian translation',
            '尚未翻译的新文本',
            locale: const Locale('ru'),
          ),
          'New copy without a Russian translation',
        );
      },
    );

    test('upgrades a false English flag when the locale is Russian', () {
      expect(
        LegacyTextLocalizer.pickForEnglishFlag(
          false,
          'Settings',
          '设置',
          locale: const Locale('ru'),
        ),
        'Настройки',
      );
      expect(
        LegacyTextLocalizer.pickForEnglishFlag(
          false,
          'Untranslated',
          '未翻译',
          locale: const Locale('ru'),
        ),
        'Untranslated',
      );

      LegacyTextLocalizer.setResolvedLocale(const Locale('ru'));
      expect(
        LegacyTextLocalizer.pickForEnglishFlag(
          false,
          'Settings',
          '设置',
          ru: 'Настройки',
        ),
        'Настройки',
      );
    });
  });

  testWidgets('context fallback preserves Russian without an app delegate', (
    tester,
  ) async {
    await tester.pumpWidget(
      Localizations(
        locale: const Locale('ru'),
        delegates: const <LocalizationsDelegate<dynamic>>[
          DefaultWidgetsLocalizations.delegate,
        ],
        child: Builder(
          builder: (context) => Directionality(
            textDirection: TextDirection.ltr,
            child: Text(context.l10n.settingsTitle),
          ),
        ),
      ),
    );

    expect(find.text('Настройки'), findsOneWidget);
  });
}
