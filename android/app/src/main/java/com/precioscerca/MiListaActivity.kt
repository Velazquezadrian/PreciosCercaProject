package com.precioscerca

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.precioscerca.adapters.MiListaAdapter
import com.precioscerca.api.ApiClient
import com.precioscerca.models.ProductoEnLista
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

/**
 * Pantalla "Mi Lista" - Muestra los productos agregados a la lista
 * con imagen, nombre, precio y total acumulado.
 * Permite terminar la lista para marcar productos como comprados.
 */
class MiListaActivity : AppCompatActivity() {

    private lateinit var recyclerLista: RecyclerView
    private lateinit var tvTotalLista: TextView
    private lateinit var tvEstadoLista: TextView
    private lateinit var btnTerminarLista: Button
    private lateinit var miListaAdapter: MiListaAdapter
    
    private val productosEnLista = mutableListOf<ProductoEnLista>()
    private var totalLista = 0.0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_mi_lista)

        // Configurar toolbar
        supportActionBar?.apply {
            title = "Mi Lista de Compra"
            setDisplayHomeAsUpEnabled(true)
        }

        // Inicializar vistas
        recyclerLista = findViewById(R.id.recyclerLista)
        tvTotalLista = findViewById(R.id.tvTotalLista)
        tvEstadoLista = findViewById(R.id.tvEstadoLista)
        btnTerminarLista = findViewById(R.id.btnTerminarLista)

        // Configurar RecyclerView
        miListaAdapter = MiListaAdapter(productosEnLista) { producto ->
            eliminarProducto(producto)
        }
        recyclerLista.layoutManager = LinearLayoutManager(this)
        recyclerLista.adapter = miListaAdapter

        // Configurar botón
        btnTerminarLista.setOnClickListener {
            terminarLista()
        }

        // Cargar lista desde el servidor
        cargarLista()
    }

    private fun cargarLista() {
        tvEstadoLista.text = "Cargando tu lista..."
        tvEstadoLista.visibility = View.VISIBLE
        recyclerLista.visibility = View.GONE
        btnTerminarLista.visibility = View.GONE

        ApiClient.api.obtenerListaCompras().enqueue(object : Callback<com.precioscerca.api.ListaComprasResponse> {
            override fun onResponse(call: Call<com.precioscerca.api.ListaComprasResponse>, response: Response<com.precioscerca.api.ListaComprasResponse>) {
                if (response.isSuccessful) {
                    val data = response.body()
                    val items = data?.items ?: emptyList()
                    
                    productosEnLista.clear()
                    totalLista = 0.0
                    
                    items.forEach { item ->
                        val producto = ProductoEnLista(
                            nombre = item.nombre,
                            precio = item.precio,
                            supermercado = item.supermercado,
                            imagen = item.imagen,
                            cantidad = item.cantidad
                        )
                        productosEnLista.add(producto)
                        totalLista += producto.precio * producto.cantidad
                    }
                    
                    if (productosEnLista.isEmpty()) {
                        tvEstadoLista.text = "Tu lista está vacía\nAgregá productos desde la búsqueda"
                        tvEstadoLista.visibility = View.VISIBLE
                        recyclerLista.visibility = View.GONE
                        btnTerminarLista.visibility = View.GONE
                    } else {
                        tvEstadoLista.visibility = View.GONE
                        recyclerLista.visibility = View.VISIBLE
                        btnTerminarLista.visibility = View.VISIBLE
                        miListaAdapter.notifyDataSetChanged()
                    }
                    
                    actualizarTotal()
                } else {
                    Toast.makeText(this@MiListaActivity, "Error al cargar la lista", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<com.precioscerca.api.ListaComprasResponse>, t: Throwable) {
                Toast.makeText(this@MiListaActivity, "Error de conexión: ${t.message}", Toast.LENGTH_SHORT).show()
                tvEstadoLista.text = "Error al cargar la lista"
            }
        })
    }

    private fun eliminarProducto(producto: ProductoEnLista) {
        // Eliminar del servidor
        val requestBody = com.precioscerca.api.EliminarItemRequest(nombre = producto.nombre)
        ApiClient.api.eliminarDeLista(requestBody).enqueue(object : Callback<com.precioscerca.api.EliminarItemResponse> {
            override fun onResponse(call: Call<com.precioscerca.api.EliminarItemResponse>, response: Response<com.precioscerca.api.EliminarItemResponse>) {
                if (response.isSuccessful) {
                    // Eliminar localmente
                    productosEnLista.remove(producto)
                    totalLista -= producto.precio * producto.cantidad
                    miListaAdapter.notifyDataSetChanged()
                    actualizarTotal()
                    
                    Toast.makeText(this@MiListaActivity, "Producto eliminado", Toast.LENGTH_SHORT).show()
                    
                    // Si la lista quedó vacía, actualizar UI
                    if (productosEnLista.isEmpty()) {
                        tvEstadoLista.text = "Tu lista está vacía"
                        tvEstadoLista.visibility = View.VISIBLE
                        recyclerLista.visibility = View.GONE
                        btnTerminarLista.visibility = View.GONE
                    }
                }
            }

            override fun onFailure(call: Call<com.precioscerca.api.EliminarItemResponse>, t: Throwable) {
                Toast.makeText(this@MiListaActivity, "Error al eliminar", Toast.LENGTH_SHORT).show()
            }
        })
    }

    private fun actualizarTotal() {
        tvTotalLista.text = "$${String.format("%.2f", totalLista)}"
    }

    private fun terminarLista() {
        if (productosEnLista.isEmpty()) {
            Toast.makeText(this, "No hay productos en la lista", Toast.LENGTH_SHORT).show()
            return
        }

        // Pasar a la pantalla de lista terminada
        val intent = Intent(this, ListaTerminadaActivity::class.java)
        intent.putParcelableArrayListExtra("productos", ArrayList(productosEnLista))
        intent.putExtra("total", totalLista)
        startActivity(intent)
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        return true
    }
}
