import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

# 1. Potongan Fungsi
kode_fungsi = b"""def sapa(nama):
    return "Halo " + nama
"""

# 2. Potongan If/Else
kode_ifelse = b"""if x > 0:
    y = 1
else:
    y = -1
"""

# 3. Potongan Kelas dengan 1 method
kode_kelas = b"""class Kalkulator:
    def tambah(self, a, b):
        return a + b
"""

# 4. Potongan Rusak (tanpa titik dua ':' setelah parameter)
kode_rusak = b"""def sapa(nama)
    return nama
"""

for judul, kode in [
    ("FUNGSI", kode_fungsi),
    ("IF-ELSE", kode_ifelse),
    ("KELAS", kode_kelas),
    ("RUSAK", kode_rusak),
]:
    print(f"=== {judul} ===")
    tree = parser.parse(kode)
    print(tree.root_node)
    print()

# Cek node bernama vs anonim pada potongan FUNGSI
tree_fn = parser.parse(kode_fungsi)
func_node = tree_fn.root_node.children[0]
print("=== NODE ANONIM PADA FUNGSI ===")
for c in func_node.children:
    print(f"{c.type!r:15} -> {'bernama' if c.is_named else 'anonim'}")

print("\n=== NODE ANONIM PADA PARAMETERS ===")
params_node = func_node.child_by_field_name("parameters")
for c in params_node.children:
    print(f"{c.type!r:15} -> {'bernama' if c.is_named else 'anonim'}")