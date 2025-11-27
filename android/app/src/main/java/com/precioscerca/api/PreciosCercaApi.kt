package com.precioscerca.api

import com.precioscerca.models.BusquedaResponse
import retrofit2.Call
import retrofit2.http.*

/**
 * Interfaz para comunicarse con la API del backend Django
 */
interface PreciosCercaApi {
    
    /**
     * Buscar productos por nombre/término
     * GET /products?query=leche&supermercado=carrefour
     */
    @GET("products")
    fun buscarProductos(
        @Query("query") query: String,
        @Query("supermercado") supermercado: String? = null
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
    
    // ========== LISTA DE COMPRAS ==========
    
    /**
     * Obtener lista de compras
     * GET /lista-compras
     */
    @GET("lista-compras")
    fun obtenerListaCompras(): Call<ListaComprasResponse>
    
    /**
     * Agregar producto a lista de compras
     * POST /lista-compras/agregar
     */
    @POST("lista-compras/agregar")
    fun agregarALista(@Body request: AgregarItemRequest): Call<AgregarItemResponse>
    
    /**
     * Eliminar producto de lista de compras
     * DELETE /lista-compras/eliminar
     */
    @HTTP(method = "DELETE", path = "lista-compras/eliminar", hasBody = true)
    fun eliminarDeLista(@Body request: EliminarItemRequest): Call<EliminarItemResponse>
    
    /**
     * Limpiar toda la lista de compras
     * POST /lista-compras/limpiar
     */
    @POST("lista-compras/limpiar")
    fun limpiarLista(): Call<LimpiarListaResponse>
    
    /**
     * Comparar precios de la lista entre supermercados
     * GET /lista-compras/comparar
     */
    @GET("lista-compras/comparar")
    fun compararLista(): Call<ComparacionResponse>
    
    /**
     * Obtener sugerencias de búsqueda (autocomplete)
     * GET /sugerencias?query=pa&supermercado=lagallega&limit=10
     */
    @GET("sugerencias")
    fun getSugerencias(
        @Query("query") query: String,
        @Query("supermercado") supermercado: String? = null,
        @Query("limit") limit: Int = 10
    ): Call<SugerenciasResponse>
    
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
    val imagen: String? = null,  // URL de la imagen del producto
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

// ============================================================================
// MODELOS DE LISTA DE COMPRAS
// ============================================================================

/**
 * Item en la lista de compras
 */
data class ItemListaCompras(
    val nombre: String,
    val cantidad: Int,
    val precio: Double = 0.0,
    val supermercado: String = "",
    val imagen: String = "",
    val agregado_en: String
)

/**
 * Respuesta de obtener lista de compras
 */
data class ListaComprasResponse(
    val items: List<ItemListaCompras>,
    val total_items: Int
)

/**
 * Request para agregar item
 */
data class AgregarItemRequest(
    val nombre: String,
    val cantidad: Int = 1,
    val precio: Double = 0.0,
    val supermercado: String = "",
    val imagen: String = ""
)

/**
 * Respuesta de agregar item
 */
data class AgregarItemResponse(
    val status: String,
    val producto: String,
    val cantidad: Int
)

/**
 * Request para eliminar item
 */
data class EliminarItemRequest(
    val nombre: String
)

/**
 * Respuesta de eliminar item
 */
data class EliminarItemResponse(
    val status: String,
    val producto: String? = null,
    val mensaje: String? = null
)

/**
 * Respuesta de limpiar lista
 */
data class LimpiarListaResponse(
    val status: String,
    val mensaje: String
)

/**
 * Producto encontrado en comparación
 */
data class ProductoComparacion(
    val nombre_buscado: String,
    val nombre_encontrado: String,
    val precio: Double
)

/**
 * Supermercado en comparación
 */
data class SupermercadoComparacion(
    val nombre: String,
    val productos: List<ProductoComparacion>,
    val total: Double,
    val productos_encontrados: Int
)

/**
 * Respuesta de comparar lista
 */
data class ComparacionResponse(
    val total_productos_buscados: Int,
    val supermercados: List<SupermercadoComparacion>,
    val mas_barato: SupermercadoComparacion?,
    val error: String? = null,
    val items: List<Any>? = null
)

/**
 * Respuesta de sugerencias de búsqueda
 */
data class SugerenciasResponse(
    val query: String,
    val sugerencias: List<String>,
    val total: Int
)
