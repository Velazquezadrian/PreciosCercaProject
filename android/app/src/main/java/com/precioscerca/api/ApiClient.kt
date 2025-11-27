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
    
    // URL base del backend Flask en Railway (producción)
    // Backend deployado en Railway con autoprecarga y 5,280 productos
    private const val BASE_URL = "https://web-production-a6410.up.railway.app/"
    
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