import re


def _strip_ansi(text: str) -> str:
    """Quita los códigos de color (como \u001b[31m) que mete GUT."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def parse_gut_output(raw: str) -> dict:
    """Convierte el texto crudo de GUT en un diccionario ordenado."""
    clean = _strip_ansi(raw)
    lines = clean.splitlines()

    result = {
        "summary": {},
        "tests": [],
        "raw_tail": raw[-2000:],
    }

    # --- Resumen ---
    def find_number(label):
        m = re.search(rf"{label}\s+(\d+)", clean)
        return int(m.group(1)) if m else 0

    failing = find_number("Failing Tests")
    result["summary"] = {
        "passing": find_number("Passing Tests"),
        "failing": failing,
        "risky": find_number("Risky Tests"),
        "pending": find_number("Pending"),
        "all_passed": failing == 0,
    }

    # --- Recoger detalles de cada fallo ---
    # Guardamos, por nombre de test, su mensaje de error y su línea.
    failures = {}
    for i, line in enumerate(lines):
        m = re.match(r"[*-]\s*(test_\w+)", line.strip())
        if not m:
            continue
        name = m.group(1)
        # Miramos las siguientes líneas buscando un [Failed].
        for j in range(i + 1, min(i + 4, len(lines))):
            nxt = lines[j].strip()
            fail_match = re.search(r"\[Failed\]:\s*(.*)", nxt)
            if fail_match:
                message = fail_match.group(1).strip()
                # Buscamos "at line N" en las líneas siguientes.
                line_no = None
                for k in range(j, min(j + 3, len(lines))):
                    lm = re.search(r"at line (\d+)", lines[k])
                    if lm:
                        line_no = int(lm.group(1))
                        break
                failures[name] = {"message": message, "line": line_no}
                break

    # --- Lista de tests (sin duplicados) ---
    current_file = None
    seen = set()
    for line in lines:
        stripped = line.strip()

        file_match = re.search(r"(res://[^\s]+\.gd)", stripped)
        if file_match:
            current_file = file_match.group(1)
            continue

        m = re.match(r"[*-]\s*(test_\w+)", stripped)
        if m:
            name = m.group(1)
            if name in seen:
                continue
            seen.add(name)

            test_entry = {
                "file": current_file,
                "test": name,
                "status": "failed" if name in failures else "passed",
            }
            # Si falló, añadimos el detalle.
            if name in failures:
                test_entry["message"] = failures[name]["message"]
                test_entry["line"] = failures[name]["line"]

            result["tests"].append(test_entry)

    return result


    
    