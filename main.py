# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 22:13:00 2026

@author: Suárez
"""
import flet as ft
import math
import traceback

def main(page: ft.Page):
    # --- 1. CONFIGURACIÓN VISUAL DE LA PÁGINA ---
    page.title = "Calculadora Rayleigh"
    page.theme_mode = ft.ThemeMode.DARK  # Modo oscuro elegante
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.HIDDEN # Evita barras de scroll innecesarias
    
    # Dimensiones para probar en PC
    page.window_width = 390
    page.window_height = 844

    # --- 2. LÓGICA MATEMÁTICA (Mantenemos la que funciona) ---
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
            # Limpiar errores previos
            txt_t1.error_text = None
            txt_t2.error_text = None
            txt_zeta.error_text = None
            
            if not txt_t1.value: txt_t1.error_text = "Requerido"; page.update(); return
            if not txt_t2.value: txt_t2.error_text = "Requerido"; page.update(); return
            if not txt_zeta.value: txt_zeta.error_text = "Requerido"; page.update(); return

            t1, t2, zeta = float(txt_t1.value), float(txt_t2.value), float(txt_zeta.value)
            
            if t1 <= 0 or t2 <= 0: raise ValueError("Periodos deben ser > 0")

            alpha, beta = calcular_coef_rayleigh_manual(t1, t2, zeta)
            
            # Actualizar interfaz con resultados
            lbl_alpha_val.value = f"{alpha:.4e}"
            lbl_beta_val.value = f"{beta:.4e}"
            
            # Animación visual: Mostrar el contenedor de resultados
            container_resultados.opacity = 1
            container_resultados.update()
            
            page.update()

        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Revisa los números ingresados"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {e}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    # --- 3. ELEMENTOS DE DISEÑO (WIDGETS) ---

    # Título con estilo
    titulo = ft.Column([
        ft.Icon(ft.icons.WAVES, size=40, color=ft.colors.CYAN_400),
        ft.Text("Análisis Rayleigh", size=26, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        ft.Text("Coeficientes de Amortiguamiento", size=14, color=ft.colors.GREY_400)
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5)

    # Campos de entrada estilizados
    def crear_input(label, hint):
        return ft.TextField(
            label=label,
            hint_text=hint,
            keyboard_type=ft.KeyboardType.NUMBER,
            width=280,
            text_size=16,
            border_color=ft.colors.BLUE_GREY_700,
            focused_border_color=ft.colors.CYAN_400,
            border_radius=12,
            content_padding=15
        )

    txt_t1 = crear_input("Periodo T1 (s)", "Ej: 0.75")
    txt_t2 = crear_input("Periodo T2 (s)", "Ej: 0.54")
    txt_zeta = crear_input("Amortiguamiento ζ", "Ej: 0.05")

    # Botón principal
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

    # --- SECCIÓN DE RESULTADOS ---
    # Labels de valores (se actualizan al calcular)
    lbl_alpha_val = ft.Text("-", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_ACCENT_400, font_family="monospace")
    lbl_beta_val = ft.Text("-", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_ACCENT_400, font_family="monospace")

    # Función para crear tarjeta de resultado
    def crear_tarjeta_resultado(titulo, subtitulo, widget_valor):
        return ft.Container(
            content=ft.Column([
                ft.Text(titulo, size=14, color=ft.colors.GREY_400),
                widget_valor,
                ft.Text(subtitulo, size=12, italic=True, color=ft.colors.GREY_600),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
            border_radius=15,
            padding=15,
            width=135, # Ancho fijo para que queden parejas
            border=ft.border.all(1, ft.colors.with_opacity(0.2, ft.colors.WHITE))
        )

    # Contenedor que agrupa los resultados (inicialmente invisible)
    container_resultados = ft.Container(
        content=ft.Row([
            crear_tarjeta_resultado("Coeficiente α", "(Masa)", lbl_alpha_val),
            crear_tarjeta_resultado("Coeficiente β", "(Rigidez)", lbl_beta_val),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        opacity=0, # Empieza invisible
        animate_opacity=500, # Animación suave de aparición
    )

    # --- 4. AGREGAR TODO A LA PÁGINA ---
    # Usamos un Card principal para agrupar los inputs y darle marco
    card_principal = ft.Container(
        content=ft.Column([
            titulo,
            ft.Divider(height=20, color="transparent"),
            txt_t1,
            txt_t2,
            txt_zeta,
            btn_calcular,
            ft.Divider(height=10, color="transparent"),
            container_resultados
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
    )

    page.add(card_principal)

ft.app(target=main)
