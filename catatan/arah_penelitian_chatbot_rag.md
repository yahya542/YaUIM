# 🧩 Arah Penelitianmu: Analisis dan Implementasi Proses Pengolahan Data pada Sistem Chatbot Kampus Menggunakan Metode Retrieval-Augmented Generation (RAG)

## 🧠 1. Garis Besar Ide

Kamu meneliti bagaimana sistem chatbot:

- Menerima pertanyaan dari user.
- Melakukan ekstraksi keyword dan context understanding.
- Melakukan pencarian ke data kampus (yang diimpor dari Excel → jadi knowledge base FAISS).
- Mengambil potongan data paling relevan.
- Memberikan konteks itu ke model LLM (Ollama).
- Menghasilkan respon akhir yang sesuai dengan konteks kampus.
- Menolak pertanyaan di luar domain ("Maaf, data Anda di luar lingkungan kampus.")

Jadi kamu membahas alur RAG secara rinci dari sisi data dan logika pemrosesan, bukan hanya hasil akhirnya.

## 📘 2. Judul yang Cocok

Kamu bisa pakai salah satu dari beberapa variasi ini (tergantung fokus akhirnya):

- "Analisis Proses Pengolahan Data pada Chatbot Kampus Menggunakan Metode Retrieval-Augmented Generation (RAG)"
- "Implementasi dan Analisis Pipeline Pengolahan Data Chatbot Domain Kampus Berbasis RAG dan Ollama"
- "Perancangan Sistem Chatbot Akademik Berbasis Django dengan Integrasi RAG untuk Pemrosesan Data Terarah"

## ⚙️ 3. Struktur Jurnal / TA-nya

### BAB I – Pendahuluan

- **Latar belakang**: (kenapa chatbot kampus dibutuhkan)
- **Rumusan masalah**:
  - Bagaimana proses pengolahan data dilakukan dalam chatbot kampus berbasis RAG?
  - Bagaimana implementasi pipeline pengolahan data agar chatbot mampu memberikan respon sesuai konteks kampus?
- **Tujuan penelitian**
- **Batasan masalah**: (data hanya lingkup kampus, berbasis data Excel)

### BAB II – Landasan Teori

Bahas teori dasar:

- Chatbot dan jenis-jenisnya
- LLM (Large Language Model) dan Ollama
- Metode Retrieval-Augmented Generation (RAG)
- FAISS (untuk pencarian semantik)
- Arsitektur sistem Django dan integrasi AI
- Flow pengolahan data (data preprocessing, vectorization, similarity search, response generation)

### BAB III – Metodologi Penelitian

- Pendekatan yang dipakai (misalnya: experimental research atau system development research)
- Arsitektur sistem chatbot
- Diagram alur data: input → preprocessing → retrieval → generation → response
- Implementasi: bagaimana Excel diubah menjadi data vektor dan dihubungkan ke FAISS
- Pengujian: input valid vs input di luar domain

### BAB IV – Hasil dan Pembahasan

- Penjelasan hasil implementasi pipeline
- Studi kasus beberapa pertanyaan (misal: "Bagaimana cara mengurus KRS?" vs "Kapan konser Coldplay?")
- Analisis hasil respon (akurasi, relevansi, waktu respon)
- Analisis kesalahan (misalnya data ambigu, hasil retrieval tidak relevan)

### BAB V – Kesimpulan dan Saran

- Kesimpulan dari proses pengolahan data
- Implikasi untuk pengembangan chatbot kampus ke depan
- Saran: optimalisasi FAISS, fine-tuning embedding, atau peningkatan model bahasa

## 💡 4. Nilai Ilmiah & Keunggulan Topikmu

Kamu tidak hanya membuat sistem, tapi juga membedah proses AI bekerja dari sisi data.

Jurnal ini bisa masuk ke bidang: Artificial Intelligence, Data Processing, atau Natural Language Understanding.

Bisa diuji dan diukur (dengan tabel hasil retrieval, relevansi, atau precision-recall).