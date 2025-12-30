package com.ex.my1stApp

import android.Manifest
import android.annotation.SuppressLint
import android.app.Activity
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothGatt
import android.bluetooth.BluetoothGattCallback
import android.bluetooth.BluetoothGattCharacteristic
import android.bluetooth.BluetoothProfile
import android.bluetooth.le.BluetoothLeScanner
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanResult
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.location.LocationManager
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.ArrayAdapter
import android.widget.ListView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.lifecycle.lifecycleScope
import com.ex.my1stApp.data.AppDatabase
import com.ex.my1stApp.data.SavedDevice
import com.ex.my1stApp.databinding.ActivityMainBinding
import kotlinx.coroutines.launch
import java.util.UUID

@SuppressLint("MissingPermission") // Permissions are checked before BLE operations
class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var devicesListView: ListView
    private lateinit var listAdapter: ArrayAdapter<String>

    private val bluetoothAdapter: BluetoothAdapter? by lazy(LazyThreadSafetyMode.NONE) {
        BluetoothAdapter.getDefaultAdapter()
    }

    private val bleScanner: BluetoothLeScanner by lazy {
        bluetoothAdapter!!.bluetoothLeScanner
    }

    private val database by lazy { AppDatabase.getDatabase(this) }
    private val savedDeviceDao by lazy { database.savedDeviceDao() }

    private var bluetoothGatt: BluetoothGatt? = null
    private var bleCharacteristic: BluetoothGattCharacteristic? = null

    private val discoveredDevices = mutableListOf<BluetoothDevice>()

    // TODO: Replace with your actual Pico W Service and Characteristic UUIDs
    private val PICO_SERVICE_UUID = UUID.fromString("00000000-0000-0000-0000-000000000000") // CHANGE THIS
    private val PICO_CHARACTERISTIC_UUID = UUID.fromString("00000000-0000-0000-0000-000000000000") // CHANGE THIS

    private val scanCallback = object : ScanCallback() {
        override fun onScanResult(callbackType: Int, result: ScanResult) {
            super.onScanResult(callbackType, result)
            if (!discoveredDevices.any { it.address == result.device.address }) {
                val deviceName = result.device.name ?: getString(R.string.unknown_device)
                listAdapter.add("$deviceName\n${result.device.address}")
                discoveredDevices.add(result.device)
            }
        }

        override fun onScanFailed(errorCode: Int) {
            Log.e(TAG, "BLE Scan Failed with error code: $errorCode")
            binding.statusTextview.text = "BLE Scan Failed: $errorCode"
        }
    }

    private fun getDeviceName(device: BluetoothDevice): String {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            if (ActivityCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                return getString(R.string.unknown_device)
            }
        }
        return device.name ?: getString(R.string.unknown_device)
    }

    private val gattCallback = object : BluetoothGattCallback() {
        override fun onConnectionStateChange(gatt: BluetoothGatt, status: Int, newState: Int) {
            val deviceAddress = gatt.device.address

            if (newState == BluetoothProfile.STATE_CONNECTED) {
                Log.d(TAG, "Successfully connected to $deviceAddress")
                bluetoothGatt = gatt
                lifecycleScope.launch {
                    val deviceName = getDeviceName(gatt.device)
                    savedDeviceDao.insert(SavedDevice(deviceAddress, deviceName))
                }
                runOnUiThread {
                    binding.statusTextview.text = getString(R.string.status_connected)
                    binding.devicesListView.visibility = View.GONE
                    invalidateOptionsMenu()
                }
                Log.d(TAG, "Attempting to discover services...")
                gatt.discoverServices()
            } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                Log.d(TAG, "Disconnected from $deviceAddress")
                gatt.close()
                bluetoothGatt = null
                runOnUiThread {
                    binding.statusTextview.text = getString(R.string.status_disconnected)
                    binding.devicesListView.visibility = View.VISIBLE
                    invalidateOptionsMenu()
                }
            }
        }

        override fun onServicesDiscovered(gatt: BluetoothGatt, status: Int) {
            if (status == BluetoothGatt.GATT_SUCCESS) {
                Log.d(TAG, "Services discovered successfully.")
                val service = gatt.getService(PICO_SERVICE_UUID)
                if (service == null) {
                    Log.e(TAG, "Pico W Service not found!")
                    return
                }
                bleCharacteristic = service.getCharacteristic(PICO_CHARACTERISTIC_UUID)
                if (bleCharacteristic == null) {
                    Log.e(TAG, "Pico W Characteristic not found!")
                }
            } else {
                Log.w(TAG, "onServicesDiscovered received: $status")
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        setSupportActionBar(binding.toolbar)

        devicesListView = binding.devicesListView

        listAdapter = ArrayAdapter(this, android.R.layout.simple_list_item_1)
        devicesListView.adapter = listAdapter
        devicesListView.setOnItemClickListener { _, _, position, _ ->
            if(position < discoveredDevices.size) {
                connectToDevice(discoveredDevices[position])
            }
        }

        if (bluetoothAdapter == null) {
            binding.statusTextview.text = getString(R.string.status_no_bluetooth)
            return
        }

        setupButtonListeners()
        requestBluetoothPermissions()
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.main_menu, menu)
        return true
    }

    override fun onPrepareOptionsMenu(menu: Menu?): Boolean {
        menu?.findItem(R.id.action_scan)?.isVisible = bluetoothGatt == null
        return super.onPrepareOptionsMenu(menu)
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_scan -> {
                startBleScan()
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    private fun requestBluetoothPermissions() {
        val permissionsToRequest = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            arrayOf(
                Manifest.permission.BLUETOOTH_SCAN,
                Manifest.permission.BLUETOOTH_CONNECT,
                Manifest.permission.ACCESS_FINE_LOCATION
            )
        } else {
            arrayOf(Manifest.permission.ACCESS_FINE_LOCATION)
        }
        ActivityCompat.requestPermissions(this, permissionsToRequest, REQUEST_PERMISSIONS_CODE)
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == REQUEST_PERMISSIONS_CODE) {
            if (grantResults.isNotEmpty() && grantResults.all { it == PackageManager.PERMISSION_GRANTED }) {
                binding.statusTextview.text = getString(R.string.status_permissions_granted)
                checkAndEnableBluetooth()
            } else {
                binding.statusTextview.text = getString(R.string.status_permissions_denied)
            }
        }
    }

    private fun checkAndEnableBluetooth() {
        if (bluetoothAdapter?.isEnabled == false) {
            val enableBtIntent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
            startActivityForResult(enableBtIntent, ENABLE_BT_REQUEST_CODE)
        } else {
            binding.statusTextview.text = getString(R.string.status_bt_ready)
        }
    }

    @Deprecated("This method is deprecated in favour of using the Activity Result API")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == ENABLE_BT_REQUEST_CODE && resultCode == Activity.RESULT_OK) {
            binding.statusTextview.text = getString(R.string.status_bt_ready)
        }
    }

    private fun startBleScan() {
        if (!hasPermissions()) return
        
        bleScanner.stopScan(scanCallback)
        listAdapter.clear()
        discoveredDevices.clear()
        binding.statusTextview.text = getString(R.string.status_starting_scan)
        bleScanner.startScan(scanCallback)
    }

    private fun connectToDevice(device: BluetoothDevice) {
        if (!hasPermissions()) return

        bleScanner.stopScan(scanCallback)
        binding.statusTextview.text = getString(R.string.status_connecting)
        device.connectGatt(this, false, gattCallback)
    }

    private fun setupButtonListeners() {
        binding.button1.setOnClickListener { sendBluetoothCommand("1") }
        binding.button2.setOnClickListener { sendBluetoothCommand("2") }
        binding.button3.setOnClickListener { sendBluetoothCommand("3") }
        binding.button4.setOnClickListener { sendBluetoothCommand("4") }
    }

    private fun sendBluetoothCommand(command: String) {
        if (bluetoothGatt == null || bleCharacteristic == null) {
            Log.e(TAG, "Not connected to a device or characteristic not found.")
            return
        }

        val data = command.toByteArray(Charsets.UTF_8)
        bleCharacteristic!!.value = data
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
             bluetoothGatt!!.writeCharacteristic(bleCharacteristic!!, data, BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT)
        } else {
            @Suppress("DEPRECATION")
            bluetoothGatt!!.writeCharacteristic(bleCharacteristic)
        }
    }

    private fun hasPermissions(): Boolean {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            if (checkSelfPermission(Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED ||
                checkSelfPermission(Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED) {
                return false
            }
        }
        val locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager
        if (!locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)) {
            binding.statusTextview.text = getString(R.string.status_location_off)
            return false
        }
        return true
    }

    override fun onDestroy() {
        super.onDestroy()
        bluetoothGatt?.close()
    }

    companion object {
        private const val TAG = "MainActivity"
        private const val REQUEST_PERMISSIONS_CODE = 101
        private const val ENABLE_BT_REQUEST_CODE = 102
    }
}