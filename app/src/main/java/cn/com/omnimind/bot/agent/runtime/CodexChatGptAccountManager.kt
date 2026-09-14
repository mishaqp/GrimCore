package cn.com.omnimind.bot.agent.runtime

import android.content.Context
import com.ai.assistance.operit.terminal.TerminalManager
import com.ai.assistance.operit.terminal.isExpectedHiddenExecReaderTermination
import com.ai.assistance.operit.terminal.terminateHiddenExecProcess
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeoutOrNull
import java.nio.charset.StandardCharsets
import java.util.UUID

internal const val CODEX_CHATGPT_HOME = "/root/.codex-chatgpt"
internal const val CODEX_DEVICE_LOGIN_COMMAND = "exec codex login --device-auth"

internal fun buildCodexDeviceLoginShellCommand(): String =
    "PATH=\"/root/.npm-global/bin:\$PATH\"; export PATH; " +
        "unset OPENAI_API_KEY OPENAI_BASE_URL; " +
        "mkdir -p '$CODEX_CHATGPT_HOME' && chmod 700 '$CODEX_CHATGPT_HOME' && " +
        CODEX_DEVICE_LOGIN_COMMAND

private val CODEX_ANSI = Regex("\\u001B\\[[;?0-9]*[ -/]*[@-~]")

internal data class CodexDeviceFlowPrompt(
    val verificationUrl: String,
    val userCode: String,
)

internal object CodexDeviceFlowParser {
    private val url = Regex("https://[^\\s]+/codex/device")
    private val codeAfterPrompt = Regex(
        "(?is)one-time code.{0,180}?\\n\\s*([A-Z0-9][A-Z0-9-]{3,31})\\s*(?:\\n|$)"
    )
    private val secretAssignment = Regex(
        "(?i)\\b(?:access_token|refresh_token|id_token|api[_-]?key)\\s*[:=]"
    )
    private val bearerSecret = Regex("(?i)\\bBearer\\s+[A-Za-z0-9._~+/=-]+")
    private val openAiKey = Regex("\\bsk-[A-Za-z0-9_-]{8,}\\b")

    fun parse(raw: String): CodexDeviceFlowPrompt? {
        val clean = CODEX_ANSI.replace(raw, "")
        val verificationUrl = url.find(clean)?.value?.trimEnd('.', ',', ';') ?: return null
        val userCode = codeAfterPrompt.find(clean)?.groupValues?.getOrNull(1)
            ?.trim()
            ?.takeIf(String::isNotEmpty)
            ?: return null
        return CodexDeviceFlowPrompt(verificationUrl, userCode)
    }

    fun safeError(raw: String): String {
        val clean = CODEX_ANSI.replace(raw, "")
            .lineSequence()
            .map(String::trim)
            .filter(String::isNotEmpty)
            .filterNot { secretAssignment.containsMatchIn(it) }
            .filterNot { it.contains("auth.json", ignoreCase = true) }
            .map { bearerSecret.replace(it, "Bearer [redacted]") }
            .map { openAiKey.replace(it, "[redacted]") }
            .toList()
            .takeLast(8)
            .joinToString(" ")
            .takeLast(320)
        return clean.ifBlank { "Codex authentication failed." }
    }
}

internal fun isChatGptLoginStatus(exitCode: Int, raw: String): Boolean =
    exitCode == 0 && CODEX_ANSI.replace(raw, "").lineSequence().any {
        it.trim().equals("Logged in using ChatGPT", ignoreCase = true)
    }

