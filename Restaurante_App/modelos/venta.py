from __future__ import annotations


class Venta:
    def __init__(self, usuario_id: str, producto_codigo: str, cantidad: int) -> None:
        if not usuario_id.strip() or not producto_codigo.strip():
            raise ValueError("El usuario y el producto son obligatorios.")
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad vendida debe ser un entero mayor que cero.")
        self.usuario_id = usuario_id.strip()
        self.producto_codigo = producto_codigo.strip()
        self.cantidad = cantidad

    def to_dict(self) -> dict[str, str | int]:
        return {"usuario_id": self.usuario_id, "producto_codigo": self.producto_codigo, "cantidad": self.cantidad}

    @classmethod
    def from_dict(cls, datos: dict[str, object]) -> "Venta":
        try:
            usuario_id = datos["usuario_id"]
            producto_codigo = datos["producto_codigo"]
            cantidad = datos["cantidad"]
        except KeyError as error:
            raise KeyError(f"Falta la clave {error.args[0]} en la venta.") from error
        if not isinstance(usuario_id, str) or not isinstance(producto_codigo, str):
            raise ValueError("Los identificadores de la venta deben ser textos.")
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise ValueError("La cantidad de la venta debe ser un entero.")
        return cls(usuario_id, producto_codigo, cantidad)