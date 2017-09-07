import os
import requests
import csv
import json
import urllib3
from datetime import datetime
from pathlib import Path

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_KEY_FILE = os.path.join(str(Path.home()), '.aemet', 'api.key')
try:
    API_KEY = open(API_KEY_FILE, 'r').read().strip()
except:
    API_KEY = ''
BASE_URL = 'https://opendata.aemet.es/opendata/api'
MUNICIPIOS_API_URL = BASE_URL + '/maestro/municipios/'
PREDICCION_SEMANAL_API_URL = BASE_URL + '/prediccion/especifica/municipio/diaria/'
PREDICCION_POR_HORAS_API_URL = BASE_URL + '/prediccion/especifica/municipio/horaria/'
PREDICCION_NORMALIZADA_API_URL = BASE_URL + '/prediccion/{}/{}/{}'
PREDICCION_MARITIMA_ALTA_MAR_API_URL = BASE_URL + '/prediccion/maritima/altamar/area/{}'
PREDICCION_MARITIMA_COSTERA_API_URL = BASE_URL + '/prediccion/maritima/costera/costa/{}'
ESTACIONES_EMA_API_URL = BASE_URL + '/valores/climatologicos/inventarioestaciones/todasestaciones'
VALORES_CLIMATOLOGICOS_NORMALES = BASE_URL + '/valores/climatologicos/normales/estacion/{}'
VALORES_CLIMATOLOGICOS_EXTREMOS = BASE_URL + '/valores/climatologicos/valoresextremos/parametro/{}/estacion/{}'
VALORES_CLIMATOLOGICOS_MENSUALES = BASE_URL + '/valores/climatologicos/mensualesanuales/datos/anioini/{}/aniofin/{}/estacion/{}'
VCP, VCT, VCV = 'P', 'T', 'V'
TIPO_COSTERA, TIPO_ALTA_MAR = 'costera', 'altamar'
OBSERVACION_CONVENCIONAL_API_URL = BASE_URL + '/observacion/convencional/todas/'
OBSERVACION_CONVENCIONAL_ESTACION_API_URL = BASE_URL + 'observacion/convencional/datos/estacion/{}/'
MAPA_RIESGO_INCENDIOS_ESTIMADO = BASE_URL + '/incendios/mapasriesgo/estimado/area/{}'
MAPA_RIESGO_INCENDIOS_PREVISTO = BASE_URL + '/incendios/mapasriesgo/previsto/dia/{}/area/{}'
MAPA_ANALISIS_API_URL = BASE_URL + '/mapasygraficos/analisis/'
MAPAS_SIGNIFICATIVOS_FECHA_API_URL = BASE_URL + '/mapasygraficos/mapassignificativos/fecha/{}/{}/{}/'
MAPAS_SIGNIFICATIVOS_API_URL = BASE_URL + '/mapasygraficos/mapassignificativos/{}/{}/'
MAPAS_SIGNIFICATIVOS_DIAS = {
    'D+0 (00-12)': 'a', 'D+0 (12-24)': 'b',
    'D+1 (00-12)': 'c', 'D+1 (12-24)': 'd',
    'D+2 (00-12)': 'e', 'D+2 (12-24)': 'f'
}
MAPA_RAYOS_API_URL = BASE_URL + '/red/rayos/mapa/'
RADAR_NACIONAL_API_URL = BASE_URL + '/red/radar/nacional'
RADAR_REGIONAL_API_URL = BASE_URL + '/red/radar/regional/{}'
SATELITE_SST = BASE_URL + '/satelites/producto/sst/'
SATELITE_NVDI = BASE_URL + '/satelites/producto/nvdi/'
CONTAMINACION_FONDO_ESTACION_API_URL = BASE_URL + '/red/especial/contaminacionfondo/estacion/{}/'
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

    def ver(self):
        print('Provincia: {}'.format(self.provincia))
        print('Versión: {}'.format(self.version))
        print('ID: {}'.format(self.id))
        print('Origen: {}'.format(self.origen))
        print('Elaborado: {}'.format(self.elaborado))
        print('Predicción: {}'.format(self.prediccion[0].ver()))
        print('Nombre: {}'.format(self.nombre))

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

    def ver(self):
        print('UV Máx.: {}'.format(self.uvMax))
        print('Racha Máxima: {}'.format(self.rachaMax))
        print('Fecha: {}'.format(self.fecha))
        print('Sensación térmica: {}'.format(self.sensTermica))
        print('Humedad relativa: {}'.format(self.humedadRelativa))
        print('Temperatura: {}'.format(self.temperatura))
        print('Cota de nieve: {}'.format(self.cotaNieveProv))
        print('Viento: {}'.format(self.viento))
        print('Probabilidad de precipitación: {}'.format(self.probPrecipitacion))

    def get_temperatura_maxima(self):
        return self.temperatura['maxima']

    def get_temperatura_minima(self):
        return self.temperatura['minima']

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

