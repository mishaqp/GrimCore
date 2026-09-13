export type AppLocale = "ru" | "en" | "zh";

export type ApiErrorCode =
  | "INVALID_CONVERSATION_ID"
  | "RUN_START_FAILED"
  | "EMPTY_REPLY"
  | "MISSING_PATH"
  | "BROWSER_FRAME_UNAVAILABLE"
  | "Access denied"
  | "Authentication required"
  | "Authentication failed"
  | "Invalid request"
  | "Resource not found"
  | "Resource no longer available"
  | "Invalid MCP origin";

export interface MessageCatalog {
  pageTitle: string;
  pageDescription: string;
  requestFailed: string;
  requestFailedWithStatus: (status: number) => string;
  apiErrors: Readonly<Record<ApiErrorCode, string>>;
  archived: string;
  restoredToConversationList: string;
  pinned: string;
  unpinned: string;
  deleteConversationConfirm: (title: string) => string;
  currentConversation: string;
  conversationDeleted: string;
  newConversation: string;
  cannotCreateConversation: string;
  fileSaved: string;
  conversationNavigation: string;
  expandLeftSidebar: string;
  collapseLeftSidebar: string;
  previousConversation: string;
  nextConversation: string;
  unarchiveConversation: string;
  archiveConversation: string;
  deleteConversation: string;
  expandRightSidebar: string;
  collapseRightSidebar: string;
  webChatAreas: string;
  chat: string;
  workspace: string;
  browser: string;
  closeConversationList: string;
  greetingWords: readonly string[];
  greetingHello: string;
  greetingHelp: string;
  readFileFailed: (name: string) => string;
  attachment: string;
  thinking: string;
  thinkingComplete: string;
  elapsed: (duration: string) => string;
  statusRunning: string;
  statusCompleted: string;
  statusFailed: string;
  statusTimeout: string;
  statusInterrupted: string;
  statusStopped: string;
  terminal: string;
  search: string;
  file: string;
  tool: string;
  toolRunning: string;
  reasoningProcess: string;
  taskCancelled: string;
  processed: string;
  processedWithDuration: (duration: string) => string;
  openConversationList: string;
  clarificationPending: string;
  removeAttachment: (name: string) => string;
  composerPlaceholder: string;
  addAttachment: string;
  composerHint: string;
  stop: string;
  send: string;
  durationSeconds: (seconds: number) => string;
  durationMinutesSeconds: (minutes: number, seconds: number) => string;
  durationHoursMinutes: (hours: number, minutes: number) => string;
  connectionOnline: string;
  connectionOffline: string;
  connectionConnecting: string;
  pinnedConversations: string;
  assistant: string;
  chatOnly: string;
  chatOnlyMode: string;
  searchConversations: string;
  clearSearch: string;
  viewArchivedConversations: string;
  archivedConversations: string;
  closeArchivedConversations: string;
  loadingArchivedConversations: string;
  restoreNamedConversation: (title: string) => string;
  restoreConversation: string;
  deleteNamedConversation: (title: string) => string;
  noArchivedConversations: string;
  createConversation: string;
  chooseConversationMode: string;
  searchResults: string;
  noSearchResults: string;
  noConversations: string;
  tryAnotherSearch: string;
  createFirstConversation: string;
  conversationActions: (title: string) => string;
  archive: string;
  unpin: string;
  pin: string;
  delete: string;
  modeNormal: string;
  justNow: string;
  login: string;
  serverToken: string;
  connecting: string;
  connect: string;
  language: string;
  download: string;
  refresh: string;
  save: string;
  emptyDirectory: string;
  selectFile: string;
  enterBrowserUrl: string;
  open: string;
  scrollUp: string;
  scrollDown: string;
  refreshFrame: string;
  noBrowserSession: string;
  browserLiveFrame: string;
  noBrowserSessionToMirror: string;
}

const formatNumber = (locale: string, value: number) =>
  new Intl.NumberFormat(locale, { maximumFractionDigits: 0 }).format(value);

