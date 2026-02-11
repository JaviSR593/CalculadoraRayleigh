# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 22:13:00 2026

@author: Suárez
"""
import flet as ft
import math

def main(page: ft.Page):
    # --- 1. Configuración de la Ventana/Pantalla ---
    page.title = "Coeficientes Rayleigh"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    
    # Dimensiones para probar en PC
    page.window_width = 390
    page.window_height = 844

    # --- 2. Lógica Matemática (SIN NUMPY - Python Puro) ---
    def calcular_coef_rayleigh_manual(T1, T2, zeta):
        # 1. Calcular frecuencias angulares (w = 2*pi / T)
        w1 = (2 * math.pi) / T1
        w2 = (2 * math.pi) / T2
        
        # El sistema de ecuaciones es:
        # alpha + beta * w1^2 = 2 * zeta * w1
        # alpha + beta * w2^2 = 2 * zeta * w2
        
        # Usamos determinantes (Regla de Cramer) para sistema 2x2
        # Matriz coeficientes:
        # | 1    w1^2 |
        # | 1    w2^2 |
        
        a1 = 1.0
        b1 = w1**2
        c1 = 2.0 * zeta * w1
        
        a2 = 1.0
        b2 = w2**2
        c2 = 2.0 * zeta * w2
        
        # Determinante principal (Det)
        det = (a1 * b2) - (a2 * b1)
        
        if det == 0:
            raise ValueError("El sistema no tiene solución (T1 y T2 son iguales)")

        # Determinante para Alpha (reemplazamos columna alpha por resultados)
        det_alpha = (c1 * b2) - (c2 * b1)
        
        # Determinante para Beta (reemplazamos columna beta por resultados)
        det_beta = (a1 * c2) - (a2 * c1)
        
        alpha = det_alpha / det
        beta = det_beta / det
        
        return alpha, beta

    # --- 3. Función del Botón (Interacción UI) ---
    def calcular(e):
        try:
            # Validamos que no estén vacíos
            if not txt_t1.value or not txt_t2.value or not txt_zeta.value:
                raise ValueError("Campos vacíos")

            val_t1 = float(txt_t1.value)
            val_t2 = float(txt_t2.value)
            val_zeta = float(txt_zeta.value)

            # Validación física
            if val_t1 == 0 or val_t2 == 0:
                raise ValueError("El periodo no puede ser 0")

            # LLAMAMOS A LA NUEVA FUNCIÓN SIN NUMPY
            alpha, beta = calcular_coef_rayleigh_manual(val_t1, val_t2, val_zeta)

            # Mostramos resultados
            lbl_alpha_res.value = f"{alpha:.4e}"
            lbl_beta_res.value = f"{beta:.4e}"
            
            lbl_alpha_res.color = ft.colors.GREEN_700
            lbl_beta_res.color = ft.colors.GREEN_700

        except Exception as error:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {error}"), bgcolor="red")
            page.snack_bar.open = True
        
        page.update()

    # --- 4. Elementos de la Interfaz (Igual que antes) ---
    lbl_titulo = ft.Text("Coeficientes Rayleigh", size=24, weight=ft.FontWeight.BOLD)

    txt_t1 = ft.TextField(label="Periodo T1", suffix_text="s", keyboard_type=ft.KeyboardType.NUMBER, width=280)
    txt_t2 = ft.TextField(label="Periodo T2", suffix_text="s", keyboard_type=ft.KeyboardType.NUMBER, width=280)
    txt_zeta = ft.TextField(label="Amortiguamiento ζ", hint_text="Ej: 0.05", keyboard_type=ft.KeyboardType.NUMBER, width=280)

    btn_calcular = ft.ElevatedButton(
        text="Calcular Coeficientes",
        icon=ft.icons.CALCULATE,
        width=280,
        height=50,
        on_click=calcular,
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_700)
    )

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

    page.add(
        lbl_titulo,
        ft.Divider(height=20, color="transparent"),
        txt_t1, txt_t2, txt_zeta,
        ft.Divider(height=10, color="transparent"),
        btn_calcular,
        ft.Divider(height=20, color="transparent"),
        contenedor_resultados
    )

ft.app(target=main)
