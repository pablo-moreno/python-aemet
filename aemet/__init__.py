from aemet.models import *  # noqa
import click


@click.command()
@click.option(
    "-p",
    "--prediccion",
    help="Muestra la predicción meteorológica dado un nombre de municipio",
)
@click.option("-k", "--key", help="API key AEMET")
@click.option("-f", "--keyfile", help="Fichero con la clave de la AEMET.")
def main(prediccion, key, keyfile):
    client = Aemet(api_key=key, api_key_file=keyfile)
    # ToDo: eliminar el for loop de los municipios si se implementa #29
    municipios = Municipio.buscar(prediccion)
    for municipio in municipios:
        print(f"Predicción de temperaturas para {municipio.nombre}:\n")
        p = client.get_prediccion(municipio.get_codigo())
        for dia in p.prediccion:
            print(dia.fecha)
            print("Máxima: {}".format(dia.temperatura["maxima"]))
            print("Mínima: {}\n".format(dia.temperatura["minima"]))
