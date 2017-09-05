from aemet.models import *  # noqa
import click

@click.command()
@click.option('-p', '--prediccion', help='Muestra la predicción meteorológica dado un nombre de municipio')
def main(prediccion):
    client = Aemet()
    municipio = Municipio.buscar(prediccion)
    p = client.get_prediccion(municipio.get_codigo())
    for dia in p.prediccion:
        print(dia.fecha)
        print('Máxima: {}'.format(dia.temperatura['maxima']))
        print('Mínima: {}'.format(dia.temperatura['minima']))
        print()
