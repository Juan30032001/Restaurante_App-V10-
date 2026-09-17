from __future__ import annotations

from typing import Iterable

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """Coordina los datos que necesita la interfaz gráfica del restaurante."""

    def __init__(
        self,
        productos: Iterable[Producto | dict[str, object]],
        usuarios: Iterable[Usuario | dict[str, object]],
        archivo_servicio: ArchivoServicio | None = None,
    ) -> None:
        self._productos = [self._convertir_producto(producto) for producto in productos]
        self._usuarios = [self._convertir_usuario(usuario) for usuario in usuarios]
        self._archivo_servicio = archivo_servicio

    @staticmethod
    def _convertir_producto(producto: Producto | dict[str, object]) -> Producto:
        return producto if isinstance(producto, Producto) else Producto.from_dict(producto)

    @staticmethod
    def _convertir_usuario(usuario: Usuario | dict[str, object]) -> Usuario:
        return usuario if isinstance(usuario, Usuario) else Usuario.from_dict(usuario)

    def validar_acceso(self, identificacion: str, contrasena: str) -> Usuario | None:
        for usuario in self._usuarios:
            if usuario.identificacion == identificacion.strip() and usuario.contrasena == contrasena:
                return usuario
        return None

    def listar_productos(self) -> list[Producto]:
        return list(self._productos)

    def buscar_producto(self, codigo: str) -> Producto | None:
        codigo_normalizado = codigo.strip()
        return next((producto for producto in self._productos if producto.codigo == codigo_normalizado), None)

    def registrar_producto(
        self, codigo: str, nombre: str, categoria: str, precio: float, stock: int
    ) -> Producto:
        producto = Producto(codigo, nombre, categoria, precio, stock)
        if self.buscar_producto(producto.codigo) is not None:
            raise ValueError(f"El código {producto.codigo} ya está registrado.")
        self._productos.append(producto)
        self._guardar_productos()
        return producto

    def actualizar_producto(
        self, codigo: str, nombre: str, categoria: str, precio: float, stock: int
    ) -> Producto:
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ValueError(f"El producto con código {codigo.strip()} no existe.")
        actualizado = Producto(producto.codigo, nombre, categoria, precio, stock)
        producto.nombre = actualizado.nombre
        producto.categoria = actualizado.categoria
        producto.precio = actualizado.precio
        producto.stock = actualizado.stock
        self._guardar_productos()
        return producto

    def eliminar_producto(self, codigo: str) -> None:
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ValueError(f"El producto con código {codigo.strip()} no existe.")
        self._productos.remove(producto)
        self._guardar_productos()

    def _guardar_productos(self) -> None:
        if self._archivo_servicio is not None and not self._archivo_servicio.guardar_productos(self._productos):
            raise OSError("No fue posible guardar los productos.")

    def listar_usuarios(self) -> list[Usuario]:
        return list(self._usuarios)