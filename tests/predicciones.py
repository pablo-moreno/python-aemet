import unittest
from aemet import *

class PrediccionTest(unittest.TestCase):
    def test_municipio(self):
        m = Municipio.buscar('Fuenmayor')
        self.assertEqual(m.get_codigo(), '26064')

    def test_prediccion(self):
        aemet = Aemet()
        p = aemet.get_prediccion('26064')
        self.assertIsNotNone(p)

if __name__ == '__main__':
    unittest.main()
