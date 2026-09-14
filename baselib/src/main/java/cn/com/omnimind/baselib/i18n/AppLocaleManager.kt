package cn.com.omnimind.baselib.i18n

import android.content.Context
import android.content.res.Configuration
import android.content.res.Resources
import android.os.Build
import android.os.LocaleList
import java.util.Locale

enum class AppLanguageMode(val storageValue: String) {
    SYSTEM("system"),
    ZH_HANS("zhHans"),
    EN("en"),
    RU("ru");

    companion object {
        fun fromStorageValue(raw: String?): AppLanguageMode {
            val normalized = raw?.trim()
            return entries.firstOrNull { it.storageValue == normalized } ?: SYSTEM
        }
    }
}

enum class PromptLocale(
    val tag: String,
    val locale: Locale
) {
    ZH_CN("zh-CN", Locale.SIMPLIFIED_CHINESE),
    EN_US("en-US", Locale.US);

    companion object {
        fun fromTag(raw: String?): PromptLocale? {
            val normalized = raw?.trim()?.lowercase().orEmpty()
            return when (normalized) {
                "zh", "zh-cn", "zh_hans", "zh-hans" -> ZH_CN
                "en", "en-us" -> EN_US
                else -> null
            }
        }
    }
}

data class LocalizedText(
    val zhCN: String,
    val enUS: String
) {
    fun resolve(locale: PromptLocale): String {
        return when (locale) {
            PromptLocale.ZH_CN -> zhCN
            PromptLocale.EN_US -> enUS
        }
    }

    fun resolve(context: Context): String = resolve(AppLocaleManager.resolvePromptLocale(context))
}

object AppLocaleManager {
    private const val FLUTTER_PREFS_NAME = "FlutterSharedPreferences"
    private const val FLUTTER_LANGUAGE_KEY = "flutter.language_option"
    private val RUSSIAN_LOCALE: Locale = Locale.forLanguageTag("ru")

    fun readStoredLanguageMode(context: Context): AppLanguageMode {
        val prefs = context.applicationContext.getSharedPreferences(
            FLUTTER_PREFS_NAME,
            Context.MODE_PRIVATE
        )
        return AppLanguageMode.fromStorageValue(prefs.getString(FLUTTER_LANGUAGE_KEY, null))
    }

    fun resolvePromptLocale(context: Context): PromptLocale {
        return resolvePromptLocale(
            mode = readStoredLanguageMode(context),
            systemLocale = systemLocale()
        )
    }

    fun resolvePromptLocale(
        mode: AppLanguageMode,
        systemLocale: Locale
    ): PromptLocale {
        return when (mode) {
            AppLanguageMode.ZH_HANS -> PromptLocale.ZH_CN
            AppLanguageMode.EN -> PromptLocale.EN_US
            // The Russian UI uses the reviewed English prompt/tool text.
            // Translating agent prompts and tool descriptions is tracked as
            // a separate follow-up step.
            AppLanguageMode.RU -> PromptLocale.EN_US
            AppLanguageMode.SYSTEM -> normalize(systemLocale)
        }
    }

    /**
     * Resolves the locale used by Android resources and native UI.
     *
     * Prompt locale is intentionally resolved separately: Russian UI still
     * uses the reviewed English model prompts until Russian prompt support is
     * implemented as its own change.
     */
    fun resolveUiLocale(
        mode: AppLanguageMode,
        systemLocale: Locale
    ): Locale {
        return when (mode) {
            AppLanguageMode.ZH_HANS -> Locale.SIMPLIFIED_CHINESE
            AppLanguageMode.EN -> Locale.US
            AppLanguageMode.RU -> RUSSIAN_LOCALE
            AppLanguageMode.SYSTEM -> normalizeUiLocale(systemLocale)
        }
    }

    fun currentPromptLocale(): PromptLocale {
        return normalize(Locale.getDefault())
    }

    fun currentLocale(context: Context): Locale {
        return resolveUiLocale(
            mode = readStoredLanguageMode(context),
            systemLocale = systemLocale()
        )
    }

    fun currentLocale(): Locale {
        return normalizeUiLocale(Locale.getDefault())
    }

    fun isEnglish(context: Context): Boolean {
        return resolvePromptLocale(context) == PromptLocale.EN_US
    }

    fun isEnglish(): Boolean {
        return currentPromptLocale() == PromptLocale.EN_US
    }

    fun brandName(context: Context): String {
        return brandName(resolvePromptLocale(context))
    }

    fun brandName(): String {
        return brandName(currentPromptLocale())
    }

    fun brandName(locale: PromptLocale): String {
        // GrimCore branding is locale independent.
        return "GrimCore"
    }

    fun applyAppLocale(context: Context): Locale {
        val locale = currentLocale(context)
        Locale.setDefault(locale)
        val resources = context.applicationContext.resources
        val configuration = Configuration(resources.configuration)
        configuration.setLocale(locale)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            configuration.setLocales(LocaleList(locale))
        }
        @Suppress("DEPRECATION")
        resources.updateConfiguration(configuration, resources.displayMetrics)
        return locale
    }

    fun localizedContext(context: Context): Context {
        val locale = currentLocale(context)
        val configuration = Configuration(context.resources.configuration)
        configuration.setLocale(locale)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            configuration.setLocales(LocaleList(locale))
        }
        return context.createConfigurationContext(configuration)
    }

    private fun systemLocale(): Locale {
        // Application resources are overwritten by applyAppLocale(). Reading
        // them here would make switching back to SYSTEM retain the previous
        // explicit app language instead of following the device language.
        val configuration = Resources.getSystem().configuration
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            configuration.locales.takeIf { !it.isEmpty }?.get(0) ?: Locale.getDefault()
        } else {
            @Suppress("DEPRECATION")
            configuration.locale ?: Locale.getDefault()
        }
    }

    private fun normalize(locale: Locale): PromptLocale {
        return if (locale.language.lowercase() == "zh") {
            PromptLocale.ZH_CN
        } else {
            PromptLocale.EN_US
        }
    }

    private fun normalizeUiLocale(locale: Locale): Locale {
        return when (locale.language.lowercase()) {
            "zh" -> Locale.SIMPLIFIED_CHINESE
            "ru" -> RUSSIAN_LOCALE
            else -> Locale.US
        }
    }
}