export const ru: MessageCatalog = {
  pageTitle: "GrimCore Web Chat",
  pageDescription: "Локальная веб-консоль GrimCore",
  requestFailed: "Не удалось выполнить запрос",
  requestFailedWithStatus: (status) => `Не удалось выполнить запрос (${status})`,
  apiErrors: {
    INVALID_CONVERSATION_ID: "Некорректный идентификатор чата",
    RUN_START_FAILED: "Не удалось запустить задачу",
    EMPTY_REPLY: "Введите ответ",
    MISSING_PATH: "Не указан путь",
    BROWSER_FRAME_UNAVAILABLE: "Изображение браузера недоступно",
    "Access denied": "Доступ запрещён",
    "Authentication required": "Требуется авторизация",
    "Authentication failed": "Ошибка авторизации",
    "Invalid request": "Некорректный запрос",
    "Resource not found": "Ресурс не найден",
    "Resource no longer available": "Ресурс больше недоступен",
    "Invalid MCP origin": "Недопустимый источник MCP-запроса",
  },
  archived: "Чат перемещён в архив",
  restoredToConversationList: "Чат восстановлен",
  pinned: "Чат закреплён",
  unpinned: "Чат откреплён",
  deleteConversationConfirm: (title) => `Удалить «${title}»? Это действие нельзя отменить.`,
  currentConversation: "текущий чат",
  conversationDeleted: "Чат удалён",
  newConversation: "Новый чат",
  cannotCreateConversation: "Не удалось создать новый чат",
  fileSaved: "Файл сохранён",
  conversationNavigation: "Навигация по чатам",
  expandLeftSidebar: "Развернуть левую панель",
  collapseLeftSidebar: "Свернуть левую панель",
  previousConversation: "Предыдущий чат",
  nextConversation: "Следующий чат",
  unarchiveConversation: "Вернуть из архива",
  archiveConversation: "Переместить в архив",
  deleteConversation: "Удалить чат",
  expandRightSidebar: "Развернуть правую панель",
  collapseRightSidebar: "Свернуть правую панель",
  webChatAreas: "Разделы Web Chat",
  chat: "Чат",
  workspace: "Рабочая область",
  browser: "Браузер",
  closeConversationList: "Закрыть список чатов",
  greetingWords: ["общаться", "выполнять", "создавать", "исследовать", "планировать", "подводить итоги", "искать", "запоминать"],
  greetingHello: "Привет 👋, я GrimCore",
  greetingHelp: "Я могу помочь вам",
  readFileFailed: (name) => `Не удалось прочитать файл ${name}`,
  attachment: "Вложение",
  thinking: "Размышляю",
  thinkingComplete: "Размышления завершены",
  elapsed: (duration) => `затрачено ${duration}`,
  statusRunning: "Выполняется",
  statusCompleted: "Готово",
  statusFailed: "Ошибка",
  statusTimeout: "Время ожидания истекло",
  statusInterrupted: "Прервано",
  statusStopped: "Остановлено",
  terminal: "Терминал",
  search: "Поиск",
  file: "Файл",
  tool: "Инструмент",
  toolRunning: "Выполнение инструмента",
  reasoningProcess: "Ход рассуждений",
  taskCancelled: "Задача отменена",
  processed: "Обработано",
  processedWithDuration: (duration) => `Обработано за ${duration}`,
  openConversationList: "Открыть список чатов",
  clarificationPending: "Агент ждёт уточнения. Отправьте следующее сообщение, чтобы продолжить.",
  removeAttachment: (name) => `Удалить вложение ${name}`,
  composerPlaceholder: "Введите сообщение",
  addAttachment: "Добавить вложение",
  composerHint: "Enter — отправить · Shift + Enter — новая строка",
  stop: "Остановить",
  send: "Отправить",
  durationSeconds: (seconds) => `${formatNumber("ru", seconds)} с`,
  durationMinutesSeconds: (minutes, seconds) => `${formatNumber("ru", minutes)} мин ${formatNumber("ru", seconds)} с`,
  durationHoursMinutes: (hours, minutes) => `${formatNumber("ru", hours)} ч ${formatNumber("ru", minutes)} мин`,
  connectionOnline: "Подключено",
  connectionOffline: "Соединение потеряно, повторная попытка",
  connectionConnecting: "Подключение к событиям",
  pinnedConversations: "Закреплённые",
  assistant: "GrimCore",
  chatOnly: "Только чат",
  chatOnlyMode: "Только чат",
  searchConversations: "Поиск чатов",
  clearSearch: "Очистить поиск",
  viewArchivedConversations: "Открыть архив",
  archivedConversations: "Архив",
  closeArchivedConversations: "Закрыть архив",
  loadingArchivedConversations: "Загрузка архива…",
  restoreNamedConversation: (title) => `Восстановить «${title}»`,
  restoreConversation: "Восстановить чат",
  deleteNamedConversation: (title) => `Удалить «${title}»`,
  noArchivedConversations: "В архиве пока ничего нет",
  createConversation: "Новый чат",
  chooseConversationMode: "Выбрать режим нового чата",
  searchResults: "Результаты поиска",
  noSearchResults: "Подходящие чаты не найдены",
  noConversations: "Чатов пока нет",
  tryAnotherSearch: "Попробуйте другой запрос",
  createFirstConversation: "Нажмите кнопку сверху, чтобы начать чат",
  conversationActions: (title) => `Действия с чатом «${title}»`,
  archive: "В архив",
  unpin: "Открепить",
  pin: "Закрепить",
  delete: "Удалить",
  modeNormal: "Обычный",
  justNow: "только что",
  login: "Вход",
  serverToken: "Токен сервера",
  connecting: "Подключение…",
  connect: "Подключиться",
  language: "Язык интерфейса",
  download: "Скачать",
  refresh: "Обновить",
  save: "Сохранить",
  emptyDirectory: "Папка пуста",
  selectFile: "Выберите файл для просмотра или редактирования",
  enterBrowserUrl: "Введите адрес для удалённого перехода",
  open: "Открыть",
  scrollUp: "Прокрутить вверх",
  scrollDown: "Прокрутить вниз",
  refreshFrame: "Обновить изображение",
  noBrowserSession: "Нет активной сессии браузера",
  browserLiveFrame: "Текущее изображение браузера",
  noBrowserSessionToMirror: "Нет сессии браузера для показа",
};

