import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { CATALOGS, type AppLocale, type MessageCatalog } from "./catalog";
import { resolveLocale } from "./locale";

const LOCALE_STORAGE_KEY = "grimcore_webchat_locale";

interface I18nValue {
  locale: AppLocale;
  messages: MessageCatalog;
  setLocale: (locale: AppLocale) => void;
}

function browserLocale(): AppLocale {
  let stored: string | null = null;
  try {
    stored = window.localStorage.getItem(LOCALE_STORAGE_KEY);
  } catch {
    // Storage can be unavailable in privacy-restricted browsers.
  }
  return resolveLocale({
    query: new URLSearchParams(window.location.search).get("lang"),
    stored,
    languages: navigator.languages?.length ? navigator.languages : [navigator.language],
  });
}

const I18nContext = createContext<I18nValue | null>(null);

export function I18nProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<AppLocale>(browserLocale);

  useEffect(() => {
    document.documentElement.lang = locale === "zh" ? "zh-CN" : locale;
    document.title = CATALOGS[locale].pageTitle;
    document.querySelector<HTMLMetaElement>('meta[name="description"]')
      ?.setAttribute("content", CATALOGS[locale].pageDescription);
  }, [locale]);

  const value = useMemo<I18nValue>(() => ({
    locale,
    messages: CATALOGS[locale],
    setLocale(nextLocale) {
      setLocaleState(nextLocale);
      try {
        window.localStorage.setItem(LOCALE_STORAGE_KEY, nextLocale);
      } catch {
        // Keep the in-memory choice when storage is unavailable.
      }
    },
  }), [locale]);

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useI18n(): I18nValue {
  const value = useContext(I18nContext);
  if (!value) throw new Error("useI18n must be used inside I18nProvider");
  return value;
}

export function LanguageSwitcher({ className = "" }: { className?: string }) {
  const { locale, messages, setLocale } = useI18n();
  return (
    <select
      className={["language-select", className].filter(Boolean).join(" ")}
      aria-label={messages.language}
      title={messages.language}
      value={locale}
      onChange={(event) => setLocale(event.target.value as AppLocale)}
    >
      <option value="ru">Русский</option>
      <option value="en">English</option>
      <option value="zh">中文</option>
    </select>
  );
}
