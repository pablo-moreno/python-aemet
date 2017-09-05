from aemet.models import *

client = Aemet()
municipio = Municipio.buscar('Logroño')
p = client.get_prediccion(municipio.get_codigo())
for dia in p.prediccion:
    print(dia.fecha)
    print('Máxima: {}'.format(dia.temperatura['maxima']))
    print('Mínima: {}'.format(dia.temperatura['minima']))
    print()
