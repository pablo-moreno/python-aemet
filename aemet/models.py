import requests
import csv
import json
import urllib3
from datetime import datetime

# Constants
API_KEY = open('data/api.key', 'r').read().strip()
BASE_URL = 'https://opendata.aemet.es/opendata/api/'
TOWN_API_URL = 'maestro/municipios/'
PREDICCION_SEMANAL_API_URL = 'prediccion/especifica/municipio/diaria/'
PREDICCION_POR_HORAS_API_URL = 'prediccion/especifica/municipio/horaria/'
PREDICCION_NORMALIZADA_API_URL = 'prediccion/{}/{}/{}'
MAPA_RIESGO_INCENDIOS_ESTIMADO = 'incendios/mapasriesgo/estimado/area/{}'
MAPA_RIESGO_INCENDIOS_PREVISTO = 'incendios/mapasriesgo/previsto/dia/{}/area/{}'
MAPA_ANALISIS_API_URL = 'mapasygraficos/analisis/'
MAPAS_SIGNIFICATIVOS_FECHA_API_URL = '/mapasygraficos/mapassignificativos/fecha/{}/{}/{}/'
MAPAS_SIGNIFICATIVOS_API_URL = '/mapasygraficos/mapassignificativos/{}/{}/'
MAPAS_SIGNIFICATIVOS_DIAS = {
    'D+0 (00-12)': 'a', 'D+0 (12-24)': 'b',
    'D+1 (00-12)': 'c', 'D+1 (12-24)': 'd',
    'D+2 (00-12)': 'e', 'D+2 (12-24)': 'f'
}
MAPA_RAYOS_API_URL = 'red/rayos/mapa/'
RADAR_NACIONAL_API_URL = 'red/radar/nacional'
RADAR_REGIONAL_API_URL = 'red/radar/regional/{}'
PERIODO_SEMANA, PERIODO_DIA = 'PERIODO_SEMANA', 'PERIODO_DIA'
INCENDIOS_MANANA, INCENDIOS_PASADO_MANANA, INCENDIOS_EN_3_DIAS = range(1, 4)
PENINSULA, CANARIAS, BALEARES = 'p', 'c', 'b'
NACIONAL, CCAA, PROVINCIA = 'nacional', 'ccaa', 'provincia'
HOY, MANANA, PASADO_MANANA, MEDIO_PLAZO, TENDENCIA = 'hoy', 'manana', 'pasadomanana', 'medioplazo', 'tendencia'

# Disable Insecure Request Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Prediccion:
    def __init__(self, provincia, version, id, origen,
            elaborado, prediccion, nombre):
        self.provincia = provincia
        self.version = version
        self.id = id
        self.origen = origen
        self.elaborado = elaborado
        self.prediccion = prediccion
        self.nombre = nombre

    @staticmethod
    def load(data, periodo):
        if periodo == PERIODO_DIA:
            prediccion = PrediccionPorHoras.load(data['prediccion'])
        elif periodo == PERIODO_SEMANA:
            prediccion = PrediccionDia.load(data['prediccion'])

        return Prediccion(
            provincia=data['provincia'],
            version=data['version'],
            id=data['id'],
            origen=data['origen'],
            elaborado=data['elaborado'],
            prediccion=prediccion,
            nombre=data['nombre']
        )

class PrediccionDia:
    def __init__(self, uvMax=0, rachaMax=[], fecha='', sensTermica=[], humedadRelativa=[],
            temperatura=[], estadoCielo=[], cotaNieveProv=[], viento=[], probPrecipitacion=[]):
        self.uvMax = uvMax
        self.rachaMax = rachaMax
        self.fecha = fecha
        self.sensTermica = sensTermica
        self.humedadRelativa = humedadRelativa
        self.temperatura = temperatura
        self.estadoCielo = estadoCielo
        self.cotaNieveProv = cotaNieveProv
        self.viento = viento
        self.probPrecipitacion = probPrecipitacion

    @staticmethod
    def load(data):
        predicciones = []
        for dia in data['dia']:
            try:
                uvMax = dia['uvMax']
            except KeyError:
                uvMax = []
            predicciones.append(
                PrediccionDia(
                    uvMax=uvMax,
                    rachaMax=dia['rachaMax'],
                    fecha=dia['fecha'],
                    sensTermica=dia['sensTermica'],
                    humedadRelativa=dia['humedadRelativa'],
                    temperatura=dia['temperatura'],
                    cotaNieveProv=dia['cotaNieveProv'],
                    viento=dia['viento'],
                    probPrecipitacion=dia['probPrecipitacion'],
                )
            )
        return predicciones

