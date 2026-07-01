<!-- mcp-name: io.github.DiegoBr4nd/godot-gut-mcp -->
# Godot GUT MCP

Servidor MCP que permite a asistentes de IA (Claude, Cursor, etc.) ejecutar
las pruebas de tu juego en Godot usando GUT, y leer los resultados.

## Instalación

```bash
pip install godot-gut-mcp
```

## Configuración en Claude Desktop

Añade esto a tu archivo de configuración:

```json
{
  "mcpServers": {
    "godot-gut": {
      "command": "godot-gut-mcp",
      "env": {
        "GODOT_PATH": "/ruta/a/godot",
        "GODOT_PROJECT_PATH": "/ruta/a/tu/proyecto"
      }
    }
  }
}
```

## Herramientas disponibles

- `run_all_tests` — ejecuta toda la suite de pruebas
- `run_test_file` — ejecuta un archivo concreto
- `get_failures` — devuelve solo las pruebas que fallaron