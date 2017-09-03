from aemet.models import *
client = AemetClient()
municipio = Municipio.buscar('Logroño')
prediccion = client.get_prediccion(municipio.get_codigo())
print(prediccion.nombre)
