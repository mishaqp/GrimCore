package cn.com.omnimind.baselib.i18n

import org.junit.Assert.assertEquals
import org.junit.Test
import java.util.Locale

class AppLocaleManagerTest {
    @Test
    fun resolvePromptLocaleRespectsExplicitModeAndSystemFallback() {
        assertEquals(
            PromptLocale.EN_US,
            AppLocaleManager.resolvePromptLocale(AppLanguageMode.EN, Locale.SIMPLIFIED_CHINESE)
        )
        assertEquals(
            PromptLocale.ZH_CN,
            AppLocaleManager.resolvePromptLocale(AppLanguageMode.ZH_HANS, Locale.US)
        )
        assertEquals(
            PromptLocale.EN_US,
            AppLocaleManager.resolvePromptLocale(AppLanguageMode.SYSTEM, Locale.US)
        )
        assertEquals(
            PromptLocale.ZH_CN,
            AppLocaleManager.resolvePromptLocale(AppLanguageMode.SYSTEM, Locale.SIMPLIFIED_CHINESE)
        )
        assertEquals(
            PromptLocale.EN_US,
            AppLocaleManager.resolvePromptLocale(AppLanguageMode.RU, Locale.SIMPLIFIED_CHINESE)
        )
    }

    @Test
    fun resolveUiLocaleKeepsRussianUiIndependentFromPromptLocale() {
        assertEquals(
            "ru",
            AppLocaleManager.resolveUiLocale(AppLanguageMode.RU, Locale.US).language
        )
        assertEquals(
            "ru",
            AppLocaleManager.resolveUiLocale(
                AppLanguageMode.SYSTEM,
                Locale.forLanguageTag("ru-RU")
            ).language
        )
        assertEquals(
            "en",
            AppLocaleManager.resolveUiLocale(
                AppLanguageMode.EN,
                Locale.forLanguageTag("ru-RU")
            ).language
        )
        assertEquals(
            "zh",
            AppLocaleManager.resolveUiLocale(
                AppLanguageMode.ZH_HANS,
                Locale.forLanguageTag("ru-RU")
            ).language
        )
    }
}
