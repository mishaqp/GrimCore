#!/usr/bin/env python3
"""Apply the Codex (ChatGPT) account-mode backend patch.

This script is intentionally executed only by GitHub Actions on the feature
branch. It is idempotent and fails closed when an expected upstream anchor has
changed, so it cannot silently corrupt a concurrent localization change.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, value: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value, encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    value = read(path)
    count = value.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one anchor, found {count}: {old[:120]!r}")
    write(path, value.replace(old, new, 1))


def regex_once(path: str, pattern: str, replacement: str, *, flags: int = 0) -> None:
    value = read(path)
    next_value, count = re.subn(pattern, replacement, value, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f"{path}: regex anchor not found: {pattern[:140]!r}")
    write(path, next_value)


MODELS = "baselib/src/main/java/cn/com/omnimind/baselib/llm/ModelProviderModels.kt"
models = read(MODELS)
if "object ModelProviderAuthMode" not in models:
    models = models.replace(
        "import com.google.gson.annotations.SerializedName\n\n",
        "import com.google.gson.annotations.SerializedName\n\n"
        "object ModelProviderAuthMode {\n"
        "    const val API_KEY = \"api_key\"\n"
        "    const val CODEX_CHATGPT = \"codex_chatgpt\"\n\n"
        "    fun fromSourceType(sourceType: String?): String =\n"
        "        if (sourceType?.trim()?.lowercase() == CODEX_CHATGPT) {\n"
        "            CODEX_CHATGPT\n"
        "        } else {\n"
        "            API_KEY\n"
        "        }\n"
        "}\n\n"
        "const val CODEX_CHATGPT_MODEL_ID = \"gpt-5.3-codex-spark\"\n\n",
        1,
    )
    models = models.replace(
        "    fun isConfigured(): Boolean = baseUrl.isNotBlank()\n}\n\ndata class ModelProviderProfile(",
        "    fun isConfigured(): Boolean = baseUrl.isNotBlank()\n"
        "    fun isCodexChatGptAccount(): Boolean =\n"
        "        ModelProviderAuthMode.fromSourceType(providerType) == ModelProviderAuthMode.CODEX_CHATGPT\n"
        "}\n\n"
        "data class ModelProviderProfile(",
        1,
    )
    models = models.replace(
        "    fun isConfigured(): Boolean = baseUrl.isNotBlank()\n}\n\n/**\n * Wire capabilities",
        "    fun isConfigured(): Boolean = baseUrl.isNotBlank()\n"
        "    fun isCodexChatGptAccount(): Boolean =\n"
        "        ModelProviderAuthMode.fromSourceType(sourceType) == ModelProviderAuthMode.CODEX_CHATGPT\n"
        "}\n\n"
        "/**\n * Wire capabilities",
        1,
    )
    write(MODELS, models)

STORE = "baselib/src/main/java/cn/com/omnimind/baselib/llm/ModelProviderConfigStore.kt"
store = read(STORE)
if "normalizedSourceType == ModelProviderAuthMode.CODEX_CHATGPT" not in store:
    store = store.replace(
        "    private fun normalizeSourceType(\n"
        "        sourceType: String?,\n"
        "        profileId: String?,\n"
        "        baseUrl: String?\n"
        "    ): String {\n"
        "        return OfficialProviderRegistry.normalizeSourceType(\n",
        "    private fun normalizeSourceType(\n"
        "        sourceType: String?,\n"
        "        profileId: String?,\n"
        "        baseUrl: String?\n"
        "    ): String {\n"
        "        val normalizedSourceType = sourceType?.trim()?.lowercase().orEmpty()\n"
        "        if (normalizedSourceType == ModelProviderAuthMode.CODEX_CHATGPT) {\n"
        "            return ModelProviderAuthMode.CODEX_CHATGPT\n"
        "        }\n"
        "        return OfficialProviderRegistry.normalizeSourceType(\n",
        1,
    )
    store = store.replace(
        "        val normalizedRequested = requestedSourceType?.trim()?.lowercase().orEmpty()\n"
        "        if (normalizedRequested == \"custom\") {\n",
        "        val normalizedRequested = requestedSourceType?.trim()?.lowercase().orEmpty()\n"
        "        if (normalizedRequested == ModelProviderAuthMode.CODEX_CHATGPT) {\n"
        "            return ModelProviderAuthMode.CODEX_CHATGPT\n"
        "        }\n"
        "        if (normalizedRequested == \"custom\") {\n",
        1,
    )
    store = store.replace(
        "    private fun enforceCredentialTransport(profile: ModelProviderProfile): ModelProviderProfile {\n"
        "        val endpoint = stripDirectRequestUrlMarker(profile.baseUrl)\n",
        "    private fun enforceCredentialTransport(profile: ModelProviderProfile): ModelProviderProfile {\n"
        "        if (profile.isCodexChatGptAccount()) {\n"
        "            return profile.copy(\n"
        "                baseUrl = \"\",\n"
        "                apiKey = \"\",\n"
        "                customHeaders = emptyMap(),\n"
        "                sourceType = ModelProviderAuthMode.CODEX_CHATGPT,\n"
        "                protocolType = \"codex_acp\",\n"
        "                wireApi = OpenAiWireApi.RESPONSES,\n"
        "            )\n"
        "        }\n"
        "        val endpoint = stripDirectRequestUrlMarker(profile.baseUrl)\n",
        1,
    )
    # Enforce account-mode invariants before the profile is persisted. Legacy
    # API-key profiles retain the exact old branch and normalization behavior.
    old = """        val nextRevision = (existingProfile?.revision ?: 0L) + 1L
        val nextProfile = ModelProviderProfile(
            id = normalizedId,
            name = sanitizedName,
            baseUrl = normalizedBaseUrl,
            apiKey = apiKey.trim(),
            customHeaders = normalizedCustomHeaders,
            sourceType = resolveSourceTypeForSave(
                requestedSourceType = sourceType,
                profileId = normalizedId,
                baseUrl = baseUrl,
                existingSourceType = current.getOrNull(currentIndex)?.sourceType
            ),
            protocolType = normalizedProtocolType,
            wireApi = normalizedWireApi,
            revision = nextRevision,
        )
