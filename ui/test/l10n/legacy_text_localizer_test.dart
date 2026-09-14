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

  group('remaining legacy call coverage', () {
    const literalSources = <String>[
      '1 个文件',
      'Agent 配置',
      'GUI 任务已完成',
      'GUI 任务未完成',
      '加载中',
      '取消归档失败',
      '取消置顶失败',
      '图像',
      '复制失败',
      '完成思考',
      '审阅',
      '审阅中',
      '展开全部分组',
      '已取消归档',
      '已取消置顶',
      '已复制对话',
      '已恢复场景默认模型',
      '已置顶',
      '已载入',
      '开启后，助手回复会在当前消息旁显示播放按钮，并可自动朗读。',
      '归档失败',
      '快速开始',
      '扫描 Codex Bridge',
      '折叠全部分组',
      '搜索',
      '搜索中',
      '暂无模型分组',
      '查看 RunLog',
      '查看中',
      '查看复用指令',
      '注册为复用指令',
      '活动中',
      '状态',
      '空闲',
      '等待确认',
      '统一由 ACP 语音场景提供播放和自动朗读。',
      '缓存',
      '编辑消息',
      '置顶失败',
      '计划',
      '设置权限',
      '语音回复',
      '语音能力',
      '语音设置已保存',
      '请先使用 /openclaw 配置 OpenClaw',
      '请先在上方“语音合成”中绑定 Provider 和模型，绑定后即可播放。',
      '请放心，这些权限你随时可以收回',
      '请等待当前 Agent 任务完成后再切换模型。',
      '账户',
      '选择此目录',
      '配置模型连接',
      '重命名失败',
      '重新查看基础配置与可选插件说明',
    ];
    final cjk = RegExp(r'[\u3400-\u9fff]');

    test('translates every remaining literal in English and Russian', () {
      for (final source in literalSources) {
        for (final locale in const <Locale>[Locale('en'), Locale('ru')]) {
          final translated = LegacyTextLocalizer.localize(
            source,
            locale: locale,
          );
          expect(translated, isNot(source), reason: '$locale: $source');
          expect(cjk.hasMatch(translated), isFalse, reason: '$locale: $source');
        }
      }
    });

    test('translates the dynamic file-count and voice messages', () {
      expect(
        LegacyTextLocalizer.localize('3 个文件', locale: const Locale('en')),
        '3 files',
      );
      expect(
        LegacyTextLocalizer.localize('3 个文件', locale: const Locale('ru')),
        '3 файла',
      );
      expect(
        LegacyTextLocalizer.localize('5 个文件', locale: const Locale('ru')),
        '5 файлов',
      );
      expect(
        LegacyTextLocalizer.localize('21 个文件', locale: const Locale('ru')),
        '21 файл',
      );
      expect(
        LegacyTextLocalizer.localize(
          '语音设置保存失败：timeout',
          locale: const Locale('en'),
        ),
        'Failed to save voice settings: timeout',
      );
      expect(
        LegacyTextLocalizer.localize(
          '语音设置保存失败：timeout',
          locale: const Locale('ru'),
        ),
        'Не удалось сохранить настройки голоса: timeout',
      );
      expect(
        LegacyTextLocalizer.localize(
          '声音：alloy · 风格：calm',
          locale: const Locale('en'),
        ),
        'Voice: alloy · Style: calm',
      );
      expect(
        LegacyTextLocalizer.localize(
          '声音：alloy · 风格：calm',
          locale: const Locale('ru'),
        ),
        'Голос: alloy · Стиль: calm',
      );
      expect(
        LegacyTextLocalizer.localize(
          '暂时无法生成回复，请重试。',
          locale: const Locale('ru'),
        ),
        'Сейчас не удаётся сформировать ответ, попробуйте ещё раз.',
      );
      expect(
        LegacyTextLocalizer.localize(
          '暂时无法生成回复，请重试。timeout',
          locale: const Locale('ru'),
        ),
        'Сейчас не удаётся сформировать ответ, попробуйте ещё раз. timeout',
      );
    });

    test('handles a Dart unicode escape as its runtime Chinese key', () {
      const escapedSource = '\u7f16\u8f91\u6d88\u606f';
      expect(
        LegacyTextLocalizer.localize(escapedSource, locale: const Locale('ru')),
        'Изменить сообщение',
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