class PrediccionMaritima:
    def __init__(self, origen={}, aviso={}, situacion={}, prediccion={},
            tendencia=[], id='', nombre='',tipo=TIPO_COSTERA):
        self.origen = origen
        self.aviso = aviso
        self.situacion = situacion
        self.prediccion = prediccion
        self.tendencia = tendencia
        self.id = id
        self.nombre = nombre
        self.tipo = tipo

    @staticmethod
    def load(data, tipo):
        if tipo == TIPO_COSTERA:
            aviso = data['aviso']
            tendencia = data['tendencia']
        else:
            aviso = {}
            tendencia = {}

        return PrediccionMaritima(
            origen=data['origen'],
            aviso=aviso,
            situacion=data['situacion'],
            prediccion=data['prediccion'],
            tendencia=tendencia,
            id=data['id'],
            nombre=data['nombre'],
            tipo=tipo
        )

class Observacion:
    def __init__(self, idema, lon, lat, fint, prec, alt, vmax, vv, dv, dmax, ubi):
        self.idema = idema
        self.lon = lon
        self.lat = lat
        self.fint = fint
        self.prec = prec
        self.alt = alt
        self.vmax = vmax
        self.vv = vv
        self.dv = dv
        self.dmax = dmax
        self.ubi = ubi

    @staticmethod
    def load(data, multiple=False):
        if multiple:
            observaciones = []
            for o in data:
                try:
                    observaciones.append(
                        Observacion(
                            idema=o['idema'],
                            lon=o['lon'],
                            lat=o['lat'],
                            fint=o['fint'],
                            prec=o['prec'],
                            alt=o['alt'],
                            vmax=o['vmax'],
                            vv=o['vv'],
                            dv=o['dv'],
                            dmax=o['dmax'],
                            ubi=o['ubi']
                        )
                    )
                except KeyError:
                    print('Error {}'.format(o['idema']))
            return observaciones
        return Observacion(
            idema=data['idema'],
            lon=data['lon'],
            lat=data['lat'],
            fint=data['fint'],
            prec=data['prec'],
            alt=data['alt'],
            vmax=data['vmax'],
            vv=data['vv'],
            dv=data['dv'],
            dmax=data['dmax'],
            ubi=data['ubi']
        )

class Municipio:
    with open(os.path.join(BASE_DIR, 'data','municipios.json')) as f:
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
        municipio = list(filter(lambda m: id == '{}{}'.format(m['CPRO'], m['CMUN']), Municipio.MUNICIPIOS))[0]
        return Municipio.load(municipio)

    @staticmethod
    def buscar(name):
        try:
            municipio = list(filter(lambda t: name in t['NOMBRE'], Municipio.MUNICIPIOS))[0]
            municipio = Municipio.load(municipio)
            return municipio
        except:
            return None

    def get_codigo(self):
        return '{}{}'.format(self.cpro, self.cmun)

