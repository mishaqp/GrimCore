import type { AppLocale, MessageCatalog } from "./catalog";

function intlLocale(locale: AppLocale): string {
  return locale === "zh" ? "zh-CN" : locale;
}

export function relativeDate(
  raw: number | undefined,
  locale: AppLocale,
  messages: MessageCatalog,
): string {
  const value = Number(raw);
  if (!Number.isFinite(value) || value <= 0) return "";
  const date = new Date(value);
  const diff = Math.max(0, Date.now() - value);
  if (diff < 60_000) return messages.justNow;
  const formatter = new Intl.RelativeTimeFormat(intlLocale(locale), { numeric: "always" });
  if (diff < 3_600_000) return formatter.format(-Math.floor(diff / 60_000), "minute");
  if (diff < 86_400_000) return formatter.format(-Math.floor(diff / 3_600_000), "hour");
  return new Intl.DateTimeFormat(intlLocale(locale), {
    month: "2-digit",
    day: "2-digit",
  }).format(date);
}