internal class BoundedCodexLoginOutput(
    private val maxChars: Int = 16_384,
) {
    private val buffer = StringBuilder()

    @Synchronized
    fun appendLine(line: String) {
        buffer.append(line.take(2_048)).append('\n')
        val overflow = buffer.length - maxChars
        if (overflow > 0) buffer.delete(0, overflow)
    }

    @Synchronized
    fun snapshot(): String = buffer.toString()
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
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private val accountMutex = Mutex()
    private var activeLogin: ActiveLogin? = null

    suspend fun handle(
        method: String,
        args: Map<String, Any?>,
    ): Map<String, Any?> = accountMutex.withLock {
        when (method) {
            "account/read" -> readStatus()
            "account/login/start" -> startLogin(args)
            "account/login/cancel" -> cancelLogin(args)
            "account/logout" -> logout()
            else -> throw IllegalArgumentException(
                "Unsupported local Codex account method: $method"
            )
        }
    }

    private suspend fun readStatus(): Map<String, Any?> {
        if (!isInstalled()) return status("not_installed", installed = false)

        activeLogin?.let { login ->
            if (nowSeconds() - login.startedAt >= LOGIN_TIMEOUT_SECONDS) {
                stopActiveLogin(login)
                writeMetadata(LoginMetadata(state = "expired"))
                return status(
                    state = "expired",
                    message = "Device code expired. Start sign-in again.",
                )
            }
            if (login.process.isAlive) {
                return waitingStatus(login)
            }
            return finishExitedLogin(login)
        }

        val metadata = readMetadata()
        val result = execute("codex login status", "codex-login-status", STATUS_TIMEOUT_MS)
        if (isChatGptLoginStatus(result.first, result.second)) {
            writeMetadata(LoginMetadata(state = "signed_in"))
            return status("signed_in", authenticated = true)
        }

        return when (metadata.state) {
            "cancelled" -> status("cancelled")
            "expired" -> status("expired", message = metadata.message)
            "error" -> status("error", message = metadata.message)
            "waiting" -> {
                val message = "Sign-in was interrupted. Start sign-in again."
                writeMetadata(LoginMetadata(state = "error", message = message))
                status("error", message = message)
            }
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
        val output = BoundedCodexLoginOutput()
        val process = try {
            terminal.startLongLivedAlpineProcess(
                command = buildCodexDeviceLoginShellCommand(),
                executorKey = "codex-login-$loginId",
                extraEnvironment = mapOf(
                    "CODEX_HOME" to CODEX_CHATGPT_HOME,
                    "OMNIBOT_HEADLESS" to "1",
                    "OMNIBOT_DISABLE_PROOT_LINK2SYMLINK" to "1",
                ),
                redirectErrorStream = true,
            )
        } catch (error: CancellationException) {
            throw error
        } catch (error: Throwable) {
            val message = CodexDeviceFlowParser.safeError(error.message.orEmpty())
            writeMetadata(LoginMetadata(state = "error", message = message))
            return status("error", message = message)
        }

        val readerJob = scope.launch {
            try {
                process.inputStream
                    .bufferedReader(StandardCharsets.UTF_8)
                    .useLines { lines -> lines.forEach(output::appendLine) }
            } catch (error: CancellationException) {
                throw error
            } catch (error: Throwable) {
                if (!isExpectedHiddenExecReaderTermination(error)) {
                    output.appendLine(error.message ?: "Codex output reader failed.")
                }
            }
        }
        val login = ActiveLogin(
            loginId = loginId,
            process = process,
            readerJob = readerJob,
            output = output,
            startedAt = nowSeconds(),
        )
        activeLogin = login
        writeMetadata(
            LoginMetadata(
                state = "waiting",
                loginId = loginId,
                startedAt = login.startedAt,
            )
        )

        repeat(LOGIN_PROMPT_POLLS) {
            CodexDeviceFlowParser.parse(output.snapshot())?.let { prompt ->
                return status(
                    state = "waiting",
                    verificationUrl = prompt.verificationUrl,
                    userCode = prompt.userCode,
                    loginId = loginId,
                )
            }
            if (!process.isAlive) return finishExitedLogin(login)
            delay(LOGIN_PROMPT_POLL_MS)
        }
        return status("waiting", loginId = loginId)
    }

    private suspend fun cancelLogin(args: Map<String, Any?>): Map<String, Any?> {
        val requested = args["loginId"]?.toString()?.trim().orEmpty()
        val currentLoginId = activeLogin?.loginId ?: readMetadata().loginId
        if (requested.isNotEmpty() && currentLoginId.isNotEmpty() && requested != currentLoginId) {
            return status("cancelled")
        }
        cancelCurrentLogin(markCancelled = true)
        return status("cancelled")
    }

    private suspend fun logout(): Map<String, Any?> {
        stopActiveLogin()
        if (!isInstalled()) return status("not_installed", installed = false)

        val result = execute("codex logout", "codex-logout", LOGOUT_TIMEOUT_MS)
        return if (result.first == 0) {
            writeMetadata(LoginMetadata(state = "signed_out"))
            status("signed_out")
        } else {
            val message = CodexDeviceFlowParser.safeError(result.second)
            writeMetadata(LoginMetadata(state = "error", message = message))
            status("error", message = message)
        }
    }

    private fun waitingStatus(login: ActiveLogin): Map<String, Any?> {
        val prompt = CodexDeviceFlowParser.parse(login.output.snapshot())
        return status(
            state = "waiting",
            verificationUrl = prompt?.verificationUrl,
            userCode = prompt?.userCode,
            loginId = login.loginId,
        )
    }

    private suspend fun finishExitedLogin(login: ActiveLogin): Map<String, Any?> {
        drainReader(login)
        if (activeLogin === login) activeLogin = null

        val result = execute("codex login status", "codex-login-status", STATUS_TIMEOUT_MS)
        if (isChatGptLoginStatus(result.first, result.second)) {
            writeMetadata(LoginMetadata(state = "signed_in"))
            return status("signed_in", authenticated = true)
        }

        val message = CodexDeviceFlowParser.safeError(
            listOf(login.output.snapshot(), result.second)
                .filter(String::isNotBlank)
                .joinToString("\n")
        )
        writeMetadata(LoginMetadata(state = "error", message = message))
        return status("error", message = message)
    }

    private suspend fun cancelCurrentLogin(markCancelled: Boolean) {
        stopActiveLogin()
        writeMetadata(
            LoginMetadata(state = if (markCancelled) "cancelled" else "signed_out")
        )
    }

    private suspend fun stopActiveLogin(expected: ActiveLogin? = null) {
        val login = activeLogin ?: return
        if (expected != null && activeLogin !== expected) return
        activeLogin = null
        withContext(Dispatchers.IO) {
            terminateHiddenExecProcess(login.process)
        }
        drainReader(login)
    }

    private suspend fun drainReader(login: ActiveLogin) {
        val drained = withTimeoutOrNull(READER_DRAIN_TIMEOUT_MS) {
            login.readerJob.join()
            true
        } ?: false
        if (!drained) {
            runCatching { login.process.inputStream.close() }
            login.readerJob.cancel()
        }
    }

    private suspend fun isInstalled(): Boolean =
        execute(
            "command -v codex >/dev/null 2>&1 && command -v codex-acp >/dev/null 2>&1",
            "codex-install-status",
            STATUS_TIMEOUT_MS,
        ).first == 0

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
        val wrapped = "$PATH_PREFIX " +
            "unset OPENAI_API_KEY OPENAI_BASE_URL; " +
            "export CODEX_HOME=${quote(CODEX_CHATGPT_HOME)}; " +
            "mkdir -p ${quote(CODEX_CHATGPT_HOME)}; " +
            "chmod 700 ${quote(CODEX_CHATGPT_HOME)}; " +
            command
        val result = terminal.executeHiddenCommand(
            command = wrapped,
            executorKey = key,
            timeoutMs = timeoutMs,
        )
        return result.exitCode to result.output
    }

    private suspend fun runSafe(command: String, key: String): String =
        runCatching { execute(command, key, STATUS_TIMEOUT_MS).second }.getOrDefault("")

    private suspend fun readMetadata(): LoginMetadata {
        val raw = runSafe("cat ${quote(META_PATH)} 2>/dev/null || true", "codex-login-meta-read")
        val values = raw.lineSequence().mapNotNull { line ->
            val index = line.indexOf('=')
            if (index <= 0) null else line.substring(0, index) to line.substring(index + 1)
        }.toMap()
        return LoginMetadata(
            state = values["state"].orEmpty().ifBlank { "signed_out" },
            loginId = values["login_id"].orEmpty(),
            startedAt = values["started_at"]?.toLongOrNull() ?: 0L,
            message = values["message"].orEmpty().take(320),
        )
    }

    private suspend fun writeMetadata(metadata: LoginMetadata) {
        val safeMessage = metadata.message.replace('\n', ' ').replace('\r', ' ').take(320)
        val content = buildString {
            append("state=").append(metadata.state).append('\n')
            append("login_id=").append(metadata.loginId).append('\n')
            append("started_at=").append(metadata.startedAt).append('\n')
            append("message=").append(safeMessage).append('\n')
        }
        val command = "printf %s ${quote(content)} > ${quote(META_PATH)}; " +
            "chmod 600 ${quote(META_PATH)}"
        runSafe(command, "codex-login-meta-write")
    }

    private fun quote(value: String): String = "'" + value.replace("'", "'\\''") + "'"
    private fun nowSeconds(): Long = System.currentTimeMillis() / 1000L

    private data class ActiveLogin(
        val loginId: String,
        val process: Process,
        val readerJob: Job,
        val output: BoundedCodexLoginOutput,
        val startedAt: Long,
    )

    private data class LoginMetadata(
        val state: String,
        val loginId: String = "",
        val startedAt: Long = 0L,
        val message: String = "",
    )

    private companion object {
        private const val PATH_PREFIX = "PATH=\"/root/.npm-global/bin:\$PATH\"; export PATH;"
        private const val LOGIN_TIMEOUT_SECONDS = 15L * 60L
        private const val LOGIN_PROMPT_POLLS = 30
        private const val LOGIN_PROMPT_POLL_MS = 200L
        private const val READER_DRAIN_TIMEOUT_MS = 1_000L
        private const val STATUS_TIMEOUT_MS = 15_000L
        private const val LOGOUT_TIMEOUT_MS = 30_000L
        private const val META_PATH = "/root/.codex-chatgpt/.grimcore-login-state"
    }
}
