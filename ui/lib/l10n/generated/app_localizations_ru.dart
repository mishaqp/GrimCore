// ignore: unused_import
import 'package:intl/intl.dart' as intl;

import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for Russian (`ru`).
class AppLocalizationsRu extends AppLocalizations {
  AppLocalizationsRu([String locale = 'ru']) : super(locale);

  @override
  String get memoryShortRetention =>
      'Краткосрочные записи хранятся на этом устройстве без автоудаления. Долгое нажатие удаляет запись, можно выбрать несколько.';

  @override
  String get memoryShortDeleteConfirm => 'Удалить краткосрочные записи?';

  @override
  String get memoryShortDeleteScope =>
      'Безвозвратно удаляются только выбранные краткосрочные записи и их поисковый индекс. История чата, исходные заметки, извлечённая долгосрочная память и контекст текущего диалога сохраняются.';

  @override
  String get memoryShortDeleteFailed =>
      'Удаление не выполнено. Список обновлён — выберите записи заново и повторите.';

  @override
  String get memoryShortDeleted => 'Краткосрочные записи удалены';

  @override
  String get appName => 'GrimCore';

  @override
  String get brandName => 'GrimCore';

  @override
  String get brandNameEnglish => 'GrimCore';

  @override
  String get commonLoading => 'Загрузка';

  @override
  String get homeDrawerSearchHint => 'Поиск';

  @override
  String get homeDrawerClearSearch => 'Очистить поиск';

  @override
  String get themeModeTitle => 'Тема';

  @override
  String get themeModeSubtitle =>
      'Переключение между светлым, тёмным и системным оформлением';

  @override
  String get themeModeLight => 'Светлая';

  @override
  String get themeModeDark => 'Тёмная';

  @override
  String get themeModeSystem => 'Системная';

  @override
  String get languageTitle => 'Язык';

  @override
  String get languageSubtitle =>
      'Язык интерфейса, промптов агента и текстов инструментов';

  @override
  String get languageFollowSystem => 'Системный';

  @override
  String get languageZhHans => '简体中文';

  @override
  String get languageEnglish => 'English';

  @override
  String get languageRussian => 'Русский';

  @override
  String get settingsTitle => 'Настройки';

  @override
  String get settingsSectionModelMemory => 'Модели и память';

  @override
  String get settingsSectionServiceEnvironment => 'Сервисы и окружение';

  @override
  String get settingsSectionExperienceAppearance => 'Интерфейс и оформление';

  @override
  String get settingsSectionPermissionInfo => 'Разрешения и информация';

  @override
  String get settingsModelProviderTitle => 'Провайдеры моделей';

  @override
  String get settingsModelProviderSubtitle =>
      'Настройка адресов, ключей API и списков моделей';

  @override
  String get settingsSceneModelTitle => 'Модели по сценам';

  @override
  String get settingsSceneModelSubtitle =>
      'Привязка моделей к сценам; для непривязанных используется модель по умолчанию';

  @override
  String get settingsWorkspaceMemoryTitle => 'Память рабочего пространства';

  @override
  String get settingsWorkspaceMemoryLoading => 'Загрузка…';

  @override
  String get settingsWorkspaceMemoryEnabled =>
      'Память рабочего пространства включена (доступен поиск по эмбеддингам)';

  @override
  String get settingsWorkspaceMemoryLexical =>
      'Использовать память рабочего пространства (сейчас лексический поиск)';

  @override
  String get settingsMcpToolsTitle => 'Инструменты MCP';

  @override
  String get settingsMcpToolsSubtitle =>
      'Добавление, включение и управление удалёнными MCP-сервисами';

  @override
  String get settingsLocalServiceTitle => 'Локальный сервис';

  @override
  String get settingsLocalServiceSubtitle =>
      'Доступ к MCP и WebChat GrimCore в локальной сети';

  @override
  String get settingsAlpineTitle => 'Терминальное окружение';

  @override
  String get settingsAlpineSubtitle =>
      'Выбор и управление встроенной системой Alpine или Ubuntu';

  @override
  String get settingsHideRecentsTitle => 'Скрыть из недавних';

  @override
  String get settingsHideRecentsSubtitle =>
      'Скрывать приложение в списке недавних задач';

  @override
  String get settingsRecentConversationsOnlyTitle =>
      'Показывать только диалоги за 7 дней';

  @override
  String get settingsRecentConversationsOnlySubtitle =>
      'Автоматически архивировать диалоги без обновлений более 7 дней, чтобы ускорить боковую панель';

  @override
  String get settingsAlarmTitle => 'Настройки будильника';

  @override
  String get settingsAlarmSubtitle =>
      'Рингтон по умолчанию, локальный mp3 или ссылка на mp3';

  @override
  String get settingsAppearanceTitle => 'Оформление';

  @override
  String get settingsAppearanceSubtitle =>
      'Тема, язык, общий фон, размер текста чата и цвет текста';

  @override
  String get settingsVibrationTitle => 'Виброотклик';

  @override
  String get settingsVibrationSubtitle =>
      'Вибрация как сигнал о ходе выполнения задачи';

  @override
  String get settingsIndependentSendButtonTitle => 'Отдельная кнопка отправки';

  @override
  String get settingsIndependentSendButtonSubtitle =>
      'Если включено, Enter переносит строку; если выключено, Enter отправляет сообщение';

  @override
  String get settingsPredictiveBackTitle => 'Жест «назад» с предпросмотром';

  @override
  String get settingsPredictiveBackSubtitle =>
      'Если включено, жест назад следует за пальцем и показывает предыдущий экран; если выключено, используется обычное поведение';

  @override
  String get settingsHabitualHandTitle => 'Ведущая рука';

  @override
  String get settingsHabitualHandSubtitle =>
      'Меняет направление смахивания для меню истории чата';

  @override
  String get settingsHabitualHandLeft => 'Левая';

  @override
  String get settingsHabitualHandRight => 'Правая';

  @override
  String get settingsAboutTitle => 'О GrimCore';

  @override
  String get settingsHideRecentsFailed =>
      'Не удалось изменить скрытие из недавних';

  @override
  String get settingsSaveFailed => 'Не удалось сохранить настройки';

  @override
  String settingsMcpEnabledToast(Object endpoint) {
    return 'MCP включён: $endpoint';
  }

  @override
  String get settingsMcpDisabledToast => 'MCP выключен';

  @override
  String get settingsMcpToggleFailed => 'Не удалось переключить MCP';

  @override
  String get settingsCopiedAddress => 'Адрес скопирован';

  @override
  String get settingsCopiedToken => 'Токен скопирован';

  @override
  String get settingsTokenRefreshed => 'Токен обновлён';

