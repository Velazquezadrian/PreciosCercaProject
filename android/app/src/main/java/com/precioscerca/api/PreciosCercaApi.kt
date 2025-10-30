package com.precioscerca.api

import com.precioscerca.models.BusquedaResponse
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Query

/**
 * Interfaz para comunicarse con la API del backend Django
 */
interface PreciosCercaApi {
    
    /**
     * Buscar productos por nombre/término
     * GET /products?query=leche
     */
    @GET("products")
    fun buscarProductos(
        @Query("query") query: String
    ): Call<BusquedaApiResponse>
    
    /**
     * Buscar productos cercanos según ubicación del usuario
     * GET /products-cercanos?query=leche&lat=-34.603&lng=-58.381&radio=10
     */
    @GET("products-cercanos")
    fun buscarProductosCercanos(
        @Query("query") query: String,
        @Query("lat") latitud: Double,
        @Query("lng") longitud: Double,
        @Query("radio") radioKm: Double = 10.0
    ): Call<BusquedaApiResponse>
    
    /**
     * Encontrar sucursal más cercana
     * GET /sucursal-cercana?supermercado=Carrefour&lat=-34.603&lng=-58.381
     */
    @GET("sucursal-cercana")
    fun sucursalCercana(
        @Query("supermercado") supermercado: String,
        @Query("lat") latitud: Double,
        @Query("lng") longitud: Double
    ): Call<SucursalCercanaResponse>
    
}

/**
 * Respuesta de la API de búsqueda (ajustada a la estructura real del backend)
 */
data class BusquedaApiResponse(
    val query: String,
    val total_encontrados: Int,
    val supermercados_consultados: List<String>,
    val productos_por_supermercado: Map<String, Int>,
    val resultados: List<ProductoResultado>,
    val ciudad_detectada: String? = null,  // Solo en búsqueda cercana
    val distancia_ciudad_km: Double? = null,  // Solo en búsqueda cercana
    val radio_km: Double? = null,  // Solo en búsqueda cercana
    val mensaje: String? = null,  // Mensaje informativo
    val supermercado_mas_cercano: String? = null,  // Supermercado más cercano al usuario
    val distancia_supermercado_mas_cercano_km: Double? = null  // Distancia al supermercado más cercano
)

/**
 * Producto individual en los resultados de búsqueda
 */
data class ProductoResultado(
    val nombre: String,
    val precio: Double,
    val supermercado: String,
    val fecha: String,
    val relevancia: Double,
    val url: String? = null,  // URL específica del producto
    val distancia_sucursal_km: Double? = null  // Distancia a la sucursal más cercana de este supermercado
)

/**
 * Respuesta de sucursal cercana
 */
data class SucursalCercanaResponse(
    val supermercado: String,
    val sucursal: SucursalInfo
)

/**
 * Información de una sucursal
 */
data class SucursalInfo(
    val nombre: String,
    val direccion: String,
    val lat: Double,
    val lng: Double,
    val ciudad: String,
    val distancia_km: Double,
    val google_maps_url: String
)