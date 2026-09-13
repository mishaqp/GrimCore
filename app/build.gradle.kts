import groovy.json.JsonOutput
import groovy.json.JsonSlurper
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.kotlin.serialization)
}

fun prop(name: String): String = (project.findProperty(name) as String?)?.trim()
    ?: System.getenv(name)?.trim()
    ?: ""

fun buildConfigString(value: String): String {
    val escaped = value
        .replace("\\", "\\\\")
        .replace("\"", "\\\"")
    return "\"$escaped\""
}

val omnibotProfile = prop("OMNIBOT_PROFILE").ifBlank { "main" }
require(omnibotProfile in setOf("main", "investor")) {
    "OMNIBOT_PROFILE must be main or investor: $omnibotProfile"
}
val isInvestorProfile = omnibotProfile == "investor"
val preferPackagedOmniFlowRuntime =
    prop("OOB_PREFER_PACKAGED_OMNIFLOW_RUNTIME") == "1"
val webChatSourceDir = rootProject.file("webchat")
val webChatDistDir = File(webChatSourceDir, "dist")
val webChatAssetsRootDir = layout.buildDirectory.dir("generated/omnibot_assets").get().asFile
val webChatAssetsDir = File(webChatAssetsRootDir, "webchat")
val pluginSourceDir = rootProject.file("plugins")
val pluginCatalogFile = File(pluginSourceDir, "catalog.v1.json")
@Suppress("UNCHECKED_CAST")
val pluginCatalog = JsonSlurper().parse(pluginCatalogFile) as Map<String, Any?>
@Suppress("UNCHECKED_CAST")
val pluginCatalogEntries = pluginCatalog.getValue("plugins") as List<Map<String, Any?>>
val omniFlowCatalogEntry = pluginCatalogEntries.first {
    it["id"] == "com.omnimind.omni-vlm-lite"
}
@Suppress("UNCHECKED_CAST")
val omniFlowRuntimeSkill = omniFlowCatalogEntry.getValue("runtimeSkill") as Map<String, Any?>
val omniFlowPackagedArchivePath = omniFlowRuntimeSkill.getValue("packagedArchivePath").toString()
require(omniFlowPackagedArchivePath.startsWith("runtime-components/")) {
    "OmniFlow packagedArchivePath must be under runtime-components: $omniFlowPackagedArchivePath"
}
val omniFlowBaselineArchive = rootProject.file(
    "artifacts/${File(omniFlowPackagedArchivePath).name}",
)
val pluginAssetsRootDir = layout.buildDirectory.dir("generated/plugin_assets/$omnibotProfile")
    .get().asFile
val webChatPackageJson = File(webChatSourceDir, "package.json")
val webChatLockFile = File(webChatSourceDir, "pnpm-lock.yaml")
val webChatInstallMarker = File(webChatSourceDir, "node_modules/.modules.yaml")
val hostOs = System.getProperty("os.name").lowercase()

fun webChatPnpmCommand(arguments: String): List<String> = when {
    hostOs.contains("windows") -> listOf("cmd", "/c", "pnpm $arguments")
    hostOs.contains("mac") -> listOf("zsh", "-lc", "pnpm $arguments")
    else -> listOf("pnpm") + arguments.split(" ")
}

val installWebChatDependencies by tasks.registering(Exec::class) {
    group = "web chat"
    description = "Install the locked React WebChat build dependencies."
    workingDir(webChatSourceDir)
    commandLine(webChatPnpmCommand("install --frozen-lockfile"))
    inputs.files(webChatPackageJson, webChatLockFile)
    outputs.file(webChatInstallMarker)
}

val buildWebChatBundle by tasks.registering(Exec::class) {
    group = "web chat"
    description = "Build the React WebChat into a static Vite bundle."
    dependsOn(installWebChatDependencies)
    workingDir(webChatSourceDir)
    commandLine(webChatPnpmCommand("run build"))
    inputs.files(
        webChatPackageJson,
        webChatLockFile,
        File(webChatSourceDir, "tsconfig.json"),
        File(webChatSourceDir, "vite.config.ts"),
        File(webChatSourceDir, "index.html"),
        File(webChatSourceDir, "styles.css")
    )
    inputs.dir(File(webChatSourceDir, "src"))
    outputs.dir(webChatDistDir)
}

