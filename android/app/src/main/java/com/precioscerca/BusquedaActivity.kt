package com.precioscerca

import android.content.Intent
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.button.MaterialButton
import com.google.android.material.textfield.TextInputEditText
import android.widget.ProgressBar
import android.widget.TextView
import com.precioscerca.adapters.ProductAdapter
import com.precioscerca.api.ApiClient
import com.precioscerca.api.BusquedaApiResponse
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

// ========== [BÚSQUEDA] BUSCAR PRODUCTOS EN SUPER ELEGIDO ==========
// Recibe supermercado_id desde SeleccionSuperActivity
// Busca productos filtrando por ese supermercado usando API
// Muestra total acumulado en tiempo real arriba
// Menu con ícono carrito para ir a MiListaActivity
// ==================================================================

class BusquedaActivity : AppCompatActivity() {
    
    private lateinit var etBusqueda: TextInputEditText
    private lateinit var btnBuscar: MaterialButton
    private lateinit var progressBar: ProgressBar
    private lateinit var tvEstado: TextView
    private lateinit var recyclerProductos: RecyclerView
    private lateinit var tvTotal: TextView
    private lateinit var productAdapter: ProductAdapter
    
    private var supermercadoId: String = ""
    private var supermercadoNombre: String = ""
    private var totalAcumulado: Double = 0.0
    private var modo: String = "CONSULTA" // LISTA o CONSULTA
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_busqueda)
        
        // Recibir datos del supermercado y modo
        supermercadoId = intent.getStringExtra("SUPERMERCADO_ID") ?: ""
        supermercadoNombre = intent.getStringExtra("SUPERMERCADO_NOMBRE") ?: ""
        modo = intent.getStringExtra("MODO") ?: "CONSULTA"
        
        // Configurar toolbar según el modo
        supportActionBar?.apply {
            title = if (modo == "LISTA") {
                "$supermercadoNombre - Mi Lista"
            } else {
                "$supermercadoNombre - Consulta"
            }
            setDisplayHomeAsUpEnabled(true)
        }
        
        initViews()
        setupListeners()
    }
    
    private fun initViews() {
        etBusqueda = findViewById(R.id.etBusqueda)
        btnBuscar = findViewById(R.id.btnBuscar)
        progressBar = findViewById(R.id.progressBar)
        tvEstado = findViewById(R.id.tvEstado)
        recyclerProductos = findViewById(R.id.recyclerProductos)
        tvTotal = findViewById(R.id.tvTotal)
        
        // Configurar RecyclerView en cuadrícula (3 columnas)
        // Pasar modoLista = true si es modo LISTA, false si es CONSULTA
        val modoLista = (modo == "LISTA")
        productAdapter = ProductAdapter(
            modoLista = modoLista,
            onProductoAgregado = { precio ->
                // Actualizar total en tiempo real cuando se agrega un producto
                actualizarTotal(precio)
            }
        )
        recyclerProductos.layoutManager = GridLayoutManager(this, 3)
        recyclerProductos.adapter = productAdapter
        
        // Mostrar/ocultar total según el modo
        if (modo == "CONSULTA") {
            tvTotal.visibility = View.GONE // No mostrar total en modo consulta
        } else {
            // Inicializar el total en $0
            actualizarTotalDisplay()
        }
        
        // Ocultar inicialmente
        recyclerProductos.visibility = View.GONE
    }
    
    private fun setupListeners() {
        // Botón de búsqueda
        btnBuscar.setOnClickListener {
            realizarBusqueda()
        }
        
        // Enter en el campo de texto
        etBusqueda.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_SEARCH) {
                realizarBusqueda()
                true
            } else {
                false
            }
        }
    }
    
    private fun realizarBusqueda() {
        val query = etBusqueda.text?.toString()?.trim()
        
        if (query.isNullOrEmpty()) {
            Toast.makeText(this, "Ingresa un producto para buscar", Toast.LENGTH_SHORT).show()
            return
        }
        
        if (query.length < 2) {
            Toast.makeText(this, "Ingresa al menos 2 caracteres", Toast.LENGTH_SHORT).show()
            return
        }
        
        buscarProductos(query)
    }
    
    private fun buscarProductos(query: String) {
        mostrarCarga(true)
        
        // Buscar productos con filtro de supermercado
        ApiClient.api.buscarProductos(query, supermercadoId).enqueue(object : Callback<BusquedaApiResponse> {
            override fun onResponse(
                call: Call<BusquedaApiResponse>,
                response: Response<BusquedaApiResponse>
            ) {
                mostrarCarga(false)
                
                if (response.isSuccessful) {
                    val busqueda = response.body()
                    if (busqueda != null && busqueda.resultados.isNotEmpty()) {
                        productAdapter.actualizarProductos(busqueda.resultados)
                        recyclerProductos.visibility = View.VISIBLE
                        tvEstado.visibility = View.GONE
                    } else {
                        recyclerProductos.visibility = View.GONE
                        tvEstado.text = "No se encontraron productos"
                        tvEstado.visibility = View.VISIBLE
                    }
                } else {
                    Toast.makeText(
                        this@BusquedaActivity,
                        "Error en la búsqueda",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            }
            
            override fun onFailure(call: Call<BusquedaApiResponse>, t: Throwable) {
                mostrarCarga(false)
                Toast.makeText(
                    this@BusquedaActivity,
                    "Error de conexión",
                    Toast.LENGTH_SHORT
                ).show()
            }
        })
    }
    
    private fun mostrarCarga(mostrar: Boolean) {
        if (mostrar) {
            progressBar.visibility = View.VISIBLE
            tvEstado.text = "Buscando productos..."
            tvEstado.visibility = View.VISIBLE
            btnBuscar.isEnabled = false
            recyclerProductos.visibility = View.GONE
        } else {
            progressBar.visibility = View.GONE
            tvEstado.visibility = View.GONE
            btnBuscar.isEnabled = true
        }
    }
    
    private fun actualizarTotal(precio: Double) {
        // Sumar el precio al total acumulado
        totalAcumulado += precio
        actualizarTotalDisplay()
    }
    
    private fun actualizarTotalDisplay() {
        // Mostrar el total con formato de moneda (sin etiqueta "Total:" porque ya está en el layout)
        tvTotal.text = "$${String.format("%.2f", totalAcumulado)}"
    }
    
    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        // Solo mostrar menú en modo LISTA
        if (modo == "LISTA") {
            menuInflater.inflate(R.menu.menu_busqueda, menu)
        }
        return true
    }
    
    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_ver_lista -> {
                // Abrir MiListaActivity para ver productos agregados
                val intent = Intent(this, MiListaActivity::class.java)
                startActivity(intent)
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
    
    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }
}
