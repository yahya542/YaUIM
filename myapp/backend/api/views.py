from rest_framework import viewsets
from .models import Dosen, Kelas, Mahasiswa, Jadwal
from .serializers import DosenSerializer, KelasSerializer, MahasiswaSerializer, JadwalSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests  # for Ollama API
import pandas as pd
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import logging

# Configure logging
logging.basicConfig(filename='chatbot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Global variables for caching
EMBEDDINGS = None
INDEX = None
DATA_TEXTS = []
MODEL = None

def load_excel_data():
    """Load and cache Excel data on server start"""
    global EMBEDDINGS, INDEX, DATA_TEXTS, MODEL

    excel_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'campus_data.xlsx')

    if not os.path.exists(excel_path):
        print("Warning: Excel file not found, using default data")
        DATA_TEXTS = [
            "Nama kampus: YaUIM",
            "Fakultas: Teknik Informatika",
            "Program Studi: Sistem Informasi"
        ]
        return

    try:
        # Read all sheets
        xls = pd.ExcelFile(excel_path)
        all_texts = []

        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            # Convert each row to text
            for _, row in df.iterrows():
                row_text = f"{sheet_name}: " + ", ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
                all_texts.append(row_text)

        DATA_TEXTS = all_texts

        # Create embeddings and FAISS index
        MODEL = SentenceTransformer('all-MiniLM-L6-v2')
        EMBEDDINGS = MODEL.encode(DATA_TEXTS)
        INDEX = faiss.IndexFlatL2(EMBEDDINGS.shape[1])
        INDEX.add(EMBEDDINGS)

        print(f"✅ Loaded {len(DATA_TEXTS)} data entries from Excel")

    except Exception as e:
        print(f"Error loading Excel data: {e}")
        DATA_TEXTS = [
            "Nama kampus: YaUIM",
            "Fakultas: Teknik Informatika",
            "Program Studi: Sistem Informasi"
        ]

# Load data on module import
load_excel_data()

class DosenViewSet(viewsets.ModelViewSet):
    queryset = Dosen.objects.all()
    serializer_class = DosenSerializer

class KelasViewSet(viewsets.ModelViewSet):
    queryset = Kelas.objects.all()
    serializer_class = KelasSerializer

class MahasiswaViewSet(viewsets.ModelViewSet):
    queryset = Mahasiswa.objects.all()
    serializer_class = MahasiswaSerializer

class JadwalViewSet(viewsets.ModelViewSet):
    queryset = Jadwal.objects.all()
    serializer_class = JadwalSerializer

@api_view(['POST'])
def import_data(request):
    """Import data from Excel file to database"""
    try:
        excel_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'campus_data.xlsx')

        if not os.path.exists(excel_path):
            return Response({'error': 'Excel file not found'}, status=status.HTTP_404_NOT_FOUND)

        xls = pd.ExcelFile(excel_path)

        # Import Dosen
        if 'Dosen' in xls.sheet_names:
            df_dosen = pd.read_excel(xls, 'Dosen')
            for _, row in df_dosen.iterrows():
                Dosen.objects.get_or_create(
                    nidn=row['NIDN'],
                    defaults={'nama': row['Nama']}
                )

        # Import Kelas
        if 'Kelas' in xls.sheet_names:
            df_kelas = pd.read_excel(xls, 'Kelas')
            for _, row in df_kelas.iterrows():
                Kelas.objects.get_or_create(
                    nama_kelas=row['Nama Kelas'],
                    angkatan=row['Angkatan']
                )

        # Import Mahasiswa
        if 'Mahasiswa' in xls.sheet_names:
            df_mahasiswa = pd.read_excel(xls, 'Mahasiswa')
            for _, row in df_mahasiswa.iterrows():
                try:
                    kelas = Kelas.objects.get(nama_kelas=row['Kelas'])
                    Mahasiswa.objects.get_or_create(
                        npm=row['NPM'],
                        defaults={'nama': row['Nama'], 'kelas': kelas}
                    )
                except Kelas.DoesNotExist:
                    continue

        # Import Jadwal
        if 'Jadwal' in xls.sheet_names:
            df_jadwal = pd.read_excel(xls, 'Jadwal')
            for _, row in df_jadwal.iterrows():
                try:
                    dosen = Dosen.objects.get(nidn=row['NIDN'])
                    kelas = Kelas.objects.get(nama_kelas=row['Kelas'])
                    Jadwal.objects.get_or_create(
                        dosen=dosen,
                        kelas=kelas,
                        hari=row['Hari'],
                        jam=row['Jam'],
                        ruang=row['Ruang']
                    )
                except (Dosen.DoesNotExist, Kelas.DoesNotExist):
                    continue

        return Response({'message': 'Data imported successfully'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def ask_chatbot(request):
    question = request.data.get('question')
    if not question:
        return Response({'error': 'Question is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Log the question
    logging.info(f"Question received: {question}")

    # Retrieve context using cached embeddings and FAISS
    question_embedding = MODEL.encode([question])
    distances, indices = INDEX.search(question_embedding, 3)

    # Check relevance based on similarity score
    min_distance = distances[0][0]  # Closest match distance
    relevance_threshold = 1.0  # Adjust threshold as needed
    is_relevant = min_distance <= relevance_threshold

    context = ""
    if is_relevant:
        # Question relevant, use RAG
        context_texts = [DATA_TEXTS[i] for i in indices[0]]
        context = ' '.join(context_texts)
        context_full = "\n".join(DATA_TEXTS)
        prompt = f"""Hai! 😊 Saya AI assistant kampus YaUIM yang siap membantu Anda.

Gunakan informasi di bawah ini untuk menjawab pertanyaan mahasiswa dengan cara yang:
- Ramah dan helpful
- Dalam Bahasa Indonesia sehari-hari
- Singkat tapi informatif
- Seperti percakapan manusia normal
- Tambahkan emoji yang sesuai jika cocok

Informasi Kampus:
{context_full}

Pertanyaan: {question}
Jawaban:"""
    else:
        # Question not relevant to campus context
        prompt = f"""Hai! 😊 Sepertinya pertanyaan Anda tidak berkaitan dengan kampus YaUIM.

Saya adalah AI assistant yang khusus membantu mahasiswa dengan informasi kampus.
Mohon maaf, saya hanya bisa menjawab pertanyaan tentang:
- Informasi kampus YaUIM
- Jadwal kuliah
- Dosen dan staf
- Informasi akademik
- Fasilitas kampus

Ada pertanyaan lain tentang kampus yang bisa saya bantu?

Pertanyaan: {question}
Jawaban singkat dan ramah:"""

    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            'model': 'tinyllama:latest',
            'prompt': prompt,
            'stream': False
        })
        if response.status_code == 200:
            answer = response.json().get('response', 'No response')
        else:
            answer = f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        answer = f'Exception: {str(e)}'

    # Log the response
    logging.info(f"Answer: {answer}, Relevant: {is_relevant}")

    return Response({
        'answer': answer,
        'context': context,
        'is_relevant': is_relevant
    })
