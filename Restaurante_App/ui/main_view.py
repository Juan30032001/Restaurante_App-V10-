from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio


class MainView(tk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        servicio: RestauranteServicio,
        usuario: Usuario,
        cerrar_sesion: Callable[[], None],
    ) -> None:
        super().__init__(master, padx=24, pady=20)
        self.servicio = servicio
        self.usuario = usuario
        self.cerrar_sesion = cerrar_sesion
        self._crear_controles()

    def _crear_controles(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        encabezado = ttk.Frame(self)
        encabezado.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        encabezado.columnconfigure(0, weight=1)
        ttk.Label(encabezado, text=f"Panel del restaurante | {self.usuario.nombre}", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Button(encabezado, text="Cerrar sesión", command=self.cerrar_sesion).grid(row=0, column=1)
        ttk.Label(self, text="Administre el catálogo y consulte la información del equipo.").grid(row=1, column=0, sticky="w", pady=(0, 12))

        self.pestanas = ttk.Notebook(self)
        self.pestanas.grid(row=2, column=0, sticky="nsew")
        productos_tab = ttk.Frame(self.pestanas, padding=14)
        usuarios_tab = ttk.Frame(self.pestanas, padding=14)
        self.pestanas.add(productos_tab, text="Productos")
        self.pestanas.add(usuarios_tab, text="Usuarios")
        self._crear_pestana_productos(productos_tab)
        self._crear_pestana_usuarios(usuarios_tab)

    def _crear_pestana_productos(self, contenedor: ttk.Frame) -> None:
        contenedor.columnconfigure(1, weight=1)
        contenedor.rowconfigure(0, weight=1)
        formulario = ttk.LabelFrame(contenedor, text="Datos del producto", padding=12)
        formulario.grid(row=0, column=0, sticky="ns", padx=(0, 14))
        campos = (("Código", "codigo"), ("Nombre", "nombre"), ("Categoría", "categoria"), ("Precio (USD)", "precio"), ("Stock", "stock"))
        self.campos: dict[str, tk.StringVar] = {}
        for fila, (etiqueta, clave) in enumerate(campos):
            self.campos[clave] = tk.StringVar()
            ttk.Label(formulario, text=etiqueta).grid(row=fila * 2, column=0, sticky="w", pady=(0, 3))
            ttk.Entry(formulario, textvariable=self.campos[clave], width=27).grid(row=fila * 2 + 1, column=0, sticky="ew", pady=(0, 9))

        acciones = ttk.Frame(formulario)
        acciones.grid(row=10, column=0, sticky="ew", pady=(4, 0))
        acciones.columnconfigure(0, weight=1)
        acciones.columnconfigure(1, weight=1)
        ttk.Button(acciones, text="Registrar", command=self.registrar_producto).grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=3)
        ttk.Button(acciones, text="Actualizar", command=self.actualizar_producto).grid(row=0, column=1, sticky="ew", padx=(4, 0), pady=3)
        ttk.Button(acciones, text="Cargar / consultar", command=self.cargar_producto).grid(row=1, column=0, columnspan=2, sticky="ew", pady=3)
        ttk.Button(acciones, text="Eliminar", command=self.eliminar_producto).grid(row=2, column=0, columnspan=2, sticky="ew", pady=3)
        ttk.Button(acciones, text="Limpiar formulario", command=self._limpiar_formulario).grid(row=3, column=0, columnspan=2, sticky="ew", pady=3)

        listado = ttk.LabelFrame(contenedor, text="Productos registrados", padding=10)
        listado.grid(row=0, column=1, sticky="nsew")
        listado.columnconfigure(0, weight=1)
        listado.rowconfigure(0, weight=1)
        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tabla_productos = ttk.Treeview(listado, columns=columnas, show="headings", selectmode="browse")
        encabezados = {"codigo": "Código", "nombre": "Nombre", "categoria": "Categoría", "precio": "Precio (USD)", "stock": "Stock"}
        anchos = {"codigo": 85, "nombre": 190, "categoria": 105, "precio": 90, "stock": 65}
        for columna in columnas:
            self.tabla_productos.heading(columna, text=encabezados[columna])
            self.tabla_productos.column(columna, width=anchos[columna], anchor="w")
        barra = ttk.Scrollbar(listado, orient="vertical", command=self.tabla_productos.yview)
        self.tabla_productos.configure(yscrollcommand=barra.set)
        self.tabla_productos.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")
        ttk.Button(listado, text="Cargar seleccionado", command=self.cargar_seleccionado).grid(row=1, column=0, columnspan=2, sticky="e", pady=(10, 0))
        self._actualizar_tabla_productos()

    def _crear_pestana_usuarios(self, contenedor: ttk.Frame) -> None:
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(0, weight=1)
        listado = ttk.LabelFrame(contenedor, text="Usuarios registrados", padding=10)
        listado.grid(row=0, column=0, sticky="nsew")
        listado.columnconfigure(0, weight=1)
        listado.rowconfigure(0, weight=1)
        self.tabla_usuarios = ttk.Treeview(listado, columns=("identificacion", "nombre", "correo"), show="headings")
        for columna, titulo, ancho in (("identificacion", "Identificación", 150), ("nombre", "Nombre", 220), ("correo", "Correo", 280)):
            self.tabla_usuarios.heading(columna, text=titulo)
            self.tabla_usuarios.column(columna, width=ancho, anchor="w")
        barra = ttk.Scrollbar(listado, orient="vertical", command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscrollcommand=barra.set)
        self.tabla_usuarios.grid(row=0, column=0, sticky="nsew")
        barra.grid(row=0, column=1, sticky="ns")
        self._actualizar_tabla_usuarios()

    def _actualizar_tabla_productos(self) -> None:
        for elemento in self.tabla_productos.get_children():
            self.tabla_productos.delete(elemento)
        for producto in self.servicio.listar_productos():
            self.tabla_productos.insert("", "end", iid=producto.codigo, values=(producto.codigo, producto.nombre, producto.categoria, f"{producto.precio:.2f}", producto.stock))

    def _actualizar_tabla_usuarios(self) -> None:
        for elemento in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(elemento)
        for usuario in self.servicio.listar_usuarios():
            self.tabla_usuarios.insert("", "end", values=(usuario.identificacion, usuario.nombre, usuario.correo))

    def _datos_formulario(self) -> tuple[str, str, str, float, int]:
        try:
            precio = float(self.campos["precio"].get().replace(",", "."))
            stock = int(self.campos["stock"].get())
        except ValueError as error:
            raise ValueError("Precio y stock deben ser valores numéricos válidos.") from error
        return (self.campos["codigo"].get(), self.campos["nombre"].get(), self.campos["categoria"].get(), precio, stock)

    def registrar_producto(self) -> None:
        try:
            self.servicio.registrar_producto(*self._datos_formulario())
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo registrar", str(error))
            return
        self._actualizar_tabla_productos()
        self._limpiar_formulario()
        messagebox.showinfo("Producto registrado", "El producto se guardó correctamente.")

    def cargar_producto(self) -> None:
        producto = self.servicio.buscar_producto(self.campos["codigo"].get())
        if producto is None:
            messagebox.showwarning("Producto no encontrado", "Ingrese un código existente para consultar.")
            return
        self._mostrar_producto(producto)

    def cargar_seleccionado(self) -> None:
        seleccion = self.tabla_productos.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Seleccione un producto de la tabla.")
            return
        producto = self.servicio.buscar_producto(seleccion[0])
        if producto is not None:
            self._mostrar_producto(producto)

    def actualizar_producto(self) -> None:
        try:
            self.servicio.actualizar_producto(*self._datos_formulario())
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo actualizar", str(error))
            return
        self._actualizar_tabla_productos()
        messagebox.showinfo("Producto actualizado", "Los cambios se guardaron correctamente.")

    def eliminar_producto(self) -> None:
        codigo = self.campos["codigo"].get().strip()
        if not codigo:
            messagebox.showwarning("Código requerido", "Ingrese o cargue un código de producto.")
            return
        if not messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar el producto {codigo}?"):
            return
        try:
            self.servicio.eliminar_producto(codigo)
        except (ValueError, OSError) as error:
            messagebox.showerror("No se pudo eliminar", str(error))
            return
        self._actualizar_tabla_productos()
        self._limpiar_formulario()
        messagebox.showinfo("Producto eliminado", "El producto dejó de estar disponible.")

    def _mostrar_producto(self, producto: Producto) -> None:
        valores = {"codigo": producto.codigo, "nombre": producto.nombre, "categoria": producto.categoria, "precio": str(producto.precio), "stock": str(producto.stock)}
        for clave, valor in valores.items():
            self.campos[clave].set(valor)

    def _limpiar_formulario(self) -> None:
        for campo in self.campos.values():
            campo.set("")