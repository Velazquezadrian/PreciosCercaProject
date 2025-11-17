package com.precioscerca

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

// ========== [INICIO] PANTALLA DE BIENVENIDA ==========
// Pantalla inicial con dos botones grandes (50% cada uno)
// Botón izquierdo: Mi Lista de Compra
// Botón derecho: Consulta los Precios
// ======================================================

class MainActivity : AppCompatActivity() {
    
    private lateinit var btnMiLista: View
    private lateinit var btnConsultaPrecios: View
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        try {
            Log.d("MainActivity", "Iniciando MainActivity")
            setContentView(R.layout.activity_main)
            
            // Ocultar action bar para pantalla de inicio limpia
            supportActionBar?.hide()
            
            initViews()
            setupListeners()
            
            Log.d("MainActivity", "MainActivity cargado correctamente")
            
        } catch (e: Exception) {
            Log.e("MainActivity", "Error al iniciar: ${e.message}", e)
            Toast.makeText(this, "Error: ${e.message}", Toast.LENGTH_LONG).show()
        }
    }
    
    private fun initViews() {
        btnMiLista = findViewById(R.id.btnMiLista)
        btnConsultaPrecios = findViewById(R.id.btnConsultaPrecios)
    }
    
    private fun setupListeners() {
        // Botón Mi Lista de Compra - Va a seleccionar supermercado en modo LISTA
        btnMiLista.setOnClickListener {
            val intent = Intent(this, SeleccionSuperActivity::class.java)
            intent.putExtra("MODO", "LISTA") // Modo para crear lista de compra
            startActivity(intent)
        }
        
        // Botón Consulta los Precios - Va a seleccionar supermercado en modo CONSULTA
        btnConsultaPrecios.setOnClickListener {
            val intent = Intent(this, SeleccionSuperActivity::class.java)
            intent.putExtra("MODO", "CONSULTA") // Modo solo consulta de precios
            startActivity(intent)
        }
    }
}
