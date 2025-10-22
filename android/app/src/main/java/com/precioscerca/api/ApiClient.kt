package com.precioscerca.api

import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

/**
 * Cliente Retrofit para manejar las llamadas a la API
 */
object ApiClient {
    
    // URL base del backend Django (ajustar según tu configuración)
    private const val BASE_URL = "http://10.0.2.2:8000/"  // Para emulador Android
    // Para dispositivo físico usar: "http://tu-ip-local:8000/"
    
    // Cliente HTTP con logging para debugging
    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        })
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()
    
    // Instancia de Retrofit
    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(GsonConverterFactory.create())
        .build()
    
    // Interfaz de la API
    val api: PreciosCercaApi = retrofit.create(PreciosCercaApi::class.java)
}