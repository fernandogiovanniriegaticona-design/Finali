import unittest
from etl import calcular_estado_academico, calcular_condicion_beca

class TestETLBusinessLogic(unittest.TestCase):

    def test_estado_academico_destacado(self):
        # Caso normal: promedio mayor o igual a 16.0
        self.assertEqual(calcular_estado_academico(18.5), "Destacado")
        self.assertEqual(calcular_estado_academico(16.0), "Destacado")

    def test_estado_academico_regular(self):
        # Caso normal: promedio entre 10.5 y 15.99
        self.assertEqual(calcular_estado_academico(14.0), "Regular")
        self.assertEqual(calcular_estado_academico(10.5), "Regular")

    def test_estado_academico_riesgo(self):
        # Caso borde / bajo: promedio menor a 10.5 o nulo
        self.assertEqual(calcular_estado_academico(8.5), "Riesgo Académico")
        self.assertEqual(calcular_estado_academico(None), "Riesgo Académico")

    def test_condicion_beca_completa(self):
        # Caso ideal: promedio >= 17.0 y creditos >= 18
        self.assertEqual(calcular_condicion_beca(18.0, 20), "Beca Completa")

    def test_condicion_beca_media(self):
        # Caso regular: promedio >= 15.5
        self.assertEqual(calcular_condicion_beca(16.0, 15), "Media Beca")

    def test_condicion_beca_ninguna(self):
        # Caso estándar o valores nulos
        self.assertEqual(calcular_condicion_beca(12.0, 12), "Sin Beneficio")
        self.assertEqual(calcular_condicion_beca(None, None), "Sin Beneficio")

if __name__ == '__main__':
    unittest.main()