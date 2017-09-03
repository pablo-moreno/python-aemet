from aemet.models import *  # noqa
import click

@click.command()
@click.option('-p', '--prediccion', help='Muestra la predicción meteorológica dado un nombre de municipio')
def main(prediccion):
    client = AemetClient()
    municipio = Municipio.buscar(prediccion)
    p = client.get_prediccion(municipio.get_codigo())
    print(p.nombre)
    for dia in p.prediccion:
        print(dia)
