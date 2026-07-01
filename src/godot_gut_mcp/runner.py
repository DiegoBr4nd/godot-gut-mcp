import subprocess
import os


class GutRunner:
    """Se encarga de hablar con Godot y ejecutar GUT."""

    def __init__(self):
        self.godot = os.environ.get("GODOT_PATH", "godot")
        self.project = os.environ.get("GODOT_PROJECT_PATH", ".")
        self.env = {**os.environ, "GODOT_DISABLE_LEAK_CHECKS": "1"}

    def ensure_import(self):
        subprocess.run(
            [self.godot, "--headless", "--path", self.project,
             "--import", "--quit"],
            capture_output=True, env=self.env, timeout=120,
        )

    def run(self, gdir=None, gtest=None, include_subdirs=False):
        cmd = [
            self.godot, "--headless", "-d",
            "--display-driver", "headless",
            "--audio-driver", "Dummy",
            "--path", self.project,
            "-s", "res://addons/gut/gut_cmdln.gd",
            "-gexit",
        ]
        if gdir:
            cmd.append(f"-gdir={gdir}")
            if include_subdirs:
                cmd.append("-ginclude_subdirs")
        if gtest:
            cmd.append(f"-gtest={gtest}")

        proc = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            env=self.env, timeout=300,
        )
        return proc.stdout



        