  @override
  String get settingsTokenRefreshFailed => 'Не удалось обновить токен';

  @override
  String get settingsMcpLocalService => 'Локальный сервис';

  @override
  String get settingsMcpAddress => 'Адрес';

  @override
  String get settingsMcpToken => 'Токен';

  @override
  String get settingsNotGenerated => 'Не сгенерирован';

  @override
  String get settingsCopyAddress => 'Скопировать адрес';

  @override
  String get settingsCopyToken => 'Скопировать токен';

  @override
  String get settingsRefreshToken => 'Обновить токен';

  @override
  String get settingsMcpSecurityNotice =>
      'Используйте локальный MCP-сервис в той же сети с заголовком Authorization: Bearer <Token> и не публикуйте адрес и токен в интернете.';

  @override
  String get settingsInstalledAppsPermissionFailed =>
      'Не удалось запросить доступ к списку приложений';

  @override
  String get appearanceTitle => 'Оформление';

  @override
  String get appearanceAutoSaving => 'Сохранение изменений…';

  @override
  String get appearanceAutosaveHint => 'Изменения сохраняются автоматически';

  @override
  String get appearanceBackgroundSource => 'Источник фона';

  @override
  String get appearancePreview => 'Предпросмотр';

  @override
  String get appearanceAdjustments => 'Настройки';

  @override
  String get appearancePreviewChat => 'Чат';

  @override
  String get appearancePreviewWorkspace => 'Рабочее пространство';

  @override
  String get appearanceEnableBackground => 'Включить фоновое изображение';

  @override
  String get appearanceEnableBackgroundSubtitle =>
      'Применяется к чату и рабочему пространству, сохраняется автоматически';

  @override
  String get appearanceSourceLocal => 'Локальное изображение';

  @override
  String get appearanceSourceRemote => 'Ссылка на изображение';

  @override
  String get appearanceNoLocalImage => 'Локальное изображение ещё не выбрано';

  @override
  String get appearancePickImage => 'Выбрать изображение';

  @override
  String get appearanceRepickImage => 'Выбрать другое';

  @override
  String get appearanceRemoteImageUrl => 'Ссылка на изображение';

  @override
  String get appearanceRemoteImageUrlHint =>
      'https://example.com/background.jpg';

  @override
  String get appearanceBackgroundBlur => 'Размытие фона';

  @override
  String get appearanceBackgroundBlurSubtitle =>
      'Размытие слоя поверх изображения';

  @override
  String get appearanceOverlayIntensity => 'Плотность слоя';

  @override
  String get appearanceOverlayIntensitySubtitle =>
      'Увеличьте плотность затемнения, чтобы элементы интерфейса читались лучше';

  @override
  String get appearanceOverlayBrightness => 'Яркость слоя';

  @override
  String get appearanceOverlayBrightnessSubtitle =>
      'Осветлить или затемнить слой, не изменяя само изображение';

  @override
  String get appearanceChatTextSize => 'Размер текста в чате';

  @override
  String get appearanceChatTextSizeSubtitle =>
      'Влияет только на ваши сообщения, ответы ИИ и панель рассуждений';

  @override
  String get appearanceTextColorTitle => 'Цвет текста в чате';

  @override
  String get appearanceTextColorSubtitle =>
      'По умолчанию подстраивается под фон, можно закрепить свой цвет';

  @override
  String get appearanceTextColorAuto => 'Авто';

  @override
  String get appearanceCustomColorLabel => 'Свой цвет';

  @override
  String get appearanceCustomColorHint => '#FFFFFF или #FF112233';

  @override
  String get appearancePreviewTip =>
      'Изображение в предпросмотре можно перетаскивать и масштабировать щипком. Предпросмотр близок к реальному результату.';

  @override
  String get appearanceColorWhite => 'Белый';

  @override
  String get appearanceColorDarkGray => 'Тёмно-серый';

  @override
  String get appearanceColorLightBlue => 'Светло-синий';

  @override
  String get appearanceColorNavy => 'Тёмно-синий';

  @override
  String get appearanceColorTeal => 'Бирюзовый';

  @override
  String get appearanceColorWarmYellow => 'Тёплый жёлтый';

  @override
  String get appearanceInvalidHttpUrl =>
      'Введите корректную ссылку http(s) на изображение';

  @override
  String get appearanceInvalidHexColor => 'Введите #RRGGBB или #AARRGGBB';

  @override
  String get appearanceInvalidHexColorFormat => 'Неверный код цвета';

  @override
  String appearancePickImageFailed(Object error) {
    return 'Не удалось выбрать изображение: $error';
  }

  @override
  String get appearancePickLocalImageFirst =>
      'Сначала выберите локальное изображение';

  @override
  String get appearanceLocalImageMissing =>
      'Локальное изображение больше не существует. Выберите его заново';

  @override
  String appearanceAutosaveFailed(Object error) {
    return 'Ошибка автосохранения: $error';
  }

  @override
  String get chatToolCalling => 'Вызов инструмента';

  @override
  String get chatFallbackReply =>
      'Сейчас не удаётся сформировать ответ. Попробуйте ещё раз.';

  @override
  String get chatPermissionRequired =>
      'Перед выполнением задач нужно выдать разрешения';

  @override
  String chatPermissionRequiredWithNames(Object names) {
    return 'Выдайте эти разрешения перед выполнением задач: $names';
  }

  @override
  String get chatRecentTerminalOutputNotice =>
      '[Показан только последний вывод терминала]\n';

  @override
  String chatUserPrefix(Object text) {
    return 'Пользователь: $text\n';
  }

  @override
  String get permissionOverlay => 'Поверх других окон';

  @override
  String get permissionInstalledApps => 'Доступ к списку приложений';

  @override
  String get permissionPublicStorage => 'Доступ к общему хранилищу';

  @override
  String get browserOverlayTitle => 'Браузер агента';

  @override
  String get browserOverlayClose => 'Закрыть окно браузера';

  @override
  String get browserOverlayUnsupported =>
      'Просмотр инструмента браузера пока не поддерживается на этой платформе';

  @override
  String get networkErrorMessage =>
      'Сеть сейчас подвела. Попробуйте отправить ещё раз.';

  @override
  String get rateLimitErrorMessage =>
      'GrimCore сейчас занят. Попробуйте чуть позже.';

  @override
  String get chatHistoryArchivedTitle => 'Архив диалогов';

  @override
  String get chatHistoryTitle => 'История чатов';

  @override
  String get chatHistoryNoArchived => 'В архиве пусто';

  @override
  String get chatHistoryEmpty => 'Диалогов пока нет';

  @override
  String get chatHistoryArchivedToast => 'В архиве';

