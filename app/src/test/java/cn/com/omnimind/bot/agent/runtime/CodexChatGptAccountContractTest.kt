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
    fun credentialLikeOutputIsRedactedButUsefulAuthorizationErrorsRemain() {
        assertNull(CodexDeviceFlowParser.parse("access_token=secret"))
        val safe = CodexDeviceFlowParser.safeError(
            """
            access_token=secret
            auth.json contains token
            device code login is not enabled for this Codex server
            network failed with Bearer abc.def.ghi and sk-secretvalue
            """.trimIndent()
        )
        assertFalse(safe.contains("secret"))
        assertFalse(safe.contains("auth.json"))
        assertFalse(safe.contains("abc.def.ghi"))
        assertTrue(safe.contains("device code login is not enabled"))
        assertTrue(safe.contains("network failed"))
    }

    @Test
    fun chatGptStatusDoesNotAcceptLegacyApiKeyLogin() {
        assertTrue(isChatGptLoginStatus(0, "Logged in using ChatGPT\n"))
        assertFalse(isChatGptLoginStatus(0, "Logged in using an API key - sk-***\n"))
        assertFalse(isChatGptLoginStatus(1, "Logged in using ChatGPT\n"))
    }

    @Test
    fun deviceLoginIsForegroundAndHasNoGuestPidProtocol() {
        assertEquals("exec codex login --device-auth", CODEX_DEVICE_LOGIN_COMMAND)
        val shellCommand = buildCodexDeviceLoginShellCommand()
        assertTrue(shellCommand.endsWith(CODEX_DEVICE_LOGIN_COMMAND))
        assertFalse(shellCommand.contains("\$!"))
        assertFalse(shellCommand.contains("\$?"))
        assertFalse(Regex("(^|[;\\s])&([;\\s]|\$)").containsMatchIn(shellCommand))
        assertFalse(shellCommand.contains(">"))
    }

    @Test
    fun loginOutputIsBoundedAndKeepsTheLatestDiagnostic() {
        val output = BoundedCodexLoginOutput(maxChars = 64)
        repeat(20) { index -> output.appendLine("line-$index") }
        assertTrue(output.snapshot().length <= 64)
        assertTrue(output.snapshot().contains("line-19"))
        assertFalse(output.snapshot().contains("line-0\n"))
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

        val mapping = CodexConfigAdapter.map(
            AgentProviderMappingInput(
                agentId = AcpAgentProfileStore.CODEX_AGENT_ID,
                provider = credentials,
                model = "gpt-5.3-codex-spark",
                harnessAdapter = AcpHarnessAdapters.codex,
            )
        )
        assertEquals(CODEX_CHATGPT_HOME, mapping.environment["CODEX_HOME"])
        assertFalse(mapping.environment.containsKey("OPENAI_API_KEY"))
        assertFalse(mapping.environment.containsKey("OPENAI_BASE_URL"))
    }
}
