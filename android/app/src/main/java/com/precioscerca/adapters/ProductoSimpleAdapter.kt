package com.precioscerca.adapters

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.recyclerview.widget.RecyclerView
import com.precioscerca.R
import com.precioscerca.api.ApiClient
import com.precioscerca.api.ProductoResultado
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ProductoSimpleAdapter(
    private var productos: List<ProductoResultado> = emptyList()
) : RecyclerView.Adapter<ProductoSimpleAdapter.ViewHolder>() {
    
    class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val tvNombre: TextView = itemView.findViewById(R.id.tvNombreProducto)
        val tvIcono: TextView = itemView.findViewById(R.id.tvIconoProducto)
        val btnAgregar: View = itemView.findViewById(R.id.btnAgregarLista)
    }
    
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_producto_simple, parent, false)
        return ViewHolder(view)
    }
    
    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val producto = productos[position]
        val context = holder.itemView.context
        
        holder.tvNombre.text = producto.nombre
        
        // Icono según tipo de producto (básico)
        holder.tvIcono.text = getIconoProducto(producto.nombre)
        
        holder.btnAgregar.setOnClickListener {
            agregarALista(context, producto)
        }
    }
    
    override fun getItemCount(): Int = productos.size
    
    fun actualizarProductos(nuevosProductos: List<ProductoResultado>) {
        productos = nuevosProductos
        notifyDataSetChanged()
    }
    
    private fun getIconoProducto(nombre: String): String {
        val nombreLower = nombre.lowercase()
        return when {
            nombreLower.contains("leche") -> "🥛"
            nombreLower.contains("pan") -> "🍞"
            nombreLower.contains("carne") -> "🥩"
            nombreLower.contains("pollo") -> "🍗"
            nombreLower.contains("pescado") -> "🐟"
            nombreLower.contains("verdura") || nombreLower.contains("vegetal") -> "🥬"
            nombreLower.contains("fruta") -> "🍎"
            nombreLower.contains("arroz") -> "🍚"
            nombreLower.contains("fideos") || nombreLower.contains("pasta") -> "🍝"
            nombreLower.contains("aceite") -> "🫒"
            nombreLower.contains("huevo") -> "🥚"
            nombreLower.contains("queso") -> "🧀"
            nombreLower.contains("yogur") -> "🥛"
            nombreLower.contains("manteca") || nombreLower.contains("margarina") -> "🧈"
            nombreLower.contains("azúcar") || nombreLower.contains("azucar") -> "🧂"
            nombreLower.contains("sal") -> "🧂"
            nombreLower.contains("café") || nombreLower.contains("cafe") -> "☕"
            nombreLower.contains("té") || nombreLower.contains("te") -> "🍵"
            nombreLower.contains("agua") -> "💧"
            nombreLower.contains("gaseosa") || nombreLower.contains("coca") || nombreLower.contains("pepsi") -> "🥤"
            nombreLower.contains("vino") -> "🍷"
            nombreLower.contains("cerveza") -> "🍺"
            nombreLower.contains("jugo") -> "🧃"
            nombreLower.contains("limpieza") || nombreLower.contains("detergente") -> "🧼"
            nombreLower.contains("jabón") || nombreLower.contains("jabon") -> "🧼"
            nombreLower.contains("shampoo") || nombreLower.contains("champú") || nombreLower.contains("champu") -> "🧴"
            nombreLower.contains("papel") -> "🧻"
            else -> "📦"
        }
    }
    
    private fun agregarALista(context: Context, producto: ProductoResultado) {
        val request = com.precioscerca.api.AgregarItemRequest(
            nombre = producto.nombre,
            cantidad = 1
        )
        
        ApiClient.api.agregarALista(request).enqueue(object : Callback<com.precioscerca.api.AgregarItemResponse> {
            override fun onResponse(
                call: Call<com.precioscerca.api.AgregarItemResponse>,
                response: Response<com.precioscerca.api.AgregarItemResponse>
            ) {
                if (response.isSuccessful) {
                    val resultado = response.body()
                    if (resultado?.status == "agregado") {
                        Toast.makeText(context, "✅ Agregado a la lista", Toast.LENGTH_SHORT).show()
                    } else if (resultado?.status == "actualizado") {
                        Toast.makeText(context, "✅ Cantidad actualizada (x${resultado.cantidad})", Toast.LENGTH_SHORT).show()
                    }
                } else {
                    Toast.makeText(context, "Error agregando a lista", Toast.LENGTH_SHORT).show()
                }
            }
            
            override fun onFailure(call: Call<com.precioscerca.api.AgregarItemResponse>, t: Throwable) {
                Toast.makeText(context, "Error de conexión", Toast.LENGTH_SHORT).show()
            }
        })
    }
}