class PrediccionPorHoras:
    def __init__(self, estadoCielo=[], precipitacion=[], vientoAndRachaMax=[], ocaso='',
            probTormenta=[], probPrecipitacion=[], orto='', humedadRelativa=[], nieve=[],
            probNieve=[], fecha='', temperatura=[], sensTermica=[]):
        self.estadoCielo = estadoCielo
        self.precipitacion = precipitacion
        self.vientoAndRachaMax = vientoAndRachaMax
        self.ocaso = ocaso
        self.probTormenta = probTormenta
        self.probPrecipitacion = probPrecipitacion
        self.orto = orto
        self.humedadRelativa = humedadRelativa
        self.nieve = nieve
        self.probNieve = probNieve
        self.fecha = fecha
        self.temperatura = temperatura
        self.sensTermica = sensTermica

    @staticmethod
    def load(data):
        periodos = []
        for p in data['dia']:
            try:
                periodos.append(
                    PrediccionPorHoras(
                        estadoCielo=p['estadoCielo'],
                        precipitacion=p['precipitacion'],
                        vientoAndRachaMax=p['vientoAndRachaMax'],
                        ocaso=p['ocaso'],
                        probTormenta=p['probTormenta'],
                        probPrecipitacion=p['probPrecipitacion'],
                        orto=p['orto'],
                        humedadRelativa=p['humedadRelativa'],
                        nieve=p['nieve'],
                        probNieve=p['probNieve'],
                        fecha=p['fecha'],
                        temperatura=p['temperatura'],
                        sensTermica=p['sensTermica']
                    )
                )
            except KeyError:
                pass
        return periodos

class Municipio:
    with open('data/municipios.json') as f:
        MUNICIPIOS = json.loads(f.read())

    def __init__(self, cod_auto, cpro, cmun, dc, nombre):
        self.cod_auto = cod_auto
        self.cpro = cpro
        self.cmun = cmun
        self.dc = dc
        self.nombre = nombre

    @staticmethod
    def load(data):
        return Municipio(
            cod_auto=data['CODAUTO'],
            cpro=data['CPRO'],
            cmun=data['CMUN'],
            dc=data['DC'],
            nombre=data['NOMBRE']
        )

    @staticmethod
    def get_municipio(id):
        print(id)
        return Municipio()

    @staticmethod
    def buscar(name):
        municipio = list(filter(lambda t: name in t['NOMBRE'], Municipio.MUNICIPIOS))[0]
        municipio = Municipio.load(municipio)
        return municipio

    def get_codigo(self):
        return '{}{}'.format(self.cpro, self.cmun)

