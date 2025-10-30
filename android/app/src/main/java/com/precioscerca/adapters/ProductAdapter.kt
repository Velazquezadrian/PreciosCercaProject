package com.precioscerca.adapters

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.location.LocationManager
import android.net.Uri
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.recyclerview.widget.RecyclerView
import com.precioscerca.R
import com.precioscerca.api.ApiClient
import com.precioscerca.api.ProductoResultado
import com.precioscerca.api.SucursalCercanaResponse
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
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
        val btnVerWeb: TextView = itemView.findViewById(R.id.btnVerWeb)
        val btnVerMapa: TextView = itemView.findViewById(R.id.btnVerMapa)
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
        
        // Click en "Ver en web"
        holder.btnVerWeb.setOnClickListener {
            abrirEnWeb(holder.itemView.context, producto)
        }
        
        // Click en "Ver en mapa"
        holder.btnVerMapa.setOnClickListener {
            abrirEnMapa(holder.itemView.context, producto)
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
        // Usar la URL específica del producto si está disponible
        val url = if (!producto.url.isNullOrEmpty()) {
            producto.url
        } else {
            // Fallback: generar URL base según el supermercado
            when (producto.supermercado.lowercase()) {
                "la reina" -> "https://www.lareinaonline.com.ar"
                "carrefour" -> "https://www.carrefour.com.ar"
                "la gallega" -> "https://www.lagallega.com.ar"
                "día %" -> "https://diaonline.supermercadosdia.com.ar"
                else -> "https://www.google.com/search?q=${producto.nombre.replace(" ", "+")}"
            }
        }
        
        try {
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            // Agregar flags para que se pueda volver fácilmente
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            // Crear chooser para permitir seleccionar navegador y volver fácilmente
            val chooser = Intent.createChooser(intent, "Abrir producto en:")
            context.startActivity(chooser)
        } catch (e: Exception) {
            // Si no se puede abrir, no hacer nada
        }
    }
    
    private fun abrirEnMapa(context: Context, producto: ProductoResultado) {
        // Obtener ubicación del usuario
        if (ActivityCompat.checkSelfPermission(
                context,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            Toast.makeText(context, "Se necesita permiso de ubicación para ver en mapa", Toast.LENGTH_LONG).show()
            return
        }
        
        try {
            val locationManager = context.getSystemService(Context.LOCATION_SERVICE) as LocationManager
            
            // Intentar obtener ubicación de GPS primero, luego Network
            var location = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER)
            if (location == null) {
                location = locationManager.getLastKnownLocation(LocationManager.NETWORK_PROVIDER)
            }
            
            if (location == null) {
                Toast.makeText(context, "⚠️ No se pudo obtener tu ubicación GPS. Configure ubicación en el emulador.", Toast.LENGTH_LONG).show()
                return
            }
            
            // Validar que la ubicación sea válida (no sea 0,0 o fuera de Argentina)
            if (!esUbicacionValida(location.latitude, location.longitude)) {
                Toast.makeText(context, "⚠️ Ubicación GPS inválida. Las sucursales están en Buenos Aires, Argentina.", Toast.LENGTH_LONG).show()
                return
            }
            
            buscarSucursalYAbrirMapa(context, producto, location.latitude, location.longitude)
            
        } catch (e: Exception) {
            Toast.makeText(context, "Error obteniendo ubicación: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }
    
    private fun esUbicacionValida(lat: Double, lng: Double): Boolean {
        // Validar que no sea la ubicación por defecto (0,0)
        if (lat == 0.0 && lng == 0.0) return false
        
        // Validar que esté dentro de rangos de Argentina
        // Argentina: lat entre -55 y -21, lng entre -73 y -53
        if (lat < -55 || lat > -21) return false
        if (lng < -73 || lng > -53) return false
        
        return true
    }
    
    private fun buscarSucursalYAbrirMapa(context: Context, producto: ProductoResultado, lat: Double, lng: Double) {
        Toast.makeText(context, "📍 Buscando sucursal cercana desde ${String.format("%.2f", lat)}, ${String.format("%.2f", lng)}...", Toast.LENGTH_SHORT).show()
        
        // Llamar a la API para obtener sucursal más cercana
        val call = ApiClient.api.sucursalCercana(producto.supermercado, lat, lng)
        
        call.enqueue(object : Callback<SucursalCercanaResponse> {
            override fun onResponse(
                call: Call<SucursalCercanaResponse>,
                response: Response<SucursalCercanaResponse>
            ) {
                if (response.isSuccessful) {
                    val sucursal = response.body()?.sucursal
                    if (sucursal != null) {
                        val distanciaKm = sucursal.distancia_km
                        
                        // Advertir si la sucursal está muy lejos
                        if (distanciaKm > 100) {
                            Toast.makeText(
                                context,
                                "⚠️ Sucursal más cercana: ${sucursal.nombre} a ${distanciaKm}km. Las sucursales están en Buenos Aires.",
                                Toast.LENGTH_LONG
                            ).show()
                        } else {
                            Toast.makeText(
                                context,
                                "✅ ${sucursal.nombre} - ${distanciaKm}km",
                                Toast.LENGTH_SHORT
                            ).show()
                        }
                        
                        // Abrir Google Maps con la ubicación de la sucursal
                        val intent = Intent(Intent.ACTION_VIEW, Uri.parse(sucursal.google_maps_url))
                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                        context.startActivity(intent)
                    }
                } else {
                    Toast.makeText(context, "No se encontraron sucursales de ${producto.supermercado}", Toast.LENGTH_SHORT).show()
                }
            }
            
            override fun onFailure(call: Call<SucursalCercanaResponse>, t: Throwable) {
                Toast.makeText(context, "Error conectando al servidor: ${t.message}", Toast.LENGTH_LONG).show()
            }
        })
    }
}