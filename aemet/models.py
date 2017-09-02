import requests
import csv
import json
import urllib3

# Constants
API_KEY = open('data/api.key', 'r').read().strip()
BASE_URL = 'https://opendata.aemet.es/opendata/api/'
TOWN_API_URL = 'maestro/municipios/'
WEEKLY_PREDICTION_API_URL = 'prediccion/especifica/municipio/diaria/'
DAILY_PREDICTION_API_URL = 'prediccion/especifica/municipio/horaria/'
TEXT_PREDICTION_API_URL = 'prediccion/{}/{}/{}'
FIRE_RISK_ESTIMATED_MAP = 'incendios/mapasriesgo/estimado/area/{}'
FIRE_RISK_PREDICTED_MAP = 'incendios/mapasriesgo/previsto/dia/{}/area/{}'
NATIONAL_RADAR_API_URL = 'red/radar/nacional'
REGIONAL_RADAR_API_URL = 'red/radar/regional/{}'
LIGHTNINGS_MAP_API_URL = 'red/rayos/mapa/'
PERIOD_WEEKLY, PERIOD_DAILY = 'PERIOD_WEEKLY', 'PERIOD_DAILY'
TOMORROW, THE_DAY_AFTER_TOMORROW, IN_THREE_DAYS = range(1, 4)
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
    def load(data, period):
        if period == PERIOD_DAILY:
            prediccion = PrediccionPorHoras.load(data['prediccion'])
        elif period == PERIOD_WEEKLY:
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
    def __init__(self, api_key=API_KEY):
        self.api_key = api_key
        self.querystring = {
            'api_key': self.api_key
        }
        self.headers = {}

    def _get_request_data(self, url, verbose=False):
        if verbose:
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

    def _get_request_normalized_data(self, url, verbose=False):
        if verbose:
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

    def _download_image_from_url(self, url, output_file, verbose=True):
        if verbose:
            print('Downloading from {}...'.format(url))
        try:
            r = requests.get(
            url,
                params=self.querystring,
                headers=self.headers,
                verify=False
            )
            img_url = r.json()['datos']
            if verbose:
                print(img_url)
            data = requests.get(img_url, verify=False).content
            with open(output_file, 'wb') as f:
                f.write(data)
        except:
            return {
                'status': r.json()['estado']
            }
        return {
            'status': 200,
            'output_file': output_file
        }

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

    def get_prediccion(self, codigo_municipio, period=PERIOD_WEEKLY):
        if period == PERIOD_WEEKLY:
            url = '{}{}{}'.format(
                BASE_URL,
                WEEKLY_PREDICTION_API_URL,
                codigo_municipio
            )
        else:
            url = '{}{}{}'.format(
                BASE_URL,
                DAILY_PREDICTION_API_URL,
                codigo_municipio
            )
        data = self._get_request_data(url)
        return Prediccion.load(data, period)

    def get_prediccion_normalizada(self, ambito=NACIONAL, dia=HOY, ccaa='',
            provincia='', fecha_elaboracion=''):
        if ccaa and provincia:
            raise Exception('You cannot set "provincia" and "ccaa" at the same time')
        if (ccaa or provincia) and ambito == NACIONAL:
            raise Exception('You cannot specify "provincia" or "ccaa" when you set "ambito=NACIONAL"')
        url = '{}{}'.format(BASE_URL, TEXT_PREDICTION_API_URL.format(ambito, dia, ccaa + provincia))
        if fecha_elaboracion:
            url += 'elaboracion/{}/'.format(fecha_elaboracion)
        return self._get_request_normalized_data(url, verbose=True)

    def descargar_mapa_riesgo_previsto_incendio(
            self, output_file, dia=TOMORROW, area=PENINSULA, verbose=True):
        url = '{}{}'.format(BASE_URL, FIRE_RISK_PREDICTED_MAP.format(dia, area))
        return self._download_image_from_url(url, output_file, verbose)

    def descargar_mapa_riesgo_estimado_incendio(
            self, output_file, area=PENINSULA, verbose=True):
        url = '{}{}'.format(BASE_URL, FIRE_RISK_ESTIMATED_MAP.format(area))
        return self._download_image_from_url(url, output_file, verbose)

    def descargar_mapa_radar_nacional(self, output_file, verbose=False):
        url = '{}{}'.format(BASE_URL, NATIONAL_RADAR_API_URL)
        return self._download_image_from_url(url, output_file, verbose)

    def descargar_mapa_radar_regional(self, output_file, region, verbose=False):
        url = '{}{}'.format(BASE_URL, REGIONAL_RADAR_API_URL.format(region))
        return self._download_image_from_url(url, output_file, verbose)

    def descargar_mapa_rayos(self, output_file, verbose=False):
        url = '{}{}'.format(BASE_URL, LIGHTNINGS_MAP_API_URL)
        return self._download_image_from_url(url, output_file, verbose)

if __name__ == '__main__':
    client = AemetClient()
    print(client.descargar_mapa_rayos('prueba.jpg', verbose=True))
