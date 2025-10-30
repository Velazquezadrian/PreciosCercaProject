package com.precioscerca

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationManager
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.precioscerca.adapters.ProductAdapter
import com.precioscerca.api.ApiClient
import com.precioscerca.api.BusquedaApiResponse
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ProductListActivity : AppCompatActivity() {

    companion object {
        const val EXTRA_QUERY = "extra_query"
        const val LOCATION_PERMISSION_REQUEST_CODE = 1001
        const val DEFAULT_RADIO_KM = 50.0
    }

    private lateinit var tvBusquedaTitulo: TextView
    private lateinit var tvTotalProductos: TextView
    private lateinit var tvSupermercados: TextView
    private lateinit var rvProductos: RecyclerView
    private lateinit var progressBar: ProgressBar
    private lateinit var tvSinResultados: TextView
    
    private lateinit var productAdapter: ProductAdapter
    private var query: String = ""
    private var radioKm: Double = DEFAULT_RADIO_KM
    private var usarBusquedaCercana: Boolean = false
    private var ubicacionUsuario: Location? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_product_list)

        // Configurar ActionBar
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.title = "Resultados"

        // Obtener query del intent
        query = intent.getStringExtra(EXTRA_QUERY) ?: ""
        
        initViews()
        setupRecyclerView()
        cargarPreferencias()
        
        // Intentar obtener ubicación antes de buscar
        if (verificarPermisosUbicacion()) {
            obtenerUbicacion()
        } else {
            solicitarPermisosUbicacion()
        }
        
        realizarBusqueda()
    }
    
    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.menu_product_list, menu)
        return true
    }
    
    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_radio -> {
                mostrarDialogoRadio()
                true
            }
            R.id.action_toggle_busqueda -> {
                toggleTipoBusqueda()
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
    
    private fun cargarPreferencias() {
        val prefs = getSharedPreferences("PreciosCerca", Context.MODE_PRIVATE)
        radioKm = prefs.getFloat("radio_km", DEFAULT_RADIO_KM.toFloat()).toDouble()
        usarBusquedaCercana = prefs.getBoolean("usar_busqueda_cercana", true)
    }
    
    private fun guardarPreferencias() {
        val prefs = getSharedPreferences("PreciosCerca", Context.MODE_PRIVATE)
        prefs.edit().apply {
            putFloat("radio_km", radioKm.toFloat())
            putBoolean("usar_busqueda_cercana", usarBusquedaCercana)
            apply()
        }
    }
    
    private fun verificarPermisosUbicacion(): Boolean {
        return ContextCompat.checkSelfPermission(
            this,
            Manifest.permission.ACCESS_FINE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED
    }
    
    private fun obtenerUbicacion() {
        if (!verificarPermisosUbicacion()) {
            return
        }
        
        try {
            val locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager
            
            // Intentar obtener última ubicación conocida
            val providers = listOf(
                LocationManager.GPS_PROVIDER,
                LocationManager.NETWORK_PROVIDER
            )
            
            for (provider in providers) {
                if (locationManager.isProviderEnabled(provider)) {
                    val location = locationManager.getLastKnownLocation(provider)
                    if (location != null && esUbicacionValida(location)) {
                        ubicacionUsuario = location
                        break
                    }
                }
            }
            
            if (ubicacionUsuario != null) {
                val lat = ubicacionUsuario!!.latitude
                val lng = ubicacionUsuario!!.longitude
                Toast.makeText(
                    this, 
                    "📍 Ubicación: ${String.format("%.4f", lat)}, ${String.format("%.4f", lng)}", 
                    Toast.LENGTH_SHORT
                ).show()
            } else {
                Toast.makeText(
                    this, 
                    "⚠️ No se pudo obtener ubicación. Configure GPS en BlueStacks.", 
                    Toast.LENGTH_LONG
                ).show()
            }
        } catch (e: SecurityException) {
            Toast.makeText(this, "Error al acceder a la ubicación", Toast.LENGTH_SHORT).show()
        }
    }
    
    private fun esUbicacionValida(location: Location): Boolean {
        val lat = location.latitude
        val lng = location.longitude
        
        // Validar que no sea la ubicación por defecto (0,0) o coordenadas inválidas
        if (lat == 0.0 && lng == 0.0) return false
        
        // Validar que esté dentro de rangos razonables de Argentina
        // Argentina: lat entre -55 y -21, lng entre -73 y -53
        if (lat < -55 || lat > -21) return false
        if (lng < -73 || lng > -53) return false
        
        return true
    }
    
    private fun mostrarDialogoRadio() {
        val opciones = arrayOf("10 km", "20 km", "30 km", "50 km", "100 km")
        val valores = arrayOf(10.0, 20.0, 30.0, 50.0, 100.0)
        
        // Encontrar opción actual
        val seleccionActual = valores.indexOfFirst { it == radioKm }.takeIf { it >= 0 } ?: 3
        
        AlertDialog.Builder(this)
            .setTitle("Radio de búsqueda")
            .setSingleChoiceItems(opciones, seleccionActual) { dialog, which ->
                radioKm = valores[which]
                guardarPreferencias()
                Toast.makeText(this, "Radio actualizado a ${opciones[which]}", Toast.LENGTH_SHORT).show()
                realizarBusqueda()
                dialog.dismiss()
            }
            .setNegativeButton("Cancelar", null)
            .show()
    }
    
    private fun toggleTipoBusqueda() {
        usarBusquedaCercana = !usarBusquedaCercana
        guardarPreferencias()
        
        val mensaje = if (usarBusquedaCercana) {
            "Búsqueda cercana activada (radio: ${radioKm.toInt()} km)"
        } else {
            "Búsqueda general activada (todos los supermercados)"
        }
        
        Toast.makeText(this, mensaje, Toast.LENGTH_SHORT).show()
        realizarBusqueda()
    }
    
    private fun solicitarPermisosUbicacion() {
        if (ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION
                ),
                LOCATION_PERMISSION_REQUEST_CODE
            )
        }
    }
    
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == LOCATION_PERMISSION_REQUEST_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "Permiso de ubicación concedido", Toast.LENGTH_SHORT).show()
                obtenerUbicacion()
                realizarBusqueda()
            } else {
                Toast.makeText(this, "Sin ubicación, mostrando todos los supermercados", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun initViews() {
        tvBusquedaTitulo = findViewById(R.id.tvBusquedaTitulo)
        tvTotalProductos = findViewById(R.id.tvTotalProductos)
        tvSupermercados = findViewById(R.id.tvSupermercados)
        rvProductos = findViewById(R.id.rvProductos)
        progressBar = findViewById(R.id.progressBar)
        tvSinResultados = findViewById(R.id.tvSinResultados)
        
        // Configurar título inicial
        tvBusquedaTitulo.text = getString(R.string.resultados_para, query)
    }

    private fun setupRecyclerView() {
        productAdapter = ProductAdapter()
        rvProductos.apply {
            layoutManager = LinearLayoutManager(this@ProductListActivity)
            adapter = productAdapter
        }
    }

    private fun realizarBusqueda() {
        mostrarCarga(true)
        
        // Decidir qué endpoint usar
        val call = if (usarBusquedaCercana && ubicacionUsuario != null && esUbicacionValida(ubicacionUsuario!!)) {
            val lat = ubicacionUsuario!!.latitude
            val lng = ubicacionUsuario!!.longitude
            println("🔍 Búsqueda cercana: lat=$lat, lng=$lng, radio=$radioKm km")
            ApiClient.api.buscarProductosCercanos(query, lat, lng, radioKm)
        } else {
            if (usarBusquedaCercana) {
                Toast.makeText(this, "Ubicación no disponible, mostrando todos", Toast.LENGTH_SHORT).show()
            }
            ApiClient.api.buscarProductos(query)
        }
        
        call.enqueue(object : Callback<BusquedaApiResponse> {
            override fun onResponse(
                call: Call<BusquedaApiResponse>,
                response: Response<BusquedaApiResponse>
            ) {
                mostrarCarga(false)
                
                if (response.isSuccessful) {
                    val busquedaResponse = response.body()
                    if (busquedaResponse != null) {
                        mostrarResultados(busquedaResponse)
                    } else {
                        mostrarError("Respuesta vacía del servidor")
                    }
                } else {
                    mostrarError("Error del servidor: ${response.code()}")
                }
            }

            override fun onFailure(call: Call<BusquedaApiResponse>, t: Throwable) {
                mostrarCarga(false)
                mostrarError("Error de conexión: ${t.message}")
            }
        })
    }

    private fun mostrarResultados(response: BusquedaApiResponse) {
        // Construir información adicional según el tipo de búsqueda
        val infoAdicional = if (usarBusquedaCercana && ubicacionUsuario != null) {
            val ciudadInfo = if (response.ciudad_detectada != null) {
                " en ${response.ciudad_detectada}"
            } else {
                ""
            }
            
            // Agregar info del supermercado más cercano si está disponible
            val superCercanoInfo = if (response.supermercado_mas_cercano != null && response.distancia_supermercado_mas_cercano_km != null) {
                "\n🏆 Más cercano: ${response.supermercado_mas_cercano} (${String.format("%.1f", response.distancia_supermercado_mas_cercano_km)} km)"
            } else {
                ""
            }
            
            // DEBUG: Mostrar coordenadas GPS del usuario
            val coordsDebug = "\n📍 Tu GPS: (${String.format("%.4f", ubicacionUsuario!!.latitude)}, ${String.format("%.4f", ubicacionUsuario!!.longitude)})"
            
            " (Radio: ${radioKm.toInt()} km$ciudadInfo)$superCercanoInfo$coordsDebug"
        } else {
            ""
        }
        
        tvTotalProductos.text = getString(R.string.productos_encontrados, response.total_encontrados)
        
        // Mostrar información de supermercados
        if (response.supermercados_consultados.isNotEmpty()) {
            tvSupermercados.text = "Supermercados: ${response.supermercados_consultados.joinToString(", ")}$infoAdicional"
        } else if (response.mensaje != null) {
            // Si hay mensaje del servidor (ej: "No hay supermercados cercanos")
            tvSupermercados.text = response.mensaje
        } else {
            tvSupermercados.text = "Sin supermercados disponibles$infoAdicional"
        }

        // Mostrar productos
        if (response.resultados.isNotEmpty()) {
            productAdapter.actualizarProductos(response.resultados)
            rvProductos.visibility = View.VISIBLE
            tvSinResultados.visibility = View.GONE
        } else {
            mostrarSinResultados()
        }
    }

    private fun mostrarSinResultados() {
        rvProductos.visibility = View.GONE
        tvSinResultados.visibility = View.VISIBLE
        tvTotalProductos.text = getString(R.string.productos_encontrados, 0)
    }

    private fun mostrarError(mensaje: String) {
        Toast.makeText(this, mensaje, Toast.LENGTH_LONG).show()
        mostrarSinResultados()
    }

    private fun mostrarCarga(mostrar: Boolean) {
        if (mostrar) {
            progressBar.visibility = View.VISIBLE
            rvProductos.visibility = View.GONE
            tvSinResultados.visibility = View.GONE
        } else {
            progressBar.visibility = View.GONE
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }
}