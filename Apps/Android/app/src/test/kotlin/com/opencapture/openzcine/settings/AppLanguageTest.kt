package com.opencapture.openzcine.settings

import org.junit.Assert.assertEquals
import org.junit.Test

class AppLanguageTest {
    @Test fun supportedLanguageTagsRoundTrip() {
        AppLanguage.entries.forEach { language ->
            assertEquals(language, AppLanguage.fromLanguageTag(language.languageTag))
        }
    }

    @Test fun missingOrUnexpectedPreferenceFallsBackToSystem() {
        assertEquals(AppLanguage.SYSTEM, AppLanguage.fromLanguageTag(null))
        assertEquals(AppLanguage.SYSTEM, AppLanguage.fromLanguageTag("fr-FR"))
        assertEquals(AppLanguage.SYSTEM, AppLanguage.fromLanguageTag(""))
    }
}
