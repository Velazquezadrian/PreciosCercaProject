package com.precioscerca.models

import com.google.gson.annotations.SerializedName

/**
 * Modelo que representa un supermercado
 */
data class Supermercado(
    val id: Long,
    val nombre: String,
    @SerializedName("url_sitio")
    val urlSitio: String,
    val activo: Boolean
)

/**
 * Modelo que representa un producto
 */
data class Producto(
    val id: Long,
    val nombre: String,
    val categoria: String
)

/**
 * Modelo que representa un precio de producto en un supermercado
 */
data class Precio(
    val id: Long,
    val supermercado: Supermercado,
    val producto: Producto,
    val precio: Double,
    @SerializedName("url_producto")
    val urlProducto: String,
    val fecha: String
)

/**
 * Respuesta de la API para búsqueda de productos
 */
data class ProductoConPrecios(
    val producto: Producto,
    val precios: List<Precio>
)

/**
 * Respuesta genérica de la API
 */
data class ApiResponse<T>(
    val success: Boolean,
    val data: T?,
    val message: String?
)

/**
 * Respuesta de búsqueda de productos
 */
data class BusquedaResponse(
    val productos: List<ProductoConPrecios>,
    val total: Int
)