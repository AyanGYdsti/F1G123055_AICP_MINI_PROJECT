# UMKM Assistant — Caption, Responder & Promo

**Ringkasan:** Aplikasi web sederhana berbasis Flask untuk membantu UMKM membuat caption media sosial, membalas pesan pelanggan, dan merancang ide promo menggunakan model AI (Hugging Face). Terdapat lapis pengamanan (blacklist + prompt guardrails) untuk mencegah penggunaan oleh brand besar atau institusi.

---

## 🔧 Fitur

- **/caption** — Buat 3 variasi caption (Santai, Formal, Lucu) beserta 5 hashtag.
- **/responder** — Balas pesan/komplain pelanggan dengan nada sesuai konteks.
- **/promo** — Ide promo bulanan dengan 3 strategi dan rentang waktu.
- **Keamanan** — Blacklist brand besar (Python-side) + system prompt guardrails (AI-side).

---

## 📦 Persyaratan

- Python 3.10+
- Paket:
  - Flask
  - python-dotenv
  - huggingface-hub
  - markdown

Instal (Windows):

```bash
python -m venv .venv
.venv\Scripts\activate
pip install flask python-dotenv huggingface-hub markdown
```

---

## ⚙️ Konfigurasi

1. Buat file `.env` di root project dan tambahkan token Hugging Face:

```
HF_TOKEN=your_huggingface_api_token_here
```

2. (Opsional) Pastikan `repo_id` di `app.py` sesuai model yang ingin digunakan (default: `Qwen/Qwen2.5-72B-Instruct`).

---

## ▶️ Menjalankan aplikasi

```bash
python app.py
```

Buka: http://127.0.0.1:5000

---

## 🧭 Cara penggunaan singkat

- **Caption:** isi nama produk, keunggulan, pilih panjang → dapat 3 gaya caption.
- **Responder:** tempel pesan pelanggan → dapat balasan yang tepat.
- **Promo:** masukkan bulan & jenis usaha → dapat 3 ide promo terstruktur.

---

## 🔒 Catatan keamanan & privasi

- Jaga `HF_TOKEN` agar tidak bocor (jangan commit ke git).
- Hati-hati dengan data sensitif — request dikirim ke API Hugging Face.
- Sistem menolak input yang berisi brand besar atau institusi.

---

## 📁 Struktur proyek (ringkasan)

- `app.py` — kode server Flask
- `templates/` — `index.html`, `caption.html`, `promo.html`, `responder.html`, `base.html`
- `.env` — variabel lingkungan (tidak ada di repo)

---

## 🤝 Kontribusi

- Buat issue atau pull request untuk fitur / perbaikan.
- Untuk menambahkan model lain, update `repo_id` dan sesuaikan prompt.

---

## 📜 Lisensi

- Tambahkan lisensi yang diinginkan (mis. **MIT**) di file `LICENSE`.


