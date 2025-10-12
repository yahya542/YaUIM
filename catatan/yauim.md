Oke Yahya 😎, kita buat pondasi dasar **skripsi chatbot kampus offline** pakai **DRF (Django Rest Framework) + React.js** supaya kamu bisa langsung eksekusi. Aku tuliskan step by step beserta tools yang harus di-install.

---

## 1️⃣ Struktur Pondasi Proyek

```
campus-chatbot/
│
├─ backend/  # Django + DRF
│   ├─ manage.py
│   ├─ requirements.txt
│   ├─ campus_chatbot/  # settings, urls
│   └─ api/  # app DRF
│       ├─ models.py       # Database: dosen, kelas, jadwal
│       ├─ serializers.py
│       ├─ views.py        # Endpoints API
│       └─ urls.py
│
├─ frontend/  # React.js
│   ├─ package.json
│   ├─ public/
│   └─ src/
│       ├─ App.js
│       ├─ components/    # Input mahasiswa, hasil jawaban
│       └─ services/      # fetch ke DRF
│
└─ ollama_setup/  # Model + RAG
    ├─ embeddings/        # Vector DB / FAISS
    ├─ data/              # Dokumen PDF / CSV jadwal & dosen
    └─ run_chatbot.py     # Script eksekusi RAG + Ollama
```

---

## 2️⃣ Tools & Library yang harus di-install

### **Backend (Python/Django)**

```bash
pip install django djangorestframework
pip install psycopg2-binary   # jika pakai PostgreSQL
pip install sentence-transformers faiss-cpu
pip install pydantic fastapi  # optional kalau mau prototyping lebih cepat
pip install python-dotenv     # untuk environment variables
```

### **Frontend (React.js)**

```bash
npx create-react-app frontend
cd frontend
npm install axios react-router-dom
```

### **Ollama / LLM**

* Pastikan Ollama sudah ter-install:

```bash
ollama pull llama3.2:latest-int8  # versi ringan
```

* Library tambahan:

```bash
pip install langchain  # opsional, untuk RAG workflow
```

---

## 3️⃣ Database Minimum

| Tabel     | Kolom                                    |
| --------- | ---------------------------------------- |
| Dosen     | id, nama, nidn                           |
| Kelas     | id, nama_kelas, angkatan                 |
| Jadwal    | id, dosen_id, kelas_id, hari, jam, ruang |
| Mahasiswa | id, nama, npm, kelas_id                  |

> Data ini akan menjadi **sumber RAG**. Semua query pertanyaan mahasiswa akan mengambil context dari sini.

---

## 4️⃣ Alur Eksekusi RAG + Ollama

1. Mahasiswa input pertanyaan di React → dikirim ke DRF endpoint
2. Backend ambil **dokumen relevan** dari database → embedding + FAISS
3. Backend kirim **context + pertanyaan** ke Ollama
4. Ollama generate jawaban → dikirim balik ke frontend

---

## 5️⃣ Langkah Pertama Eksekusi

1. Buat environment Python:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

2. Install dependencies (backend + RAG)

```bash
pip install -r backend/requirements.txt
```

3. Jalankan server Django:

```bash
python manage.py migrate
python manage.py runserver
```

4. Jalankan React frontend:

```bash
npm start
```

5. Jalankan chatbot:

```bash
python ollama_setup/run_chatbot.py
```

---

Kalau mau, Yahya, aku bisa langsung bikinkan **contoh implementasi minimal**:

* Backend DRF endpoint `/ask`
* React input + tampil jawaban
* Ollama RAG + FAISS integrasi

Sehingga nanti kamu tinggal **isi data jadwal kampus** dan langsung bisa nanya mahasiswa.

Mau aku bikinkan contoh itu sekarang?
