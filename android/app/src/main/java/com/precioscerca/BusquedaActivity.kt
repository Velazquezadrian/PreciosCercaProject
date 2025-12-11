package com.precioscerca

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.text.Editable
import android.text.TextWatcher
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
import com.precioscerca.adapters.SugerenciasAdapter
import com.precioscerca.api.ApiClient
import com.precioscerca.api.BusquedaApiResponse
import com.precioscerca.api.SugerenciasResponse
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
    private lateinit var recyclerSugerencias: RecyclerView
    private lateinit var tvTotal: TextView
    private lateinit var productAdapter: ProductAdapter
    private lateinit var sugerenciasAdapter: SugerenciasAdapter
    
    private var supermercadoId: String = ""
    private var supermercadoNombre: String = ""
    private var totalAcumulado: Double = 0.0
    private var modo: String = "CONSULTA" // LISTA o CONSULTA
    
    // Paginación
    private var currentPage = 1
    private var isLoading = false
    private var hasMorePages = false
    private var currentQuery = ""
    
    // Handler para debouncing del autocomplete
    private val searchHandler = Handler(Looper.getMainLooper())
    private var searchRunnable: Runnable? = null
    
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
        recyclerSugerencias = findViewById(R.id.recyclerSugerencias)
        tvTotal = findViewById(R.id.tvTotal)
        
        // Configurar RecyclerView de productos en cuadrícula (2 columnas)
        // Pasar modoLista = true si es modo LISTA, false si es CONSULTA
        val modoLista = (modo == "LISTA")
        productAdapter = ProductAdapter(
            modoLista = modoLista,
            onProductoAgregado = { precio ->
                // Actualizar total en tiempo real cuando se agrega un producto
                actualizarTotal(precio)
            }
        )
        recyclerProductos.layoutManager = LinearLayoutManager(this)
        recyclerProductos.adapter = productAdapter
        
        // Agregar scroll listener para paginación infinita
        recyclerProductos.addOnScrollListener(object : RecyclerView.OnScrollListener() {
            override fun onScrolled(recyclerView: RecyclerView, dx: Int, dy: Int) {
                super.onScrolled(recyclerView, dx, dy)
                
                val layoutManager = recyclerView.layoutManager as LinearLayoutManager
                val visibleItemCount = layoutManager.childCount
                val totalItemCount = layoutManager.itemCount
                val firstVisibleItemPosition = layoutManager.findFirstVisibleItemPosition()
                
                // Si llegó al final y hay más páginas
                if (!isLoading && hasMorePages) {
                    if ((visibleItemCount + firstVisibleItemPosition) >= totalItemCount 
                        && firstVisibleItemPosition >= 0) {
                        // Cargar siguiente página
                        cargarSiguientePagina()
                    }
                }
            }
        })
        
        // Configurar RecyclerView de sugerencias (lista vertical)
        sugerenciasAdapter = SugerenciasAdapter(emptyList()) { sugerenciaSeleccionada ->
            // Cuando el usuario toca una sugerencia
            etBusqueda.setText(sugerenciaSeleccionada)
            etBusqueda.setSelection(sugerenciaSeleccionada.length) // Cursor al final
            recyclerSugerencias.visibility = View.GONE
            realizarBusqueda()
        }
        recyclerSugerencias.layoutManager = LinearLayoutManager(this)
        recyclerSugerencias.adapter = sugerenciasAdapter
        
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
            // Ocultar sugerencias y cancelar búsquedas pendientes
            searchRunnable?.let { searchHandler.removeCallbacks(it) }
            recyclerSugerencias.visibility = View.GONE
            realizarBusqueda()
        }
        
        // Enter en el campo de texto
        etBusqueda.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_SEARCH) {
                // Ocultar sugerencias y cancelar búsquedas pendientes
                searchRunnable?.let { searchHandler.removeCallbacks(it) }
                recyclerSugerencias.visibility = View.GONE
                realizarBusqueda()
                true
            } else {
                false
            }
        }
        
        // TextWatcher con debouncing para autocomplete
        etBusqueda.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
            
            override fun afterTextChanged(s: Editable?) {
                // Cancelar búsqueda anterior si existe
                searchRunnable?.let { searchHandler.removeCallbacks(it) }
                
                val query = s?.toString()?.trim() ?: ""
                
                // Si el texto es muy corto, ocultar sugerencias
                if (query.length < 2) {
                    recyclerSugerencias.visibility = View.GONE
                    return
                }
                
                // Crear nueva búsqueda con delay de 1 segundo
                searchRunnable = Runnable {
                    cargarSugerencias(query)
                }
                searchHandler.postDelayed(searchRunnable!!, 1000)
            }
        })
    }
    
    private fun cargarSugerencias(query: String) {
        // Llamar al endpoint de sugerencias
        ApiClient.api.getSugerencias(query, supermercadoId, 10).enqueue(object : Callback<SugerenciasResponse> {
            override fun onResponse(
                call: Call<SugerenciasResponse>,
                response: Response<SugerenciasResponse>
            ) {
                if (response.isSuccessful) {
                    val sugerencias = response.body()
                    if (sugerencias != null && sugerencias.sugerencias.isNotEmpty()) {
                        sugerenciasAdapter.actualizarSugerencias(sugerencias.sugerencias)
                        recyclerSugerencias.visibility = View.VISIBLE
                    } else {
                        recyclerSugerencias.visibility = View.GONE
                    }
                } else {
                    recyclerSugerencias.visibility = View.GONE
                }
            }
            
            override fun onFailure(call: Call<SugerenciasResponse>, t: Throwable) {
                // En caso de error, simplemente no mostrar sugerencias
                recyclerSugerencias.visibility = View.GONE
            }
        })
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
        
        // Resetear paginación para nueva búsqueda
        currentPage = 1
        currentQuery = query
        productAdapter.limpiarProductos()
        
        buscarProductos(query, currentPage)
    }
    
    private fun cargarSiguientePagina() {
        if (currentQuery.isNotEmpty() && !isLoading && hasMorePages) {
            currentPage++
            buscarProductos(currentQuery, currentPage)
        }
    }
    
    private fun buscarProductos(query: String, page: Int = 1) {
        isLoading = true
        mostrarCarga(true, page > 1)
        
        // Buscar productos con filtro de supermercado y paginación
        ApiClient.api.buscarProductosPaginado(query, supermercadoId, page, 30).enqueue(object : Callback<BusquedaApiResponse> {
            override fun onResponse(
                call: Call<BusquedaApiResponse>,
                response: Response<BusquedaApiResponse>
            ) {
                isLoading = false
                mostrarCarga(false, false)
                
                if (response.isSuccessful) {
                    val busqueda = response.body()
                    
                    // ✅ VERIFICAR SI ESTÁ EN MANTENIMIENTO
                    if (busqueda?.maintenance == true) {
                        hasMorePages = false
                        if (page == 1) {
                            recyclerProductos.visibility = View.GONE
                            tvEstado.text = "🔧 Servidor en mantenimiento (8:00 AM)\n\nActualizando catálogo de productos.\nIntenta de nuevo en unos minutos."
                            tvEstado.visibility = View.VISIBLE
                        }
                        return
                    }
                    
                    if (busqueda != null && busqueda.resultados.isNotEmpty()) {
                        // Actualizar flag de más páginas
                        hasMorePages = busqueda.has_more ?: false
                        
                        if (page == 1) {
                            // Primera página: reemplazar productos
                            productAdapter.actualizarProductos(busqueda.resultados)
                        } else {
                            // Páginas siguientes: agregar productos
                            productAdapter.agregarProductos(busqueda.resultados)
                        }
                        
                        recyclerProductos.visibility = View.VISIBLE
                        tvEstado.visibility = View.GONE
                        
                        // Mostrar toast con info de paginación
                        if (page > 1) {
                            Toast.makeText(
                                this@BusquedaActivity,
                                "Mostrando ${busqueda.resultados.size} productos más",
                                Toast.LENGTH_SHORT
                            ).show()
                        }
                    } else {
                        if (page == 1) {
                            recyclerProductos.visibility = View.GONE
                            tvEstado.text = "No se encontraron productos"
                            tvEstado.visibility = View.VISIBLE
                        }
                        hasMorePages = false
                    }
                } else if (response.code() == 503) {
                    // Servidor en mantenimiento
                    hasMorePages = false
                    if (page == 1) {
                        recyclerProductos.visibility = View.GONE
                        tvEstado.text = "🔧 Servidor en mantenimiento (8:00 AM)\n\nActualizando catálogo de productos.\nIntenta de nuevo en unos minutos."
                        tvEstado.visibility = View.VISIBLE
                    }
                } else {
                    hasMorePages = false
                    if (page == 1) {
                        Toast.makeText(
                            this@BusquedaActivity,
                            "Error en la búsqueda",
                            Toast.LENGTH_SHORT
                        ).show()
                    }
                }
            }
            
            override fun onFailure(call: Call<BusquedaApiResponse>, t: Throwable) {
                isLoading = false
                mostrarCarga(false, false)
                hasMorePages = false
                
                if (page == 1) {
                    Toast.makeText(
                        this@BusquedaActivity,
                        "Error de conexión: ${t.message}",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            }
        })
    }
    
    private fun mostrarCarga(mostrar: Boolean, esPaginacion: Boolean = false) {
        if (mostrar) {
            if (esPaginacion) {
                // Mostrar loading discreto para paginación
                tvEstado.text = "Cargando más productos..."
                tvEstado.visibility = View.VISIBLE
            } else {
                // Loading normal para primera búsqueda
                progressBar.visibility = View.VISIBLE
                tvEstado.text = "Buscando productos..."
                tvEstado.visibility = View.VISIBLE
                btnBuscar.isEnabled = false
                recyclerProductos.visibility = View.GONE
            }
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
