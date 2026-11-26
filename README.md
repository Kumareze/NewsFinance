# FinPulse

Agregator berita keuangan Indonesia. Berita diambil otomatis dari beberapa penerbit, ditandai sentimennya sebagai **positif** atau **negatif**, lalu disajikan dalam antarmuka baca yang dipisah per sentimen.

Isi repositori: API FastAPI, frontend Next.js, dan worker scraper Python yang berbagi model database yang sama.

## Sekilas

| Atribut | Nilai |
| --- | --- |
| Tujuan | Membaca berita keuangan Indonesia berdasarkan sentimen |
| Pengambilan berita | Otomatis tiap 30 menit (`SCRAPER_INTERVAL`) |
| Sumber berita | Didaftarkan di tabel `news_sources`: nama, situs, URL RSS, status aktif |
| Backend | FastAPI, prefix `/api/v1`, dokumentasi di `/docs` |
| Frontend | Next.js App Router, data dari `NEXT_PUBLIC_API_URL` |
| Basis data | PostgreSQL, skema lewat Alembic |

## Cara Kerja

```text
Penerbit (RSS/HTML)
        │
        ▼
scraper/   fetch → parse → validasi → cek duplikat → klasifikasi sentimen
        │
        ▼
PostgreSQL   news_sources · news · scrape_logs
        │
        ▼
backend/   FastAPI  /api/v1
        │
        ▼
frontend/  Next.js  Header → Hero → Search → Positive → Negative
```

1. **Ambil.** `scraper/fetchers` menarik feed RSS atau halaman HTML tiap sumber berita yang aktif.
2. **Urai.** `scraper/parsers` mengambil judul, ringkasan, isi, URL, thumbnail, dan waktu terbit. Ada parser khusus CNBC dan Reuters, sisanya parser generik.
3. **Saring.** Validasi dan normalisasi membuang artikel tidak lengkap lalu menyeragamkan teks dan tanggal.
4. **Cek duplikat.** Artikel dengan URL yang sudah ada tidak disimpan dua kali.
5. **Klasifikasi.** `backend/app/sentiment/analyzer.py` menghitung kata kunci positif dan negatif, memperhitungkan kata penyangkal, lalu memberi label `positive`, `negative`, atau `neutral`.
6. **Sajikan.** Frontend membaca daftar berita dan halaman detail dari API.

Repositori:

```text
finpulse/
├── backend/     # API FastAPI, model, service, repository, sentimen, Alembic
├── frontend/    # Next.js: beranda dan detail /news/[slug]
├── scraper/     # fetchers, parsers, pipelines, scheduler
├── dosc/        # dokumen PRD, arsitektur, API, runbook
├── nginx/       # reverse proxy Docker Compose
└── docker-compose.yml
```

## API

Base URL `/api/v1`.

| Metode | Path | Keterangan |
| --- | --- | --- |
| `GET` | `/news/` | Daftar berita: paginasi, filter sentimen dan sumber, sort, pencarian |
| `GET` | `/news/{slug}` | Satu artikel berdasarkan slug |
| `GET` | `/sources/` | Daftar sumber berita |
| `GET` | `/sources/active` | Sumber berita aktif |
| `GET` | `/health` | Health check ringan |

Parameter `GET /news/`:

| Parameter | Nilai | Bawaan |
| --- | --- | --- |
| `page` | >= 1 | `1` |
| `page_size` | 1 sampai 100 | `20` |
| `sentiment` | `positive`, `negative`, `neutral` | semua |
| `source` | nama sumber | semua |
| `sort` | `latest`, `oldest`, `positive`, `negative`, `mixed` | `latest` |
| `q` | kata kunci judul | kosong |

Respons daftar berbentuk `{ items, total, page, page_size }`. Endpoint `POST`, `PUT`, `DELETE` untuk berita dan sumber tersedia untuk keperluan administratif.

## Batasan

- Pencarian hanya mencocokkan judul, belum isi artikel.
- Pola pencarian `ILIKE` dibentuk langsung dari input, sehingga karakter `_` dan `%` bisa memberi hasil yang tidak sesuai harapan.
- Sentimen memakai daftar kata kunci, bukan model bahasa, jadi artikel bernuansa campuran bisa salah kelas.
- Backend menghasilkan label `neutral`, tetapi beranda hanya punya section Positive dan Negative; artikel netral hanya muncul di headline terbaru.
- Filter dan sort didukung API namun belum ditampilkan di antarmuka.
- Thumbnail dimuat sebagai `<img>` biasa karena domain gambar penerbit berbeda-beda.
- Isi artikel tidak selalu tersedia dari RSS; halaman detail menyediakan tautan ke sumber asli.

## Catatan Keamanan

`SECRET_KEY` masih nilai pengembangan, CORS diatur `*`, dan endpoint tulis belum diautentikasi. Semuanya perlu dirapikan sebelum dibuka untuk publik.

## Lisensi

Lihat [`LICENSE`](LICENSE). Hak atas judul, ringkasan, gambar, dan isi artikel tetap milik penerbit masing-masing; repositori ini hanya mengumpulkan tautan dan metadata.