"""
    new = """        val nextRevision = (existingProfile?.revision ?: 0L) + 1L
        val resolvedSourceType = resolveSourceTypeForSave(
            requestedSourceType = sourceType,
            profileId = normalizedId,
            baseUrl = baseUrl,
            existingSourceType = current.getOrNull(currentIndex)?.sourceType
        )
        val isCodexChatGptAccount =
            resolvedSourceType == ModelProviderAuthMode.CODEX_CHATGPT
        val nextProfile = ModelProviderProfile(
            id = normalizedId,
            name = sanitizedName,
            baseUrl = if (isCodexChatGptAccount) "" else normalizedBaseUrl,
            apiKey = if (isCodexChatGptAccount) "" else apiKey.trim(),
            customHeaders = if (isCodexChatGptAccount) emptyMap() else normalizedCustomHeaders,
            sourceType = resolvedSourceType,
            protocolType = if (isCodexChatGptAccount) "codex_acp" else normalizedProtocolType,
            wireApi = if (isCodexChatGptAccount) OpenAiWireApi.RESPONSES else normalizedWireApi,
            revision = nextRevision,
        )
"""
    if old not in store:
        raise RuntimeError("ModelProviderConfigStore.kt: saveProfile anchor changed")
    store = store.replace(old, new, 1)
    write(STORE, store)

DISPATCH = "app/src/main/java/cn/com/omnimind/bot/agent/runtime/AgentDispatchConfiguration.kt"
write(DISPATCH, '''package cn.com.omnimind.bot.agent.runtime

import cn.com.omnimind.baselib.llm.CODEX_CHATGPT_MODEL_ID
import cn.com.omnimind.baselib.llm.ModelProviderAuthMode
import cn.com.omnimind.baselib.llm.ModelProviderConfigStore
import cn.com.omnimind.baselib.llm.ModelProviderProfile
import cn.com.omnimind.baselib.llm.SceneModelBindingStore
import cn.com.omnimind.baselib.llm.isCodexChatGptAccount

/**
 * Read-only view of the Provider and model selected for Dispatch execution.
 *
 * ACP adapters and out-of-band plugin capabilities must resolve this state in
 * exactly the same way. Keeping the lookup here prevents a local runtime from
 * silently reviving a stale Provider or choosing its own default model.
 */
internal object AgentDispatchConfiguration {
    private const val DISPATCH_SCENE_ID = "scene.dispatch.model"

    fun providerProfile(): ModelProviderProfile? = runCatching {
        val binding = SceneModelBindingStore.getBinding(DISPATCH_SCENE_ID)
        val configuredProfile = binding
            ?.providerProfileId
            ?.let(ModelProviderConfigStore::getProfile)
        resolveDispatchAgentProviderProfile(
            boundProviderProfileId = binding?.providerProfileId,
            configuredProfile = configuredProfile,
            editingProfile = ModelProviderConfigStore.getEditingProfile(),
        )
    }.getOrNull()

    fun providerCredentials(): AgentProviderCredentials? = providerProfile()?.let { profile ->
        if (profile.isCodexChatGptAccount()) {
            return@let AgentProviderCredentials(
                baseUrl = "",
                apiKey = "",
                wireApi = profile.wireApi,
                customHeaders = emptyMap(),
                protocolType = "codex_acp",
                authMode = ModelProviderAuthMode.CODEX_CHATGPT,
                supportsNamespaceTools = false,
            ).normalized()
        }
        val apiKey = resolveAgentProviderApiKey(profile) ?: return@let null
        AgentProviderCredentials(
            baseUrl = profile.baseUrl,
            apiKey = apiKey,
            wireApi = profile.wireApi,
            customHeaders = profile.customHeaders,
            protocolType = profile.protocolType,
            authMode = ModelProviderAuthMode.API_KEY,
            supportsNamespaceTools = false,
        ).normalized()
    }

    fun modelId(): String? = runCatching {
        val binding = SceneModelBindingStore.getBinding(DISPATCH_SCENE_ID)
        val profile = binding?.let {
            resolveAgentProviderProfile(
                boundProviderProfileId = it.providerProfileId,
                configuredProfile = ModelProviderConfigStore.getProfile(it.providerProfileId),
            )
        } ?: providerProfile() ?: return@runCatching null
        if (profile.isCodexChatGptAccount()) {
            return@runCatching binding?.modelId
                ?.trim()
                ?.takeIf(String::isNotEmpty)
                ?: CODEX_CHATGPT_MODEL_ID
        }
        if (profile.baseUrl.isBlank()) return@runCatching null
        resolveSharedAgentModel(
            boundProviderProfileId = binding?.providerProfileId,
            boundModel = binding?.modelId,
        )
    }.getOrNull()
}
''')

CONFIG_ADAPTERS = "app/src/main/java/cn/com/omnimind/bot/agent/runtime/AgentConfigAdapters.kt"
adapters = read(CONFIG_ADAPTERS)
if "val authMode: String = ModelProviderAuthMode.API_KEY" not in adapters:
    adapters = adapters.replace(
        "import cn.com.omnimind.baselib.llm.OpenAiWireApi\n",
        "import cn.com.omnimind.baselib.llm.OpenAiWireApi\n"
        "import cn.com.omnimind.baselib.llm.ModelProviderAuthMode\n",
        1,
    )
    adapters = adapters.replace(
        "    val protocolType: String = \"openai_compatible\",\n"
        "    /** First-party Responses endpoints understand Codex's namespace tools. */\n",
        "    val protocolType: String = \"openai_compatible\",\n"
        "    val authMode: String = ModelProviderAuthMode.API_KEY,\n"
        "    /** First-party Responses endpoints understand Codex's namespace tools. */\n",
        1,
    )
    old_normalized = '''internal fun AgentProviderCredentials.normalized(): AgentProviderCredentials {
    val normalizedBaseUrl = baseUrl.trim()
    require(normalizedBaseUrl.isNotEmpty()) { "Provider base URL is empty." }
    require(!normalizedBaseUrl.any(Char::isWhitespace)) {
        "Provider base URL contains whitespace."
    }
    val normalizedHeaders = ProviderCustomHeaderUtils
        .sanitizeCustomHeaders(customHeaders)
        .mapValues { (_, value) -> value.trim() }
    return copy(
        baseUrl = normalizedBaseUrl,
        apiKey = apiKey.trim(),
        wireApi = OpenAiWireApi.normalize(wireApi),
        customHeaders = normalizedHeaders,
        protocolType = protocolType.trim().lowercase().ifEmpty { "openai_compatible" },
    )
}
'''
    new_normalized = '''internal fun AgentProviderCredentials.normalized(): AgentProviderCredentials {
    val normalizedAuthMode = if (
        authMode.trim().lowercase() == ModelProviderAuthMode.CODEX_CHATGPT
    ) {
        ModelProviderAuthMode.CODEX_CHATGPT
    } else {
        ModelProviderAuthMode.API_KEY
    }
    if (normalizedAuthMode == ModelProviderAuthMode.CODEX_CHATGPT) {
        return copy(
            baseUrl = "",
            apiKey = "",
            wireApi = OpenAiWireApi.RESPONSES,
            customHeaders = emptyMap(),
            protocolType = "codex_acp",
            authMode = normalizedAuthMode,
        )
    }
    val normalizedBaseUrl = baseUrl.trim()
    require(normalizedBaseUrl.isNotEmpty()) { "Provider base URL is empty." }
    require(!normalizedBaseUrl.any(Char::isWhitespace)) {
        "Provider base URL contains whitespace."
    }
    val normalizedHeaders = ProviderCustomHeaderUtils
        .sanitizeCustomHeaders(customHeaders)
        .mapValues { (_, value) -> value.trim() }
    return copy(
        baseUrl = normalizedBaseUrl,
        apiKey = apiKey.trim(),
        wireApi = OpenAiWireApi.normalize(wireApi),
        customHeaders = normalizedHeaders,
        protocolType = protocolType.trim().lowercase().ifEmpty { "openai_compatible" },
        authMode = normalizedAuthMode,
    )
}
'''
    if old_normalized not in adapters:
        raise RuntimeError("AgentConfigAdapters.kt: normalization anchor changed")
    adapters = adapters.replace(old_normalized, new_normalized, 1)
    write(CONFIG_ADAPTERS, adapters)

HARNESS = "app/src/main/java/cn/com/omnimind/bot/agent/runtime/AcpHarnessConfigAdapters.kt"
harness = read(HARNESS)
if "isChatGptAccount(input)" not in harness:
    harness = harness.replace(
        "import cn.com.omnimind.baselib.llm.OpenAiWireApi\n",
        "import cn.com.omnimind.baselib.llm.OpenAiWireApi\n"
        "import cn.com.omnimind.baselib.llm.ModelProviderAuthMode\n",
        1,
    )
    start = harness.index("internal object CodexConfigAdapter : AgentConfigAdapter {")
    end = harness.index("\ninternal object ClaudeCodeConfigAdapter", start)
    codex_block = '''internal object CodexConfigAdapter : AgentConfigAdapter {
    private fun isChatGptAccount(input: AgentProviderMappingInput): Boolean =
        input.provider?.authMode == ModelProviderAuthMode.CODEX_CHATGPT

    override suspend fun readConfig(
        input: AgentProviderMappingInput,
        access: AgentConfigFileAccess,
    ): Map<String, Any?> {
        if (isChatGptAccount(input)) {
            return linkedMapOf(
                "agentId" to input.agentId,
                "kind" to "codex_chatgpt",
                "model" to input.model.orEmpty(),
                "authMode" to ModelProviderAuthMode.CODEX_CHATGPT,
            )
        }
        val configToml = access.read(
            CODEX_CONFIG_TOML_PATH,
            "codex-agent-config-read",
        )
        val authJson = access.read(
            CODEX_AUTH_JSON_PATH,
            "codex-agent-auth-read",
        )
        val provider = input.provider
        return linkedMapOf(
            "agentId" to input.agentId,
            "kind" to "codex",
            "configPath" to CODEX_CONFIG_TOML_DISPLAY_PATH,
            "authPath" to CODEX_AUTH_JSON_DISPLAY_PATH,
            "baseUrl" to (provider?.baseUrl
                ?: extractTomlString(configToml, "base_url").orEmpty()),
            "model" to input.model.orEmpty(),
            "apiKey" to extractOpenAiApiKey(authJson).orEmpty(),
            "authMode" to ModelProviderAuthMode.API_KEY,
        )
    }

    override fun directConfigWrites(
        input: AgentProviderMappingInput,
        args: Map<String, Any?>,
        providerModels: List<ProviderModelOption>,
    ): List<AgentConfigWrite> {
        if (isChatGptAccount(input)) return emptyList()
        val baseUrl = args.agentConfigStringValue("baseUrl")
            ?: throw IllegalArgumentException("Base URL is required.")
        val model = args.agentConfigStringValue("model")
            ?: throw IllegalArgumentException("Model ID is required.")
        val apiKey = args.agentConfigStringValue("apiKey")
            ?: throw IllegalArgumentException("API Key is required.")
        val resolvedModel = resolveAcpLaunchModel(
            providerModelIds = providerModels.map(ProviderModelOption::id),
            boundModel = model,
        ) ?: throw IllegalArgumentException(
            "Model must be selected from the current Provider /models response."
        )
        val provider = input.provider ?: throw IllegalArgumentException(
            "Provider settings are required for Codex configuration."
        )
        val mapping = map(input.copy(
            provider = provider.copy(baseUrl = baseUrl, apiKey = apiKey),
            model = resolvedModel,
        ))
        return listOf(
            AgentConfigWrite(
                path = CODEX_CONFIG_TOML_PATH,
                content = buildCodexConfigToml(
                    baseUrl = mapping.codexBaseUrl ?: normalizeCodexBaseUrl(baseUrl),
                    model = mapping.codexModel ?: resolvedModel,
                    wireApi = mapping.codexWireApi ?: OpenAiWireApi.RESPONSES,
                    modelCatalogPath = CODEX_MODEL_CATALOG_JSON_PATH,
                    envHttpHeaders = mapping.codexEnvHttpHeaders,
                ),
                executorKey = "codex-agent-config-write",
            ),
            AgentConfigWrite(
                path = CODEX_AUTH_JSON_PATH,
                content = buildCodexAuthJson(apiKey),
                executorKey = "codex-agent-config-write",
            ),
            AgentConfigWrite(
                path = CODEX_MODEL_CATALOG_JSON_PATH,
                content = buildCodexModelCatalogJson(
                    providerModels = providerModels,
                    provider = provider,
                ),
                executorKey = "codex-agent-config-write",
            ),
        )
    }

    override fun map(input: AgentProviderMappingInput): AgentProviderMapping {
        val provider = input.provider
        if (isChatGptAccount(input)) {
            return AgentProviderMapping(
                environment = mapOf("CODEX_HOME" to AgentRuntimeDefaults.CODEX_HOME),
                codexModel = input.model?.trim()?.takeIf(String::isNotEmpty),
            )
        }
        require(provider?.protocolType != "anthropic") {
            "Codex requires an OpenAI Responses-compatible endpoint; the current Provider is configured as Anthropic."
        }
        val headerBindings = provider?.let { buildAcpHeaderBindings(it.customHeaders) }
        val environment = if (provider == null) {
            mapOf("CODEX_HOME" to AgentRuntimeDefaults.CODEX_HOME)
        } else {
            mapOf(
                "CODEX_HOME" to AgentRuntimeDefaults.CODEX_HOME,
                "OPENAI_BASE_URL" to normalizeCodexBaseUrl(provider.baseUrl),
                "OPENAI_API_KEY" to provider.apiKey
            ) + headerBindings?.environment.orEmpty()
        }
        return AgentProviderMapping(
            environment = environment,
            codexModel = input.model?.trim()?.takeIf { it.isNotEmpty() },
            codexWireApi = provider?.let { OpenAiWireApi.RESPONSES },
            codexBaseUrl = provider?.baseUrl?.let(::normalizeCodexBaseUrl),
            codexEnvHttpHeaders = headerBindings?.envHttpHeaders.orEmpty(),
        )
    }

    override fun launchConfigWrites(
        input: AgentProviderMappingInput,
        mapping: AgentProviderMapping,
        providerModels: List<ProviderModelOption>,
        existingConfig: String,
    ): List<AgentConfigWrite> {
        if (isChatGptAccount(input)) return emptyList()
        val provider = input.provider ?: return emptyList()
        val model = mapping.codexModel ?: return emptyList()
        return listOf(
            AgentConfigWrite(
                path = CODEX_CONFIG_TOML_PATH,
                content = buildCodexConfigToml(
                    baseUrl = mapping.codexBaseUrl ?: provider.baseUrl,
                    model = model,
                    wireApi = mapping.codexWireApi ?: OpenAiWireApi.RESPONSES,
                    modelCatalogPath = CODEX_MODEL_CATALOG_JSON_PATH,
                    envHttpHeaders = mapping.codexEnvHttpHeaders,
                ),
                executorKey = "codex-agent-config-write",
            ),
            AgentConfigWrite(
                path = CODEX_AUTH_JSON_PATH,
                content = buildCodexAuthJson(provider.apiKey),
                executorKey = "codex-agent-config-write",
            ),
            AgentConfigWrite(
                path = CODEX_MODEL_CATALOG_JSON_PATH,
                content = buildCodexModelCatalogJson(
                    providerModels = providerModels,
                    provider = provider,
                ),
                executorKey = "codex-agent-config-write",
            ),
        )
    }
}
'''
    harness = harness[:start] + codex_block + harness[end:]
    write(HARNESS, harness)

ACCOUNT_MANAGER = "app/src/main/java/cn/com/omnimind/bot/agent/runtime/CodexChatGptAccountManager.kt"
write(ACCOUNT_MANAGER, r'''package cn.com.omnimind.bot.agent.runtime

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
''')

RUNTIME = "app/src/main/java/cn/com/omnimind/bot/agent/runtime/AgentRuntimeManager.kt"
runtime = read(RUNTIME)
if "CODEX_CHATGPT_MODEL_ID" not in runtime:
    runtime = runtime.replace(
        "import cn.com.omnimind.baselib.llm.ModelProviderProfile\n",
        "import cn.com.omnimind.baselib.llm.ModelProviderProfile\n"
        "import cn.com.omnimind.baselib.llm.CODEX_CHATGPT_MODEL_ID\n"
        "import cn.com.omnimind.baselib.llm.isCodexChatGptAccount\n",
        1,
    )
    runtime = runtime.replace(
        '''internal suspend fun fetchAgentProviderModels(
    profile: ModelProviderProfile,
    forceRefresh: Boolean = false,
): List<ProviderModelOption> {
    return HttpController.fetchProviderModels(
''',
        '''internal suspend fun fetchAgentProviderModels(
    profile: ModelProviderProfile,
    forceRefresh: Boolean = false,
): List<ProviderModelOption> {
    if (profile.isCodexChatGptAccount()) {
        return listOf(
            ProviderModelOption(
                id = CODEX_CHATGPT_MODEL_ID,
                displayName = CODEX_CHATGPT_MODEL_ID,
                ownedBy = "openai",
                reasoning = true,
                toolCall = true,
                inputModalities = listOf("text", "image"),
            )
        )
    }
    return HttpController.fetchProviderModels(
''',
        1,
    )
    runtime = runtime.replace(
        "    private val acpAgentProfileStore = AcpAgentProfileStore(appContext)\n",
        "    private val acpAgentProfileStore = AcpAgentProfileStore(appContext)\n"
        "    private val codexChatGptAccountManager = CodexChatGptAccountManager(appContext)\n",
        1,
    )
    old_handle = '''    suspend fun handleMethod(method: String, args: Map<String, Any?>): Any? {
        val compatibilityRequest = AcpLegacyCompatibilityAdapter.adapt(method, args)
'''
    new_handle = '''    suspend fun handleMethod(method: String, args: Map<String, Any?>): Any? {
        if (method in CODEX_CHATGPT_ACCOUNT_METHODS &&
            runCatching { ModelProviderConfigStore.getEditingProfile().isCodexChatGptAccount() }
                .getOrDefault(false)
        ) {
            return codexChatGptAccountManager.handle(method, args)
        }
        val compatibilityRequest = AcpLegacyCompatibilityAdapter.adapt(method, args)
'''
    if old_handle not in runtime:
        raise RuntimeError("AgentRuntimeManager.kt: handleMethod anchor changed")
    runtime = runtime.replace(old_handle, new_handle, 1)
    # Add account-method set beside existing top-level method sets.
    marker = "private val LOCAL_ACP_METHODS = setOf("
    index = runtime.find(marker)
    if index < 0:
        raise RuntimeError("AgentRuntimeManager.kt: LOCAL_ACP_METHODS anchor changed")
    runtime = runtime[:index] + '''private val CODEX_CHATGPT_ACCOUNT_METHODS = setOf(
    "account/read",
    "account/login/start",
    "account/login/cancel",
    "account/logout",
)

''' + runtime[index:]
    write(RUNTIME, runtime)

MANAGER = "app/src/main/java/cn/com/omnimind/bot/manager/AssistsCoreManager.kt"
manager = read(MANAGER)
if '"authMode" to ModelProviderAuthMode.fromSourceType' not in manager:
    manager = manager.replace(
        "import cn.com.omnimind.baselib.llm.ModelProviderConfigStore\n",
        "import cn.com.omnimind.baselib.llm.ModelProviderConfigStore\n"
        "import cn.com.omnimind.baselib.llm.ModelProviderAuthMode\n"
        "import cn.com.omnimind.baselib.llm.isCodexChatGptAccount\n",
        1,
    )
    manager = manager.replace(
        '            "configured" to isConfigured(),\n            "wireApi" to wireApi,',
        '            "configured" to (isConfigured() || isCodexChatGptAccount()),\n'
        '            "authMode" to ModelProviderAuthMode.fromSourceType(providerType),\n'
        '            "acpOnly" to isCodexChatGptAccount(),\n'
        '            "wireApi" to wireApi,',
        1,
    )
    # The profile map has sourceType/protocolType and a second configured key.
    manager = manager.replace(
        '            "configured" to isConfigured(),\n            "protocolType" to protocolType,',
        '            "configured" to (isConfigured() || isCodexChatGptAccount()),\n'
        '            "authMode" to ModelProviderAuthMode.fromSourceType(sourceType),\n'
        '            "acpOnly" to isCodexChatGptAccount(),\n'
        '            "protocolType" to protocolType,',
        1,
    )
    manager = manager.replace(
        '        val sourceType = call.argument<String>("sourceType")?.trim()\n'
        '        val protocolType = call.argument<String>("protocolType")?.trim() ?: "openai_compatible"\n',
        '        val authMode = call.argument<String>("authMode")?.trim()?.lowercase()\n'
        '        val sourceType = if (authMode == ModelProviderAuthMode.CODEX_CHATGPT) {\n'
        '            ModelProviderAuthMode.CODEX_CHATGPT\n'
        '        } else {\n'
        '            call.argument<String>("sourceType")?.trim()\n'
        '        }\n'
        '        val protocolType = if (authMode == ModelProviderAuthMode.CODEX_CHATGPT) {\n'
        '            "codex_acp"\n'
        '        } else {\n'
        '            call.argument<String>("protocolType")?.trim() ?: "openai_compatible"\n'
        '        }\n',
        1,
    )
    write(MANAGER, manager)

# Remove stale API environment from the packaged Codex profile. The legacy
# adapter continues to inject those variables dynamically for API-key mode.
AGENTS = "app/src/main/assets/acp/agents.json"
data = json.loads(read(AGENTS))
agents = data.get("agents", data if isinstance(data, list) else [])
for agent in agents:
    if agent.get("id") == "codex-acp":
        environment = agent.setdefault("environment", {})
        environment.pop("OPENAI_API_KEY", None)
        environment.pop("OPENAI_BASE_URL", None)
        environment["CODEX_HOME"] = "/root/.codex"
        models = agent.setdefault("models", [])
        if "gpt-5.3-codex-spark" not in models:
            models.append("gpt-5.3-codex-spark")
        break
else:
    raise RuntimeError("agents.json: codex-acp profile not found")
write(AGENTS, json.dumps(data, ensure_ascii=False, indent=2) + "\n")

# Monotonic installable build for the existing package.
GRADLE = "app/build.gradle.kts"
gradle = read(GRADLE)
gradle = gradle.replace("versionCode = 10003", "versionCode = 10004", 1)
gradle = gradle.replace('versionName = "0.1.0-grim.3"', 'versionName = "0.1.0-grim.4"', 1)
write(GRADLE, gradle)

# Pure JVM contract tests: no device, network, account, or token fixtures.
write("app/src/test/java/cn/com/omnimind/bot/agent/runtime/CodexChatGptAccountContractTest.kt", r'''package cn.com.omnimind.bot.agent.runtime

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
''')

write("baselib/src/test/java/cn/com/omnimind/baselib/llm/ModelProviderAuthModeTest.kt", '''package cn.com.omnimind.baselib.llm

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
''')

print("Codex ChatGPT backend patch applied")
