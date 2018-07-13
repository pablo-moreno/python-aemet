from unittest
from aemet import Municipio

class TestMunicipios(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_busqueda_municipios(self):
        resultados_madrid = Municipio.buscar('Madrid')
        # self.assert(len(resultados_madrid), )
