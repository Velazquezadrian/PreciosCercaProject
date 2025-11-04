package com.precioscerca.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.precioscerca.R
import com.precioscerca.api.ItemListaCompras

class ListaComprasAdapter(
    private var items: List<ItemListaCompras> = emptyList(),
    private val onEliminarClick: (ItemListaCompras) -> Unit
) : RecyclerView.Adapter<ListaComprasAdapter.ViewHolder>() {
    
    class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val tvNombre: TextView = itemView.findViewById(R.id.tvNombreItem)
        val tvCantidad: TextView = itemView.findViewById(R.id.tvCantidad)
        val btnEliminar: View = itemView.findViewById(R.id.btnEliminar)
    }
    
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_lista_compras, parent, false)
        return ViewHolder(view)
    }
    
    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = items[position]
        
        holder.tvNombre.text = item.nombre
        holder.tvCantidad.text = "x${item.cantidad}"
        
        holder.btnEliminar.setOnClickListener {
            onEliminarClick(item)
        }
    }
    
    override fun getItemCount(): Int = items.size
    
    fun actualizarItems(nuevosItems: List<ItemListaCompras>) {
        items = nuevosItems
        notifyDataSetChanged()
    }
}
