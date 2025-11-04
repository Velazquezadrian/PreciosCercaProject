package com.precioscerca

import android.content.Intent
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.precioscerca.adapters.ProductoSimpleAdapter
import com.precioscerca.api.ApiClient
import com.precioscerca.api.BusquedaApiResponse
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ListaModoActivity : AppCompatActivity() {
    
    private lateinit var etBusqueda: EditText
    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: ProductoSimpleAdapter
    private lateinit var progressBar: ProgressBar
    private lateinit var tvMensaje: TextView
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_lista_modo)
        
        // Configurar toolbar
        supportActionBar?.apply {
            title = "Hacer Lista de Compras"
            setDisplayHomeAsUpEnabled(true)
        }
        
        initViews()
        setupListeners()
    }
    
    private fun initViews() {
        etBusqueda = findViewById(R.id.etBusqueda)
        recyclerView = findViewById(R.id.recyclerProductos)
        progressBar = findViewById(R.id.progressBar)
        tvMensaje = findViewById(R.id.tvMensaje)
        
        // Configurar RecyclerView
        adapter = ProductoSimpleAdapter()
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = adapter
    }
    
    private fun setupListeners() {
        // Enter en el campo de búsqueda
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
            Toast.makeText(this, "Ingresa un producto", Toast.LENGTH_SHORT).show()
            return
        }
        
        if (query.length < 2) {
            Toast.makeText(this, "Ingresa al menos 2 caracteres", Toast.LENGTH_SHORT).show()
            return
        }
        
        // Mostrar carga
        progressBar.visibility = View.VISIBLE
        recyclerView.visibility = View.GONE
        tvMensaje.visibility = View.GONE
        
        // Buscar productos
        ApiClient.api.buscarProductos(query).enqueue(object : Callback<BusquedaApiResponse> {
            override fun onResponse(
                call: Call<BusquedaApiResponse>,
                response: Response<BusquedaApiResponse>
            ) {
                progressBar.visibility = View.GONE
                
                if (response.isSuccessful) {
                    val busqueda = response.body()
                    if (busqueda != null && busqueda.resultados.isNotEmpty()) {
                        adapter.actualizarProductos(busqueda.resultados)
                        recyclerView.visibility = View.VISIBLE
                        Toast.makeText(
                            this@ListaModoActivity,
                            "${busqueda.total_encontrados} productos encontrados",
                            Toast.LENGTH_SHORT
                        ).show()
                    } else {
                        mostrarMensaje("No se encontraron productos para \"$query\"")
                    }
                } else {
                    mostrarMensaje("Error buscando productos")
                }
            }
            
            override fun onFailure(call: Call<BusquedaApiResponse>, t: Throwable) {
                progressBar.visibility = View.GONE
                mostrarMensaje("Error de conexión: ${t.message}")
            }
        })
    }
    
    private fun mostrarMensaje(mensaje: String) {
        tvMensaje.text = mensaje
        tvMensaje.visibility = View.VISIBLE
        recyclerView.visibility = View.GONE
    }
    
    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.menu_lista_modo, menu)
        return true
    }
    
    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_ver_lista -> {
                val intent = Intent(this, ListaComprasActivity::class.java)
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
