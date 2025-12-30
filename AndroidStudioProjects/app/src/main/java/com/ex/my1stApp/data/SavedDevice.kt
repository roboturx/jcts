package com.ex.my1stApp.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "saved_devices")
data class SavedDevice(
    @PrimaryKey
    val address: String,
    val name: String
)