"""
TODO This code was heavily ai generated and should be reviewed more carefully at some point

Functional helper to grab a single Java method (plus its helpers & DI
chain) and copy everything to the clipboard.

Usage (from `main.py`):
-------------------------------------------------------------
>>> from method_extractor import extract_method_chain
>>> extract_method_chain(args.clazz, args.method)

Assumptions
-------------------------------------------------------------
* The project has an up‑to‑date `file_cache` in `libra-config.json` that
  maps **fully‑qualified class names** (FQCN) to absolute file paths.
* Java sources follow typical Spring / Lombok style:
  – Constructor‑injected dependencies are parameters of the first
    constructor.  
  – Private helper methods are declared `private`.
  – Imports at the top are of the form `import com.example.Foo;`.
* We parse with *regex heuristics*, not a full Java parser. For most CRUD
  services this is sufficient; edge‑cases can be patched as discovered.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

from file_parsing.copy_to_clipboard import copy_to_clipboard
from file_parsing.stringify_file import stringify_file
from utils.open_json import open_json
from utils.colorize import colorize, BOLD, CYAN

CONFIG_PATH = "./libra-config.json"

# ---------------------------------------------------------------------------
# Regex helpers
# ---------------------------------------------------------------------------

IMPORT_RE = re.compile(r"^import\s+([\w.]+);", re.MULTILINE)

METHOD_SIG_TMPL = (
    r"[ \t]*(?:public|protected|private|static|final|synchronized|abstract|native|strictfp|transient|\s)+?"  # modifiers
    r"[\w\[\]<>?, \t]+?\s+{method}\s*\([^)]*\)\s*\{"
)

CONSTRUCTOR_SIG_TMPL = (
    r"[ \t]*(?:public|protected|private|\s)*?{class_name}\s*\((?P<params>[^)]*)\)"
)

CALL_RE = re.compile(r"\b([A-Za-z_][A-Za-z_0-9]*)\s*\(")

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def extract_method_chain(fqcn: str, method: str, *, config_path: str = CONFIG_PATH) -> None:
    """Collect the requested method and any directly‑used code, then copy to clipboard."""
    cfg = open_json(config_path)
    file_cache: Dict[str, str] = cfg.get("file_cache", {})

    collected: List[str] = []
    visited: Set[Tuple[str, str]] = set()

    def _lookup_path(name: str) -> str | None:
        if name in file_cache:
            return file_cache[name]
        # Fallback: endswith match
        for key, path in file_cache.items():
            if key.endswith(f".{name}"):
                return path
        return None

    def _file_level_imports(src: str) -> List[str]:
        return IMPORT_RE.findall(src)

    def _extract_method_body(name: str, src: str) -> str | None:
        sig_re = re.compile(METHOD_SIG_TMPL.format(method=re.escape(name)), re.DOTALL)
        m = sig_re.search(src)
        if not m:
            return None
        start = m.start()
        brace_count = 0
        i = m.end() - 1
        while i < len(src):
            if src[i] == "{":
                brace_count += 1
            elif src[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    return src[start : i + 1]
            i += 1
        return None

    def _find_private_helpers(body: str, src: str) -> Dict[str, str]:
        candidates = {n for n in CALL_RE.findall(body) if not n.startswith("new")}
        helpers: Dict[str, str] = {}
        for n in candidates:
            b = _extract_method_body(n, src)
            if b and re.search(r"\bprivate\b", b.split("\n", 1)[0]):
                helpers[n] = b
        return helpers

    def _constructor_param_types(class_name: str, src: str) -> List[str]:
        m = re.search(CONSTRUCTOR_SIG_TMPL.format(class_name=class_name), src)
        if not m:
            return []
        params = m.group("params")
        types = []
        for p in params.split(","):
            tokens = p.strip().split()
            if len(tokens) >= 2:
                types.append(tokens[-2].split("<")[-1])
        return types

    def _process_class(name: str, target_method: str) -> None:
        if (name, target_method) in visited:
            return
        visited.add((name, target_method))

        path = _lookup_path(name)
        if not path or not Path(path).exists():
            return

        src = stringify_file("", path, is_file_path_included=False)
        if not src:
            return

        # 1️⃣  Main method
        body = _extract_method_body(target_method, src)
        if not body:
            return
        collected.append(f"// {name}.{target_method} — {path}\n{body}")

        # 2️⃣  Private helpers
        helpers = _find_private_helpers(body, src)
        collected.extend(helpers.values())

        # 3️⃣  Recurse into DI deps
        simple_name = name.split(".")[-1]
        deps = _constructor_param_types(simple_name, src)
        imports = _file_level_imports(src)
        imp_map = {imp.split(".")[-1]: imp for imp in imports}
        for dep in deps:
            fq = imp_map.get(dep)
            if fq:
                _process_class(fq, dep.split(".")[-1])

    # kick off recursion
    _process_class(fqcn, method)

    # dump to clipboard
    if collected:
        copy_to_clipboard("\n\n".join(collected))
        print(colorize(f"{BOLD}{CYAN}", f"Copied {len(collected)} fragments to clipboard"))
    else:
        print("[method_extractor] Nothing found to copy.")
