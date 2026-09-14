package cn.com.omnimind.bot.agent.runtime

import cn.com.omnimind.baselib.llm.ModelProviderAuthMode
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class CodexChatGptAccountContractTest {
    @Test
    fun officialDevicePromptParsesWithoutReturningSecrets() {
        val parsed = CodexDeviceFlowParser.parse(
            """
            Follow these steps to sign in with ChatGPT using device code authorization:
            1. Open this link in your browser and sign in to your account
               https://auth.openai.com/codex/device
            2. Enter this one-time code (expires in 15 minutes)
               ABCD-EFGH
            """.trimIndent()
        )
        assertEquals("https://auth.openai.com/codex/device", parsed?.verificationUrl)
        assertEquals("ABCD-EFGH", parsed?.userCode)
    }

    @Test
    fun malformedOrCredentialLikeOutputIsNotExposed() {
        assertNull(CodexDeviceFlowParser.parse("access_token=secret"))
        val safe = CodexDeviceFlowParser.safeError("access_token=secret\nauth.json contains token\nnetwork failed")
        assertFalse(safe.contains("secret"))
        assertFalse(safe.contains("auth.json"))
        assertTrue(safe.contains("network failed"))
    }

    @Test
    fun accountCredentialNormalizationHasNoHttpOrApiEnvironmentInputs() {
        val credentials = AgentProviderCredentials(
            baseUrl = "https://should-not-survive.example/v1",
            apiKey = "should-not-survive",
            customHeaders = mapOf("Authorization" to "secret"),
            authMode = ModelProviderAuthMode.CODEX_CHATGPT,
        ).normalized()
        assertEquals("", credentials.baseUrl)
        assertEquals("", credentials.apiKey)
        assertTrue(credentials.customHeaders.isEmpty())
        assertEquals("codex_acp", credentials.protocolType)
    }
}