  @override
  String get chatHistoryUnarchivedToast => 'Возвращено из архива';

  @override
  String get chatHistoryArchiveFailed => 'Не удалось архивировать диалог';

  @override
  String get chatHistoryUnarchiveFailed => 'Не удалось вернуть диалог';

  @override
  String get chatHistoryArchiveHint =>
      'Смахните диалог влево, чтобы архивировать';

  @override
  String get homeDrawerArchive => 'Архив';

  @override
  String get homeDrawerNewChat => 'Новый диалог';

  @override
  String get webchatNoChats => 'Начать новый диалог';

  @override
  String get memoryCenterTitle => 'Центр памяти';

  @override
  String get memoryShortTermTitle => 'Краткосрочная память';

  @override
  String get memoryLongTermTitle => 'Долгосрочная память';

  @override
  String get memoryNoShortTerm => 'Краткосрочной памяти пока нет';

  @override
  String get memoryNoShortTermDesc =>
      'Информация из диалогов оседает в краткосрочной памяти и позже упорядочивается в долгосрочную.';

  @override
  String get memoryFilteredNoShortTerm =>
      'По текущему фильтру краткосрочных записей нет';

  @override
  String get memoryFilteredNoShortTermDesc =>
      'Загляните позже — новые записи появятся постепенно.';

  @override
  String get memoryNoLongTerm => 'Долгосрочная память ещё не инициализирована';

  @override
  String get memoryNoLongTermDesc =>
      'Когда память включена, ваши долгосрочные записи между сессиями накапливаются здесь.';

  @override
  String get memoryDeleteConfirmTitle => 'Точно удалить?';

  @override
  String get memoryDeleteWarning => 'Это действие нельзя отменить';

  @override
  String get memoryEditDisabled =>
      'Редактирование краткосрочной памяти не поддерживается';

  @override
  String get memoryDeleteDisabled =>
      'Удаление краткосрочной памяти не поддерживается';

  @override
  String get memoryGreeting => 'Привет,\nздесь мы сохраняем ваши воспоминания.';

  @override
  String memorySelectedCount(Object n) {
    return 'Выбрано: $n';
  }

  @override
  String get memoryDeselectAll => 'Снять выделение';

  @override
  String get memoryEditTitle => 'Изменить запись';

  @override
  String get memoryIdLabel => 'ID записи';

  @override
  String get memoryMatchScore => 'Релевантность';

  @override
  String get memoryAdditionalInfo => 'Дополнительно';

  @override
  String get memoryAddLongTerm => 'Добавить долгосрочную запись';

  @override
  String get memorySaveToLongTerm => 'Сохранить в долгосрочную память';

  @override
  String get memoryLongTermAdded => 'Долгосрочная запись добавлена';

  @override
  String get memoryEditLongTerm => 'Изменить долгосрочную запись';

  @override
  String get memorySaveChanges => 'Сохранить изменения';

  @override
  String get memoryDeleteLongTermConfirm => 'Удалить эту долгосрочную запись?';

  @override
  String get memoryLongTermDeleted => 'Долгосрочная запись удалена';

  @override
  String memoryLongTermFailed(Object error) {
    return 'Ошибка операции с долгосрочной памятью: $error';
  }

  @override
  String get memoryNoMemories => 'Записей нет';

  @override
  String get memoryNoMemoriesDesc =>
      'Начните исследовать и добавляйте то, что нравится';

  @override
  String get pluginMarketTitle => 'Магазин плагинов';

  @override
  String get pluginMarketEmpty => 'Плагинов нет';

  @override
  String get pluginMarketEmptyDesc =>
      'Официальные плагины появятся здесь после подключения';

  @override
  String get pluginInstall => 'Установить';

  @override
  String get pluginUpdate => 'Обновить';

  @override
  String get pluginUninstall => 'Удалить';

  @override
  String get pluginCancel => 'Отмена';

  @override
  String get pluginNoDescription => 'Без описания';

  @override
  String get pluginIncompatible => 'Этот плагин несовместим с текущей версией';

  @override
  String get pluginLoadFailed => 'Не удалось загрузить магазин плагинов';

  @override
  String get pluginInstallFailed => 'Не удалось установить плагин';

  @override
  String get pluginUpdateFailed => 'Не удалось обновить плагин';

  @override
  String get pluginToggleFailed => 'Не удалось переключить плагин';

  @override
  String get pluginUninstallFailed => 'Не удалось удалить плагин';

  @override
  String get pluginUninstallTitle => 'Удаление плагина';

  @override
  String pluginUninstallConfirmMsg(Object name) {
    return 'Удалить «$name»?';
  }

  @override
  String pluginInstalledMsg(Object name) {
    return 'Установлено: $name';
  }

  @override
  String pluginUpdatedMsg(Object name) {
    return 'Обновлено: $name';
  }

  @override
  String pluginEnabledMsg(Object name) {
    return 'Включено: $name';
  }

  @override
  String pluginDisabledMsg(Object name) {
    return 'Выключено: $name';
  }

  @override
  String pluginUninstalledMsg(Object name) {
    return 'Удалено: $name';
  }

  @override
  String get pluginKindBundledModule => 'Встроенный модуль';

  @override
  String get pluginKindRuntimeBundle => 'Загружаемый пакет';

  @override
  String get pluginKindCompanionApp => 'Приложение-компаньон';

  @override
  String get pluginDetailTitle => 'О плагине';

  @override
  String get pluginSearchHint => 'Поиск плагинов, описаний, возможностей';

  @override
  String get pluginSearchEmpty => 'Подходящих плагинов нет';

  @override
  String get pluginAboutTitle => 'Описание';

  @override
  String get pluginCapabilitiesTitle => 'Возможности';

  @override
  String get pluginNoCapabilities =>
      'Плагин не объявляет дополнительных возможностей';

  @override
  String get pluginInformationTitle => 'Информация';

  @override
  String get pluginPublisherLabel => 'Разработчик';

  @override
  String get pluginVersionLabel => 'Версия';

  @override
  String get pluginTypeLabel => 'Тип';

  @override
  String get pluginDownloadSizeLabel => 'Размер загрузки';

  @override
  String get pluginInterfaceVersionLabel => 'Версия интерфейса';

  @override
  String get pluginStatusInstalled => 'Установлен';

  @override
  String get pluginStatusEnabled => 'Включён';

  @override
  String get pluginStatusNotInstalled => 'Не установлен';

  @override
  String get pluginEnableTitle => 'Включить плагин';

  @override
  String get pluginEnableDescription =>
      'Разрешить агенту использовать возможности этого плагина';

  @override
  String get pluginRetry => 'Повторить';

  @override
  String get skillStoreTitle => 'Магазин навыков';

