package cn.com.omnimind.baselib.permission

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.os.Handler
import android.util.SparseArray
import android.widget.TextView
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import cn.com.omnimind.baselib.R

/**
 * 透明Activity方式实现权限请求工具类
 * 通过启动一个透明的Activity来处理权限请求，避免在业务Activity中处理复杂的权限逻辑。
 * 索取敏感权限时在顶部展示使用目的说明（不可点击），并直接使用系统权限弹窗获取权限。
 */
class PermissionRequest : Activity() {

    companion object {
        private const val PERMISSION_REQUEST_CODE = 1001
        private const val EXTRA_PERMISSIONS = "extra_permissions"

        private val requestCallbacks = SparseArray<(Map<String, Boolean>) -> Unit>()
        private var requestCode = 0

        internal data class PermissionDisclosureResources(
            val labelResId: Int,
            val purposeResId: Int
        )

        /**
         * String resources for sensitive-permission disclosures. Keeping
         * resource IDs here lets Android select the active UI locale while
         * preserving a single permission-to-disclosure mapping.
         */
        private val PERMISSION_DISCLOSURES = mapOf(
            android.Manifest.permission.POST_NOTIFICATIONS to PermissionDisclosureResources(
                R.string.permission_label_notifications,
                R.string.permission_purpose_notifications
            ),
            android.Manifest.permission.BLUETOOTH_CONNECT to PermissionDisclosureResources(
                R.string.permission_label_bluetooth_connect,
                R.string.permission_purpose_bluetooth_connect
            ),
            android.Manifest.permission.BLUETOOTH_SCAN to PermissionDisclosureResources(
                R.string.permission_label_bluetooth_scan,
                R.string.permission_purpose_bluetooth_scan
            ),
            android.Manifest.permission.RECORD_AUDIO to PermissionDisclosureResources(
                R.string.permission_label_microphone,
                R.string.permission_purpose_microphone
            ),
            android.Manifest.permission.READ_MEDIA_IMAGES to PermissionDisclosureResources(
                R.string.permission_label_read_images,
                R.string.permission_purpose_read_images
            ),
            android.Manifest.permission.READ_MEDIA_AUDIO to PermissionDisclosureResources(
                R.string.permission_label_read_audio,
                R.string.permission_purpose_read_audio
            ),
            android.Manifest.permission.READ_EXTERNAL_STORAGE to PermissionDisclosureResources(
                R.string.permission_label_read_storage,
                R.string.permission_purpose_read_storage
            ),
            android.Manifest.permission.WRITE_EXTERNAL_STORAGE to PermissionDisclosureResources(
                R.string.permission_label_write_storage,
                R.string.permission_purpose_write_storage
            ),
            android.Manifest.permission.WRITE_SETTINGS to PermissionDisclosureResources(
                R.string.permission_label_write_settings,
                R.string.permission_purpose_write_settings
            ),
            android.Manifest.permission.ACCESS_COARSE_LOCATION to PermissionDisclosureResources(
                R.string.permission_label_coarse_location,
                R.string.permission_purpose_coarse_location
            ),
            android.Manifest.permission.ACCESS_FINE_LOCATION to PermissionDisclosureResources(
                R.string.permission_label_fine_location,
                R.string.permission_purpose_fine_location
            ),
            android.Manifest.permission.CAMERA to PermissionDisclosureResources(
                R.string.permission_label_camera,
                R.string.permission_purpose_camera
            ),
            android.Manifest.permission.READ_CALENDAR to PermissionDisclosureResources(
                R.string.permission_label_read_calendar,
                R.string.permission_purpose_read_calendar
            ),
            android.Manifest.permission.WRITE_CALENDAR to PermissionDisclosureResources(
                R.string.permission_label_write_calendar,
                R.string.permission_purpose_write_calendar
            )
        )

        /**
         * 请求权限
         * @param context 上下文
         * @param permissions 需要请求的权限数组
         * @param callback 权限请求结果回调
         */
        fun requestPermissions(
            context: Context,
            permissions: Array<String>,
            callback: (Map<String, Boolean>) -> Unit
        ) {
            requestCode++
            requestCallbacks.put(requestCode, callback)

            val intent = Intent(context, PermissionRequest::class.java)
                .putExtra(EXTRA_PERMISSIONS, permissions)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            context.startActivity(intent)
        }

        /**
         * 检查是否已授予指定权限
         * @param context 上下文
         * @param permission 权限名称
         * @return 是否已授权
         */
        fun isPermissionGranted(context: Context, permission: String): Boolean {
            return ContextCompat.checkSelfPermission(
                context,
                permission
            ) == PackageManager.PERMISSION_GRANTED
        }

        internal fun getDisclosureResourcesForPermission(
            permission: String
        ): PermissionDisclosureResources? = PERMISSION_DISCLOSURES[permission]
    }

    private var currentRequestCode = 0
    private var pendingPermissionsToRequest: Array<String> = emptyArray()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setTheme(R.style.Theme_OmnibotApp_Permission)

        val permissions = intent.getStringArrayExtra(EXTRA_PERMISSIONS)
        if (permissions == null || permissions.isEmpty()) {
            Handler().postDelayed({ finish() }, 1000)
            return
        }

        currentRequestCode = requestCode

        // 检查是否已经拥有权限
        val permissionsToRequest = permissions.filter { permission ->
            ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED
        }.toTypedArray()

        if (permissionsToRequest.isEmpty()) {
            onRequestPermissionsResult(
                PERMISSION_REQUEST_CODE,
                permissions,
                IntArray(permissions.size) { PackageManager.PERMISSION_GRANTED })
        } else {
            pendingPermissionsToRequest = permissionsToRequest
            showPermissionPurposeDialogThenRequest(permissionsToRequest)
        }
    }

    /**
     * 在顶部展示权限使用说明（仅展示、不可点击），并直接调用系统权限请求。
     */
    private fun showPermissionPurposeDialogThenRequest(permissionsToRequest: Array<String>) {
        val purposeLines = permissionsToRequest.mapNotNull { permission ->
            getDisclosureResourcesForPermission(permission)?.let { disclosure ->
                getString(
                    R.string.permission_disclosure_template,
                    getString(disclosure.labelResId),
                    getString(disclosure.purposeResId)
                )
            }
        }
        if (purposeLines.isNotEmpty()) {
            setContentView(R.layout.permission_request_top_info)
            findViewById<TextView>(R.id.permission_info).text = purposeLines.joinToString("\n\n")
        }
        // 直接使用系统获取权限（无自定义按钮）
        window.decorView.post { doRequestPermissions(pendingPermissionsToRequest) }
    }

    private fun doRequestPermissions(permissions: Array<String>) {
        ActivityCompat.requestPermissions(this, permissions, PERMISSION_REQUEST_CODE)
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)

        val resultMap = mutableMapOf<String, Boolean>()
        permissions.forEachIndexed { index, permission ->
            resultMap[permission] = grantResults[index] == PackageManager.PERMISSION_GRANTED
        }

        // 回调结果
        requestCallbacks.get(currentRequestCode)?.invoke(resultMap)
        requestCallbacks.remove(currentRequestCode)

        // 关闭透明Activity
        finish()
    }
}
