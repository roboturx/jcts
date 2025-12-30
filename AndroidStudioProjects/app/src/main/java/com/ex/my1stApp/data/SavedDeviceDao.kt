package com.ex.my1stApp.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface SavedDeviceDao {

    @Query("SELECT * FROM saved_devices ORDER BY name ASC")
    fun getAlphabetizedDevices(): Flow<List<SavedDevice>>

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insert(device: SavedDevice)

    @Query("DELETE FROM saved_devices")
    suspend fun deleteAll()
}