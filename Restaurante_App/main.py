from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import ttk

from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    archivo_servicio = ArchivoServicio(
        str(base_dir / "datos" / "productos.json"),
        str(base_dir / "datos" / "usuarios.json"),
    )
    servicio = RestauranteServicio(
        archivo_servicio.cargar_productos(),
        archivo_servicio.cargar_usuarios(),
        archivo_servicio,
    )

    ventana = tk.Tk()
    ventana.title("Restaurante App")
    ventana.geometry("1050x650")
    ventana.minsize(900, 560)
    estilo = ttk.Style(ventana)
    estilo.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
    vista_actual: tk.Frame | None = None

    def mostrar_login() -> None:
        nonlocal vista_actual
        if vista_actual is not None:
            vista_actual.destroy()
        vista_actual = LoginView(ventana, servicio, mostrar_principal)
        vista_actual.pack(fill="both", expand=True)

    def mostrar_principal(usuario: Usuario) -> None:
        nonlocal vista_actual
        if vista_actual is not None:
            vista_actual.destroy()
        vista_actual = MainView(ventana, servicio, usuario, mostrar_login)
        vista_actual.pack(fill="both", expand=True)

    mostrar_login()
    ventana.mainloop()


if __name__ == "__main__":
    main()
