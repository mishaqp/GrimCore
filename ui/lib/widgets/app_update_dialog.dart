import 'package:ui/l10n/legacy_text_localizer.dart';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher_string.dart';
import 'package:ui/services/app_update_service.dart';
import 'package:ui/services/special_permission.dart';
import 'package:ui/theme/theme_context.dart';
import 'package:ui/utils/ui.dart';

Future<void> showAppUpdateDialog(
  BuildContext context,
  AppUpdateStatus status,
) async {
  final hasDirectInstall = status.canInstall;
  final isEnglish = Localizations.localeOf(context).languageCode == 'en';
  final palette = context.omniPalette;
  final confirmed = await AppDialog.confirm(
    context,
    title: LegacyTextLocalizer.pickForEnglishFlag(
      isEnglish,
      'New version available',
      '发现新版本',
      ru: 'Доступна новая версия',
    ),
    cancelText: LegacyTextLocalizer.pickForEnglishFlag(
      isEnglish,
      'Later',
      '稍后',
      ru: 'Позже',
    ),
    confirmText: hasDirectInstall
        ? (LegacyTextLocalizer.pickForEnglishFlag(
            isEnglish,
            'Update now',
            '立即更新',
            ru: 'Обновить сейчас',
          ))
        : (LegacyTextLocalizer.pickForEnglishFlag(
            isEnglish,
            'Go to Release',
            '前往 Release',
            ru: 'Перейти к релизу',
          )),
    confirmButtonColor: context.isDarkTheme
        ? Color.lerp(palette.accentPrimary, palette.pageBackground, 0.42)!
        : palette.accentPrimary,
    content: _AppUpdateDialogContent(status: status),
    barrierDismissible: true,
    glassStyle: true,
  );

  if (confirmed != true || !context.mounted) {
    return;
  }

  if (!hasDirectInstall) {
    if (status.releaseUrl.isEmpty) {
      showToast(
        LegacyTextLocalizer.pickForEnglishFlag(
          isEnglish,
          'No available Release URL',
          '缺少可用的 Release 地址',
          ru: 'Ссылка на релиз недоступна',
        ),
        type: ToastType.error,
      );
      return;
    }
    final launched = await launchUrlString(
      status.releaseUrl,
      mode: LaunchMode.externalApplication,
    );
    if (!launched) {
      showToast(
        LegacyTextLocalizer.pickForEnglishFlag(
          isEnglish,
          'Failed to open Release page',
          '打开 Release 页面失败',
          ru: 'Не удалось открыть страницу релиза',
        ),
        type: ToastType.error,
      );
    }
    return;
  }

  try {
    final notificationGranted = await ensureNotificationPermission();
    if (!notificationGranted) {
      showToast(
        LegacyTextLocalizer.pickForEnglishFlag(
          isEnglish,
          'Notification permission is not granted. Download will continue, but system download progress will not be shown.',
          '未授予通知权限，下载仍会继续，但不会显示系统下载进度',
          ru: 'Нет разрешения на уведомления. Загрузка продолжится, но системный индикатор прогресса отображаться не будет.',
        ),
        type: ToastType.warning,
      );
    }
    final result = await AppUpdateService.installLatestApk();
    final toastType = result.success ? ToastType.success : ToastType.warning;
    final message = result.message.isEmpty
        ? (LegacyTextLocalizer.pickForEnglishFlag(
            isEnglish,
            'Update installation failed',
            '更新安装失败',
            ru: 'Не удалось установить обновление',
          ))
        : result.message;
    showToast(message, type: toastType);
  } catch (_) {
    showToast(
      LegacyTextLocalizer.pickForEnglishFlag(
        isEnglish,
        'Failed to start update',
        '拉起更新失败',
        ru: 'Не удалось запустить обновление',
      ),
      type: ToastType.error,
    );
  }
}

class _AppUpdateDialogContent extends StatelessWidget {
  final AppUpdateStatus status;

  const _AppUpdateDialogContent({required this.status});

  @override
  Widget build(BuildContext context) {
    final palette = context.omniPalette;
    final isDark = context.isDarkTheme;
    final isEnglish = Localizations.localeOf(context).languageCode == 'en';
    final notesSurfaceColor = isDark
        ? palette.surfaceSecondary.withValues(alpha: 0.82)
        : const Color(0xFFF6F8FA);
    final notesBorderColor = isDark
        ? palette.borderSubtle.withValues(alpha: 0.72)
        : const Color(0xFFE6EDF5);
    final publishedAt = status.publishedAt > 0
        ? DateTime.fromMillisecondsSinceEpoch(status.publishedAt)
        : null;
    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _InfoRow(
          label: LegacyTextLocalizer.pickForEnglishFlag(
            isEnglish,
            'Current version',
            '当前版本',
            ru: 'Текущая версия',
          ),
          value: status.currentVersionLabel,
        ),
        const SizedBox(height: 8),
        _InfoRow(
          label: LegacyTextLocalizer.pickForEnglishFlag(
            isEnglish,
            'Latest version',
            '最新版本',
            ru: 'Последняя версия',
          ),
          value: status.latestVersionLabel,
        ),
        if (publishedAt != null) ...[
          const SizedBox(height: 8),
          _InfoRow(
            label: LegacyTextLocalizer.pickForEnglishFlag(
              isEnglish,
              'Published at',
              '发布时间',
              ru: 'Дата публикации',
            ),
            value:
                '${publishedAt.year.toString().padLeft(4, '0')}-${publishedAt.month.toString().padLeft(2, '0')}-${publishedAt.day.toString().padLeft(2, '0')}',
          ),
        ],
        if (status.releaseNotes.isNotEmpty) ...[
          const SizedBox(height: 12),
          Text(
            LegacyTextLocalizer.pickForEnglishFlag(
              isEnglish,
              'Release notes',
              '更新说明',
              ru: 'Что нового',
            ),
            style: TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w600,
              color: palette.textPrimary,
            ),
          ),
          const SizedBox(height: 6),
          Container(
            constraints: const BoxConstraints(maxHeight: 140),
            width: double.infinity,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: notesSurfaceColor,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: notesBorderColor),
            ),
            child: SingleChildScrollView(
              child: Text(
                status.releaseNotes,
                style: TextStyle(
                  fontSize: 12,
                  height: 1.6,
                  color: palette.textSecondary,
                ),
              ),
            ),
          ),
        ],
      ],
    );
  }
}

class _InfoRow extends StatelessWidget {
  final String label;
  final String value;

  const _InfoRow({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    final palette = context.omniPalette;
    final labelColor = context.isDarkTheme
        ? palette.textTertiary
        : const Color(0xFF5F6F89);
    return Row(
      children: [
        SizedBox(
          width: 68,
          child: Text(
            label,
            style: TextStyle(
              fontSize: 12,
              color: labelColor,
              fontWeight: FontWeight.w500,
            ),
          ),
        ),
        Expanded(
          child: Text(
            value,
            style: TextStyle(
              fontSize: 13,
              color: palette.textPrimary,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ],
    );
  }
}