  @override
  String get skillBuiltin => 'Встроенный';

  @override
  String get skillOfficial => 'Официальный';

  @override
  String get skillUser => 'Пользовательский';

  @override
  String get skillInstalled => 'Установлен';

  @override
  String get skillNotInstalled => 'Не установлен';

  @override
  String get skillEnabled => 'Включён';

  @override
  String get skillDisabled => 'Выключен';

  @override
  String get skillInstall => 'Установить';

  @override
  String get skillDelete => 'Удалить';

  @override
  String get skillEmpty => 'Навыков нет';

  @override
  String get skillNoDescription => 'Без описания';

  @override
  String get skillBuiltinRemovedDesc =>
      'Этот встроенный навык удалён из рабочего пространства. Его можно установить заново в любой момент.';

  @override
  String get skillDeleteTitle => 'Удаление навыка';

  @override
  String skillDeleteConfirmMsg(Object name) {
    return 'Удалить «$name»?';
  }

  @override
  String get skillDeleted => 'Удалено';

  @override
  String get skillDeleteFailed => 'Не удалось удалить';

  @override
  String skillInstalledMsg(Object name) {
    return 'Установлено: $name';
  }

  @override
  String get skillInstallFailed => 'Не удалось установить';

  @override
  String skillEnabledMsg(Object name) {
    return 'Включено: $name';
  }

  @override
  String skillDisabledMsg(Object name) {
    return 'Выключено: $name';
  }

  @override
  String get skillToggleFailed => 'Не удалось переключить';

  @override
  String get skillSyncOfficialTooltip =>
      'Установить/обновить официальные навыки';

  @override
  String skillSyncOfficialSuccess(Object count) {
    return 'Официальные навыки синхронизированы ($count)';
  }

  @override
  String get skillSyncOfficialFailed =>
      'Не удалось синхронизировать официальные навыки';

  @override
  String get skillLoadFailed => 'Не удалось загрузить навыки';

  @override
  String get modelProviderConfigTitle => 'Настройка провайдера';

  @override
  String get modelProviderConfigDesc =>
      'Добавляйте и переключайте провайдеров, настраивайте их адреса и ключи.';

  @override
  String get modelProviderName => 'Название провайдера';

  @override
  String get modelProviderNameHint => 'например, DeepSeek';

  @override
  String get modelProviderBaseUrlHint =>
      'Добавьте # в конце, чтобы отключить автодополнение пути запроса';

  @override
  String get modelProviderApiKeyHint =>
      'Если ключ API не указан, запросы будут без авторизации.';

  @override
  String get modelListTitle => 'Список моделей';

  @override
  String get modelListDesc =>
      'Можно добавлять модели вручную или получать удалённый список моделей текущего провайдера.';

  @override
  String modelListCount(Object count) {
    return 'Всего моделей: $count';
  }

  @override
  String get modelAddPrompt => 'Добавьте модель!';

  @override
  String get modelBuiltinProvider => 'Встроенный провайдер';

  @override
  String get modelIdEmpty =>
      'ID модели не может быть пустым и не может начинаться с \'scene.\'';

  @override
  String get modelAlreadyExists => 'Такая модель уже есть';

  @override
  String get modelAdded => 'Модель добавлена';

  @override
  String get modelDeleted => 'Модель удалена';

  @override
  String get modelDeleteFailed => 'Не удалось удалить модель';

  @override
  String get modelIdHint => 'Введите ID модели';

  @override
  String get modelAddProviderTitle => 'Добавить провайдера';

  @override
  String get modelAddButton => 'Добавить';

  @override
  String get modelProviderAdded => 'Провайдер добавлен';

  @override
  String modelProviderAddFailed(Object error) {
    return 'Не удалось добавить провайдера: $error';
  }

  @override
  String get modelDeleteProviderTitle => 'Удаление провайдера';

  @override
  String modelDeleteProviderMsg(Object name) {
    return 'Удалить «$name»? Привязки сцен сохранятся, но потребуется выбрать доступного провайдера заново.';
  }

  @override
  String get modelProviderDeleted => 'Провайдер удалён';

  @override
  String modelProviderDeleteFailed(Object error) {
    return 'Не удалось удалить провайдера: $error';
  }

  @override
  String get modelProviderLoadFailed =>
      'Не удалось загрузить настройки провайдеров';

  @override
  String modelProviderSwitchFailed(Object error) {
    return 'Не удалось переключить провайдера: $error';
  }

  @override
  String get modelProviderBaseUrlRequired => 'Сначала укажите Base URL';

  @override
  String get modelProviderInvalidBaseUrl =>
      'Введите корректный http(s) Base URL';

  @override
  String modelProviderFetchedModels(Object count) {
    return 'Получено моделей: $count';
  }

  @override
  String modelProviderFetchFailed(Object error) {
    return 'Не удалось получить список моделей: $error';
  }

  @override
  String get sceneModelMapping => 'Привязка сцен';

  @override
  String get sceneModelMappingDesc =>
      'Привязка провайдеров и моделей к сценам. Для непривязанных сцен используется модель по умолчанию.';

  @override
  String get sceneModelRefreshList => 'Обновить список моделей';

  @override
  String get sceneModelSearchHint =>
      'Кнопка справа позволяет искать, сворачивать и выбирать модели по провайдерам; верхняя строка поиска остаётся на месте.';

  @override
  String get sceneModelNoScenes => 'Нет сцен для настройки';

  @override
  String get sceneModelLoadFailed =>
      'Не удалось загрузить настройки моделей по сценам';

  @override
  String sceneModelPartialUpdateFailed(Object profiles) {
    return 'Часть моделей обновлена, но у этих провайдеров ошибка: $profiles';
  }

  @override
  String sceneModelUpdatedModels(Object count) {
    return 'Обновлено моделей: $count';
  }

  @override
  String sceneModelRefreshFailed(Object error) {
    return 'Не удалось обновить список моделей: $error';
  }

  @override
  String get sceneModelInvalidModelId =>
      'ID модели не может начинаться с scene.';

  @override
  String sceneModelBoundToast(Object scene, Object model) {
    return '$scene теперь использует $model';
  }

  @override
  String sceneModelSaveFailed(Object scene, Object error) {
    return 'Не удалось сохранить $scene: $error';
  }

  @override
  String sceneModelBindingCleared(Object scene) {
    return 'Привязка для $scene снята';
  }

  @override
  String sceneModelDefaultRestored(Object scene) {
    return '$scene снова использует модель по умолчанию';
  }

  @override
  String sceneModelClearFailed(Object scene, Object error) {
    return 'Не удалось очистить $scene: $error';
  }

