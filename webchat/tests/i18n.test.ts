import assert from "node:assert/strict";
import test from "node:test";
import { en, ru, zh } from "../src/i18n/catalog.ts";
import { localizedRequestErrorMessage } from "../src/i18n/errorMessage.ts";
import { resolveLocale } from "../src/i18n/locale.ts";
import { relativeDate } from "../src/i18n/relativeDate.ts";

test("locale resolution follows query, storage, browser, then Russian fallback", () => {
  assert.equal(resolveLocale({ query: "ru-RU", stored: "en", languages: ["zh-CN"] }), "ru");
  assert.equal(resolveLocale({ query: "de", stored: "en-US", languages: ["zh-CN"] }), "en");
  assert.equal(resolveLocale({ query: null, stored: null, languages: ["de", "zh-Hans"] }), "zh");
  assert.equal(resolveLocale({ query: null, stored: null, languages: ["de-DE"] }), "ru");
});

test("all locale catalogs expose the same keys", () => {
  assert.deepEqual(Object.keys(en).sort(), Object.keys(ru).sort());
  assert.deepEqual(Object.keys(zh).sort(), Object.keys(ru).sort());
  assert.deepEqual(Object.keys(en.apiErrors).sort(), Object.keys(ru.apiErrors).sort());
  assert.deepEqual(Object.keys(zh.apiErrors).sort(), Object.keys(ru.apiErrors).sort());
  for (const catalog of [ru, en, zh]) {
    assert.equal(catalog.assistant, "GrimCore");
    assert.equal(catalog.pageTitle, "GrimCore Web Chat");
  }
});

test("relative timestamps use locale-aware grammar", () => {
  const previousNow = Date.now;
  Date.now = () => Date.UTC(2026, 8, 13, 12, 0, 0);
  try {
    const fiveMinutesAgo = Date.now() - 5 * 60_000;
    assert.equal(relativeDate(fiveMinutesAgo, "ru", ru), "5 минут назад");
    assert.equal(relativeDate(fiveMinutesAgo, "en", en), "5 minutes ago");
    assert.equal(relativeDate(fiveMinutesAgo, "zh", zh), "5分钟前");
  } finally {
    Date.now = previousNow;
  }
});

test("dynamic messages keep interpolated values", () => {
  assert.equal(ru.deleteConversationConfirm("План"), "Удалить «План»? Это действие нельзя отменить.");
  assert.equal(en.removeAttachment("notes.md"), "Remove notes.md");
  assert.equal(zh.readFileFailed("a.txt"), "无法读取 a.txt");
  assert.equal(ru.apiErrors.MISSING_PATH, "Не указан путь");
});

test("unknown Chinese backend errors do not leak into Russian or English UI", () => {
  assert.equal(
    localizedRequestErrorMessage(503, "数据库连接失败", "ru", ru),
    "Не удалось выполнить запрос (503)",
  );
  assert.equal(
    localizedRequestErrorMessage(503, "数据库连接失败", "en", en),
    "Request failed (503)",
  );
  assert.equal(
    localizedRequestErrorMessage(503, "数据库连接失败", "zh", zh),
    "数据库连接失败",
  );
});

test("known error mappings and useful locale-compatible details are preserved", () => {
  assert.equal(
    localizedRequestErrorMessage(400, "MISSING_PATH", "ru", ru),
    "Не указан путь",
  );
  assert.equal(
    localizedRequestErrorMessage(422, "Validation failed", "ru", ru),
    "Validation failed",
  );
});