export const en: MessageCatalog = {
  pageTitle: "GrimCore Web Chat",
  pageDescription: "GrimCore local Web Chat console",
  requestFailed: "Request failed",
  requestFailedWithStatus: (status) => `Request failed (${status})`,
  apiErrors: {
    INVALID_CONVERSATION_ID: "Invalid conversation ID",
    RUN_START_FAILED: "Could not start the task",
    EMPTY_REPLY: "Enter a reply",
    MISSING_PATH: "A path is required",
    BROWSER_FRAME_UNAVAILABLE: "The browser frame is unavailable",
    "Access denied": "Access denied",
    "Authentication required": "Authentication required",
    "Authentication failed": "Authentication failed",
    "Invalid request": "Invalid request",
    "Resource not found": "Resource not found",
    "Resource no longer available": "Resource no longer available",
    "Invalid MCP origin": "Invalid MCP request origin",
  },
  archived: "Conversation archived",
  restoredToConversationList: "Conversation restored",
  pinned: "Conversation pinned",
  unpinned: "Conversation unpinned",
  deleteConversationConfirm: (title) => `Delete “${title}”? This action cannot be undone.`,
  currentConversation: "current conversation",
  conversationDeleted: "Conversation deleted",
  newConversation: "New conversation",
  cannotCreateConversation: "Could not create a new conversation",
  fileSaved: "File saved",
  conversationNavigation: "Conversation navigation",
  expandLeftSidebar: "Expand left sidebar",
  collapseLeftSidebar: "Collapse left sidebar",
  previousConversation: "Previous conversation",
  nextConversation: "Next conversation",
  unarchiveConversation: "Restore from archive",
  archiveConversation: "Archive conversation",
  deleteConversation: "Delete conversation",
  expandRightSidebar: "Expand right sidebar",
  collapseRightSidebar: "Collapse right sidebar",
  webChatAreas: "Web Chat areas",
  chat: "Chat",
  workspace: "Workspace",
  browser: "Browser",
  closeConversationList: "Close conversation list",
  greetingWords: ["chat", "execute", "build", "explore", "plan", "summarize", "search", "remember"],
  greetingHello: "Hi 👋, I’m GrimCore",
  greetingHelp: "I can help you",
  readFileFailed: (name) => `Could not read ${name}`,
  attachment: "Attachment",
  thinking: "Thinking",
  thinkingComplete: "Thought process complete",
  elapsed: (duration) => `took ${duration}`,
  statusRunning: "Running",
  statusCompleted: "Completed",
  statusFailed: "Failed",
  statusTimeout: "Timed out",
  statusInterrupted: "Interrupted",
  statusStopped: "Stopped",
  terminal: "Terminal",
  search: "Search",
  file: "File",
  tool: "Tool",
  toolRunning: "Running tool",
  reasoningProcess: "Reasoning",
  taskCancelled: "Task cancelled",
  processed: "Processed",
  processedWithDuration: (duration) => `Processed in ${duration}`,
  openConversationList: "Open conversation list",
  clarificationPending: "The Agent is waiting for more information. Send another message to continue.",
  removeAttachment: (name) => `Remove ${name}`,
  composerPlaceholder: "Type a message",
  addAttachment: "Add attachment",
  composerHint: "Enter to send · Shift + Enter for a new line",
  stop: "Stop",
  send: "Send",
  durationSeconds: (seconds) => `${formatNumber("en", seconds)}s`,
  durationMinutesSeconds: (minutes, seconds) => `${formatNumber("en", minutes)}m ${formatNumber("en", seconds)}s`,
  durationHoursMinutes: (hours, minutes) => `${formatNumber("en", hours)}h ${formatNumber("en", minutes)}m`,
  connectionOnline: "Connected",
  connectionOffline: "Connection lost, retrying",
  connectionConnecting: "Connecting to live events",
  pinnedConversations: "Pinned",
  assistant: "GrimCore",
  chatOnly: "Chat only",
  chatOnlyMode: "Chat-only mode",
  searchConversations: "Search conversations",
  clearSearch: "Clear search",
  viewArchivedConversations: "View archived conversations",
  archivedConversations: "Archived",
  closeArchivedConversations: "Close archived conversations",
  loadingArchivedConversations: "Loading archived conversations…",
  restoreNamedConversation: (title) => `Restore “${title}”`,
  restoreConversation: "Restore conversation",
  deleteNamedConversation: (title) => `Delete “${title}”`,
  noArchivedConversations: "No archived conversations",
  createConversation: "New conversation",
  chooseConversationMode: "Choose a conversation mode",
  searchResults: "Search results",
  noSearchResults: "No matching conversations",
  noConversations: "No conversations yet",
  tryAnotherSearch: "Try another search",
  createFirstConversation: "Use the button above to start a conversation",
  conversationActions: (title) => `Actions for “${title}”`,
  archive: "Archive",
  unpin: "Unpin",
  pin: "Pin",
  delete: "Delete",
  modeNormal: "Normal",
  justNow: "just now",
  login: "Sign in",
  serverToken: "Server token",
  connecting: "Connecting…",
  connect: "Connect",
  language: "Interface language",
  download: "Download",
  refresh: "Refresh",
  save: "Save",
  emptyDirectory: "This directory is empty",
  selectFile: "Select a file to view or edit",
  enterBrowserUrl: "Enter an address to navigate remotely",
  open: "Open",
  scrollUp: "Scroll up",
  scrollDown: "Scroll down",
  refreshFrame: "Refresh view",
  noBrowserSession: "No active browser session",
  browserLiveFrame: "Live browser view",
  noBrowserSessionToMirror: "No browser session is available to mirror",
};

