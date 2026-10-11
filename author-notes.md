# Author Notes — SawitNet IDOR (Solusi Referensi)

> ℹ️ Ini dokumen **solusi referensi** — boleh publik (repo ini memang publik by design agar orang bisa deploy sendiri). Hanya *flag asli* yang perlu dirahasiakan bila challenge dipakai untuk kompetisi nyata: set lewat `.env` (ter-gitignore), jangan di-commit. File ini tidak di-bake ke image (lihat `.dockerignore`).

## Ringkasan Chain

```
Login (akun mitra biasa) -> IDOR pada parameter user_id -> akses dashboard admin -> decode base64 -> FLAG
```

Cukup satu hop exploit: IDOR vertikal (horizontal privilege escalation).

## Detail Solusi

1. **Login** dengan akun mitra mana pun, mis. `budi_santoso : budi123`.
2. Setelah login, URL berisi `http://localhost:5000/dashboard/<user_id>` (mis. `/dashboard/1`).
3. Route `/dashboard/<int:user_id>` **tidak** memvalidasi apakah `user_id` milik sesi yang aktif. Jadi cukup ganti angkanya untuk membaca dashboard user lain.
4. **Akun administrator** adalah `XrunZ` dengan **`user_id = 13`**.
   - ID 13 muncul karena `init_db()` menyisipkan 20 user berurutan (AUTOINCREMENT mulai dari 1) dan `XrunZ` berada di urutan ke-13 pada list seed di `app.py`.
   - Kode **tidak** meng-hardcode 13: dashboard menampilkan flag kapan pun user target punya `role == 'admin'`. Kalau urutan seed diubah, ID admin ikut bergeser dan challenge tetap konsisten.
5. Akses `/dashboard/13` → muncul blok `flag_b64`.
6. **Decode base64 DUA kali** → `TCC{...}`.

### Breadcrumb discovery (dibuat sengaja)

Supaya player bisa menemukan ID admin **tanpa menebak**, ada dua sinyal di dalam aplikasi:

- **Footer** setiap halaman: `Made by WSE DIVISION </XrunZ>`.
- **Menu "Direktori Mitra"** (`/mitra`) menampilkan seluruh mitra terdaftar (username + perusahaan). Di situ terlihat user `XrunZ` dengan perusahaan `WSE DIVISION` — cocok dengan footer. Dari sini player tahu siapa adminnya, lalu melakukan enumerasi ID (ruang ID kecil: 1–20).

`/mitra` **sengaja** tidak menampilkan role, ID, maupun link ke dashboard — supaya langkah exploit (menebak/mengenumerasi ID + IDOR) tetap harus dilakukan player.

## Sumber Flag

- Satu sumber kebenaran: env **`FLAG_B64`** = flag asli yang di-encode base64 **satu kali**.
- Dashboard menampilkan `FLAG_B64` yang di-encode **sekali lagi** (`FLAG_DISPLAY`), jadi player harus **decode 2x**.
- Default (kalau env tidak di-set) = **dummy lokal** `TCC{local_dummy_flag_seccess}` + peringatan ke stderr.
- Untuk event sungguhan: set `FLAG_B64` lewat `.env` (lihat `.env.example`). **Jangan** commit flag asli.
- Rotasi flag per event cukup dengan mengganti nilai env — tidak perlu ubah kode.

## Remediasi (untuk materi)

Tambahkan validasi kepemilikan sesi di **setiap** route yang menerima `user_id`:

```python
from flask import abort

@app.route("/dashboard/<int:user_id>")
@login_required
def dashboard(user_id):
    # User hanya boleh mengakses datanya sendiri; admin boleh semua.
    if session.get("user_id") != user_id and session.get("role") != "admin":
        abort(403)
    user = get_user(user_id)
    ...
```

Pola yang sama harus diterapkan pada `/pesanan`, `/buat-pesanan`, `/transaksi`, `/profil`, `/pengaturan`, dan `/api/profile`. Intinya: **jangan percaya `user_id` dari URL** — ambil identitas dari sesi server-side.

## Catatan Deploy

- Jalankan via `docker compose up --build`. Image memakai `gunicorn -w 1` (worker tunggal) — cukup untuk CTF dan menjaga konsistensi sesi/DB.
- DB SQLite dibuat ulang tiap boot (tanpa volume), jadi state selalu bersih.
- `SECRET_KEY` bisa di-set lewat env; kalau kosong, dipakai kunci acak per-boot (aman untuk 1 worker).
- Admin password di-generate acak 24 karakter saat seed — tidak bisa di-brute force dan tidak pernah ditampilkan.

## Yang JANGAN dilakukan

- ❌ Commit flag asli ke repo/compose. Gunakan `.env` yang ter-gitignore.
- ❌ Bagikan `author-notes.md` / `solve.py` ke player.
- ❌ Hardcode ID admin (13) di kode/template — sudah dihapus; jaga agar tidak kembali.
- ❌ Menaruh petunjuk solusi di README publik.

## Validasi Sebelum Rilis

- [ ] Leak sweep: `curl` `/app.py`, `/package.json`, `/.git/config`, `/static/../app.py` → semua `404`.
- [ ] Unintended solve: pastikan flag **hanya** muncul di dashboard user ber-`role='admin'`, tidak di `/api/profile` atau route lain.
- [ ] Negative test: patch bug-nya (tambah cek `session['user_id'] != user_id`) → exploit gagal.
- [ ] Black-box: beri instance + `chall.md` saja ke orang lain, pastikan bisa solve tanpa source.
- [ ] `docker compose config` menghasilkan `FLAG_B64` yang benar.
