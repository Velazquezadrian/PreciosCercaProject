package com.precioscerca

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.FileProvider
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.precioscerca.adapters.ListaTerminadaAdapter
import com.precioscerca.models.ProductoEnLista
import java.io.File

/**
 * Pantalla "Lista Terminada" - Muestra los productos con opción de marcar como comprados
 * (escala de grises). Permite compartir la lista por WhatsApp u otras apps.
 */
class ListaTerminadaActivity : AppCompatActivity() {

    private lateinit var recyclerListaTerminada: RecyclerView
    private lateinit var tvTotalTerminado: TextView
    private lateinit var btnCompartir: Button
    private lateinit var listaTerminadaAdapter: ListaTerminadaAdapter
    
    private val productosEnLista = mutableListOf<ProductoEnLista>()
    private var totalLista = 0.0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_lista_terminada)

        // Configurar toolbar
        supportActionBar?.apply {
            title = "Lista Terminada"
            setDisplayHomeAsUpEnabled(true)
        }

        // Inicializar vistas
        recyclerListaTerminada = findViewById(R.id.recyclerListaTerminada)
        tvTotalTerminado = findViewById(R.id.tvTotalTerminado)
        btnCompartir = findViewById(R.id.btnCompartir)

        // Obtener datos del intent
        productosEnLista.addAll(intent.getParcelableArrayListExtra("productos") ?: emptyList())
        totalLista = intent.getDoubleExtra("total", 0.0)

        // Configurar RecyclerView
        listaTerminadaAdapter = ListaTerminadaAdapter(productosEnLista)
        recyclerListaTerminada.layoutManager = LinearLayoutManager(this)
        recyclerListaTerminada.adapter = listaTerminadaAdapter

        // Actualizar total
        tvTotalTerminado.text = "$${String.format("%.2f", totalLista)}"

        // Configurar botón compartir
        btnCompartir.setOnClickListener {
            compartirLista()
        }
    }

    private fun compartirLista() {
        try {
            // Generar contenido de la lista
            val contenido = StringBuilder()
            contenido.append("🛒 MI LISTA DE COMPRA\n")
            contenido.append("=" .repeat(30))
            contenido.append("\n\n")
            
            productosEnLista.forEachIndexed { index, producto ->
                val estado = if (producto.comprado) "✅" else "⬜"
                contenido.append("${index + 1}. $estado ${producto.nombre}\n")
                contenido.append("   ${producto.supermercado} - $${String.format("%.2f", producto.precio)}\n")
                if (producto.cantidad > 1) {
                    contenido.append("   Cantidad: ${producto.cantidad}\n")
                }
                contenido.append("\n")
            }
            
            contenido.append("=" .repeat(30))
            contenido.append("\n💰 TOTAL: $${String.format("%.2f", totalLista)}\n")
            contenido.append("\n📱 Creado con Mi Lista de Precios")

            // Crear archivo temporal
            val archivo = File(cacheDir, "mi_lista_compras.txt")
            archivo.writeText(contenido.toString())

            // Compartir archivo
            val uri = FileProvider.getUriForFile(
                this,
                "${packageName}.fileprovider",
                archivo
            )

            val shareIntent = Intent(Intent.ACTION_SEND).apply {
                type = "text/plain"
                putExtra(Intent.EXTRA_TEXT, contenido.toString())
                putExtra(Intent.EXTRA_STREAM, uri)
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }

            startActivity(Intent.createChooser(shareIntent, "Compartir lista de compras"))

        } catch (e: Exception) {
            Toast.makeText(this, "Error al compartir: ${e.message}", Toast.LENGTH_SHORT).show()
            e.printStackTrace()
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        onBackPressed()
        return true
    }
}
