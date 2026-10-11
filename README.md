# SawitNet — IDOR CTF Challenge

**Dibuat oleh:** XrunZ (WSE DIVISION)

SawitNet adalah aplikasi web simulasi pemesanan kelapa sawit yang **sengaja** dibuat rentan terhadap **IDOR (Insecure Direct Object Reference)**. Challenge ini dipakai untuk pelatihan keamanan siber (CTF) — khususnya belajar menemukan dan memperbaiki celah kontrol akses.

> ⚠️ **Disclaimer:** Aplikasi ini dibuat untuk tujuan edukasi. Jangan menjalankan/meniru pola rentan ini di lingkungan produksi nyata.

---

## Cara Menjalankan

**Docker (disarankan):**

```bash
docker compose up --build
```

**Tanpa Docker:**

```bash
pip install -r requirements.txt
python app.py
```

Lalu buka browser ke: <http://localhost:5000>

---

## Akun Demo

Gunakan salah satu akun berikut untuk masuk pertama kali. Akun administrator **tidak** diberikan — itulah target challenge.

| Username | Password | Perusahaan |
|---|---|---|
| budi_santoso | budi123 | PT Sawit Makmur |
| dewi_rahayu | dewi456 | CV Hijau Nusantara |
| agus_priyanto | agus789 | PT Borneo Palm |
| siti_aminah | siti321 | UD Subur Jaya |
| hendra_wijaya | hendra654 | PT Sawit Unggul |
| rina_kusuma | rina987 | CV Mitra Tani |

---

## Dokumentasi

| File | Untuk siapa | Isi |
|---|---|---|
| `chall.md` | **Player** | Deskripsi challenge, hint, format flag |
| `author-notes.md` | **Panitia (RAHASIA)** | Full chain, solusi, remediasi, catatan deploy |
| `solve.py` | **Panitia** | Solver otomatis end-to-end |

> ℹ️ Repo ini **publik by design** — siapa pun boleh deploy instance-nya sendiri. `author-notes.md` dan `solve.py` disertakan sebagai **solusi referensi** (silakan dibaca). Kalau challenge ini dipakai untuk **kompetisi nyata**, rahasiakan hanya *flag asli*-nya (set via `.env` yang ter-gitignore). File solusi tetap tidak ikut ter-bake ke image (lihat `.dockerignore`).

---

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
├── author-notes.md       # Dokumentasi untuk panitia (rahasia)
└── solve.py              # Solver otomatis
```

---

## Konfigurasi Flag

Flag dibaca dari env `FLAG_B64` = flag asli yang di-encode base64 **satu kali**. Dashboard menampilkannya dengan encode sekali lagi, jadi player harus **decode 2x**. Lihat `.env.example`.

```bash
# Encode flag asli lalu taruh di .env
echo "FLAG_B64=$(echo -n 'TCC{flag_asli_kamu}' | base64)" > .env
docker compose up --build
```

Jika `FLAG_B64` tidak di-set, aplikasi memakai **flag dummy lokal** dan mencetak peringatan.
