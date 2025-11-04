package com.precioscerca.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.precioscerca.R
import com.precioscerca.api.SupermercadoComparacion

class ComparacionAdapter(
    private var supermercados: List<SupermercadoComparacion> = emptyList()
) : RecyclerView.Adapter<ComparacionAdapter.ViewHolder>() {
    
    class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val tvNombre: TextView = itemView.findViewById(R.id.tvNombreSuper)
        val tvTotal: TextView = itemView.findViewById(R.id.tvTotal)
        val tvProductos: TextView = itemView.findViewById(R.id.tvProductos)
        val tvBadge: TextView = itemView.findViewById(R.id.tvBadgeMasBarato)
    }
    
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_comparacion, parent, false)
        return ViewHolder(view)
    }
    
    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val super_data = supermercados[position]
        
        holder.tvNombre.text = super_data.nombre
        holder.tvTotal.text = String.format("$%.2f", super_data.total)
        holder.tvProductos.text = "${super_data.productos_encontrados} productos encontrados"
        
        // Mostrar badge "MÁS BARATO" solo para el primero (ya viene ordenado)
        if (position == 0) {
            holder.tvBadge.visibility = View.VISIBLE
        } else {
            holder.tvBadge.visibility = View.GONE
        }
    }
    
    override fun getItemCount(): Int = supermercados.size
    
    fun actualizarSupermercados(nuevosSupermercados: List<SupermercadoComparacion>) {
        supermercados = nuevosSupermercados
        notifyDataSetChanged()
    }
}
