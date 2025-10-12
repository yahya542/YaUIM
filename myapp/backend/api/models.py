from django.db import models

class Dosen(models.Model):
    nama = models.CharField(max_length=100)
    nidn = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nama

class Kelas(models.Model):
    nama_kelas = models.CharField(max_length=50)
    angkatan = models.IntegerField()

    def __str__(self):
        return f"{self.nama_kelas} {self.angkatan}"

class Mahasiswa(models.Model):
    nama = models.CharField(max_length=100)
    npm = models.CharField(max_length=20, unique=True)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama

class Jadwal(models.Model):
    dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    hari = models.CharField(max_length=10)  # e.g., 'Senin'
    jam = models.TimeField()
    ruang = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.dosen.nama} - {self.kelas.nama_kelas} - {self.hari}"
