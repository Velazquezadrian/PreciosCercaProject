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
    
}

/**
 * Respuesta de la API de búsqueda (ajustada a la estructura real del backend)
 */
data class BusquedaApiResponse(
    val query: String,
    val total_encontrados: Int,
    val supermercados_consultados: List<String>,
    val productos_por_supermercado: Map<String, Int>,
    val resultados: List<ProductoResultado>
)

/**
 * Producto individual en los resultados de búsqueda
 */
data class ProductoResultado(
    val nombre: String,
    val precio: Double,
    val supermercado: String,
    val fecha: String,
    val relevancia: Double
)