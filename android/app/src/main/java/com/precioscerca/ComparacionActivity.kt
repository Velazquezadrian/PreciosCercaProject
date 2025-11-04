package com.precioscerca

import android.os.Bundle
import android.view.View
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.precioscerca.adapters.ComparacionAdapter
import com.precioscerca.api.ApiClient
import com.precioscerca.api.ComparacionResponse
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ComparacionActivity : AppCompatActivity() {
    
    private lateinit var progressBar: ProgressBar
    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: ComparacionAdapter
    private lateinit var tvTitulo: TextView
    private lateinit var tvMasBarato: TextView
    private lateinit var containerMasBarato: View
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_comparacion)
        
        // Configurar toolbar
        supportActionBar?.apply {
            title = "Comparación de Precios"
            setDisplayHomeAsUpEnabled(true)
        }
        
        // Inicializar vistas
        progressBar = findViewById(R.id.progressBar)
        recyclerView = findViewById(R.id.recyclerComparacion)
        tvTitulo = findViewById(R.id.tvTitulo)
        tvMasBarato = findViewById(R.id.tvMasBarato)
        containerMasBarato = findViewById(R.id.containerMasBarato)
        
        // Configurar RecyclerView
        adapter = ComparacionAdapter()
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = adapter
        
        // Cargar comparación
        compararPrecios()
    }
    
    private fun compararPrecios() {
        progressBar.visibility = View.VISIBLE
        recyclerView.visibility = View.GONE
        containerMasBarato.visibility = View.GONE
        
        ApiClient.api.compararLista().enqueue(object : Callback<ComparacionResponse> {
            override fun onResponse(
                call: Call<ComparacionResponse>,
                response: Response<ComparacionResponse>
            ) {
                progressBar.visibility = View.GONE
                
                if (response.isSuccessful) {
                    val comparacion = response.body()
                    
                    if (comparacion?.error != null) {
                        Toast.makeText(
                            this@ComparacionActivity,
                            comparacion.error,
                            Toast.LENGTH_LONG
                        ).show()
                        finish()
                        return
                    }
                    
                    if (comparacion != null && comparacion.supermercados.isNotEmpty()) {
                        mostrarComparacion(comparacion)
                    } else {
                        Toast.makeText(
                            this@ComparacionActivity,
                            "No se encontraron productos",
                            Toast.LENGTH_LONG
                        ).show()
                        finish()
                    }
                } else {
                    Toast.makeText(
                        this@ComparacionActivity,
                        "Error al comparar precios",
                        Toast.LENGTH_SHORT
                    ).show()
                    finish()
                }
            }
            
            override fun onFailure(call: Call<ComparacionResponse>, t: Throwable) {
                progressBar.visibility = View.GONE
                Toast.makeText(
                    this@ComparacionActivity,
                    "Error de conexión: ${t.message}",
                    Toast.LENGTH_LONG
                ).show()
                finish()
            }
        })
    }
    
    private fun mostrarComparacion(comparacion: ComparacionResponse) {
        tvTitulo.text = "Comparando ${comparacion.total_productos_buscados} producto(s)"
        
        // Mostrar el más barato
        if (comparacion.mas_barato != null) {
            containerMasBarato.visibility = View.VISIBLE
            tvMasBarato.text = String.format(
                "🏆 Más barato: %s - $%.2f\n(%d productos encontrados)",
                comparacion.mas_barato.nombre,
                comparacion.mas_barato.total,
                comparacion.mas_barato.productos_encontrados
            )
        }
        
        // Mostrar todos los supermercados
        adapter.actualizarSupermercados(comparacion.supermercados)
        recyclerView.visibility = View.VISIBLE
    }
    
    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }
}
