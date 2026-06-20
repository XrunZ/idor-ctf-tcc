# 🌴 SawitNet — IDOR CTF Challenge
> **Dibuat oleh:** WSE DIVISION </XrunZ>
> **Versi:** 2.2 (2026)

**SawitNet** adalah aplikasi web simulasi pemesanan kelapa sawit yang sengaja dirancang memiliki kerentanan **IDOR (Insecure Direct Object Reference)**. Challenge ini ditujukan untuk pelatihan keamanan siber (CTF) dalam mempelajari eksploitasi dan remediasi akses kontrol.

---

## 🚀 Cara Menjalankan

Aplikasi ini dapat langsung dijalankan menggunakan Docker Compose:

```bash
docker compose up --build
```

Setelah kontainer berjalan, buka browser dan akses:
👉 **[http://localhost:5000](http://localhost:5000)**

---

## 👥 Akun Demo (19 Pengguna Biasa)

Gunakan salah satu kredensial akun berikut untuk masuk pertama kali ke sistem:

| Username       | Password     | Perusahaan           |
|----------------|--------------|----------------------|
| budi_santoso   | budi123      | PT Sawit Makmur      |
| dewi_rahayu    | dewi456      | CV Hijau Nusantara   |
| agus_priyanto  | agus789      | PT Borneo Palm       |
| siti_aminah    | siti321      | UD Subur Jaya        |
| hendra_wijaya  | hendra654    | PT Sawit Unggul      |
| rina_kusuma    | rina987      | CV Mitra Tani        |
| bambang_eko    | bambang111   | PT Eko Sawit         |
| nurul_hidayah  | nurul222     | UD Berkah Tani       |
| wahyu_setiawan | wahyu333     | PT Setiawan Agro     |
| fitri_lestari  | fitri444     | CV Lestari Abadi     |
| joko_susilo    | joko555      | PT Susilo Palm Oil   |
| maya_indrawati | maya666      | UD Indra Sawit       |
| ahmad_fauzi    | ahmad777     | PT Fauzi Agri        |
| lilis_suryani  | lilis888     | CV Surya Tani        |
| doni_prakoso   | doni999      | PT Prakoso Sawit     |
| yanti_marlina  | yanti000     | UD Marlina Sejahtera |
| rudi_hartono   | rudi101      | PT Hartono Agro      |
| sri_wahyuni    | sri202       | CV Wahyuni Palm      |
| teguh_prasetyo | teguh303     | PT Prasetyo Sawit    |

> ⚠️ **Catatan:** Akun Administrator utama bernama **XrunZ**. Password admin tidak diberikan dan harus dilewati menggunakan teknik eksploitasi IDOR!

---

## 🎯 Objektif & Skenario Eksploitasi

1. **Autentikasi Awal:** Login ke sistem menggunakan salah satu akun pengguna biasa di atas.
2. **Analisis Pola:** Perhatikan struktur URL halaman dashboard setelah Anda login:
   `http://localhost:5000/dashboard/<user_id>`
3. **Tahap Enumerasi:** Lakukan modifikasi angka ID pada parameter `<user_id>` untuk memeriksa data profil pengguna lain.
4. **Temukan Administrator:** Akun admin (**XrunZ**) terdaftar di database dengan **ID 13**.
5. **Dapatkan Bendera (Flag):** Akses dashboard admin secara tidak sah (`/dashboard/13`) untuk mendapatkan flag yang tersimpan di sana.

---

## 🐛 Analisis Kerentanan & Cara Memperbaikinya

Aplikasi ini rentan karena tidak memvalidasi apakah pengguna yang sedang login di sesi aktif memiliki hak akses untuk membaca profil `user_id` yang diminta pada URL.

### Kode yang Rentan (di `app.py`):
```python
@app.route("/dashboard/<int:user_id>")
@login_required
def dashboard(user_id):
    user = get_user(user_id)
    # ... langsung merender profil user tanpa mencocokkan dengan session aktif
```

### Solusi Perbaikan (Remediasi):
Untuk menutup celah keamanan ini, tambahkan validasi kepemilikan sesi di setiap rute sebelum menampilkan data:
```python
@app.route("/dashboard/<int:user_id>")
@login_required
def dashboard(user_id):
    # Validasi apakah user yang login sesuai dengan ID yang diakses
    if session.get("user_id") != user_id and session.get("role") != "admin":
        return abort(403) # Kembalikan kode Forbidden jika tidak berhak
    
    user = get_user(user_id)
    # ...
```
