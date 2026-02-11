# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 22:13:00 2026

@author: Suárez
"""
import flet as ft
import math
import traceback # Importante para ver los detalles del error

def main(page: ft.Page):
    try:
        # --- CONFIGURACIÓN SEGURA ---
        page.title = "Coeficientes Rayleigh"
        page.scroll = ft.ScrollMode.AUTO
        page.window_width = 390
        page.window_height = 844
        
        # --- TU LÓGICA (Dentro del bloque seguro) ---
        def calcular_coef_rayleigh_manual(T1, T2, zeta):
            w1 = (2 * math.pi) / T1
            w2 = (2 * math.pi) / T2
            
            a1, b1, c1 = 1.0, w1**2, 2.0 * zeta * w1
            a2, b2, c2 = 1.0, w2**2, 2.0 * zeta * w2
            
            det = (a1 * b2) - (a2 * b1)
            if det == 0: raise ValueError("Sistema sin solución")
            
            alpha = ((c1 * b2) - (c2 * b1)) / det
            beta = ((a1 * c2) - (a2 * c1)) / det
            return alpha, beta

        def calcular(e):
            try:
                if not txt_t1.value or not txt_t2.value or not txt_zeta.value:
                    raise ValueError("Campos vacíos")
                
                t1, t2, zeta = float(txt_t1.value), float(txt_t2.value), float(txt_zeta.value)
                if t1 == 0 or t2 == 0: raise ValueError("Periodo no puede ser 0")

                alpha, beta = calcular_coef_rayleigh_manual(t1, t2, zeta)
                
                lbl_alpha_res.value = f"{alpha:.4e}"
                lbl_beta_res.value = f"{beta:.4e}"
                lbl_alpha_res.color = ft.colors.GREEN_700
                lbl_beta_res.color = ft.colors.GREEN_700
                page.update()
            except Exception as e:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error cálculo: {e}"), bgcolor="red")
                page.snack_bar.open = True
                page.update()

        # --- INTERFAZ ---
        txt_t1 = ft.TextField(label="Periodo T1", keyboard_type=ft.KeyboardType.NUMBER)
        txt_t2 = ft.TextField(label="Periodo T2", keyboard_type=ft.KeyboardType.NUMBER)
        txt_zeta = ft.TextField(label="Zeta", keyboard_type=ft.KeyboardType.NUMBER)
        
        lbl_alpha_res = ft.Text("...", size=20, weight=ft.FontWeight.BOLD)
        lbl_beta_res = ft.Text("...", size=20, weight=ft.FontWeight.BOLD)
        
        btn_calcular = ft.ElevatedButton("Calcular", on_click=calcular)

        page.add(
            ft.Text("Calculadora Rayleigh", size=24),
            txt_t1, txt_t2, txt_zeta,
            btn_calcular,
            lbl_alpha_res, lbl_beta_res
        )
    
    except Exception as e:
        # SI ALGO FALLA AL INICIAR, ESTO TE LO MOSTRARÁ EN PANTALLA
        error_msg = traceback.format_exc()
        page.add(
            ft.Text("¡ERROR CRÍTICO!", color="red", size=30),
            ft.Text(f"Detalle: {e}", color="red"),
            ft.Text(error_msg, size=10, font_family="monospace")
        )

ft.app(target=main)

