package com.precioscerca

import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.precioscerca.adapters.ListaComprasAdapter
import com.precioscerca.api.ApiClient
import com.precioscerca.api.AgregarItemRequest
import com.precioscerca.api.EliminarItemRequest
import com.precioscerca.api.ListaComprasResponse
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ListaComprasActivity : AppCompatActivity() {
    
    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: ListaComprasAdapter
    private lateinit var progressBar: ProgressBar
    private lateinit var tvVacia: LinearLayout
    private lateinit var etNuevoItem: EditText
    private lateinit var btnAgregar: Button
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_lista_compras)
        
        // Configurar toolbar
        supportActionBar?.apply {
            title = "Mi Lista de Compras"
            setDisplayHomeAsUpEnabled(true)
        }
        
        initViews()
        setupListeners()
        cargarLista()
    }
    
    private fun initViews() {
        recyclerView = findViewById(R.id.recyclerListaCompras)
        progressBar = findViewById(R.id.progressBar)
        tvVacia = findViewById(R.id.tvListaVacia)
        etNuevoItem = findViewById(R.id.etNuevoItem)
        btnAgregar = findViewById(R.id.btnAgregar)
        
        // Configurar RecyclerView
        adapter = ListaComprasAdapter(
            onEliminarClick = { item ->
                eliminarProducto(item.nombre)
            }
        )
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = adapter
    }
    
    private fun setupListeners() {
        btnAgregar.setOnClickListener {
            agregarItem()
        }
    }
    
    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.menu_lista_compras, menu)
        return true
    }
    
    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_limpiar -> {
                confirmarLimpiarLista()
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
    
    private fun agregarItem() {
        val nombre = etNuevoItem.text.toString().trim()
        
        if (nombre.isEmpty()) {
            Toast.makeText(this, "Escribe el nombre del producto", Toast.LENGTH_SHORT).show()
            return
        }
        
        val request = AgregarItemRequest(nombre, 1)
        
        ApiClient.api.agregarALista(request).enqueue(object : Callback<com.precioscerca.api.AgregarItemResponse> {
            override fun onResponse(
                call: Call<com.precioscerca.api.AgregarItemResponse>,
                response: Response<com.precioscerca.api.AgregarItemResponse>
            ) {
                if (response.isSuccessful) {
                    Toast.makeText(
                        this@ListaComprasActivity,
                        "✅ Agregado",
                        Toast.LENGTH_SHORT
                    ).show()
                    etNuevoItem.text.clear()
                    cargarLista()
                }
            }
            
            override fun onFailure(call: Call<com.precioscerca.api.AgregarItemResponse>, t: Throwable) {
                Toast.makeText(
                    this@ListaComprasActivity,
                    "Error agregando producto",
                    Toast.LENGTH_SHORT
                ).show()
            }
        })
    }
    
    private fun cargarLista() {
        progressBar.visibility = View.VISIBLE
        
        ApiClient.api.obtenerListaCompras().enqueue(object : Callback<ListaComprasResponse> {
            override fun onResponse(
                call: Call<ListaComprasResponse>,
                response: Response<ListaComprasResponse>
            ) {
                progressBar.visibility = View.GONE
                
                if (response.isSuccessful) {
                    val lista = response.body()
                    if (lista != null && lista.items.isNotEmpty()) {
                        adapter.actualizarItems(lista.items)
                        recyclerView.visibility = View.VISIBLE
                        tvVacia.visibility = View.GONE
                    } else {
                        recyclerView.visibility = View.GONE
                        tvVacia.visibility = View.VISIBLE
                    }
                } else {
                    Toast.makeText(
                        this@ListaComprasActivity,
                        "Error cargando lista",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            }
            
            override fun onFailure(call: Call<ListaComprasResponse>, t: Throwable) {
                progressBar.visibility = View.GONE
                Toast.makeText(
                    this@ListaComprasActivity,
                    "Error de conexión",
                    Toast.LENGTH_SHORT
                ).show()
            }
        })
    }
    
    private fun eliminarProducto(nombre: String) {
        val request = EliminarItemRequest(nombre)
        
        ApiClient.api.eliminarDeLista(request).enqueue(object : Callback<com.precioscerca.api.EliminarItemResponse> {
            override fun onResponse(
                call: Call<com.precioscerca.api.EliminarItemResponse>,
                response: Response<com.precioscerca.api.EliminarItemResponse>
            ) {
                if (response.isSuccessful) {
                    Toast.makeText(
                        this@ListaComprasActivity,
                        "Eliminado",
                        Toast.LENGTH_SHORT
                    ).show()
                    cargarLista()
                }
            }
            
            override fun onFailure(call: Call<com.precioscerca.api.EliminarItemResponse>, t: Throwable) {
                Toast.makeText(
                    this@ListaComprasActivity,
                    "Error",
                    Toast.LENGTH_SHORT
                ).show()
            }
        })
    }
    
    private fun confirmarLimpiarLista() {
        AlertDialog.Builder(this)
            .setTitle("Limpiar lista")
            .setMessage("¿Eliminar todos los productos?")
            .setPositiveButton("Sí") { _, _ ->
                limpiarLista()
            }
            .setNegativeButton("Cancelar", null)
            .show()
    }
    
    private fun limpiarLista() {
        ApiClient.api.limpiarLista().enqueue(object : Callback<com.precioscerca.api.LimpiarListaResponse> {
            override fun onResponse(
                call: Call<com.precioscerca.api.LimpiarListaResponse>,
                response: Response<com.precioscerca.api.LimpiarListaResponse>
            ) {
                if (response.isSuccessful) {
                    Toast.makeText(
                        this@ListaComprasActivity,
                        "Lista limpiada",
                        Toast.LENGTH_SHORT
                    ).show()
                    cargarLista()
                }
            }
            
            override fun onFailure(call: Call<com.precioscerca.api.LimpiarListaResponse>, t: Throwable) {
                Toast.makeText(
                    this@ListaComprasActivity,
                    "Error",
                    Toast.LENGTH_SHORT
                ).show()
            }
        })
    }
    
    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }
}
