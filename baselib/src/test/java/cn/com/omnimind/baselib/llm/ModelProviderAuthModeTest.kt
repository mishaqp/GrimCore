package cn.com.omnimind.baselib.llm

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class ModelProviderAuthModeTest {
    @Test
    fun legacyProfilesDefaultToApiKeyMode() {
        assertEquals(ModelProviderAuthMode.API_KEY, ModelProviderAuthMode.fromSourceType(null))
        assertEquals(ModelProviderAuthMode.API_KEY, ModelProviderAuthMode.fromSourceType("custom"))
        assertFalse(ModelProviderProfile("legacy", "Legacy").isCodexChatGptAccount())
    }

    @Test
    fun codexChatGptModeIsExplicitAndDoesNotRequireHttpConfiguration() {
        val profile = ModelProviderProfile(
            id = "codex-chatgpt",
            name = "Codex (ChatGPT)",
            sourceType = ModelProviderAuthMode.CODEX_CHATGPT,
            protocolType = "codex_acp",
        )
        assertTrue(profile.isCodexChatGptAccount())
        assertFalse(profile.isConfigured())
        assertEquals(
            ModelProviderAuthMode.CODEX_CHATGPT,
            ModelProviderAuthMode.fromSourceType(profile.sourceType),
        )
    }
}
