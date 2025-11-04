package com.precioscerca

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.precioscerca.adapters.ProductAdapter
import com.precioscerca.api.ApiClient
import com.precioscerca.api.BusquedaApiResponse
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MainActivity : AppCompatActivity() {
    
    private lateinit var etBusqueda: EditText
    private lateinit var btnBuscar: Button
    private lateinit var recyclerProductos: RecyclerView
    private lateinit var progressBar: ProgressBar
    private lateinit var fabVerLista: FloatingActionButton
    private lateinit var productAdapter: ProductAdapter
    
    // Lista de términos para buscar aleatoriamente
    private val terminosAleatorios = listOf(
        "leche", "pan", "arroz", "fideos", "aceite", 
        "azúcar", "yerba", "café", "galletitas", "agua"
    )
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // Configurar título
        supportActionBar?.title = "PreciosCerca"
        
        initViews()
        setupListeners()
        cargarProductosAleatorios()
    }
    
    private fun initViews() {
        etBusqueda = findViewById(R.id.etBusqueda)
        btnBuscar = findViewById(R.id.btnBuscar)
        recyclerProductos = findViewById(R.id.recyclerProductos)
        progressBar = findViewById(R.id.progressBar)
        fabVerLista = findViewById(R.id.fabVerLista)
        
        // Configurar RecyclerView
        productAdapter = ProductAdapter()
        recyclerProductos.layoutManager = LinearLayoutManager(this)
        recyclerProductos.adapter = productAdapter
    }
    
    private fun setupListeners() {
        // Buscar al presionar el botón
        btnBuscar.setOnClickListener {
            realizarBusqueda()
        }
        
        // Buscar al presionar Enter
        etBusqueda.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_SEARCH) {
                realizarBusqueda()
                true
            } else {
                false
            }
        }
        
        // Botón flotante para ver lista
        fabVerLista.setOnClickListener {
            val intent = Intent(this, ListaComprasActivity::class.java)
            startActivity(intent)
        }
    }
    
    private fun realizarBusqueda() {
        val query = etBusqueda.text.toString().trim()
        
        if (query.isEmpty()) {
            Toast.makeText(this, "Escribí un producto para buscar", Toast.LENGTH_SHORT).show()
            return
        }
        
        if (query.length < 2) {
            Toast.makeText(this, "Escribí al menos 2 caracteres", Toast.LENGTH_SHORT).show()
            return
        }
        
        // Ir a la pantalla de resultados
        val intent = Intent(this, ProductListActivity::class.java)
        intent.putExtra(ProductListActivity.EXTRA_QUERY, query)
        startActivity(intent)
    }
    
    private fun cargarProductosAleatorios() {
        // Elegir un término aleatorio
        val terminoAleatorio = terminosAleatorios.random()
        
        progressBar.visibility = View.VISIBLE
        recyclerProductos.visibility = View.GONE
        
        // Buscar productos
        ApiClient.api.buscarProductos(terminoAleatorio).enqueue(object : Callback<BusquedaApiResponse> {
            override fun onResponse(
                call: Call<BusquedaApiResponse>,
                response: Response<BusquedaApiResponse>
            ) {
                progressBar.visibility = View.GONE
                
                if (response.isSuccessful) {
                    val busqueda = response.body()
                    if (busqueda != null && busqueda.resultados.isNotEmpty()) {
                        // Mostrar solo los primeros 10 productos
                        val productosLimitados = busqueda.resultados.take(10)
                        productAdapter.actualizarProductos(productosLimitados)
                        recyclerProductos.visibility = View.VISIBLE
                    }
                }
            }
            
            override fun onFailure(call: Call<BusquedaApiResponse>, t: Throwable) {
                progressBar.visibility = View.GONE
                Toast.makeText(
                    this@MainActivity,
                    "Error cargando productos",
                    Toast.LENGTH_SHORT
                ).show()
            }
        })
    }
    
    override fun onResume() {
        super.onResume()
        // Recargar productos aleatorios cada vez que vuelve a la pantalla
        cargarProductosAleatorios()
    }
}
