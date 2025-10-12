from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'dosen', views.DosenViewSet)
router.register(r'kelas', views.KelasViewSet)
router.register(r'mahasiswa', views.MahasiswaViewSet)
router.register(r'jadwal', views.JadwalViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ask/', views.ask_chatbot, name='ask_chatbot'),
]