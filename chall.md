# SawitNet — IDOR

| | |
|---|---|
| **Kategori** | Web |
| **Kesulitan** | Ez |
| **Format Flag** | `TCC{...}` |
| **Author** | XrunZ (WSE DIVISION) |

## Deskripsi

SawitNet adalah platform B2B pemesanan kelapa sawit. Platform ini memiliki banyak mitra terdaftar dan satu akun administrator yang menyimpan flag rahasia.

Kamu diberikan akses ke sebuah akun mitra biasa. Tugasmu: **temukan akun administrator dan ambil flag-nya.**

> Flag di dashboard administrator disimpan dalam bentuk **base64 dua layer** — decode **dua kali** untuk mendapatkan flag aslinya.

## Cara Menjalankan

```bash
docker compose up --build
```

Buka <http://localhost:5000>.

## Akun Demo

| Username | Password |
|---|---|
| budi_santoso | budi123 |
| dewi_rahayu | dewi456 |
| agus_priyanto | agus789 |

(Masih ada banyak mitra lain terdaftar di sistem.)

## Objektif

1. Login ke sistem dengan salah satu akun demo.
2. Jelajahi aplikasi dan pahami cara sistem mengidentifikasi pengguna.
3. Temukan akun administrator.
4. Ambil flag dari dashboard administrator, lalu decode.

## Hints

<details>
<summary>Hint 1 — di mana harus melihat</summary>

Perhatikan URL halaman setelah kamu login. Ada sebuah angka yang mengidentifikasi dirimu di dalamnya. Apa yang terjadi kalau angkanya diubah?

</details>

<details>
<summary>Hint 2 — menemukan si admin</summary>

Kamu tidak tahu ID administrator. Tapi aplikasi menyediakan beberapa tempat untuk mengenali siapa saja yang terdaftar — coba jelajahi seluruh menu, dan jangan lewatkan bagian bawah halaman (footer).

</details>

<details>
<summary>Hint 3 — flag</summary>

Flag yang muncul ter-encode base64 **dua kali**. Decode dua kali, mis. `echo '<string>' | base64 -d | base64 -d`.

</details>