  @override
  String get modelsNoAvailableModels => 'Доступных моделей нет';

  @override
  String get alarmSaved => 'Настройки будильника сохранены';

  @override
  String get alarmRingtoneSource => 'Источник рингтона';

  @override
  String get alarmSystemDefault => 'Системный по умолчанию';

  @override
  String get alarmSystemDefaultDesc =>
      'Дополнительная настройка не нужна, лучшая совместимость';

  @override
  String get alarmLocalMp3 => 'Локальный MP3';

  @override
  String get alarmLocalMp3Desc =>
      'Выберите mp3-файл на телефоне как рингтон будильника';

  @override
  String get alarmMp3Url => 'Ссылка на MP3';

  @override
  String get alarmMp3UrlDesc => 'Воспроизведение онлайн-MP3 по ссылке HTTP(S)';

  @override
  String get alarmAudioPermissionDenied => 'Нет разрешения на чтение аудио';

  @override
  String get alarmInvalidFilePath => 'Неверный путь к файлу, выберите заново';

  @override
  String get alarmSelectLocalFirst => 'Сначала выберите локальный mp3-файл';

  @override
  String get alarmEnterHttpsUrl => 'Введите ссылку HTTP(S) на MP3';

  @override
  String get alarmLocalFile => 'Локальный файл';

  @override
  String get alarmSelectMp3 => 'Выбрать mp3-файл';

  @override
  String get authorizePageTitle => 'Разрешения приложения';

  @override
  String get authorizeReceiveNotifications =>
      'Получать уведомления о сообщениях';

  @override
  String get authorizeNotificationsDesc =>
      'Включите, чтобы вовремя получать сведения о ходе задач';

  @override
  String get storageUsageTitle => 'Использование памяти';

  @override
  String get storageUsageSubtitle =>
      'Подробности использования памяти и очистка по категориям';

  @override
  String get storageAnalyzeFailed =>
      'Не удалось проанализировать память, попробуйте ещё раз';

  @override
  String storageCategoryCleaned(Object name, Object size) {
    return 'Очищено «$name», освобождено $size';
  }

  @override
  String get storageCleanFailed => 'Очистка не удалась, попробуйте позже';

  @override
  String storageCleanCategory(Object name) {
    return 'Очистить «$name»';
  }

  @override
  String get storageCleanConfirmMsg => 'Подтвердить очистку этой категории?';

  @override
  String get storageCleanScope => 'Область очистки';

  @override
  String get storageCleanAll => 'Всё';

  @override
  String get storageClean7Days => 'Старше 7 дней';

  @override
  String get storageClean30Days => 'Старше 30 дней';

  @override
  String storageStrategyName(Object name) {
    return 'Стратегия: $name';
  }

  @override
  String storageStrategyDone(Object size) {
    return 'Стратегия выполнена, освобождено $size';
  }

  @override
  String storageStrategyPartialDone(Object count, Object size) {
    return 'Очистка завершена: освобождено $size, не удалось очистить элементов: $count.';
  }

  @override
  String get storageStrategyFailed =>
      'Стратегия не выполнена, попробуйте позже';

  @override
  String get storageLoadFailed => 'Не удалось загрузить';

  @override
  String get storageReanalyze => 'Проанализировать снова';

  @override
  String get storageTotalUsage => 'Всего занято';

  @override
  String get storageAppSize => 'Размер приложения';

  @override
  String get storageUserData => 'Данные пользователя';

  @override
  String get storageCleanable => 'Можно очистить';

  @override
  String storageStatsSource(Object source) {
    return 'Источник статистики: $source';
  }

  @override
  String storagePackageName(Object name) {
    return 'Текущий пакет: $name';
  }

  @override
  String get storageTrendFirst =>
      'Это первый анализ. Тренды использования появятся в следующих анализах.';

  @override
  String get storageSmartCleanup => 'Умная очистка';

  @override
  String get storageExecute => 'Выполнить';

  @override
  String get storageUsageAnalysis => 'Анализ использования';

  @override
  String get storageClean => 'Очистить';

  @override
  String get storageRiskLow => 'Низкий риск';

  @override
  String get storageRiskCaution => 'Осторожно';

  @override
  String get storageRiskHigh => 'Высокий риск';

  @override
  String get storageReadOnly => 'Только чтение';

  @override
  String get storageSystemStats =>
      'Системная статистика (ближе к настройкам системы)';

  @override
  String get storageDirectoryScan => 'Оценка по сканированию каталогов';

  @override
  String get storageAdditionalInfo => 'Дополнительно';

  @override
  String get storageCatAppBinary => 'Бинарные файлы приложения';

  @override
  String get storageCatAppBinaryDesc =>
      'Файлы установленного приложения (APK/AAB split)';

  @override
  String get storageCatCache => 'Кэш';

  @override
  String get storageCatCacheDesc =>
      'Временные файлы и кэш изображений, безопасно очищать';

  @override
  String get storageCatCacheHint =>
      'После очистки кэш создастся заново по мере работы';

  @override
  String get storageCatConversation => 'История диалогов';

  @override
  String get storageCatConversationDesc =>
      'История чатов и выполнения инструментов (оценка)';

  @override
  String get storageCatConversationHint =>
      'Будут удалены записи сообщений без возможности восстановления';

  @override
  String get storageCatDatabaseOther => 'Прочие базы данных';

  @override
  String get storageCatDatabaseOtherDesc => 'Индексы и системные таблицы';

  @override
  String get storageCatWorkspaceBrowser => 'Артефакты браузера';

  @override
  String get storageCatWorkspaceBrowserDesc =>
      'Снимки экрана браузера, загрузки и промежуточные файлы';

  @override
  String get storageCatWorkspaceBrowserHint =>
      'Будут удалены промежуточные файлы инструмента браузера';

  @override
  String get storageCatWorkspaceOffloads => 'Выгрузки рабочего пространства';

  @override
  String get storageCatWorkspaceOffloadsDesc =>
      'Офлайн-вывод инструментов и временные файлы';

  @override
  String get storageCatWorkspaceOffloadsHint =>
      'Удаляются только офлайн-артефакты, основная функциональность не затрагивается';

  @override
  String get storageCatWorkspaceAttachments => 'Вложения рабочего пространства';

  @override
  String get storageCatWorkspaceAttachmentsDesc =>
      'Файлы вложений, использованные в прошлых задачах';

  @override
  String get storageCatWorkspaceAttachmentsHint =>
      'Может повлиять на просмотр вложений в прошлых задачах';

  @override
  String get storageCatWorkspaceShared => 'Общие файлы пространства';

  @override
  String get storageCatWorkspaceSharedDesc =>
      'Файлы рабочего пространства, общие для задач';

