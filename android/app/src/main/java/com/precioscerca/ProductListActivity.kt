package com.precioscerca

import android.os.Bundle
import android.view.View
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
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
    }

    private lateinit var tvBusquedaTitulo: TextView
    private lateinit var tvTotalProductos: TextView
    private lateinit var tvSupermercados: TextView
    private lateinit var rvProductos: RecyclerView
    private lateinit var progressBar: ProgressBar
    private lateinit var tvSinResultados: TextView
    
    private lateinit var productAdapter: ProductAdapter
    private var query: String = ""

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
        realizarBusqueda()
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
        
        val call = ApiClient.api.buscarProductos(query)
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
        // Actualizar información de búsqueda
        tvTotalProductos.text = getString(R.string.productos_encontrados, response.total_encontrados)
        tvSupermercados.text = getString(R.string.supermercados_consultados, 
            response.supermercados_consultados.joinToString(", "))

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