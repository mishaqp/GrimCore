package cn.com.omnimind.bot.update

import org.json.JSONObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class AppUpdateManagerTest {
    @Test
    fun normalizeAndCompareVersionsSupportGrimCoreReleases() {
        assertEquals("0.1.0-grim.3", AppUpdateManager.normalizeVersion("v0.1.0-grim.3"))
        assertEquals(1, AppUpdateManager.compareVersions("0.1.0-grim.3", "0.1.0-grim.2"))
        assertEquals(0, AppUpdateManager.compareVersions("v1.2.0", "1.2"))
        assertEquals(-1, AppUpdateManager.compareVersions("1.9.9", "2.0.0"))
    }

    @Test
    fun releaseTrackAcceptsGrimCoreStableAndBetaReleases() {
        assertEquals(
            ReleaseTrack.STABLE,
            AppUpdateManager.classifyReleaseTrack("0.1.0-grim.3")
        )
        assertEquals(
            ReleaseTrack.BETA,
            AppUpdateManager.classifyReleaseTrack("1.6.1.2")
        )
        assertEquals(
            ReleaseTrack.BETA,
            AppUpdateManager.classifyReleaseTrack("0.1.0-grim.3", prerelease = true)
        )
    }

    @Test
    fun selectLatestReleaseHonorsBetaPreference() {
        val stable = ReleaseCandidate(
            version = "0.1.0-grim.3",
            track = ReleaseTrack.STABLE,
            publishedAt = 1L,
            releaseUrl = "https://example.com/stable",
            releaseNotes = "",
            assets = emptyList()
        )
        val beta = ReleaseCandidate(
            version = "1.6.1.2",
            track = ReleaseTrack.BETA,
            publishedAt = 2L,
            releaseUrl = "https://example.com/beta",
            releaseNotes = "",
            assets = emptyList()
        )

        assertEquals(
            stable,
            AppUpdateManager.selectLatestRelease(listOf(stable, beta), includeBeta = false)
        )
        assertEquals(
            beta,
            AppUpdateManager.selectLatestRelease(listOf(stable, beta), includeBeta = true)
        )
    }

    @Test
    fun selectsOnlyTheForkReleaseAssetNamingConvention() {
        val assets = listOf(
            ReleaseAsset(
                name = "OpenOmniBot-v0.4.0-standard.apk",
                downloadUrl = "https://example.com/upstream.apk"
            ),
            ReleaseAsset(
                name = "GrimCore-v0.1.0-grim.3-arm64-v8a.apk",
                downloadUrl = "https://example.com/grimcore.apk"
            )
        )

        assertEquals(
            "GrimCore-v0.1.0-grim.3-arm64-v8a.apk",
            AppUpdateManager.selectPreferredApkAsset(assets)?.name
        )
        assertNull(
            AppUpdateManager.selectPreferredApkAsset(
                listOf(assets.first()),
                edition = "standard"
            )
        )
    }

    @Test
    fun downloadUrlAlwaysTargetsTheForkGitHubRelease() {
        val asset = ReleaseAsset(
            name = "GrimCore-v0.1.0-grim.3-arm64-v8a.apk",
            downloadUrl = ""
        )

        assertEquals(
            "https://github.com/mishaqp/GrimCore/releases/download/v0.1.0-grim.3/" +
                "GrimCore-v0.1.0-grim.3-arm64-v8a.apk",
            AppUpdateManager.resolveApkDownloadUrl("0.1.0-grim.3", asset)
        )
    }

    @Test
    fun parsesAStandardGitHubReleaseWithoutCloudPolicyFields() {
        val state = AppUpdateManager.parseReleaseUpdateState(
            payload = JSONObject(
                """
                {
                  "tag_name": "v0.1.0-grim.4",
                  "prerelease": false,
                  "html_url": "https://github.com/mishaqp/GrimCore/releases/tag/v0.1.0-grim.4",
                  "assets": [
                    {
                      "name": "GrimCore-v0.1.0-grim.4-arm64-v8a.apk",
                      "browser_download_url": "https://example.com/GrimCore-v0.1.0-grim.4-arm64-v8a.apk"
                    }
                  ]
                }
                """.trimIndent()
            ),
            currentVersion = "0.1.0-grim.3",
            includeBeta = false,
            checkedAt = 42L
        )

        assertTrue(state.hasUpdate)
        assertEquals("0.1.0-grim.4", state.latestVersion)
        assertEquals(42L, state.checkedAt)
        assertFalse(state.apkDownloadUrl.isBlank())
    }
}