  @override
  String get storageCatWorkspaceSharedHint =>
      'Может повлиять на повторное использование общих файлов';

  @override
  String get storageCatWorkspaceMemory => 'Данные памяти пространства';

  @override
  String get storageCatWorkspaceMemoryDesc =>
      'Данные долгосрочной и краткосрочной памяти, а также поисковый индекс';

  @override
  String get storageCatWorkspaceUserFiles =>
      'Пользовательские файлы пространства';

  @override
  String get storageCatWorkspaceUserFilesDesc =>
      'Файлы, сохранённые пользователем в рабочее пространство';

  @override
  String get storageCatTerminalLocal => 'Среда терминала (локальная)';

  @override
  String get storageCatTerminalLocalDesc =>
      'Локальный каталог среды терминала Alpine/Ubuntu';

  @override
  String get storageCatTerminalLocalHint =>
      'Каталог терминала будет удалён, потребуется повторная инициализация';

  @override
  String get storageCatTerminalBootstrap => 'Среда терминала (bootstrap)';

  @override
  String get storageCatTerminalBootstrapDesc =>
      'Загрузочные файлы proot/lib/rootfs';

  @override
  String get storageCatTerminalBootstrapHint =>
      'Загрузочные файлы терминала будут удалены, потребуется повторная инициализация';

  @override
  String get storageCatSharedDrafts => 'Общие черновики';

  @override
  String get storageCatSharedDraftsDesc =>
      'Кэш черновиков, созданных через системное меню «Поделиться»';

  @override
  String get storageCatSharedDraftsHint =>
      'Неотправленные вложения черновиков будут удалены';

  @override
  String get storageCatMcpInbox => 'Входящие MCP';

  @override
  String get storageCatMcpInboxDesc => 'Каталог приёма файлов MCP';

  @override
  String get storageCatMcpInboxHint => 'Файлы во входящих MCP будут удалены';

  @override
  String get storageCatLegacyWorkspace => 'Устаревшие данные';

  @override
  String get storageCatLegacyWorkspaceDesc =>
      'Старые каталоги рабочего пространства, оставшиеся после обновления';

  @override
  String get storageCatLegacyWorkspaceHint =>
      'Перед очисткой убедитесь, что они больше не нужны';

  @override
  String get storageCatOtherUserData => 'Прочие данные';

  @override
  String get storageCatOtherUserDataDesc =>
      'Данные, не подходящие ни под одну категорию';

  @override
  String get storageStrategySafeQuick => 'Безопасная быстрая очистка';

  @override
  String get storageStrategySafeQuickDesc =>
      'Сначала очищаются кэш и временные артефакты с низким риском';

  @override
  String get storageStrategyBalanceDeep => 'Сбалансированная глубокая очистка';

  @override
  String get storageStrategyBalanceDeepDesc =>
      'Освобождает больше места, сохраняя основные данные и файлы';

  @override
  String get storageStrategyFree1gb => 'Цель — освободить 1 ГБ';

  @override
  String get storageStrategyFree1gbDesc =>
      'Сначала удаляются данные, которые освобождают больше места; цель — 1 ГБ.';

  @override
  String get storageHintConversation =>
      'Если занятое историей место не освободилось, вернитесь на страницу и нажмите «Проанализировать снова».';

  @override
  String get storageHintTerminal =>
      'После очистки среды терминала её можно инициализировать заново на странице «Терминальное окружение»';

  @override
  String get storageHintGeneral =>
      'Если очистка не удалась, попробуйте позже или перезапустите приложение';

  @override
  String get storageHintNotCleanable => 'Эту категорию сейчас нельзя очистить';

  @override
  String get storageHintSkipped => 'Категория пропущена (необязательно)';

  @override
  String storageCleanPartialFailed(Object hint) {
    return 'Часть очистки не удалась: $hint';
  }

  @override
  String get storageCleanPartialFailedGeneric =>
      'Некоторые файлы не удалось очистить, попробуйте позже';

  @override
  String storageTrendVsLast(Object cleanable, Object total) {
    return 'К прошлому анализу: всего $total, можно очистить $cleanable';
  }

  @override
  String storageLastAnalyzed(Object time) {
    return 'Последний анализ: $time';
  }

  @override
  String get aboutDescription =>
      'GrimCore — приложение-ассистент с ИИ, построенное вокруг\nинтеллектуального диалога: семантическое понимание\nи постоянное обучение помогают обрабатывать информацию,\nподдерживать решения и вести повседневные дела.';

  @override
  String get aboutBetaProgramTitle => 'Участвовать в бета-тестировании';

  @override
  String get aboutBetaProgramDescription =>
      'Раньше получать бета-версии с четырёхкомпонентным номером.';

  @override
  String get aboutBetaProgramToggleFailed =>
      'Не удалось изменить настройку бета-тестирования';

  @override
  String get aboutPreferencesSectionTitle => 'Обновления и тестирование';

  @override
  String get aboutUpdateHintDefault =>
      'Проверьте обновления, чтобы получить последнюю версию';

  @override
  String get workspaceMemoryLoadFailed =>
      'Не удалось загрузить настройки памяти рабочего пространства';

  @override
  String get agentSoulSaved => 'Настройка «души» агента сохранена';

  @override
  String get agentSoulSaveFailed =>
      'Не удалось сохранить настройку «души» агента';

  @override
  String get chatPromptSaved => 'Системный промпт только для чата сохранён';

  @override
  String get chatPromptSaveFailed =>
      'Не удалось сохранить системный промпт чата';

  @override
  String get workspaceMemorySaved => 'MEMORY.md сохранён';

  @override
  String get workspaceMemorySaveFailed => 'Не удалось сохранить MEMORY.md';

  @override
  String get workspaceEmbeddingToggleFailed =>
      'Не удалось изменить переключатель эмбеддингов памяти';

  @override
  String get workspaceRollupToggleFailed =>
      'Не удалось изменить настройку ночной консолидации памяти';

  @override
  String get workspaceRollupDone => 'Консолидация памяти завершена';

  @override
  String get workspaceRollupFailed => 'Не удалось консолидировать память';

  @override
  String get workspaceNone => 'Нет';

  @override
  String get workspaceMemoryTitle => 'Память рабочего пространства';

  @override
  String get workspaceMemoryCapability => 'Возможности памяти';

  @override
  String get workspaceEmbeddingReady => 'Настроено, доступен векторный поиск';

  @override
  String get workspaceEmbeddingNotReady =>
      'Не настроено, будет использован лексический поиск';

  @override
  String get workspaceGoToConfig =>
      'Перейдите в настройку моделей по сценам и задайте модель эмбеддингов';

