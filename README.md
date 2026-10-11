<h1 align="center">SawitNet</h1>

<p align="center">
  <b>IDOR CTF Challenge</b><br>
  <sub>oleh XrunZ · WSE DIVISION</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white" alt="Python 3.11">
  <img src="https://img.shields.io/badge/Flask-3.0.3-000000?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Kategori-Web%20Exploitation-critical" alt="Kategori Web Exploitation">
  <img src="https://img.shields.io/badge/Lisensi-MIT-2ea44f" alt="Lisensi MIT">
</p>

Aplikasi web simulasi pemesanan kelapa sawit yang **sengaja** dibuat rentan terhadap **IDOR (Insecure Direct Object Reference)**. Cocok untuk latihan keamanan siber: belajar menemukan, mengeksploitasi, sekaligus memperbaiki celah kontrol akses.

> **Disclaimer:** Dibuat murni untuk edukasi. Jangan meniru pola rentan ini di lingkungan produksi.

## Cara Menjalankan

**Docker (disarankan)**

```bash
docker compose up --build
```

**Tanpa Docker**

```bash
pip install -r requirements.txt
python app.py
```

Buka browser ke <http://localhost:5000>.

## Akun Demo

Masuk pakai salah satu akun berikut. Akun administrator **tidak** diberikan, dan itulah target challenge.

| Username | Password | Perusahaan |
|---|---|---|
| budi_santoso | budi123 | PT Sawit Makmur |
| dewi_rahayu | dewi456 | CV Hijau Nusantara |
| agus_priyanto | agus789 | PT Borneo Palm |
| siti_aminah | siti321 | UD Subur Jaya |
| hendra_wijaya | hendra654 | PT Sawit Unggul |
| rina_kusuma | rina987 | CV Mitra Tani |

## Dokumentasi

| File | Untuk siapa | Isi |
|---|---|---|
| `chall.md` | Player | Deskripsi challenge, hint, format flag |
| `author-notes.md` | Referensi | Full chain, solusi, remediasi, catatan deploy |
| `solve.py` | Referensi | Solver otomatis end-to-end |

> Repo ini **publik by design**, siapa pun boleh deploy instance-nya sendiri. `author-notes.md` dan `solve.py` disertakan sebagai **solusi referensi**. Kalau dipakai untuk kompetisi nyata, rahasiakan hanya *flag asli*-nya (set via `.env` yang ter-gitignore). File solusi tetap tidak ikut ter-bake ke image (lihat `.dockerignore`).

## Struktur Proyek

```
.
├── app.py                # Aplikasi Flask (bug IDOR ada di sini)
├── templates/            # Template Jinja2
├── static/css/           # Stylesheet
├── Dockerfile
├── docker-compose.yml
├── .env.example          # Contoh konfigurasi flag & secret key
├── .dockerignore
├── requirements.txt
├── chall.md              # Dokumentasi untuk player
├── author-notes.md       # Solusi referensi
└── solve.py              # Solver otomatis
```

## Konfigurasi Flag

Flag dibaca dari env `FLAG_B64`, yaitu flag asli yang di-encode base64 **satu kali**. Dashboard menampilkannya dengan encode sekali lagi, jadi player harus **decode 2x**. Contoh ada di `.env.example`.

```bash
echo "FLAG_B64=$(echo -n 'TCC{flag_asli_kamu}' | base64)" > .env
docker compose up --build
```

Kalau `FLAG_B64` tidak di-set, aplikasi memakai **flag dummy lokal** dan mencetak peringatan.

## Lisensi

Dirilis di bawah [MIT License](LICENSE). © 2026 XrunZ (WSE DIVISION).
