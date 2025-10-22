package com.precioscerca

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.button.MaterialButton
import com.google.android.material.textfield.TextInputEditText
import android.widget.ProgressBar
import android.widget.TextView

class MainActivity : AppCompatActivity() {
    
    private lateinit var etBusqueda: TextInputEditText
    private lateinit var btnBuscar: MaterialButton
    private lateinit var progressBar: ProgressBar
    private lateinit var tvEstado: TextView
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        initViews()
        setupListeners()
    }
    
    private fun initViews() {
        etBusqueda = findViewById(R.id.etBusqueda)
        btnBuscar = findViewById(R.id.btnBuscar)
        progressBar = findViewById(R.id.progressBar)
        tvEstado = findViewById(R.id.tvEstado)
    }
    
    private fun setupListeners() {
        // Botón de búsqueda
        btnBuscar.setOnClickListener {
            realizarBusqueda()
        }
        
        // Enter en el campo de texto
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
            Toast.makeText(this, "Ingresa un producto para buscar", Toast.LENGTH_SHORT).show()
            return
        }
        
        if (query.length < 2) {
            Toast.makeText(this, "Ingresa al menos 2 caracteres", Toast.LENGTH_SHORT).show()
            return
        }
        
        // Mostrar indicadores de carga
        mostrarCarga(true)
        
        // Navegar a ProductListActivity
        val intent = Intent(this, ProductListActivity::class.java).apply {
            putExtra(ProductListActivity.EXTRA_QUERY, query)
        }
        startActivity(intent)
        
        // Ocultar carga cuando regrese
        mostrarCarga(false)
    }
    
    private fun mostrarCarga(mostrar: Boolean) {
        if (mostrar) {
            progressBar.visibility = View.VISIBLE
            tvEstado.visibility = View.VISIBLE
            btnBuscar.isEnabled = false
        } else {
            progressBar.visibility = View.GONE
            tvEstado.visibility = View.GONE
            btnBuscar.isEnabled = true
        }
    }
    
    override fun onResume() {
        super.onResume()
        // Ocultar carga si regresa de otra pantalla
        mostrarCarga(false)
    }
}