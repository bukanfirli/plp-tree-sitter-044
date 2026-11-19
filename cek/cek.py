import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNGSI = Query(PY, "(function_definition name: (identifier) @nama) @fungsi")

ABAIKAN_FOLDER = {"venv", ".venv", ".git", "__pycache__", "node_modules"}

def cari_baris_error(node):
    if node.is_error or node.is_missing:
        return node.start_point[0] + 1
    for child in node.children:
        baris = cari_baris_error(child)
        if baris is not None:
            return baris
    return None

def cek_file(path):
    kode = path.read_bytes()
    tree = parser.parse(kode)

    # Fitur 1: Komentar TODO / FIXME
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        teks = node.text.decode(errors="replace").strip()
        print(f"[TODO/FIXME] {path}:{node.start_point[0] + 1} -> {teks}")

    # Fitur 2: Fungsi lebih dari 30 baris
    for _, cap in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        fn_node = cap["fungsi"][0]
        nama_node = cap["nama"][0]
        panjang = fn_node.end_point[0] - fn_node.start_point[0] + 1
        if panjang > 30:
            nama = nama_node.text.decode(errors="replace")
            print(f"[FUNGSI PANJANG] {path}:{fn_node.start_point[0] + 1} -> fungsi '{nama}' ({panjang} baris)")

    # Fitur 3: File mengandung syntax error
    if tree.root_node.has_error:
        baris_err = cari_baris_error(tree.root_node)
        print(f"[SYNTAX ERROR] {path}:{baris_err} -> pohon mengandung node ERROR/MISSING")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Penggunaan: python cek.py <folder>")
        sys.exit(1)

    target = Path(sys.argv[1])
    for path in target.rglob("*.py"):
        if any(bagian in ABAIKAN_FOLDER for bagian in path.parts):
            continue
        cek_file(path)