export const zh: MessageCatalog = {
  pageTitle: "GrimCore Web Chat",
  pageDescription: "GrimCore 局域网 Web Chat 控制台",
  requestFailed: "请求失败",
  requestFailedWithStatus: (status) => `请求失败 (${status})`,
  apiErrors: {
    INVALID_CONVERSATION_ID: "会话 ID 无效",
    RUN_START_FAILED: "无法启动任务",
    EMPTY_REPLY: "请输入回复",
    MISSING_PATH: "未指定路径",
    BROWSER_FRAME_UNAVAILABLE: "浏览器画面不可用",
    "Access denied": "访问被拒绝",
    "Authentication required": "需要身份验证",
    "Authentication failed": "身份验证失败",
    "Invalid request": "请求无效",
    "Resource not found": "未找到资源",
    "Resource no longer available": "资源已不可用",
    "Invalid MCP origin": "MCP 请求来源无效",
  },
  archived: "已归档",
  restoredToConversationList: "已恢复到会话列表",
  pinned: "已置顶",
  unpinned: "已取消置顶",
  deleteConversationConfirm: (title) => `删除“${title}”？此操作无法撤销。`,
  currentConversation: "当前对话",
  conversationDeleted: "会话已删除",
  newConversation: "新对话",
  cannotCreateConversation: "无法创建新对话",
  fileSaved: "文件已保存",
  conversationNavigation: "对话导航",
  expandLeftSidebar: "展开左侧边栏",
  collapseLeftSidebar: "收起左侧边栏",
  previousConversation: "回退到上一会话",
  nextConversation: "前进到下一会话",
  unarchiveConversation: "取消归档",
  archiveConversation: "归档对话",
  deleteConversation: "删除对话",
  expandRightSidebar: "展开右侧边栏",
  collapseRightSidebar: "收起右侧边栏",
  webChatAreas: "Web Chat 区域",
  chat: "聊天",
  workspace: "工作区",
  browser: "浏览器",
  closeConversationList: "关闭对话列表",
  greetingWords: ["聊天", "执行", "构建", "探索", "规划", "总结", "检索", "记忆"],
  greetingHello: "你好 👋，我是 GrimCore",
  greetingHelp: "我可以帮助你",
  readFileFailed: (name) => `无法读取 ${name}`,
  attachment: "附件",
  thinking: "正在思考",
  thinkingComplete: "思考完成",
  elapsed: (duration) => `用时${duration}`,
  statusRunning: "运行中",
  statusCompleted: "已完成",
  statusFailed: "失败",
  statusTimeout: "超时",
  statusInterrupted: "已中断",
  statusStopped: "已停止",
  terminal: "终端",
  search: "搜索",
  file: "文件",
  tool: "工具",
  toolRunning: "工具运行",
  reasoningProcess: "思考过程",
  taskCancelled: "任务已取消",
  processed: "已处理",
  processedWithDuration: (duration) => `已处理 ${duration}`,
  openConversationList: "打开对话列表",
  clarificationPending: "Agent 正在等待你的补充说明，发送下一条消息后继续。",
  removeAttachment: (name) => `移除 ${name}`,
  composerPlaceholder: "请输入内容",
  addAttachment: "添加附件",
  composerHint: "Enter 发送 · Shift + Enter 换行",
  stop: "停止",
  send: "发送",
  durationSeconds: (seconds) => `${formatNumber("zh-CN", seconds)}秒`,
  durationMinutesSeconds: (minutes, seconds) => `${formatNumber("zh-CN", minutes)}分${formatNumber("zh-CN", seconds)}秒`,
  durationHoursMinutes: (hours, minutes) => `${formatNumber("zh-CN", hours)}小时${formatNumber("zh-CN", minutes)}分`,
  connectionOnline: "实时连接正常",
  connectionOffline: "连接中断，正在重试",
  connectionConnecting: "正在连接实时事件",
  pinnedConversations: "置顶会话",
  assistant: "GrimCore",
  chatOnly: "纯聊天",
  chatOnlyMode: "纯聊天模式",
  searchConversations: "搜索对话",
  clearSearch: "清除搜索",
  viewArchivedConversations: "查看归档对话",
  archivedConversations: "已归档",
  closeArchivedConversations: "关闭归档会话",
  loadingArchivedConversations: "正在加载归档会话…",
  restoreNamedConversation: (title) => `恢复“${title}”`,
  restoreConversation: "恢复会话",
  deleteNamedConversation: (title) => `删除“${title}”`,
  noArchivedConversations: "暂无归档会话",
  createConversation: "新建对话",
  chooseConversationMode: "选择新对话模式",
  searchResults: "搜索结果",
  noSearchResults: "没有找到相关对话",
  noConversations: "还没有对话",
  tryAnotherSearch: "换个关键词试试",
  createFirstConversation: "点击右上角开始新对话",
  conversationActions: (title) => `“${title}”操作`,
  archive: "归档",
  unpin: "取消置顶",
  pin: "置顶",
  delete: "删除",
  modeNormal: "普通",
  justNow: "刚刚",
  login: "登录",
  serverToken: "服务器令牌",
  connecting: "正在连接…",
  connect: "连接",
  language: "界面语言",
  download: "下载",
  refresh: "刷新",
  save: "保存",
  emptyDirectory: "目录为空",
  selectFile: "选择文件以查看或编辑",
  enterBrowserUrl: "输入网址并远程导航",
  open: "打开",
  scrollUp: "上滑",
  scrollDown: "下滑",
  refreshFrame: "刷新画面",
  noBrowserSession: "暂无浏览器会话",
  browserLiveFrame: "浏览器实时画面",
  noBrowserSessionToMirror: "当前没有可镜像的浏览器会话",
};

export const CATALOGS: Record<AppLocale, MessageCatalog> = { ru, en, zh };
