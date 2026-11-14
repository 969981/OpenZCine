package com.opencapture.openzcine.settings

import android.app.Activity
import android.content.Context
import android.content.ContextWrapper
import android.content.res.Configuration
import java.util.Locale

/**
 * User-selected display locale. Empty tag means follow Android's system languages.
 * Persist the *choice*, not a captured device language, so SYSTEM follows future changes.
 */
internal enum class AppLanguage(val languageTag: String) {
    SYSTEM(""),
    ENGLISH("en"),
    SIMPLIFIED_CHINESE("zh-Hans"),
    TRADITIONAL_CHINESE("zh-Hant");

    companion object {
        fun fromLanguageTag(raw: String?): AppLanguage =
            entries.firstOrNull { it.languageTag == raw } ?: SYSTEM
    }
}

internal object AppLanguagePreferences {
    private const val FILE_NAME = "openzcine-ui-language"
    private const val KEY_LANGUAGE = "language"

    fun selected(context: Context): AppLanguage =
        AppLanguage.fromLanguageTag(
            context.getSharedPreferences(FILE_NAME, Context.MODE_PRIVATE)
                .getString(KEY_LANGUAGE, ""),
        )

    /** Used before Activity.onCreate; no process-wide Locale.setDefault mutation. */
    fun localizedContext(context: Context): Context {
        val language = selected(context)
        if (language == AppLanguage.SYSTEM) return context
        val locale = Locale.forLanguageTag(language.languageTag)
        val configuration = Configuration(context.resources.configuration)
        configuration.setLocale(locale)
        configuration.setLayoutDirection(locale)
        return context.createConfigurationContext(configuration)
    }

    fun select(context: Context, language: AppLanguage): Boolean {
        if (selected(context) == language) return false
        context.getSharedPreferences(FILE_NAME, Context.MODE_PRIVATE)
            .edit().putString(KEY_LANGUAGE, language.languageTag).apply()
        return true
    }
}

internal tailrec fun Context.findHostActivity(): Activity? = when (this) {
    is Activity -> this
    is ContextWrapper -> if (baseContext === this) null else baseContext.findHostActivity()
    else -> null
}