class Estacion:
    def __init__(self, altitud, indicativo, provincia, longitud, nombre, latitud, indsinop):
        self.altitud = altitud
        self.indicativo = indicativo
        self.provincia = provincia
        self.longitud = longitud
        self.nombre = nombre
        self.latitud = latitud
        self.indsinop = indsinop

    def __str__(self):
        return 'Nombre: {}'.format(self.nombre)

    @staticmethod
    def get_estaciones():
        """
        Devuelve un diccionario con la información de todas las estaciones
        """
        url = ESTACIONES_EMA_API_URL
        return Aemet()._get_request_data(url, todos=True)

    @staticmethod
    def buscar_estacion(nombre):
        """
        Devuelve un diccionario con la información de la estación pasado su nombre por parámetro
        :param nombre: Nombre de la estación
        """
        nombre = nombre.upper()
        estaciones = Estacion.get_estaciones()
        estaciones = list(filter(lambda e: nombre in e['nombre'], estaciones))
        result = []
        for estacion in estaciones:
            result.append(
                Estacion(
                    altitud=estacion['altitud'],
                    indicativo=estacion['indicativo'],
                    provincia=estacion['provincia'],
                    longitud=estacion['longitud'],
                    nombre=estacion['nombre'],
                    latitud=estacion['latitud'],
                    indsinop=estacion['indsinop']
                )
            )
        return result

