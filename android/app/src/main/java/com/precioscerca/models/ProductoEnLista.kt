package com.precioscerca.models

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class ProductoEnLista(
    val nombre: String,
    val precio: Double,
    val supermercado: String,
    val imagen: String = "",
    val cantidad: Int = 1,
    var comprado: Boolean = false  // Para marcar productos en lista terminada
) : Parcelable
