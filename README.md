<!-- mcp-name: io.github.DiegoBr4nd/godot-gut-mcp -->
# Godot GUT MCP

Servidor MCP que permite a asistentes de IA (Claude, Cursor, etc.) ejecutar las
pruebas unitarias de tu juego en Godot usando [GUT](https://github.com/bitwes/Gut),
y leer los resultados de forma estructurada. Ideal para el ciclo
"la IA escribe código → ejecuta los tests → lee los fallos → corrige".

## Requisitos

- Python 3.10 o superior
- Godot 4.x
- [GUT 9.x](https://github.com/bitwes/Gut) instalado en tu proyecto (carpeta `res://addons/gut/`)

## Instalación

```bash
pip install godot-gut-mcp
```

## Configuración en Claude Desktop

Añade esto a tu archivo de configuración de Claude Desktop:

```json
{
  "mcpServers": {
    "godot-gut": {
      "command": "godot-gut-mcp",
      "env": {
        "GODOT_PATH": "C:/ruta/a/godot.exe",
        "GODOT_PROJECT_PATH": "C:/ruta/a/tu/proyecto"
      }
    }
  }
}
```

- `GODOT_PATH`: ruta al ejecutable de Godot.
- `GODOT_PROJECT_PATH`: ruta a la carpeta de tu proyecto (la que contiene `project.godot`).

## Herramientas disponibles

| Herramienta | Qué hace |
|---|---|
| `run_all_tests` | Ejecuta toda la suite de pruebas y devuelve un resumen |
| `run_test_file` | Ejecuta un archivo de pruebas concreto |
| `get_failures` | Devuelve solo las pruebas que fallaron, con el mensaje y la línea del error |

## Ejemplo de respuesta

```json
{
  "summary": { "passing": 1, "failing": 1, "all_passed": false },
  "tests": [
    {
      "test": "test_suma_basica",
      "status": "failed",
      "message": "expected to equal [2]: Dos más dos debe ser cuatro",
      "line": 4
    }
  ]
}
```

## Licencia

MIT