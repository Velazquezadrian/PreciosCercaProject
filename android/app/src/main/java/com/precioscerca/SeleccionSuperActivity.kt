package com.precioscerca

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.cardview.widget.CardView

// ========== [SELECCIÓN] ELEGIR SUPERMERCADO ==========
// Muestra 3 cards grandes con Carrefour, Día % y La Reina
// Soporta dos modos:
// - LISTA: Para crear lista de compra con subtotal
// - CONSULTA: Solo para consultar precios sin agregar a lista
// ======================================================

class SeleccionSuperActivity : AppCompatActivity() {
    
    private var modo: String = "CONSULTA" // Por defecto modo consulta
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_seleccion_super)
        
        // Obtener el modo desde el intent
        modo = intent.getStringExtra("MODO") ?: "CONSULTA"
        
        // Cambiar título según el modo
        supportActionBar?.title = if (modo == "LISTA") {
            "Elegí el supermercado para tu lista"
        } else {
            "Elegí el supermercado a consultar"
        }
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        
        setupSuperCards()
    }
    
    private fun setupSuperCards() {
        val cardCarrefour = findViewById<CardView>(R.id.cardCarrefour)
        val cardDia = findViewById<CardView>(R.id.cardDia)
        val cardLaReina = findViewById<CardView>(R.id.cardLaReina)
        val cardLaGallega = findViewById<CardView>(R.id.cardLaGallega)
        val cardCoto = findViewById<CardView>(R.id.cardCoto)
        
        cardCarrefour.setOnClickListener {
            abrirBusqueda("carrefour", "Carrefour")
        }
        
        cardDia.setOnClickListener {
            abrirBusqueda("dia", "Día %")
        }
        
        cardLaReina.setOnClickListener {
            abrirBusqueda("lareina", "La Reina")
        }
        
        cardLaGallega.setOnClickListener {
            abrirBusqueda("lagallega", "La Gallega")
        }
        
        cardCoto.setOnClickListener {
            abrirBusqueda("coto", "Coto")
        }
    }
    
    private fun abrirBusqueda(supermercadoId: String, supermercadoNombre: String) {
        val intent = Intent(this, BusquedaActivity::class.java)
        intent.putExtra("SUPERMERCADO_ID", supermercadoId)
        intent.putExtra("SUPERMERCADO_NOMBRE", supermercadoNombre)
        intent.putExtra("MODO", modo) // Pasar el modo a BusquedaActivity
        startActivity(intent)
        finish() // No volver a esta pantalla con back
    }
    
    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }
}