class AemetClient:
    def __init__(self, api_key=API_KEY, api_key_file='', verbose=False):
        if not api_key and not api_key_file:
            raise Exception('You must provide an API KEY')
        if api_key_file:
            with open('api_key_file') as f:
                api_key = f.read().strip()
        self.api_key = api_key
        self.querystring = {
            'api_key': self.api_key
        }
        self.headers = {}
        self.verbose = verbose

    def _get_request_data(self, url):
        if self.verbose:
            print(url)
        r = requests.get(
            url,
            headers=self.headers,
            params=self.querystring,
            verify=False    # Avoid SSL Verification .__.
        )
        if r.status_code == 200:
            r = requests.get(r.json()['datos'], verify=False)
            data = r.json()[0]
            return data
        return {
            'error': r.status_code
        }

    def _get_request_normalized_data(self, url):
        if self.verbose:
            print(url)
        r = requests.get(
            url,
            headers=self.headers,
            params=self.querystring,
            verify=False    # Avoid SSL Verification .__.
        )
        if r.status_code == 200:
            r = requests.get(r.json()['datos'], verify=False)
            data = r.text
            return data
        return {
            'error': r.status_code
        }

    def _download_image_from_url(self, url, archivo_salida):
        if self.verbose:
            print('Downloading from {}...'.format(url))
        try:
            r = requests.get(
                url,
                params=self.querystring,
                headers=self.headers,
                verify=False
            )
            error = ''
            img_url = r.json()['datos']
            if self.verbose:
                print(img_url)
            r = requests.get(img_url, verify=False)
            try:
                error = r.json()
            except:
                pass
            if error:
                raise Exception(error)
            data = r.content
            with open(archivo_salida, 'wb') as f:
                f.write(data)
        except:
            return {'status': r.json()['estado']}
        return {
            'status': 200,
            'archivo_salida': archivo_salida
        }

    def _get_fecha_hoy():
        print(datetime.now())
        return '{:%Y-%m-%d}'.format(datetime.now())

    def get_municipio(self, name):
        url = '{}{}'.format(BASE_URL, TOWN_API_URL)
        r = requests.get(
            url,
            params = {
                "nombre": name,
                'api_key': self.api_key
            },
            headers=self.headers,
            verify=False
        )
        data = r.json()
        return data

    def get_prediccion(self, codigo_municipio, periodo=PERIODO_SEMANA):
        if periodo == PERIODO_SEMANA:
            url = '{}{}{}'.format(
                BASE_URL,
                PREDICCION_SEMANAL_API_URL,
                codigo_municipio
            )
        else:
            url = '{}{}{}'.format(
                BASE_URL,
                PREDICCION_POR_HORAS_API_URL,
                codigo_municipio
            )
        data = self._get_request_data(url)
        return Prediccion.load(data, periodo)

    def get_prediccion_normalizada(self, ambito=NACIONAL, dia=HOY, ccaa='',
            provincia='', fecha_elaboracion=''):
        if ccaa and provincia:
            raise Exception('You cannot set "provincia" and "ccaa" at the same time')
        if (ccaa or provincia) and ambito == NACIONAL:
            raise Exception('You cannot specify "provincia" or "ccaa" when you set "ambito=NACIONAL"')
        url = '{}{}'.format(BASE_URL, PREDICCION_NORMALIZADA_API_URL.format(ambito, dia, ccaa + provincia))
        if fecha_elaboracion:
            url += 'elaboracion/{}/'.format(fecha_elaboracion)
        return self._get_request_normalized_data(url)

    def descargar_mapa_analisis(self, archivo_salida):
        url = '{}{}'.format(BASE_URL, MAPA_ANALISIS_API_URL)
        return self._download_image_from_url(url, archivo_salida)

    def descargar_mapas_significativos(
            self, archivo_salida, fecha='',
            ambito='esp', dia=MAPAS_SIGNIFICATIVOS_DIAS['D+0 (00-12)']
    ):
        if fecha:
            url = '{}{}'.format(BASE_URL, MAPAS_SIGNIFICATIVOS_FECHA_API_URL.format(fecha, ambito, dia))
        else:
            url = '{}{}'.format(BASE_URL, MAPAS_SIGNIFICATIVOS_API_URL.format(ambito, dia))
        return self._download_image_from_url(url, archivo_salida)

    def descargar_mapa_riesgo_previsto_incendio(
            self, archivo_salida, dia=INCENDIOS_MANANA, area=PENINSULA):
        url = '{}{}'.format(BASE_URL, MAPA_RIESGO_INCENDIOS_PREVISTO.format(dia, area))
        return self._download_image_from_url(url, archivo_salida)

    def descargar_mapa_riesgo_estimado_incendio(self, archivo_salida, area=PENINSULA):
        url = '{}{}'.format(BASE_URL, MAPA_RIESGO_INCENDIOS_ESTIMADO.format(area))
        return self._download_image_from_url(url, archivo_salida)

    def descargar_mapa_radar_nacional(self, archivo_salida):
        url = '{}{}'.format(BASE_URL, RADAR_NACIONAL_API_URL)
        return self._download_image_from_url(url, archivo_salida)

    def descargar_mapa_radar_regional(self, archivo_salida, region):
        url = '{}{}'.format(BASE_URL, RADAR_REGIONAL_API_URL.format(region))
        return self._download_image_from_url(url, archivo_salida)

    def descargar_mapa_rayos(self, archivo_salida):
        url = '{}{}'.format(BASE_URL, MAPA_RAYOS_API_URL)
        return self._download_image_from_url(url, archivo_salida)

if __name__ == '__main__':
    client = AemetClient(verbose=True)
    print(client.descargar_mapas_significativos('prueba.jpg'))
