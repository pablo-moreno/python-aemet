import click

@click.command()
@click.option('--option', default=1, help='')
def main(option):
    print('Hello, AEMET')
