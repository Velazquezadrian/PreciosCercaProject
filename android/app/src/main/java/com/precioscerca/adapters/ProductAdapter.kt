package com.precioscerca.adapters

import android.content.Intent
import android.net.Uri
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.precioscerca.R
import com.precioscerca.api.ProductoResultado
import java.text.SimpleDateFormat
import java.util.*

class ProductAdapter(
    private var productos: List<ProductoResultado> = emptyList()
) : RecyclerView.Adapter<ProductAdapter.ProductViewHolder>() {

    class ProductViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val tvNombreProducto: TextView = itemView.findViewById(R.id.tvNombreProducto)
        val tvSupermercado: TextView = itemView.findViewById(R.id.tvSupermercado)
        val tvPrecio: TextView = itemView.findViewById(R.id.tvPrecio)
        val tvFecha: TextView = itemView.findViewById(R.id.tvFecha)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ProductViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_producto, parent, false)
        return ProductViewHolder(view)
    }

    override fun onBindViewHolder(holder: ProductViewHolder, position: Int) {
        val producto = productos[position]
        
        // Configurar datos del producto
        holder.tvNombreProducto.text = producto.nombre
        holder.tvSupermercado.text = producto.supermercado
        holder.tvPrecio.text = formatearPrecio(producto.precio)
        holder.tvFecha.text = formatearFecha(producto.fecha)
        
        // Click listener para abrir en web
        holder.itemView.setOnClickListener {
            // Por ahora, solo mostrar el nombre del supermercado
            // En el futuro se puede agregar URL específica del producto
            abrirEnWeb(holder.itemView.context, producto)
        }
    }

    override fun getItemCount(): Int = productos.size

    fun actualizarProductos(nuevosProductos: List<ProductoResultado>) {
        productos = nuevosProductos
        notifyDataSetChanged()
    }

    private fun formatearPrecio(precio: Double): String {
        return String.format("$%.2f", precio)
    }

    private fun formatearFecha(fechaString: String): String {
        try {
            // Parsear fecha ISO (viene del backend)
            val inputFormat = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.getDefault())
            val fecha = inputFormat.parse(fechaString)
            
            // Formatear para mostrar
            val now = Date()
            val diffInHours = (now.time - (fecha?.time ?: 0)) / (1000 * 60 * 60)
            
            return when {
                diffInHours < 1 -> "Hace menos de 1h"
                diffInHours < 24 -> "Hace ${diffInHours}h"
                else -> {
                    val outputFormat = SimpleDateFormat("dd/MM", Locale.getDefault())
                    outputFormat.format(fecha ?: now)
                }
            }
        } catch (e: Exception) {
            return "Hoy"
        }
    }

    private fun abrirEnWeb(context: android.content.Context, producto: ProductoResultado) {
        // Generar URL base según el supermercado
        val urlBase = when (producto.supermercado.lowercase()) {
            "la reina" -> "https://www.lareinaonline.com.ar"
            "carrefour" -> "https://www.carrefour.com.ar"
            "la gallega" -> "https://www.lagallega.com.ar"
            else -> "https://www.google.com/search?q=${producto.nombre.replace(" ", "+")}"
        }
        
        try {
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(urlBase))
            context.startActivity(intent)
        } catch (e: Exception) {
            // Si no se puede abrir, no hacer nada
        }
    }
}