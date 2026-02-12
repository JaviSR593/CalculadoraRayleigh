# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 22:13:00 2026

@author: Suárez
"""
import flet as ft
import math
import time
import threading

def main(page: ft.Page):
    # --- 1. CONFIGURACIÓN GENERAL ---
    page.title = "Calculadora Rayleigh"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.HIDDEN
    
    # Dimensiones simuladas (útil para ver en PC)
    page.window_width = 390
    page.window_height = 844

    # ==========================================
    #   PANTALLA DE CARGA (SPLASH SCREEN)
    # ==========================================
    def pantalla_carga():
        # Elementos de la pantalla de carga
        icono_animado = ft.Icon(ft.icons.WAVES, size=60, color=ft.colors.CYAN_400)
        spinner = ft.ProgressRing(width=30, height=30, stroke_width=2, color=ft.colors.CYAN_200)
        texto_credito = ft.Text("Aplicación elaborada por\nDayana Guanotuña", text_align=ft.TextAlign.CENTER, color=ft.colors.GREY_400, italic=True)
        
        contenedor_carga = ft.Column([
            ft.Container(height=50), # Espacio
            icono_animado,
            ft.Container(height=20),
            spinner,
            ft.Container(height=20),
            texto_credito
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        page.add(contenedor_carga)
        page.update()
        
        # Simulamos tiempo de carga (3 segundos)
        time.sleep(3)
        
        # Limpiamos la pantalla para mostrar la calculadora
        page.clean()
        mostrar_calculadora()

    # ==========================================
    #   PANTALLA PRINCIPAL (CALCULADORA)
    # ==========================================
    def mostrar_calculadora():
        
        # --- Lógica Matemática ---
        def calcular_coef_rayleigh_manual(T1, T2, zeta):
            w1 = (2 * math.pi) / T1
            w2 = (2 * math.pi) / T2
            a1, b1, c1 = 1.0, w1**2, 2.0 * zeta * w1
            a2, b2, c2 = 1.0, w2**2, 2.0 * zeta * w2
            det = (a1 * b2) - (a2 * b1)
            if det == 0: raise ValueError("Sistema sin solución (T1 = T2)")
            alpha = ((c1 * b2) - (c2 * b1)) / det
            beta = ((a1 * c2) - (a2 * c1)) / det
            return alpha, beta

        def calcular(e):
            try:
                txt_t1.error_text = None
                txt_t2.error_text = None
                txt_zeta.error_text = None
                
                if not txt_t1.value: txt_t1.error_text = "Req."; page.update(); return
                if not txt_t2.value: txt_t2.error_text = "Req."; page.update(); return
                if not txt_zeta.value: txt_zeta.error_text = "Req."; page.update(); return

                t1, t2, zeta = float(txt_t1.value), float(txt_t2.value), float(txt_zeta.value)
                if t1 <= 0 or t2 <= 0: raise ValueError("Periodos > 0")

                alpha, beta = calcular_coef_rayleigh_manual(t1, t2, zeta)
                
                # Actualizar interfaz
                lbl_alpha_val.value = f"{alpha:.4e}"
                lbl_beta_val.value = f"{beta:.4e}"
                
                container_resultados.opacity = 1
                container_resultados.update()
                page.update()

            except Exception as e:
                page.snack_bar = ft.SnackBar(ft.Text("Verifique los datos ingresados"), bgcolor="red")
                page.snack_bar.open = True
                page.update()

        # --- Diseño de Interfaz ---

        titulo = ft.Column([
            ft.Icon(ft.icons.WAVES, size=40, color=ft.colors.CYAN_400),
            ft.Text("Análisis Rayleigh", size=26, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        # Función para crear inputs flexibles
        def crear_input(label, hint, ancho=None):
            return ft.TextField(
                label=label,
                hint_text=hint,
                keyboard_type=ft.KeyboardType.NUMBER,
                width=ancho, # Ancho personalizable
                text_size=15,
                border_color=ft.colors.BLUE_GREY_700,
                focused_border_color=ft.colors.CYAN_400,
                border_radius=12,
                content_padding=15,
                expand=True if ancho is None else False # Si no hay ancho fijo, se expande
            )

        # Fila para T1 y T2 (Lado a lado)
        row_periodos = ft.Row([
            crear_input("Periodo T1 (s)", "Ej: 0.75"),
            ft.VerticalDivider(width=10), # Espacio pequeño entre ellos
            crear_input("Periodo T2 (s)", "Ej: 0.54"),
        ], alignment=ft.MainAxisAlignment.CENTER)

        # Input Zeta (Centrado y ancho fijo para que se vea bien)
        txt_zeta = ft.TextField(
            label="Amortiguamiento ζ",
            hint_text="Ej: 0.05",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=200, # Un poco más angosto para estética visual
            text_size=16,
            border_color=ft.colors.BLUE_GREY_700,
            focused_border_color=ft.colors.CYAN_400,
            border_radius=12,
            content_padding=15,
            text_align=ft.TextAlign.CENTER # Texto centrado al escribir
        )

        # Recuperamos las referencias de los inputs creados en la fila para usarlos en logica
        # Nota: Como están dentro de una Row, accedemos a ellos por sus controles
        global txt_t1, txt_t2 
        txt_t1 = row_periodos.controls[0]
        txt_t2 = row_periodos.controls[2] # El índice 1 es el divisor

        btn_calcular = ft.Container(
            content=ft.ElevatedButton(
                text="CALCULAR",
                icon=ft.icons.CALCULATE_OUTLINED,
                style=ft.ButtonStyle(
                    color=ft.colors.BLACK,
                    bgcolor=ft.colors.CYAN_400,
                    shape=ft.RoundedRectangleBorder(radius=12),
                    padding=15,
                ),
                width=280,
                on_click=calcular
            ),
            padding=ft.padding.only(top=10, bottom=10)
        )

        # --- Resultados ---
        # Selectable=True permite copiar el texto manteniendo presionado
        lbl_alpha_val = ft.Text("-", size=16, selectable=True, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_ACCENT_400, font_family="monospace")
        lbl_beta_val = ft.Text("-", size=16, selectable=True, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_ACCENT_400, font_family="monospace")

        def crear_tarjeta_resultado(titulo, subtitulo, widget_valor):
            return ft.Container(
                content=ft.Column([
                    ft.Text(titulo, size=13, color=ft.colors.GREY_400),
                    widget_valor,
                    ft.Text(subtitulo, size=11, italic=True, color=ft.colors.GREY_600),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
                border_radius=15,
                padding=15,
                expand=True, # Para que ocupen el mismo espacio
                border=ft.border.all(1, ft.colors.with_opacity(0.2, ft.colors.WHITE))
            )

        global container_resultados
        container_resultados = ft.Container(
            content=ft.Row([
                crear_tarjeta_resultado("Coeficiente α", "(Masa)", lbl_alpha_val),
                crear_tarjeta_resultado("Coeficiente β", "(Rigidez)", lbl_beta_val),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            opacity=0,
            animate_opacity=500,
        )

        # Agregar todo a la página nueva
        card_principal = ft.Container(
            content=ft.Column([
                titulo,
                ft.Divider(height=20, color="transparent"),
                row_periodos, # Fila T1 y T2
                ft.Divider(height=5, color="transparent"),
                txt_zeta,     # Zeta centrado
                ft.Divider(height=10, color="transparent"),
                btn_calcular,
                ft.Divider(height=10, color="transparent"),
                container_resultados
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=10,
        )
        page.add(card_principal)

    # Iniciar con la pantalla de carga
    pantalla_carga()

ft.app(target=main)