  @override
  String get workspaceNightlyRollup => 'Ночная консолидация памяти (22:00)';

  @override
  String workspaceLastRun(Object time) {
    return 'Прошлый запуск: $time';
  }

  @override
  String workspaceNextRun(Object time) {
    return 'Следующий запуск: $time';
  }

  @override
  String get workspaceRollupNow => 'Консолидировать сейчас';

  @override
  String get workspaceSettingsAndMemory => 'Настройки агента и память';

  @override
  String get agentSoulSetting => 'Душа агента';

  @override
  String get chatPromptSetting => 'Системный промпт только для чата';

  @override
  String get workspaceMemoryMd => 'MEMORY.md (долгосрочная память)';

  @override
  String get alpineNodeJs => 'Среда Node.js';

  @override
  String get alpineNpm => 'Менеджер пакетов Node.js';

  @override
  String get alpineGit => 'Система контроля версий Git';

  @override
  String get alpinePython => 'Интерпретатор Python';

  @override
  String get alpinePip => 'Проекты и пакеты Python';

  @override
  String get alpinePipInstall => 'Установщик пакетов Python';

  @override
  String get alpineCodex => 'OpenAI Codex CLI для ACP-агентов';

  @override
  String get alpineClaudeCode => 'Anthropic Claude Code CLI для ACP-агентов';

  @override
  String get alpineOpenCode => 'OpenCode CLI со встроенной поддержкой ACP';

  @override
  String get alpineDeepSeekHarness =>
      'Официальная ACP-среда DeepSeek Harness (dsh)';

  @override
  String get alpineKimiCode =>
      'Официальный CLI Kimi Code и локальный веб-интерфейс';

  @override
  String get alpineSshClient => 'SSH-клиент';

  @override
  String get alpineSshpass => 'Помощник для паролей SSH';

  @override
  String get alpineOpenSshServer => 'Сервер OpenSSH';

  @override
  String get alpineDetectFailed => 'Не удалось определить среду терминала';

  @override
  String get alpineBootTasksLoadFailed =>
      'Не удалось загрузить задачи автозапуска';

  @override
  String get alpineConfigOpenFailed =>
      'Не удалось открыть настройку терминального окружения';

  @override
  String get alpineBootTaskAdded => 'Задача автозапуска добавлена';

  @override
  String get alpineBootTaskUpdated => 'Задача автозапуска обновлена';

  @override
  String get alpineBootTaskSaveFailed =>
      'Не удалось сохранить задачу автозапуска';

  @override
  String get alpineBootEnabled => 'Автозапуск при старте приложения включён';

  @override
  String get alpineBootDisabled => 'Автозапуск выключен';

  @override
  String get alpineBootTaskUpdateFailed => 'Не удалось обновить задачу';

  @override
  String get alpineDeleteBootTask => 'Удаление задачи автозапуска';

  @override
  String alpineDeleteBootTaskMsg(Object name) {
    return 'Удалить «$name»?';
  }

  @override
  String get alpineBootTaskDeleted => 'Задача автозапуска удалена';

  @override
  String get alpineBootTaskDeleteFailed => 'Не удалось удалить задачу';

  @override
  String get alpineCommandSent => 'Команда запуска отправлена';

  @override
  String get alpineStartFailed => 'Не удалось запустить задачу';

  @override
  String get alpineDetecting => 'Определение окружения';

  @override
  String alpineStartConfig(Object count) {
    return 'Конфигурация запуска (элементов: $count)';
  }

  @override
  String get alpineAllReady => 'Всё готово';

  @override
  String get alpineDetectingDesc =>
      'Определение версий типовых инструментов разработки в выбранной терминальной системе.';

  @override
  String alpineReadyCount(Object ready, Object total) {
    return 'Готово $ready из $total элементов в выбранной терминальной системе. Проверьте недостающие компоненты и настройте их автоматически в ReTerminal.';
  }

  @override
  String get alpineBootTasks => 'Задачи автозапуска';

  @override
  String get alpineBootTasksDesc =>
      'При запуске GrimCore включённые задачи проверяются в фоне, и команды запускаются в соответствующей сессии ReTerminal. Подходит для постоянных сервисов.';

  @override
  String get alpineAddTask => 'Добавить задачу';

  @override
  String get alpineOpenTerminal => 'Открыть терминал';

  @override
  String get alpineNoTasksDesc =>
      'Задач нет. Можно добавить постоянные команды вроде `python app.py`, `node server.js` или `./start.sh`.';

  @override
  String get alpineBootOnAppOpen => 'Запускать после открытия приложения';

  @override
  String get alpineNotEnabled => 'Не включено';

  @override
  String get alpineRunning => 'Выполняется';

  @override
  String get alpineStartNow => 'Запустить сейчас';

  @override
  String get alpineEdit => 'Изменить';

  @override
  String get alpineVersionDetected => 'Версия определена';

  @override
  String get alpineVersionNotFound => 'Не обнаружено';

  @override
  String get alpineTaskNameHint => 'Введите название задачи';

  @override
  String get alpineCommandHint => 'Введите команду запуска';

  @override
  String get alpineEditBootTask => 'Изменение задачи автозапуска';

  @override
  String get alpineAddBootTask => 'Новая задача автозапуска';

  @override
  String get alpineTaskName => 'Название задачи';

  @override
  String get alpineTaskNameExample => 'например, локальный API-сервис';

  @override
  String get alpineStartCommand => 'Команда запуска';

  @override
  String get alpineCommandExample => 'например, python app.py или pnpm start';

  @override
  String get alpineWorkDir => 'Рабочий каталог';

  @override
  String get alpineBootAutoStart => 'Автозапуск при открытии GrimCore';

  @override
  String get alpineDevEnv => 'Среда разработки';

  @override
  String get alpineAiAgent => 'ИИ-агент';

  @override
  String get alpineEnvConfig => 'Настройка окружения';

  @override
  String alpineWorkDirValue(Object dir) {
    return 'Рабочий каталог: $dir';
  }

  @override
  String get workspaceEmbeddingRetrieval => 'Поиск по эмбеддингам памяти';

  @override
  String get chatHistoryStartConversation => 'Начать диалог';

  @override
  String get homeDrawerSearching => 'Поиск диалогов…';

  @override
  String get homeDrawerNoResults => 'Подходящих диалогов не найдено';

  @override
  String get homeDrawerSearchHint2 =>
      'Попробуйте короткие ключевые слова или переформулируйте запрос';

  @override
  String get homeDrawerSearchResults => 'Результаты поиска';

  @override
  String get homeDrawerResultCount => 'рез.';

  @override
  String get homeDrawerScheduled => 'По расписанию';

