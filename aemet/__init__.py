import click
from aemet.models import AemetClient, Municipio

@click.command()
@click.option('--option', default=1, help='')
def main(option):
    client = AemetClient()
    municipio = Municipio.buscar('Fuenmayor')
    p = client.get_prediccion(municipio.get_codigo())
    print(p.nombre)
    for dia in p.prediccion:
        print(dia)