val syncWebChatBundle by tasks.registering(Copy::class) {
    group = "web chat"
    description = "Copy only the built React WebChat static files into Android assets."
    dependsOn(buildWebChatBundle)
    from(webChatDistDir)
    into(webChatAssetsDir)
    outputs.upToDateWhen { false }
    doFirst {
        // Always clear the dedicated generated root so an incremental build
        // cannot retain the removed Flutter Web/CanvasKit bundle.
        delete(webChatAssetsRootDir)
    }
}

val syncPluginAssets by tasks.registering(Sync::class) {
    group = "plugin packaging"
    description = "Generate the packaged plugin catalog for the selected build profile."
    inputs.file(pluginCatalogFile)
    inputs.file(omniFlowBaselineArchive)
    inputs.property("omnibotProfile", omnibotProfile)
    from(pluginSourceDir)
    from(omniFlowBaselineArchive) {
        into("runtime-components")
    }
    into(pluginAssetsRootDir)
    exclude("catalog.v1.json")
    if (!isInvestorProfile) {
        exclude("omni-vlm-lite/**", "vibe-project/**", "omnilink-agent/**")
    }
    doFirst {
        delete(pluginAssetsRootDir)
    }
    doLast {
        @Suppress("UNCHECKED_CAST")
        val source = JsonSlurper().parse(pluginCatalogFile)
            as Map<String, Any?>
        @Suppress("UNCHECKED_CAST")
        val plugins = source.getValue("plugins") as List<Map<String, Any?>>
        val filteredPlugins = plugins.filter { plugin ->
            @Suppress("UNCHECKED_CAST")
            val profiles = plugin["profiles"] as? List<String>
                ?: listOf("main", "investor")
            omnibotProfile in profiles
        }
        val profileCatalog = LinkedHashMap(source).apply {
            this["plugins"] = filteredPlugins
        }
        File(pluginAssetsRootDir, "catalog.v1.json").writeText(
            JsonOutput.prettyPrint(JsonOutput.toJson(profileCatalog)) + "\n"
        )
    }
}

