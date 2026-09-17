from __future__ import annotations


class Usuario:
    def __init__(self, identificacion: str, nombre: str, correo: str, contrasena: str = "1234") -> None:
        self.identificacion = identificacion.strip()
        self.nombre = nombre.strip()
        self.correo = correo.strip()
        self.contrasena = contrasena

        if not self.identificacion:
            raise ValueError("La identificación del usuario es obligatoria.")
        if not self.nombre:
            raise ValueError("El nombre del usuario es obligatorio.")
        if not self.correo:
            raise ValueError("El correo del usuario es obligatorio.")
        if not self.contrasena:
            raise ValueError("La contraseña del usuario es obligatoria.")

    def mostrar_informacion(self) -> str:
        return (
            f"Usuario: {self.nombre} | Identificación: {self.identificacion} | "
            f"Correo: {self.correo}"
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "contrasena": self.contrasena,
        }

    @classmethod
    def from_dict(cls, datos: dict[str, object]) -> "Usuario":
        try:
            identificacion = datos["identificacion"]
            nombre = datos["nombre"]
            correo = datos["correo"]
        except KeyError as error:
            raise KeyError(f"Falta la clave {error.args[0]} en el usuario.") from error
        contrasena = datos.get("contrasena", "1234")
        if not all(isinstance(valor, str) for valor in (identificacion, nombre, correo, contrasena)):
            raise ValueError("Los datos del usuario deben ser textos.")
        return cls(identificacion, nombre, correo, contrasena)
