package com.precioscerca.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.precioscerca.R

class SugerenciasAdapter(
    private var sugerencias: List<String>,
    private val onSugerenciaClick: (String) -> Unit
) : RecyclerView.Adapter<SugerenciasAdapter.SugerenciaViewHolder>() {

    inner class SugerenciaViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val tvSugerencia: TextView = view.findViewById(R.id.tvSugerencia)
        
        init {
            view.setOnClickListener {
                val position = adapterPosition
                if (position != RecyclerView.NO_POSITION) {
                    onSugerenciaClick(sugerencias[position])
                }
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): SugerenciaViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_sugerencia, parent, false)
        return SugerenciaViewHolder(view)
    }

    override fun onBindViewHolder(holder: SugerenciaViewHolder, position: Int) {
        holder.tvSugerencia.text = sugerencias[position]
    }

    override fun getItemCount() = sugerencias.size

    fun actualizarSugerencias(nuevasSugerencias: List<String>) {
        sugerencias = nuevasSugerencias
        notifyDataSetChanged()
    }
}
