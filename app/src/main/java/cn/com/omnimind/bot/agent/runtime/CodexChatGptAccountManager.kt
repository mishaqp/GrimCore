package cn.com.omnimind.bot.agent.runtime

import android.content.Context
import com.ai.assistance.operit.terminal.TerminalManager
import kotlinx.coroutines.delay
import java.util.UUID

internal data class CodexDeviceFlowPrompt(
    val verificationUrl: String,
    val userCode: String,
)

internal object CodexDeviceFlowParser {
    private val ansi = Regex("\\u001B\\[[;?0-9]*[ -/]*[@-~]")
    private val url = Regex("https://[^\\s]+/codex/device")
    private val codeAfterPrompt = Regex(
        "(?is)one-time code.{0,180}?\\n\\s*([A-Z0-9][A-Z0-9-]{3,31})\\s*(?:\\n|$)"
    )

    fun parse(raw: String): CodexDeviceFlowPrompt? {
        val clean = ansi.replace(raw, "")
        val verificationUrl = url.find(clean)?.value?.trimEnd('.', ',', ';') ?: return null
        val userCode = codeAfterPrompt.find(clean)?.groupValues?.getOrNull(1)
            ?.trim()
            ?.takeIf(String::isNotEmpty)
            ?: return null
        return CodexDeviceFlowPrompt(verificationUrl, userCode)
    }

    fun safeError(raw: String): String {
        val clean = ansi.replace(raw, "")
            .lineSequence()
            .map(String::trim)
            .filter(String::isNotEmpty)
            .filterNot { it.contains("token", ignoreCase = true) }
            .filterNot { it.contains("authorization", ignoreCase = true) }
            .filterNot { it.contains("auth.json", ignoreCase = true) }
            .joinToString(" ")
            .take(320)
        return clean.ifBlank { "Codex authentication failed." }
    }
}

/**
 * Thin host bridge around the official Codex CLI authentication contract.
 * The CLI exclusively owns CODEX_HOME/auth.json. This class never reads,
 * writes, logs, copies, or returns credentials.
 */