android {
    namespace = "cn.com.omnimind.bot"
    compileSdk = 37

    defaultConfig {
        applicationId = "com.mishaqp.grimcore"
        minSdk = 29
        targetSdk = 36
        // GrimCore independent version scheme. versionCode is monotonic and
        // never decreases inside the com.mishaqp.grimcore package:
        // major *1000000 + minor *10000 + patch *100 + grim
        // 0.1.0-grim.3 -> 10003
        versionCode = 10003
        versionName = "0.1.0-grim.3"
        buildConfigField("String", "OMNIBOT_PROFILE", buildConfigString(omnibotProfile))
        buildConfigField("boolean", "ALLOW_PACKAGED_PLUGIN_FALLBACK", "true")
        buildConfigField(
            "boolean",
            "PREFER_PACKAGED_OMNIFLOW_RUNTIME",
            preferPackagedOmniFlowRuntime.toString(),
        )
        ndk {
            // The GrimCore user APK is arm64-v8a only. x86_64 stays available
            // only for emulator test builds that opt in with -PgrimAbiArm64Only=false.
            val grimAbiArm64Only = (project.findProperty("grimAbiArm64Only") as String?)
                ?.toBooleanStrictOrNull() ?: true
            if (grimAbiArm64Only) {
                abiFilters.add("arm64-v8a")
            } else {
                abiFilters.addAll(listOf("arm64-v8a", "x86_64"))
            }
        }

    }
    // 添加 flavor 维度
    flavorDimensions += listOf("version", "edition")

    productFlavors {
        create("develop") {
            dimension = "version"
        }

        create("production") {
            dimension = "version"
        }

        create("standard") {
            dimension = "edition"
            buildConfigField("String", "APP_EDITION", "\"standard\"")
        }
    }
    signingConfigs {
        create("release") {
            // GrimCore signing material. Secrets are never stored in the
            // repository: they arrive as Gradle properties / env vars from CI.
            // The upstream OMNI_RELEASE_* names remain a fallback so that
            // unmodified upstream build flows keep working.
            fun grimSigningProperty(grimName: String, upstreamName: String): String? {
                // Gradle exposes -P properties and ORG_GRADLE_PROJECT_* environment
                // entries through findProperty. System.getenv is the last resort so a
                // plain environment variable also works for local release builds.
                val grimValue = (project.findProperty(grimName) as String?)
                    ?: System.getenv(grimName)
                if (!grimValue.isNullOrBlank()) return grimValue
                val upstreamValue = (project.findProperty(upstreamName) as String?)
                    ?: System.getenv(upstreamName)
                return upstreamValue?.takeIf { it.isNotBlank() }
            }
            storeFile = grimSigningProperty("GRIM_RELEASE_STORE_FILE", "OMNI_RELEASE_STORE_FILE")
                ?.let { file(it) }
            storePassword = grimSigningProperty("GRIM_RELEASE_STORE_PWD", "OMNI_RELEASE_STORE_PWD")
            keyAlias = grimSigningProperty("GRIM_RELEASE_KEY_ALIAS", "OMNI_RELEASE_KEY_ALIAS")
            keyPassword = grimSigningProperty("GRIM_RELEASE_KEY_PWD", "OMNI_RELEASE_KEY_PWD")

            // V2/V3签名配置（minSdk=30）
            enableV1Signing = false
            enableV2Signing = true
            enableV3Signing = true
        }
    }
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
        debug {
            signingConfig = signingConfigs.getByName("debug")
            // There is one installable debug app for device validation.  A
            // suffix here creates a second launcher entry beside the normal
            // package, which makes users switch between two identical APKs.
            applicationIdSuffix = ""
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    buildFeatures {
        compose = true
        buildConfig = true
    }
    testOptions {
        unitTests.isReturnDefaultValues = true
    }

    packaging {
        jniLibs {
            useLegacyPackaging = true
            pickFirsts += setOf(
                "**/libc++_shared.so"
            )
        }
        resources {
            excludes += setOf(
                "META-INF/INDEX.LIST",
                "META-INF/io.netty.versions.properties",
                "META-INF/MANIFEST.MF",
                "META-INF/DEPENDENCIES",
                "META-INF/LICENSE",
                "META-INF/LICENSE.txt",
                "META-INF/NOTICE",
                "META-INF/NOTICE.txt",
                "DebugProbesKt.bin"
            )
        }
    }

    sourceSets {
        getByName("main") {
            assets.srcDirs(
                "src/main/assets",
                "../skills",
                pluginAssetsRootDir,
                webChatAssetsRootDir
            )
        }
    }

    lint {
        // 使用项目根目录的 lint.xml 配置
        lintConfig = file("../lint.xml")
        // 将错误视为警告继续构建
        abortOnError = false
    }
}

kotlin {
    compilerOptions {
        jvmTarget.set(JvmTarget.JVM_17)
    }
}

tasks.named("preBuild").configure {
    dependsOn(syncWebChatBundle, syncPluginAssets)
}
dependencies {
    implementation(libs.agent.client.protocol)
    implementation(project(":flutter"))
    implementation(project(":uikit"))
    implementation(project(":baselib"))
    implementation(project(":androidgui"))
    implementation(project(":omniflow-android"))
    implementation(project(":core:main"))
    implementation(project(":core:terminal-view"))
    implementation(project(":core:terminal-emulator"))
    implementation(fileTree(mapOf("dir" to "libs", "include" to listOf("*.aar","*.jar"))))
    implementation(project(":assists"))
//    implementation(project(":lib"))

    implementation(libs.androidx.core.ktx)
    implementation(libs.androidsvg)
    implementation(libs.androidx.documentfile)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.lifecycle.livedata.ktx)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.ui)
    implementation(libs.androidx.ui.graphics)
    implementation(libs.androidx.ui.tooling.preview)
    implementation(libs.androidx.material3)
    implementation(libs.kotlin.stdlib)
    implementation(libs.kotlinx.serialization.json)
    implementation(libs.kotlinx.coroutines.android)
    implementation(libs.androidx.appcompat)
    implementation(libs.androidx.lifecycle.service)
    implementation(libs.work.runtime)
    implementation(libs.androidx.security.crypto)
    implementation(libs.androidx.core.splashscreen)
    implementation(libs.shizuku.provider)
    implementation(libs.ktor.server.core)
    implementation(libs.ktor.server.cio)
    implementation(libs.ktor.server.auth)
    implementation(libs.ktor.server.content.negotiation)
    implementation(libs.ktor.serialization.gson)
    implementation(libs.ktor.serialization.kotlinx.json)
    implementation(libs.ktor.server.call.logging)
    implementation(libs.mcp.kotlin.sdk.server)
    testImplementation(libs.junit)
    testImplementation("org.mockito:mockito-core:5.20.0")
    testImplementation(libs.okhttp.mockwebserver)
    debugImplementation(libs.androidx.ui.tooling)
    debugImplementation(libs.androidx.ui.test.manifest )
}
