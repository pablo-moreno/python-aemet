from aemet.models import *  # noqa
import click

@click.command()
@click.option('--option', default=1, help='')
def main(option):
    client = AemetClient()
    municipio = Municipio.buscar('Fuenmayor')
    p = client.get_prediccion(municipio.get_codigo())
    print(p.nombre)
    for dia in p.prediccion:
        print(dia)
