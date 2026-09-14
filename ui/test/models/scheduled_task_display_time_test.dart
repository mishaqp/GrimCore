import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ui/l10n/legacy_text_localizer.dart';
import 'package:ui/models/scheduled_task.dart';

void main() {
  tearDown(LegacyTextLocalizer.clearResolvedLocale);

  ScheduledTask task({
    required ScheduledTaskType type,
    String? fixedTime,
    int? countdownMinutes,
  }) {
    return ScheduledTask(
      id: 'display-time',
      title: 'Display time',
      type: type,
      fixedTime: fixedTime,
      countdownMinutes: countdownMinutes,
      createdAt: 0,
    );
  }

  test('formats fixed time for each locale', () {
    final scheduledTask = task(
      type: ScheduledTaskType.fixedTime,
      fixedTime: '08:30',
    );

    LegacyTextLocalizer.setResolvedLocale(const Locale('en'));
    expect(scheduledTask.getDisplayTimeText(), 'at 08:30');

    LegacyTextLocalizer.setResolvedLocale(const Locale('zh'));
    expect(scheduledTask.getDisplayTimeText(), '08:30');

    LegacyTextLocalizer.setResolvedLocale(const Locale('ru'));
    expect(scheduledTask.getDisplayTimeText(), 'в 08:30');
  });

  test('formats countdown with hours and minutes for each locale', () {
    final scheduledTask = task(
      type: ScheduledTaskType.countdown,
      countdownMinutes: 65,
    );

    LegacyTextLocalizer.setResolvedLocale(const Locale('en'));
    expect(scheduledTask.getDisplayTimeText(), 'in 1h 5m');

    LegacyTextLocalizer.setResolvedLocale(const Locale('zh'));
    expect(scheduledTask.getDisplayTimeText(), '1小时5分钟后');

    LegacyTextLocalizer.setResolvedLocale(const Locale('ru'));
    expect(scheduledTask.getDisplayTimeText(), 'через 1 ч 5 мин');
  });

  test('formats countdown without an empty time component', () {
    final hoursOnly = task(
      type: ScheduledTaskType.countdown,
      countdownMinutes: 120,
    );
    final minutesOnly = task(
      type: ScheduledTaskType.countdown,
      countdownMinutes: 20,
    );

    LegacyTextLocalizer.setResolvedLocale(const Locale('ru'));
    expect(hoursOnly.getDisplayTimeText(), 'через 2 ч');
    expect(minutesOnly.getDisplayTimeText(), 'через 20 мин');
  });
}
