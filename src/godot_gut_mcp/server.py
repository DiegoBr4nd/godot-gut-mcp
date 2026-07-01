from mcp.server.fastmcp import FastMCP
from .runner import GutRunner
from .parser import parse_gut_output

# Crear el servidor con su nombre 

mcp = FastMCP("godot-gut")
runner = GutRunner()

@mcp.tool()
def run_all_tests(test_dir: str = "res://test") -> dict:
    """Ejecutar todas las pruebas del proyecto Godot y devolver un resumen"""
    runner.ensure_import()
    raw = runner.run(gdir=test_dir, include_subdirs=True)
    return parse_gut_output(raw)


@mcp.tool()
def run_test_file(file_path:str) -> dict:
    """Ejecutar un archivo de pruebas. Ejemplo: res://test_test_player.gd"""
    runner.ensure_import()
    raw = runner.run(gtest=file_path)
    return parse_gut_output(raw)


@mcp.tool()
def get_failures(test_dir: str = "res://test") -> list:
    """Devolver solo las pruebas que fallaron. Para corregir rápido."""
    runner.ensure_import()
    result = parse_gut_output(runner.run(gdir=test_dir,include_subdirs=True))
    return [t for t in result["tests"] if t["status"] == "failed"]


def main():
    """Inicio del Servidor"""
    mcp.run()

if __name__ == "__main__":
    main()
