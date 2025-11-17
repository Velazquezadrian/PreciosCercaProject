package com.precioscerca.adapters

import android.graphics.ColorMatrix
import android.graphics.ColorMatrixColorFilter
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.precioscerca.R
import com.precioscerca.models.ProductoEnLista

/**
 * Adapter para mostrar productos en "Lista Terminada"
 * Permite tocar productos para marcarlos como comprados (escala de grises)
 */
class ListaTerminadaAdapter(
    private val productos: List<ProductoEnLista>
) : RecyclerView.Adapter<ListaTerminadaAdapter.ViewHolder>() {

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val ivProductoTerminado: ImageView = view.findViewById(R.id.ivProductoTerminado)
        val tvNombreTerminado: TextView = view.findViewById(R.id.tvNombreTerminado)
        val tvSupermercadoTerminado: TextView = view.findViewById(R.id.tvSupermercadoTerminado)
        val tvPrecioTerminado: TextView = view.findViewById(R.id.tvPrecioTerminado)
        val tvEstadoComprado: TextView = view.findViewById(R.id.tvEstadoComprado)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_producto_terminado, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val producto = productos[position]
        
        holder.tvNombreTerminado.text = producto.nombre
        holder.tvSupermercadoTerminado.text = producto.supermercado
        holder.tvPrecioTerminado.text = "$${String.format("%.2f", producto.precio)}"
        
        // Cargar imagen
        if (producto.imagen.isNotEmpty()) {
            Glide.with(holder.itemView.context)
                .load(producto.imagen)
                .placeholder(R.drawable.ic_shopping_cart)
                .error(R.drawable.ic_shopping_cart)
                .into(holder.ivProductoTerminado)
        } else {
            holder.ivProductoTerminado.setImageResource(R.drawable.ic_shopping_cart)
        }
        
        // Aplicar estado (comprado = escala de grises)
        actualizarEstadoVisual(holder, producto)
        
        // Click para marcar/desmarcar como comprado
        holder.itemView.setOnClickListener {
            producto.comprado = !producto.comprado
            actualizarEstadoVisual(holder, producto)
        }
    }

    private fun actualizarEstadoVisual(holder: ViewHolder, producto: ProductoEnLista) {
        if (producto.comprado) {
            // Escala de grises
            val matrix = ColorMatrix()
            matrix.setSaturation(0f)
            val filter = ColorMatrixColorFilter(matrix)
            holder.ivProductoTerminado.colorFilter = filter
            
            holder.tvNombreTerminado.alpha = 0.5f
            holder.tvSupermercadoTerminado.alpha = 0.5f
            holder.tvPrecioTerminado.alpha = 0.5f
            
            holder.tvEstadoComprado.text = "✅ Comprado"
            holder.tvEstadoComprado.visibility = View.VISIBLE
        } else {
            // Color normal
            holder.ivProductoTerminado.colorFilter = null
            
            holder.tvNombreTerminado.alpha = 1.0f
            holder.tvSupermercadoTerminado.alpha = 1.0f
            holder.tvPrecioTerminado.alpha = 1.0f
            
            holder.tvEstadoComprado.visibility = View.GONE
        }
    }

    override fun getItemCount() = productos.size
}
