from rest_framework import serializers
from .models import Dosen, Kelas, Mahasiswa, Jadwal

class DosenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dosen
        fields = '__all__'

class KelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kelas
        fields = '__all__'

class MahasiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahasiswa
        fields = '__all__'

class JadwalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jadwal
        fields = '__all__'