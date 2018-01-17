from aemet import Aemet, Estacion
import json

aemet = Aemet()
estaciones = Estacion.get_estaciones()[:3]
datos = []
anyo_inicio, anyo_fin = 2016, 2017 + 1


for estacion in estaciones:
    print('{}: {}'.format(estacion['indicativo'], estacion['nombre']))
    for anyo in range(anyo_inicio, anyo_fin):
        vcm = aemet.get_valores_climatologicos_mensuales(anyo, estacion['indicativo'])
        resultado = {
            'estacion': estacion,
            'valores_climatologicos': vcm,
            'anyo': anyo
        }
        datos.append(resultado)

print(json.dumps(datos, indent=2))
