# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 22:13:00 2026

@author: Suárez
"""

import flet as ft
import numpy as np
import math

def main(page: ft.Page):
    # --- 1. Configuración de la Ventana/Pantalla ---
    page.title = "Coeficientes Rayleigh"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT  # Opcional: LIGHT o DARK
    page.scroll = ft.ScrollMode.AUTO      # Importante para móviles pequeños
    
    # Dimensiones para probar en PC simulando móvil
    page.window_width = 390
    page.window_height = 844

    # --- 2. Lógica Matemática (Tu función original adaptada) ---
    def calcular_coef_rayleigh(T1, T2, zeta):
        # Conversión a frecuencias angulares
        w1 = 2 * np.pi / T1
        w2 = 2 * np.pi / T2
        
        # Sistema de ecuaciones lineales
        A = np.array([[1, w1**2], [1, w2**2]])
        B = np.array([[2 * zeta * w1], [2 * zeta * w2]]) # Corrección: B debe ser columna para linalg.solve
        
        # Se resuelve el sistema
        coef = np.linalg.solve(A, B)
        return coef[0][0], coef[1][0]

    # --- 3. Función del Botón (Interacción UI) ---
    def calcular(e):
        try:
            # Validamos que no estén vacíos
            if not txt_t1.value or not txt_t2.value or not txt_zeta.value:
                raise ValueError("Campos vacíos")

            val_t1 = float(txt_t1.value)
            val_t2 = float(txt_t2.value)
            val_zeta = float(txt_zeta.value)

            # Validación física (evitar división por cero)
            if val_t1 == 0 or val_t2 == 0:
                raise ValueError("El periodo no puede ser 0")

            alpha, beta = calcular_coef_rayleigh(val_t1, val_t2, val_zeta)

            # Mostramos resultados con notación científica
            lbl_alpha_res.value = f"{alpha:.4e}"
            lbl_beta_res.value = f"{beta:.4e}"
            
            # Feedback visual (cambia color a verde si sale bien)
            lbl_alpha_res.color = ft.colors.GREEN_700
            lbl_beta_res.color = ft.colors.GREEN_700

        except Exception as error:
            # Mostramos error en una barra inferior (SnackBar)
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: Verifique sus datos ({error})"), bgcolor="red")
            page.snack_bar.open = True
        
        page.update()

    # --- 4. Elementos de la Interfaz (Widgets) ---
    
    # Título
    lbl_titulo = ft.Text("Coeficientes Rayleigh", size=24, weight=ft.FontWeight.BOLD)

    # Campos de Entrada (Optimizados para móvil)
    txt_t1 = ft.TextField(
        label="Periodo T1", 
        suffix_text="s", 
        keyboard_type=ft.KeyboardType.NUMBER, # Abre teclado numérico en Android
        width=280
    )
    txt_t2 = ft.TextField(
        label="Periodo T2", 
        suffix_text="s", 
        keyboard_type=ft.KeyboardType.NUMBER,
        width=280
    )
    txt_zeta = ft.TextField(
        label="Amortiguamiento ζ", 
        hint_text="Ej: 0.05", 
        keyboard_type=ft.KeyboardType.NUMBER,
        width=280
    )

    # Botón
    btn_calcular = ft.ElevatedButton(
        text="Calcular Coeficientes",
        icon=ft.icons.CALCULATE,
        width=280,
        height=50,
        on_click=calcular,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_700,
        )
    )

    # Contenedores de Resultados (Estilo "Card")
    lbl_alpha_res = ft.Text("...", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREY)
    lbl_beta_res = ft.Text("...", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREY)

    contenedor_resultados = ft.Container(
        content=ft.Column([
            ft.Row([ft.Text("Coeficiente α (Masa):"), lbl_alpha_res], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            ft.Row([ft.Text("Coeficiente β (Rigidez):"), lbl_beta_res], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ]),
        bgcolor=ft.colors.BLUE_50,
        padding=20,
        border_radius=10,
        width=280
    )

    # --- 5. Agregar todo a la página ---
    page.add(
        lbl_titulo,
        ft.Divider(height=20, color="transparent"),
        txt_t1,
        txt_t2,
        txt_zeta,
        ft.Divider(height=10, color="transparent"),
        btn_calcular,
        ft.Divider(height=20, color="transparent"),
        contenedor_resultados
    )

ft.app(target=main)