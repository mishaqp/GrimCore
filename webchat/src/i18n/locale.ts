import type { AppLocale } from "./catalog";

export interface LocaleSources {
  query?: string | null;
  stored?: string | null;
  languages?: readonly string[];
}

export function parseLocale(value: string | null | undefined): AppLocale | null {
  const normalized = value?.trim().toLowerCase().replaceAll("_", "-");
  if (!normalized) return null;
  if (normalized === "ru" || normalized.startsWith("ru-")) return "ru";
  if (normalized === "en" || normalized.startsWith("en-")) return "en";
  if (normalized === "zh" || normalized.startsWith("zh-")) return "zh";
  return null;
}

export function resolveLocale({ query, stored, languages = [] }: LocaleSources): AppLocale {
  const fromQuery = parseLocale(query);
  if (fromQuery) return fromQuery;
  const fromStorage = parseLocale(stored);
  if (fromStorage) return fromStorage;
  for (const language of languages) {
    const resolved = parseLocale(language);
    if (resolved) return resolved;
  }
  return "ru";
}