internal class CodexChatGptAccountManager(
    context: Context,
) {
    private val appContext = context.applicationContext
    private val terminal by lazy { TerminalManager.getInstance(appContext) }

    suspend fun handle(method: String, args: Map<String, Any?>): Map<String, Any?> = when (method) {
        "account/read" -> readStatus()
        "account/login/start" -> startLogin(args)
        "account/login/cancel" -> cancelLogin(args)
        "account/logout" -> logout()
        else -> throw IllegalArgumentException("Unsupported local Codex account method: $method")
    }

    private suspend fun readStatus(): Map<String, Any?> {
        if (!isInstalled()) return status("not_installed", installed = false)
        val metadata = readMetadata()
        if (metadata.state == "waiting") {
            val output = runSafe("cat ${quote(LOG_PATH)} 2>/dev/null || true", "codex-login-read")
            CodexDeviceFlowParser.parse(output)?.let { prompt ->
                if (metadata.startedAt > 0 && nowSeconds() - metadata.startedAt >= LOGIN_TIMEOUT_SECONDS) {
                    terminate(metadata.pid)
                    writeMetadata(LoginMetadata(state = "expired"))
                    return status("expired", message = "Device code expired. Start sign-in again.")
                }
                if (metadata.pid > 0 && isProcessAlive(metadata.pid)) {
                    return status(
                        state = "waiting",
                        verificationUrl = prompt.verificationUrl,
                        userCode = prompt.userCode,
                        loginId = metadata.loginId,
                    )
                }
            }
        }
        val result = execute("codex login status", "codex-login-status", STATUS_TIMEOUT_MS)
        if (result.first == 0 && isSignedIn(result.second)) {
            writeMetadata(LoginMetadata(state = "signed_in"))
            return status("signed_in", authenticated = true)
        }
        return when (metadata.state) {
            "cancelled" -> status("cancelled")
            "expired" -> status("expired")
            "error" -> status("error", message = metadata.message)
            else -> status("signed_out")
        }
    }

    private suspend fun startLogin(args: Map<String, Any?>): Map<String, Any?> {
        val type = args["type"]?.toString()?.trim().orEmpty()
        require(type.isEmpty() || type == "chatgptDeviceCode" || type == "chatgpt") {
            "Codex ChatGPT account mode supports only the official device flow."
        }
        if (!isInstalled()) return status("not_installed", installed = false)
        readStatus().takeIf { it["authenticated"] == true }?.let { return it }
        cancelCurrentLogin(markCancelled = false)
        val loginId = UUID.randomUUID().toString()
        val command = """
            mkdir -p ${quote(AgentRuntimeDefaults.CODEX_HOME)}
            chmod 700 ${quote(AgentRuntimeDefaults.CODEX_HOME)}
            rm -f ${quote(LOG_PATH)}
            (CODEX_HOME=${quote(AgentRuntimeDefaults.CODEX_HOME)} codex login --device-auth >${quote(LOG_PATH)} 2>&1; echo \\$? >${quote(EXIT_PATH)}) </dev/null >/dev/null 2>&1 &
            echo \\$!
        """.trimIndent()
        val result = execute(command, "codex-login-start", START_TIMEOUT_MS)
        val pid = result.second.lineSequence().map(String::trim)
            .firstOrNull { it.toLongOrNull() != null }?.toLongOrNull() ?: 0L
        if (result.first != 0 || pid <= 0) {
            val message = CodexDeviceFlowParser.safeError(result.second)
            writeMetadata(LoginMetadata(state = "error", message = message))
            return status("error", message = message)
        }
        val metadata = LoginMetadata(
            state = "waiting",
            loginId = loginId,
            pid = pid,
            startedAt = nowSeconds(),
        )
        writeMetadata(metadata)
        repeat(30) {
            val output = runSafe("cat ${quote(LOG_PATH)} 2>/dev/null || true", "codex-login-prompt")
            CodexDeviceFlowParser.parse(output)?.let { prompt ->
                return status(
                    state = "waiting",
                    verificationUrl = prompt.verificationUrl,
                    userCode = prompt.userCode,
                    loginId = loginId,
                )
            }
            if (!isProcessAlive(pid)) {
                val final = readStatus()
                if (final["authenticated"] == true) return final
                val message = CodexDeviceFlowParser.safeError(output)
                writeMetadata(LoginMetadata(state = "error", message = message))
                return status("error", message = message)
            }
            delay(200)
        }
        return status("waiting", loginId = loginId)
    }

    private suspend fun cancelLogin(args: Map<String, Any?>): Map<String, Any?> {
        val requested = args["loginId"]?.toString()?.trim().orEmpty()
        val current = readMetadata()
        if (requested.isNotEmpty() && current.loginId.isNotEmpty() && requested != current.loginId) {
            return status("cancelled")
        }
        cancelCurrentLogin(markCancelled = true)
        return status("cancelled")
    }

    private suspend fun logout(): Map<String, Any?> {
        cancelCurrentLogin(markCancelled = false)
        if (!isInstalled()) return status("not_installed", installed = false)
        val result = execute("codex logout", "codex-logout", LOGOUT_TIMEOUT_MS)
        clearTransientFiles()
        return if (result.first == 0) {
            status("signed_out")
        } else {
            status("error", message = CodexDeviceFlowParser.safeError(result.second))
        }
    }

    private suspend fun cancelCurrentLogin(markCancelled: Boolean) {
        val metadata = readMetadata()
        terminate(metadata.pid)
        clearTransientFiles()
        writeMetadata(LoginMetadata(state = if (markCancelled) "cancelled" else "signed_out"))
    }

    private suspend fun terminate(pid: Long) {
        if (pid <= 0) return
        runSafe("kill $pid 2>/dev/null || true", "codex-login-cancel")
    }

    private suspend fun isInstalled(): Boolean =
        execute("command -v codex >/dev/null 2>&1", "codex-install-status", STATUS_TIMEOUT_MS).first == 0

    private suspend fun isProcessAlive(pid: Long): Boolean =
        pid > 0 && execute("kill -0 $pid 2>/dev/null", "codex-login-alive", STATUS_TIMEOUT_MS).first == 0

    private fun isSignedIn(output: String): Boolean {
        val normalized = output.lowercase()
        return normalized.contains("logged in") ||
            normalized.contains("signed in") ||
            normalized.contains("chatgpt") && !normalized.contains("not logged")
    }

    private fun status(
        state: String,
        installed: Boolean = true,
        authenticated: Boolean = false,
        verificationUrl: String? = null,
        userCode: String? = null,
        loginId: String? = null,
        message: String? = null,
    ): Map<String, Any?> = linkedMapOf<String, Any?>(
        "agentId" to AcpAgentProfileStore.CODEX_AGENT_ID,
        "authMode" to "codex_chatgpt",
        "state" to state,
        "installed" to installed,
        "authenticated" to authenticated,
    ).apply {
        verificationUrl?.let { put("verificationUrl", it) }
        userCode?.let { put("userCode", it) }
        loginId?.let { put("loginId", it) }
        message?.takeIf(String::isNotBlank)?.let { put("message", it) }
    }

    private suspend fun execute(command: String, key: String, timeoutMs: Long): Pair<Int, String> {
        val wrapped = "$PATH_PREFIX CODEX_HOME=${quote(AgentRuntimeDefaults.CODEX_HOME)} $command"
        val result = terminal.executeHiddenCommand(
            command = wrapped,
            executorKey = key,
            timeoutMs = timeoutMs,
        )
        return result.exitCode to result.output
    }

    private suspend fun runSafe(command: String, key: String): String =
        runCatching { execute(command, key, STATUS_TIMEOUT_MS).second }.getOrDefault("")

    private suspend fun clearTransientFiles() {
        runSafe("rm -f ${quote(LOG_PATH)} ${quote(EXIT_PATH)}", "codex-login-cleanup")
    }

    private suspend fun readMetadata(): LoginMetadata {
        val raw = runSafe("cat ${quote(META_PATH)} 2>/dev/null || true", "codex-login-meta-read")
        val values = raw.lineSequence().mapNotNull { line ->
            val index = line.indexOf('=')
            if (index <= 0) null else line.substring(0, index) to line.substring(index + 1)
        }.toMap()
        return LoginMetadata(
            state = values["state"].orEmpty().ifBlank { "signed_out" },
            loginId = values["login_id"].orEmpty(),
            pid = values["pid"]?.toLongOrNull() ?: 0L,
            startedAt = values["started_at"]?.toLongOrNull() ?: 0L,
            message = values["message"].orEmpty().take(320),
        )
    }

    private suspend fun writeMetadata(metadata: LoginMetadata) {
        val safeMessage = metadata.message.replace('\n', ' ').replace('\r', ' ').take(320)
        val content = buildString {
            append("state=").append(metadata.state).append('\n')
            append("login_id=").append(metadata.loginId).append('\n')
            append("pid=").append(metadata.pid).append('\n')
            append("started_at=").append(metadata.startedAt).append('\n')
            append("message=").append(safeMessage).append('\n')
        }
        val command = "mkdir -p ${quote(AgentRuntimeDefaults.CODEX_HOME)}; " +
            "printf %s ${quote(content)} > ${quote(META_PATH)}; chmod 600 ${quote(META_PATH)}"
        runSafe(command, "codex-login-meta-write")
    }

    private fun quote(value: String): String = "'" + value.replace("'", "'\\''") + "'"
    private fun nowSeconds(): Long = System.currentTimeMillis() / 1000L

    private data class LoginMetadata(
        val state: String,
        val loginId: String = "",
        val pid: Long = 0L,
        val startedAt: Long = 0L,
        val message: String = "",
    )

    private companion object {
        private const val PATH_PREFIX = "PATH=\"/root/.npm-global/bin:\\$PATH\"; export PATH;"
        private const val LOGIN_TIMEOUT_SECONDS = 15L * 60L
        private const val STATUS_TIMEOUT_MS = 15_000L
        private const val START_TIMEOUT_MS = 10_000L
        private const val LOGOUT_TIMEOUT_MS = 30_000L
        private const val META_PATH = "${AgentRuntimeDefaults.CODEX_HOME}/.grimcore-login-state"
        private const val LOG_PATH = "${AgentRuntimeDefaults.CODEX_HOME}/.grimcore-login-output"
        private const val EXIT_PATH = "${AgentRuntimeDefaults.CODEX_HOME}/.grimcore-login-exit"
    }
}
