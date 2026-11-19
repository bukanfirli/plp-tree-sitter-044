import os
import sys as system
from pathlib import Path
from typing import List, Dict

def sapa(nama):
    print("Halo", nama)
    return nama

def hitung_luas(panjang, lebar, tinggi):
    volume = panjang * lebar * tinggi
    print("Volume:", volume)
    return volume

def tanpa_param():
    print("Selesai")

sapa("Budi")