class Aemet:
    def __init__(self, api_key=API_KEY, api_key_file='', verbose=False):
        if not api_key and not api_key_file:
            raise Exception('You must provide an API KEY')
        if api_key_file:
            with open(api_key_file) as f:
                api_key = f.read().strip()
        self.api_key = api_key
        self.querystring = {
            'api_key': self.api_key
        }
        self.headers = {}
        self.verbose = verbose

    @staticmethod
    def guardar_clave_api():
        api_key = input('Escriba su clave de API: ')
        if not api_key:
            raise Exception('La clave de API no puede estar vacía')
        with open(API_KEY_FILE, 'w') as f:
            f.write(api_key)
        print('Clave de API almacenada en {}'.format(API_KEY_FILE))

    def _get_request_data(self, url, todos=False):
        """
        Returns the JSON formatted request data
        """
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
            if todos:
                data = r.json()
            else:
                try:
                    data = r.json()[0]
                except:
                    return r.json()
            return data
        return {
            'error': r.status_code
        }

    def _get_request_normalized_data(self, url):
        """
        Return the request raw content data
        """
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

    def _get_fecha_hoy():
        """
        Devuelve la fecha formateada en el formato que acepta AEMET
        """
        print(datetime.now())
        return '{:%Y-%m-%d}'.format(datetime.now())

    def _get_archivo_codigos_idema(self, archivo_salida):
        """
        Crea un archivo json con todos los registros de estaciones de IDEMA
        :param archivo_salida: Nombre del archivo de salida
        """
        url = OBSERVACION_CONVENCIONAL_API_URL
        estaciones = self._get_request_data(url, todos=True)
        data = {estacion['idema']: estacion['ubi'] for estacion in estaciones}
        with open(archivo_salida, 'w') as f:
            f.write(json.dumps(data, indent=4))

    def _download_image_from_url(self, url, out_file):
        """
        Creates a new file with the content of the image response from an url
        :param url: The URL
        :param out_file: Image filename
        """
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
            with open(out_file, 'wb') as f:
                f.write(data)
        except:
            return {'status': r.json()['estado']}
        return {
            'status': 200,
            'out_file': out_file
        }

    def get_municipio(self, name):
        # TODO
        url = MUNICIPIOS_API_URL
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
        """
        Devuelve un objeto de la clase Prediccion dado un código de municipio y
        un periodo de consulta.
        :param codigo_municipio: Código del municipio
        :param periodo: Periodo de tiempo a consultar, determinado por las constantes PERIODO_SEMANA (p.d.) y PERIODO_DIA
        """
        if periodo == PERIODO_SEMANA:
            url = '{}{}'.format(
                PREDICCION_SEMANAL_API_URL,
                codigo_municipio
            )
        else:
            url = '{}{}'.format(
                PREDICCION_POR_HORAS_API_URL,
                codigo_municipio
            )
        data = self._get_request_data(url)
        return Prediccion.load(data, periodo)

    def get_prediccion_normalizada(self, ambito=NACIONAL, dia=HOY, ccaa='',
            provincia='', fecha_elaboracion=''):
        """
        Devuelve el texto elaborado por AEMET de la predicción meteorológica para
        un determinado ámbito, día, Comunidad Autónoma, provincia y/o fecha de elaboración.
        :param ambito: Ámbito a consultar para la predicción (Constantes NACIONAL (p.d.), CCAA, PROVINCIA)
        :param dia: Día a consultar (Constantes HOY (p.d.), MANANA, PASADO_MANANA)
        :param ccaa: ID de la Comunidad Autónoma
        :param provincia: ID de la provincia
        """
        if ccaa and provincia:
            raise Exception('You cannot set "provincia" and "ccaa" at the same time')
        if (ccaa or provincia) and ambito == NACIONAL:
            raise Exception('You cannot specify "provincia" or "ccaa" when you set "ambito=NACIONAL"')
        url = PREDICCION_NORMALIZADA_API_URL.format(ambito, dia, ccaa + provincia)
        if fecha_elaboracion:
            url += 'elaboracion/{}/'.format(fecha_elaboracion)
        return self._get_request_normalized_data(url)

    def get_observacion_convencional(self, estacion=''):
        """
        Devuelve un objeto de la clase Observacion con los datos de la consulta
        sobre una estación
        :param estacion: [Opcional] Id de la estación a consultar. Por defecto, estación de Madrid
        """
        if estacion:
            url = OBSERVACION_CONVENCIONAL_ESTACION_API_URL.format(estacion)
            return Observacion.load(self._get_request_data(url))
        else:
            url = OBSERVACION_CONVENCIONAL_API_URL
            return Observacion.load(self._get_request_data(url, todos=True), multiple=True)

    def get_valores_climatologicos_mensuales(self, anyo, estacion):
        """
        Devuelve un diccionario con la información de todas las estaciones
        """
        url = VALORES_CLIMATOLOGICOS_MENSUALES.format(anyo, anyo, estacion)
        return self._get_request_data(url)

    def get_contaminacion_fondo(self, estacion):
        # TODO
        url = CONTAMINACION_FONDO_ESTACION_API_URL.format(estacion)
        data = self._get_request_normalized_data(url).splitlines()
        return data

    def get_prediccion_maritima(self, tipo=TIPO_COSTERA, costa='', area=''):
        """
        Devuelve un objeto de la clase PrediccionMaritima dado un tipo de predicción
        (TIPO_COSTERA por defecto o TIPO_ALTA_MAR) y un valor de costa o un valor de área
        :param tipo: Si es de COSTA o de ALTA MAR (definidos por las constantes TIPO_COSTERA y TIPO_ALTA_MAR)
        :param costa: Id de la costa
        :param area: Id del área
        """
        if tipo == TIPO_COSTERA:
            if not costa:
                raise Exception('You must provide a "costa" value')
            url = PREDICCION_MARITIMA_COSTERA_API_URL.format(costa)
        elif tipo == TIPO_ALTA_MAR:
            if not area:
                raise Exception('You must provide an "area" value')
            url = PREDICCION_MARITIMA_ALTA_MAR_API_URL.format(area)
        else:
            raise Exception('Error: "tipo" value not valid')

        return PrediccionMaritima.load(self._get_request_data(url), tipo)

    def get_valores_climatologicos_normales(self, estacion):
        """
        Valores climatológicos normales (periodo 1981-2010) para la estación pasada por parámetro.
        Periodicidad: 1 vez al día.
        :param estacion: ID de la estación de IDEMA
        """
        url = VALORES_CLIMATOLOGICOS_NORMALES.format(estacion)
        return self._get_request_data(url)

    def get_valores_climatologicos_extremos(self, estacion, parametro=VCP):
        """
        Valores extremos para la estación y la variable (precipitación, temperatura y viento) pasadas por parámetro.
        Periodicidad: 1 vez al día.
        :param estacion: ID de la estación de IDEMA
        """
        url = VALORES_CLIMATOLOGICOS_EXTREMOS.format(parametro, estacion)
        return self._get_request_data(url)

    def descargar_mapa_analisis(self, archivo_salida):
        """
        Descarga una imagen con el mapa de análisis
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        """
        url = MAPA_ANALISIS_API_URL
        return self._download_image_from_url(url, archivo_salida)

    def descargar_mapas_significativos(
            self, archivo_salida, fecha='',
            ambito='esp', dia=MAPAS_SIGNIFICATIVOS_DIAS['D+0 (00-12)']):
        """
        Descarga una imagen con los mapas significativos
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        :param ambito: Código de Comunidad Autónoma o de España
        :param dia: Código para fecha determinada [a, b, c, d, e, f]
        Ver MAPAS_SIGNIFICATIVOS_DIAS
        """
        if fecha:
            url = MAPAS_SIGNIFICATIVOS_FECHA_API_URL.format(fecha, ambito, dia)
        else:
            url = MAPAS_SIGNIFICATIVOS_API_URL.format(ambito, dia)
        return self._download_image_from_url(url, archivo_salida)

    def descargar_mapa_riesgo_previsto_incendio(
            self, archivo_salida, dia=INCENDIOS_MANANA, area=PENINSULA):
        """
        Descarga una imagen con el mapa del riesgo previsto de incendio
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        :param area: [Opcional] Área consultada (PENINSULA, BALEARES o CANARIAS)
        """
        url = MAPA_RIESGO_INCENDIOS_PREVISTO.format(dia, area)
        return self._download_image_from_url(url, archivo_salida)

    def descargar_mapa_riesgo_estimado_incendio(self, archivo_salida, area=PENINSULA):
        """
        Descarga una imagen con el mapa del riesgo estimado de incendio
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        :param area: [Opcional] Área consultada (PENINSULA, BALEARES o CANARIAS)
        """
        url = MAPA_RIESGO_INCENDIOS_ESTIMADO.format(area)
        return self._download_image_from_url(url, archivo_salida)

    def descargar_mapa_radar_nacional(self, archivo_salida):
        """
        Descarga una imagen con el mapa del radar por región
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        """
        url = RADAR_NACIONAL_API_URL
        return self._download_image_from_url(url, archivo_salida)

    def descargar_mapa_radar_regional(self, archivo_salida, region):
        """
        Descarga una imagen con el mapa del radar por región
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        :param region: Región consultada
        """
        url = RADAR_REGIONAL_API_URL.format(region)
        return self._download_image_from_url(url, archivo_salida)

    def descargar_mapa_rayos(self, archivo_salida):
        """
        Descarga una imagen con el mapa de rayos a nivel nacional
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        """
        url = MAPA_RAYOS_API_URL
        return self._download_image_from_url(url, archivo_salida)

    def descargar_mapa_satelite_sst(self, archivo_salida):
        """
        Descarga una imagen con el mapa del satélite (SST)
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        """
        url = SATELITE_SST
        return self._download_image_from_url(url, archivo_salida)

    def descargar_mapa_satelite_nvdi(self, archivo_salida):
        """
        Descarga una imagen con el mapa del satélite (NVDI)
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        """
        url = SATELITE_NVDI
        return self._download_image_from_url(url, archivo_salida)

if __name__ == '__main__':
    aemet = Aemet()
    municipio = Municipio.buscar('Logroño')
    prediccion = aemet.get_prediccion(municipio.get_codigo())
    for dia in prediccion.prediccion:
        print(dia.fecha)
        print(dia.get_temperatura_maxima())
        print(dia.get_temperatura_minima())
    estaciones = Estacion.buscar_estacion('Logroño')
    logrono = estaciones[0]
    print(logrono)
