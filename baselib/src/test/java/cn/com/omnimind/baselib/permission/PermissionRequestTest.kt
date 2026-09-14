package cn.com.omnimind.baselib.permission

import android.Manifest
import org.junit.Assert.assertNotEquals
import org.junit.Assert.assertNotNull
import org.junit.Test

class PermissionRequestTest {
    @Test
    fun sensitivePermissionDisclosuresCoverExistingAndNewCapabilities() {
        val permissions = listOf(
            Manifest.permission.BLUETOOTH_CONNECT,
            Manifest.permission.BLUETOOTH_SCAN,
            Manifest.permission.RECORD_AUDIO,
            Manifest.permission.READ_MEDIA_IMAGES,
            Manifest.permission.READ_MEDIA_AUDIO,
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_SETTINGS,
            Manifest.permission.POST_NOTIFICATIONS,
            Manifest.permission.ACCESS_COARSE_LOCATION,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.CAMERA,
            Manifest.permission.READ_CALENDAR,
            Manifest.permission.WRITE_CALENDAR,
        )

        permissions.forEach { permission ->
            val resources = PermissionRequest.getDisclosureResourcesForPermission(permission)
            assertNotNull(permission, resources)
            resources ?: return@forEach
            assertNotEquals(permission, 0, resources.labelResId)
            assertNotEquals(permission, 0, resources.purposeResId)
        }
    }
}
