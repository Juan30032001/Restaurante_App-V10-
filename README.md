# Restaurante App

Aplicación gráfica educativa desarrollada para la Semana 14. Conserva la arquitectura modular de las semanas anteriores y amplía la interfaz con componentes y contenedores de Tkinter/ttk para consultar usuarios y gestionar productos.

## Estructura

```text
datos/
  productos.json
  usuarios.json
modelos/
  producto.py
  usuario.py
  bebida.py
  cliente.py
  venta.py
servicios/
  archivo_servicio.py
  restaurante_servicio.py
  restaurante.py
ui/
  login_view.py
  main_view.py
main.py
```

- `modelos/` define las entidades del restaurante.
- `servicios/` concentra las validaciones, las operaciones CRUD y la persistencia JSON.
- `ui/` contiene el login y el panel principal. La vista usa `Frame`, `Notebook`, `LabelFrame`, `Entry`, `Button`, `Treeview` y `Scrollbar`, organizados con `pack` y `grid`.
- `datos/` mantiene los registros persistentes.
- `main.py` prepara las dependencias y coordina el cambio entre login y panel.

## Funcionalidades de la Semana 14

1. Inicio de sesión mediante `RestauranteServicio`.
2. Consulta de usuarios en una tabla.
3. Registro de productos con código, nombre, categoría, precio y stock.
4. Carga/consulta por código o desde la selección de la tabla.
5. Actualización y eliminación de productos.
6. Refresco inmediato de la tabla después de cada operación.

Los botones solo coordinan la interfaz mediante `command=`. Las reglas de validación y las operaciones del catálogo se ejecutan en `RestauranteServicio`, que delega la lectura y escritura de `datos/productos.json` en `ArchivoServicio`.

## Ejecución

Requiere Python 3.10 o superior y Tkinter, incluido normalmente en Python para Windows.

```powershell
python main.py
```

Credenciales de ejemplo:

- Identificación: `C001`, contraseña: `1234`
- Identificación: `C002`, contraseña: `abcd`

Para ejecutar las pruebas:

```powershell
python -m unittest discover -s tests -v
```

La autenticación es simulada con fines pedagógicos; no representa un sistema de seguridad real.
