from django.test import TestCase
from ..services.analisis_service import AnalisisService

class AnalisisServiceTestCase(TestCase):
    def test_dificultad_vs_valoracion(self):
        response = AnalisisService.dificultad_vs_valoracion('todas', 'todas')
        self.assertEqual(response.status_code, 200)