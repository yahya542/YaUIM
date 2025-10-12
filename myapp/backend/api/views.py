from rest_framework import viewsets
from .models import Dosen, Kelas, Mahasiswa, Jadwal
from .serializers import DosenSerializer, KelasSerializer, MahasiswaSerializer, JadwalSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests  # for Ollama API

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
def ask_chatbot(request):
    question = request.data.get('question')
    if not question:
        return Response({'error': 'Question is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Placeholder for RAG logic
    # Here you would retrieve relevant data from DB, create embeddings, etc.
    # For now, just forward to Ollama
    
    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            'model': 'llama3.2:latest-int8',
            'prompt': question,
            'stream': False
        })
        answer = response.json().get('response', 'No response')
    except Exception as e:
        answer = f'Error: {str(e)}'
    
    return Response({'answer': answer})
