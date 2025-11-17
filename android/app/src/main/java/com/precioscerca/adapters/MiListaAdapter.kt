package com.precioscerca.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageButton
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.precioscerca.R
import com.precioscerca.models.ProductoEnLista

/**
 * Adapter para mostrar productos en "Mi Lista"
 * Muestra imagen pequeña, nombre, supermercado, precio y botón eliminar
 */
class MiListaAdapter(
    private val productos: List<ProductoEnLista>,
    private val onEliminarClick: (ProductoEnLista) -> Unit
) : RecyclerView.Adapter<MiListaAdapter.ViewHolder>() {

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val ivProductoLista: ImageView = view.findViewById(R.id.ivProductoLista)
        val tvNombreLista: TextView = view.findViewById(R.id.tvNombreLista)
        val tvSupermercadoLista: TextView = view.findViewById(R.id.tvSupermercadoLista)
        val tvPrecioLista: TextView = view.findViewById(R.id.tvPrecioLista)
        val tvCantidadLista: TextView = view.findViewById(R.id.tvCantidadLista)
        val btnEliminar: ImageButton = view.findViewById(R.id.btnEliminar)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_producto_lista, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val producto = productos[position]
        
        holder.tvNombreLista.text = producto.nombre
        holder.tvSupermercadoLista.text = producto.supermercado
        holder.tvPrecioLista.text = "$${String.format("%.2f", producto.precio)}"
        
        if (producto.cantidad > 1) {
            holder.tvCantidadLista.text = "x${producto.cantidad}"
            holder.tvCantidadLista.visibility = View.VISIBLE
        } else {
            holder.tvCantidadLista.visibility = View.GONE
        }
        
        // Cargar imagen
        if (producto.imagen.isNotEmpty()) {
            Glide.with(holder.itemView.context)
                .load(producto.imagen)
                .placeholder(R.drawable.ic_shopping_cart)
                .error(R.drawable.ic_shopping_cart)
                .into(holder.ivProductoLista)
        } else {
            holder.ivProductoLista.setImageResource(R.drawable.ic_shopping_cart)
        }
        
        // Botón eliminar
        holder.btnEliminar.setOnClickListener {
            onEliminarClick(producto)
        }
    }

    override fun getItemCount() = productos.size
}