  @override
  String get homeDrawerScheduledTasks => 'Запланированные задачи';

  @override
  String get homeDrawerPinnedConversations => 'Закреплённые диалоги';

  @override
  String get homeDrawerAgentSection => 'Агент';

  @override
  String get homeDrawerOmniAiSection => 'GrimCore';

  @override
  String get homeDrawerChatOnlySection => 'Только чат';

  @override
  String get homeDrawerAgentNoProject => 'Другое';

  @override
  String get homeDrawerGreeting => 'Привет!';

  @override
  String get homeDrawerWelcome => 'Добро пожаловать в GrimCore';

  @override
  String get homeDrawerDawnGreeting => 'Глубокая ночь';

  @override
  String get homeDrawerDawnSub => 'Ещё не спите?';

  @override
  String get homeDrawerDawnGreeting2 => 'Перед рассветом';

  @override
  String get homeDrawerDawnSub2 => 'Рано встали — берегите себя!';

  @override
  String get homeDrawerDawnGreeting3 => 'Тихая полночь';

  @override
  String get homeDrawerDawnSub3 => 'Не забудьте отдохнуть.';

  @override
  String get homeDrawerMorningGreeting => 'Доброе утро!';

  @override
  String get homeDrawerMorningSub => 'Начните день с энергией';

  @override
  String get homeDrawerMorningGreeting2 => 'Утро!';

  @override
  String get homeDrawerMorningSub2 => 'Новый день начался';

  @override
  String get homeDrawerForenoonGreeting => 'Доброе утро!';

  @override
  String get homeDrawerForenoonSub => 'Разомните плечи';

  @override
  String get homeDrawerForenoonGreeting2 => 'Отличный темп!';

  @override
  String get homeDrawerForenoonSub2 => 'Так держать';

  @override
  String get homeDrawerLunchGreeting => 'Обеденное время!';

  @override
  String get homeDrawerLunchSub => 'Поешьте как следует';

  @override
  String get homeDrawerLunchGreeting2 => 'Добрый день~';

  @override
  String get homeDrawerLunchSub2 => 'После обеда немного отдохните';

  @override
  String get homeDrawerLunchGreeting3 => 'Не знаете, что съесть?';

  @override
  String get homeDrawerLunchSub3 => 'GrimCore подскажет';

  @override
  String get homeDrawerAfternoonGreeting => 'Время чая';

  @override
  String get homeDrawerAfternoonSub => 'У вас всё получится!';

  @override
  String get homeDrawerAfternoonGreeting2 => 'Отведите взгляд';

  @override
  String get homeDrawerAfternoonSub2 => 'Дайте глазам отдохнуть';

  @override
  String get homeDrawerEveningGreeting => 'Спокойной дороги домой';

  @override
  String get homeDrawerEveningSub => 'Отдохните сегодня вечером';

  @override
  String get homeDrawerEveningGreeting2 => 'Вечерний ветер';

  @override
  String get homeDrawerEveningSub2 => 'Приятно, правда?';

  @override
  String get homeDrawerEveningGreeting3 => 'Долгий был день';

  @override
  String get homeDrawerEveningSub3 => 'Побалуйте себя хорошим ужином';

  @override
  String get homeDrawerNightGreeting => 'Добрый вечер!';

  @override
  String get homeDrawerNightSub => 'Посвятите время себе';

  @override
  String get homeDrawerNightGreeting2 => 'Ночь сгущается';

  @override
  String get homeDrawerNightSub2 => 'Ложитесь спать пораньше';

  @override
  String get homeDrawerNightGreeting3 => 'Пора отдохнуть';

  @override
  String get homeDrawerNightSub3 => 'GrimCore поставит будильник за вас';

  @override
  String get homeDrawerLateNightGreeting => 'Отложите телефон и ложитесь спать';

  @override
  String get homeDrawerLateNightSub => 'Наберитесь сил на завтра';

  @override
  String get homeDrawerLateNightGreeting2 => 'Уже поздно';

  @override
  String get homeDrawerLateNightSub2 =>
      'Скажите сегодняшнему дню «спокойной ночи»';

  @override
  String get modelProviderCodexChatGptName => 'Codex (ChatGPT)';

  @override
  String get modelProviderCodexDescription =>
      'Использует официальный вход Codex CLI по коду устройства и существующий Codex ACP runtime. API-ключ не сохраняется.';

  @override
  String get modelProviderCodexNotInstalled => 'Codex не установлен';

  @override
  String get modelProviderCodexInstalling => 'Установка Codex…';

  @override
  String get modelProviderCodexSignedOut => 'Вход не выполнен';

  @override
  String get modelProviderCodexWaiting => 'Ожидание входа через ChatGPT';

  @override
  String get modelProviderCodexSignedIn => 'Вход через ChatGPT выполнен';

  @override
  String get modelProviderCodexExpired => 'Код входа истёк';

  @override
  String get modelProviderCodexCancelled => 'Вход отменён';

  @override
  String get modelProviderCodexError => 'Ошибка входа Codex';

  @override
  String get modelProviderCodexInstall => 'Установить Codex';

  @override
  String get modelProviderCodexLogin => 'Войти через ChatGPT';

  @override
  String get modelProviderCodexCheckStatus => 'Проверить статус';

  @override
  String get modelProviderCodexLogout => 'Выйти';

  @override
  String get modelProviderCodexCancelLogin => 'Отменить вход';

  @override
  String get modelProviderCodexCopyCode => 'Копировать код';

  @override
  String get modelProviderCodexOpenBrowser => 'Открыть браузер';

  @override
  String get modelProviderCodexDeviceInstructions =>
      'Откройте официальную страницу, войдите в ChatGPT и введите одноразовый код. Токены никогда не показываются в приложении.';

  @override
  String get modelProviderCodexVerificationUrl => 'Официальная страница входа';

  @override
  String get modelProviderCodexDeviceCode => 'Одноразовый код';

  @override
  String get modelProviderCodexModelNote =>
      'Модель: gpt-5.3-codex-spark. Если она недоступна вашему тарифу, Codex покажет реальную ошибку тарифа или rollout без подмены модели.';

  @override
  String get modelProviderCodexCodeCopied => 'Код скопирован';

  @override
  String get modelProviderCodexBrowserFailed => 'Не удалось открыть браузер';

  @override
  String get modelProviderCodexInstallFailed => 'Не удалось установить Codex';

  @override
  String get modelProviderCodexLoginFailed =>
      'Не удалось запустить вход через ChatGPT';

  @override
  String get modelProviderCodexLogoutFailed => 'Не удалось выйти из Codex';

  @override
  String get modelProviderCodexStatusFailed =>
      'Не удалось проверить статус входа Codex';
}
