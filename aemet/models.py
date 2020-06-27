import requests
import json
import urllib3
from datetime import datetime
from aemet.constants import *

# Disable Insecure Request Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Prediccion:
    def __init__(self, provincia, version, id, origen, elaborado, prediccion, nombre):
        self.provincia = provincia
        self.version = version
        self.id = id
        self.origen = origen
        self.elaborado = elaborado
        self.prediccion = prediccion
        self.nombre = nombre

    @staticmethod
    def from_json(data, periodo):
        prediccion = ''
        if periodo == PERIODO_DIA:
            prediccion = PrediccionPorHoras.from_json(data.get('prediccion'))
        elif periodo == PERIODO_SEMANA:
            prediccion = PrediccionDia.from_json(data.get('prediccion'))

        return Prediccion(
            provincia=data.get('provincia'),
            version=data.get('version'),
            id=data.get('id'),
            origen=data.get('origen'),
            elaborado=data.get('elaborado'),
            prediccion=prediccion,
            nombre=data.get('nombre'),
        )

    def ver(self):
        print('Provincia: {}'.format(self.provincia))
        print('Versión: {}'.format(self.version))
        print('ID: {}'.format(self.id))
        print('Origen: {}'.format(self.origen))
        print('Elaborado: {}'.format(self.elaborado))
        print('Predicción: {}'.format(self.prediccion[0].ver()))
        print('Nombre: {}'.format(self.nombre))

    def __str__(self):
        return '{} @ {}'.format(
            self.nombre,
            self.provincia
        )


class PrediccionDia:
    def __init__(self, uv_max=0, racha_max=(), fecha='', sens_termica=(), humedad_relativa=(),
                 temperatura=(), estado_cielo=(), cota_nieve_prov=(), viento=(), prob_precipitacion=()):
        self.uvMax = uv_max
        self.rachaMax = racha_max
        self.fecha = fecha
        self.sensTermica = sens_termica
        self.humedadRelativa = humedad_relativa
        self.temperatura = temperatura
        self.estadoCielo = estado_cielo
        self.cotaNieveProv = cota_nieve_prov
        self.viento = viento
        self.probPrecipitacion = prob_precipitacion

    @staticmethod
    def from_json(data):
        predicciones = []
        for dia in data.get('dia'):
            predicciones.append(
                PrediccionDia(
                    uv_max=dia.get('uvMax', []),
                    racha_max=dia.get('rachaMax', ()),
                    fecha=dia.get('fecha', ''),
                    sens_termica=dia.get('sensTermica', ()),
                    humedad_relativa=dia.get('humedadRelativa', ()),
                    temperatura=dia.get('temperatura', ()),
                    estado_cielo=dia.get('estadoCielo', ()),
                    cota_nieve_prov=dia.get('cotaNieveProv', ()),
                    viento=dia.get('viento', ()),
                    prob_precipitacion=dia.get('probPrecipitacion', ()),
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
        print('Estado del cielo: {}'.format(self.estadoCielo))
        print('Cota de nieve: {}'.format(self.cotaNieveProv))
        print('Viento: {}'.format(self.viento))
        print('Probabilidad de precipitación: {}'.format(self.probPrecipitacion))

    def get_temperatura_maxima(self):
        return self.temperatura.get('maxima')

    def get_temperatura_minima(self):
        return self.temperatura.get('minima')

    def __str__(self):
        return 'PrediccionDia @ {}'.format(
            self.fecha
        )


class PrediccionPorHoras:
    def __init__(self, estadoCielo=(), precipitacion=(), vientoAndRachaMax=(), ocaso='',
                 probTormenta=(), probPrecipitacion=(), orto='', humedadRelativa=(), nieve=(),
                 probNieve=(), fecha='', temperatura=(), sensTermica=()):
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
    def from_json(data):
        periodos = []
        for p in data.get('dia'):
            try:
                periodos.append(
                    PrediccionPorHoras(
                        estadoCielo=p.get('estadoCielo'),
                        precipitacion=p.get('precipitacion'),
                        vientoAndRachaMax=p.get('vientoAndRachaMax'),
                        ocaso=p.get('ocaso'),
                        probTormenta=p.get('probTormenta'),
                        probPrecipitacion=p.get('probPrecipitacion'),
                        orto=p.get('orto'),
                        humedadRelativa=p.get('humedadRelativa'),
                        nieve=p.get('nieve'),
                        probNieve=p.get('probNieve'),
                        fecha=p.get('fecha'),
                        temperatura=p.get('temperatura'),
                        sensTermica=p.get('sensTermica')
                    )
                )
            except KeyError:
                pass
        return periodos


class PrediccionMaritima:
    def __init__(self, origen=None, aviso=None, situacion=None, prediccion=None,
                 tendencia=(), id='', nombre='', tipo=TIPO_COSTERA):
        self.origen = origen
        self.aviso = aviso
        self.situacion = situacion
        self.prediccion = prediccion
        self.tendencia = tendencia
        self.id = id
        self.nombre = nombre
        self.tipo = tipo

    @staticmethod
    def from_json(data, tipo):
        if tipo == TIPO_COSTERA:
            aviso = data.get('aviso', '')
            tendencia = data('tendencia', '')
        else:
            aviso = None
            tendencia = None

        return PrediccionMaritima(
            origen=data.get('origen'),
            aviso=aviso,
            situacion=data.get('situacion'),
            prediccion=data.get('prediccion'),
            tendencia=tendencia,
            id=data.get('id'),
            nombre=data.get('nombre'),
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
    def from_json(data, multiple=False):
        if multiple:
            observaciones = []
            for o in data:
                observaciones.append(
                    Observacion(
                        idema=o.get('idema', ''),
                        lon=o.get('lon', ''),
                        lat=o.get('lat', ''),
                        fint=o.get('fint', ''),
                        prec=o.get('prec', ''),
                        alt=o.get('alt', ''),
                        vmax=o.get('vmax', ''),
                        vv=o.get('vv', ''),
                        dv=o.get('dv', ''),
                        dmax=o.get('dmax', ''),
                        ubi=o.get('ubi', ''),
                    )
                )
            return observaciones
        return Observacion(
            idema=data.get('idema', ''),
            lon=data.get('lon', ''),
            lat=data.get('lat', ''),
            fint=data.get('fint', ''),
            prec=data.get('prec', ''),
            alt=data.get('alt', ''),
            vmax=data.get('vmax', ''),
            vv=data.get('vv', ''),
            dv=data.get('dv', ''),
            dmax=data.get('dmax', ''),
            ubi=data.get('ubi', ''),
        )


class Municipio:
    with open(os.path.join(BASE_DIR, 'data', 'municipios.json')) as f:
        MUNICIPIOS = json.loads(f.read())

    def __init__(self, cod_auto, cpro, cmun, dc, nombre):
        self.cod_auto = cod_auto
        self.cpro = cpro
        self.cmun = cmun
        self.dc = dc
        self.nombre = nombre

    @staticmethod
    def from_json(data):
        return Municipio(
            cod_auto=data.get('CODAUTO', ''),
            cpro=data.get('CPRO', ''),
            cmun=data.get('CMUN', ''),
            dc=data.get('DC', ''),
            nombre=data.get('NOMBRE', '')
        )

    @staticmethod
    def get_municipio(id):
        municipio = list(filter(lambda m: id == '{}{}'.format(m.get('CPRO'), m.get('CMUN')), Municipio.MUNICIPIOS))[0]
        return Municipio.from_json(municipio)

    @staticmethod
    def buscar(nombre):
        """
        Devuelve una lista con los resultados de la búsqueda
        :param nombre: Nombre del municipio
        """
        try:
            municipios_raw = list(filter(lambda t: nombre in t.get('NOMBRE'), Municipio.MUNICIPIOS))
            municipios = list(map(lambda m: Municipio.from_json(m), municipios_raw))
            return municipios
        except:
            return None

    def get_codigo(self):
        return '{}{}'.format(self.cpro, self.cmun)

    def __str__(self):
        return '{}: {}'.format(self.nombre, self.get_codigo())


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
    def get_estaciones(api_key):
        """
        Devuelve un diccionario con la información de todas las estaciones
        """
        url = ESTACIONES_EMA_API_URL
        return Aemet(api_key=api_key).get_request_data(url, todos=True)

    @staticmethod
    def buscar_estacion(nombre, api_key):
        """
        Devuelve un array de Estaciones que contienen el nombre pasado por parámetro
        :param nombre: Nombre de la estación
        :param api_key: Clave API
        """
        nombre = nombre.upper()
        estaciones = Estacion.get_estaciones(api_key=api_key)
        estaciones = list(filter(lambda e: nombre in e.get('nombre'), estaciones))
        result = []
        for estacion in estaciones:
            result.append(
                Estacion(
                    altitud=estacion.get('altitud'),
                    indicativo=estacion.get('indicativo'),
                    provincia=estacion.get('provincia'),
                    longitud=estacion.get('longitud'),
                    nombre=estacion.get('nombre'),
                    latitud=estacion.get('latitud'),
                    indsinop=estacion.get('indsinop'),
                )
            )
        return result

class AemetHttpClient(object):
    def __init__(self, api_key=API_KEY, api_key_file='', headers=dict(), querystring=dict(), verbose=False):
        if not api_key and not api_key_file:
            raise Exception('Tienes que añadir una clave de API')

        if api_key_file:
            with open(api_key_file) as f:
                api_key = f.read().strip()

        self.api_key = api_key
        self.querystring = querystring
        self.headers = headers
        self.verbose = verbose

    def get_api_key(self):
        return self.api_key

    def set_api_key(self, api_key):
        self.api_key = api_key

    def get_querystring(self):
        return self.querystring

    def set_querystring(self, querystring):
        self.querystring = querystring

    def get_headers(self):
        return {
            'api_key': self.get_api_key(),
            **self.headers
        }

    def set_headers(self, headers):
        self.headers = headers

    @staticmethod
    def guardar_clave_api():
        api_key = input('Escriba su clave de API: ')
        if not api_key:
            raise Exception('La clave de API no puede estar vacía')

        with open(API_KEY_FILE, 'w') as f:
            f.write(api_key)

        print('Clave de API almacenada en {}'.format(API_KEY_FILE))

    def get_request_data(self, url, todos=False):
        """
        Returns the JSON formatted request data
        """
        if self.verbose:
            print(url)

        r = requests.get(
            url,
            headers=self.get_headers(),
            params=self.get_querystring(),
            verify=False  # Avoid SSL Verification .__.
        )

        if r.status_code != 200:
            raise Exception(f'Error {r.json()}')

        url = r.json().get('datos')

        if not url:
            return r.json()

        if self.verbose:
            print(url)

        r = requests.get(url, verify=False)

        if todos:
            return r.json()

        try:
            return r.json()[0]
        except IndexError:
            return r.json()

        return r.json()

    def get_request_normalized_data(self, url):
        """
        Return the request raw content data
        """
        if self.verbose:
            print(url)
        r = requests.get(
            url,
            headers=self.get_headers(),
            params=self.get_querystring(),
            verify=False  # Avoid SSL Verification .__.
        )
        if r.status_code == 200:
            r = requests.get(r.json().get('datos'), verify=False)
            data = r.text
            return data
        return {
            'error': r.status_code
        }

    def download_file_from_url(self, url, out_file):
        """
        Creates a new file with the content of the image response from an url
        :param url: The URL
        :param out_file: Image filename
        """
        if self.verbose:
            print('Downloading from {}...'.format(url))
        r = requests.get(
            url,
            params=self.get_querystring(),
            headers=self.get_headers(),
            verify=False
        )
        try:
            error = r.json().get('estado')
            return {
                'error': error
            }
        except KeyError:
            data = r.content
            with open(out_file, 'wb') as f:
                f.write(data)
            return {
                'status': 200,
                'out_file': out_file
            }

    def download_image_from_url(self, url, out_file):
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
                params=self.get_querystring(),
                headers=self.get_headers(),
                verify=False
            )
            error = ''
            img_url = r.json().get('datos')
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
            return {'status': r.json().get('estado', 'error')}
        return {
            'status': 200,
            'out_file': out_file
        }


class Aemet(AemetHttpClient):
    def get_fecha_hoy(self):
        """
        Devuelve la fecha formateada en el formato que acepta AEMET
        """
        print(datetime.now())
        return '{:%Y-%m-%d}'.format(datetime.now())

    def get_archivo_codigos_idema(self, archivo_salida):
        """
        Crea un archivo json con todos los registros de estaciones de IDEMA
        :param archivo_salida: Nombre del archivo de salida
        """
        url = OBSERVACION_CONVENCIONAL_API_URL
        estaciones = self.get_request_data(url, todos=True)
        data = {estacion.get('idema'): estacion.get('ubi') for estacion in estaciones}
        with open(archivo_salida, 'w') as f:
            f.write(json.dumps(data, indent=4))

    def get_municipio(self, id_municipio):
        url = MUNICIPIOS_DETALLE_API_URL.format(id_municipio)
        r = requests.get(
            url,
            params={
                'api_key': self.api_key
            },
            headers=self.headers,
            verify=False
        )
        data = r.json()
        return data

    def get_prediccion(self, codigo_municipio, periodo=PERIODO_SEMANA, raw=False):
        """
        Devuelve un objeto de la clase Prediccion dado un código de municipio y
        un periodo de consulta.
        :param codigo_municipio: Código del municipio
        :param periodo: Periodo de tiempo a consultar, determinado por las constantes PERIODO_SEMANA (p.d.) y PERIODO_DIA
        :param raw: [Opcional] Devolver el resultado en formato json
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
        data = self.get_request_data(url)
        if raw:
            return data
        return Prediccion.from_json(data, periodo)

    def get_prediccion_normalizada(self, ambito=NACIONAL, dia=HOY, ccaa='',
                                   provincia='', fecha_elaboracion=''):
        """
        Devuelve el texto elaborado por AEMET de la predicción meteorológica para
        un determinado ámbito, día, Comunidad Autónoma, provincia y/o fecha de elaboración.
        :param ambito: Ámbito a consultar para la predicción (Constantes NACIONAL (p.d.), CCAA, PROVINCIA)
        :param dia: Día a consultar (Constantes HOY (p.d.), MANANA, PASADO_MANANA)
        :param ccaa: ID de la Comunidad Autónoma
        :param provincia: ID de la provincia
        :param fecha_elaboracion: Fecha de elaboración de la predicción
        """
        if ccaa and provincia:
            raise Exception('No puedes establecer un valor de "provincia" y de "ccaa" a la vez')
        if (ccaa or provincia) and ambito == NACIONAL:
            raise Exception('No puedes especificar una "provincia" o "ccaa" cuando "ambito=NACIONAL"')
        url = PREDICCION_NORMALIZADA_API_URL.format(ambito, dia, ccaa + provincia)
        if fecha_elaboracion:
            url += 'elaboracion/{}/'.format(fecha_elaboracion)
        return self.get_request_normalized_data(url)

    def get_prediccion_especifica_montanya(self, area, dia=-1, raw=False):
        """
        Predicción meteorológica para la zona montañosa que se pasa como parámetro
        (area) con validez para el día (día). Periodicidad de actualización: continuamente
        :param area: Área de consulta
        :param dia: [Opcional] Día a consultar (0, +1, +2, +3)
        :param raw: [Opcional] Devolver el resultado en formato json
        """
        if dia == -1:
            url = PREDICCION_ESPECIFICA_MONTANYA_API_URL.format(area)
        else:
            url = PREDICCION_ESPECIFICA_MONTANYA_DIA_API_URL.format(area, dia)
        data = self.get_request_data(url)
        if raw:
            return data
        # TODO
        return data

    def get_prediccion_nivologica(self, area):
        """
        Información nivológica para la zona montañosa que se pasa como parámetro (area)
        :param area: Área de consulta (0: Pirineo Catalán 1: Pirineo Navarro y Aragonés)
        """
        if area != 0 and area != 1:
            raise Exception('Error: Área no válida (0, 1)')
        url = PREDICCION_NIVOLOGICA_API_URL.format(area)
        return self.get_request_normalized_data(url)

    def get_prediccion_especifica_playa(self, playa, raw=False):
        """
        La predicción diaria de la playa que se pasa como parámetro.
        Establece el estado de nubosidad para unas horas determinadas, las 11 y
        las 17 hora oficial. Se analiza también si se espera precipitación en
        el entorno de esas horas, entre las 08 y las 14 horas y entre las 14 y 20 horas.
        :param playa: ID de la playa
        :param raw: [Opcional] Devuelve el resultado en formato json
        """
        url = PREDICCION_ESPECIFICA_PLAYA_API_URL.format(playa)
        data = self.get_request_data(url)
        if raw:
            return data
        # TODO
        return data

    def get_prediccion_especifica_uvi(self, dia=0):
        """
        Predicción de Índice de radiación UV máximo en condiciones de cielo
        despejado para el día seleccionado.
        :param dia: Día de consulta (0, 1, 2, 3, 4)
        """
        url = PREDICCION_ESPECIFICA_UVI_API_URL.format(dia)
        return self.get_request_normalized_data(url)

    def get_observacion_convencional(self, estacion='', raw=False):
        """
        Devuelve un objeto de la clase Observacion con los datos de la consulta
        sobre una estación
        :param estacion: [Opcional] Id de la estación a consultar. Por defecto, estación de Madrid
        :param raw: [Opcional] Devuelve el resultado en formato json
        """
        if estacion:
            url = OBSERVACION_CONVENCIONAL_ESTACION_API_URL.format(estacion)
            data = self.get_request_data(url)
            if raw:
                return data
            return Observacion.from_json(data)
        else:
            url = OBSERVACION_CONVENCIONAL_API_URL
            data = self.get_request_data(url, todos=True)
            if raw:
                return data
            return Observacion.from_json(data, multiple=True)

    def get_valores_climatologicos_mensuales(self, anyo, estacion, raw=False):
        """
        Devuelve un diccionario con la información de todas las estaciones
        :param anyo: Año de consulta
        :param estacion: ID de estación de IDEMA
        :param raw: [Opcional] Devuelve el resultado en formato json
        """
        url = VALORES_CLIMATOLOGICOS_MENSUALES.format(anyo, anyo, estacion)
        data = self.get_request_data(url, todos=True)
        if raw:
            return data
        # TODO
        return data

    def get_valores_climatologicos_diarios(self, fechaini, fechafin, estacion, raw=False):
        """
        Devuelve un diccionario con la información de todas las estaciones
        :param fechaini: Fecha inicio consulta
        :param fechafin: Fecha fin consulta
        :param estacion: ID de estación de IDEMA
        :param raw: [Opcional] Devuelve el resultado en formato json
        """
        url = VALORES_CLIMATOLOGICOS_DIARIOS.format(fechaini, fechafin, estacion)
        data = self.get_request_data(url, todos=True)
        if raw:
            return data
        # TODO
        return data

    def get_contaminacion_fondo(self, estacion):
        # TODO
        url = CONTAMINACION_FONDO_ESTACION_API_URL.format(estacion)
        data = self.get_request_normalized_data(url).splitlines()
        return data

    def get_prediccion_maritima(self, tipo=TIPO_COSTERA, costa='', area='', raw=False):
        """
        Devuelve un objeto de la clase PrediccionMaritima dado un tipo de predicción
        (TIPO_COSTERA por defecto o TIPO_ALTA_MAR) y un valor de costa o un valor de área
        :param tipo: Si es de COSTA o de ALTA MAR (definidos por las constantes TIPO_COSTERA y TIPO_ALTA_MAR)
        :param costa: Id de la costa
        :param area: Id del área
        :param raw: [Opcional] Devuelve el resultado en formato json
        """
        if tipo == TIPO_COSTERA:
            if not costa:
                raise Exception('Es obligatorio utilizar el parámetro "costa"')
            url = PREDICCION_MARITIMA_COSTERA_API_URL.format(costa)
        elif tipo == TIPO_ALTA_MAR:
            if not area:
                raise Exception('Es obligatorio utilizar el parámetro "area"')
            url = PREDICCION_MARITIMA_ALTA_MAR_API_URL.format(area)
        else:
            raise Exception('Error: "tipo" no válido')

        data = self.get_request_data(url)
        if raw:
            return data
        return PrediccionMaritima.from_json(data, tipo)

    def get_valores_climatologicos_normales(self, estacion, raw=False):
        """
        Valores climatológicos normales (periodo 1981-2010) para la estación pasada por parámetro.
        Periodicidad: 1 vez al día.
        :param estacion: ID de la estación de IDEMA
        :param raw: [Opcional] Devuelve el resultado en formato json
        """
        url = VALORES_CLIMATOLOGICOS_NORMALES.format(estacion)
        data = self.get_request_data(url)
        if raw:
            return data
        # TODO
        return data

    def get_valores_climatologicos_extremos(self, estacion, parametro=VCP):
        """
        Valores extremos para la estación y la variable (precipitación, temperatura y viento) pasadas por parámetro.
        Periodicidad: 1 vez al día.
        :param estacion: ID de la estación de IDEMA
        :param parametro: Valores de las constantes (VCP, VCT, VCV)
        """
        url = VALORES_CLIMATOLOGICOS_EXTREMOS.format(parametro, estacion)
        return self.get_request_data(url)

    def descargar_mapa_analisis(self, archivo_salida):
        """
        Descarga una imagen con el mapa de análisis
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        """
        url = MAPA_ANALISIS_API_URL
        return self.download_image_from_url(url, archivo_salida)

    def descargar_mapas_significativos(
            self, archivo_salida, fecha='',
            ambito='esp', dia=MAPAS_SIGNIFICATIVOS_DIAS.get('HOY_0_12')):
        """
        Descarga una imagen con los mapas significativos
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        :param fecha: Fecha
        :param ambito: Código de Comunidad Autónoma o de España
        :param dia: Código para fecha determinada [a, b, c, d, e, f]
        Ver MAPAS_SIGNIFICATIVOS_DIAS
        """
        if fecha:
            url = MAPAS_SIGNIFICATIVOS_FECHA_API_URL.format(fecha, ambito, dia)
        else:
            url = MAPAS_SIGNIFICATIVOS_API_URL.format(ambito, dia)
        return self.download_image_from_url(url, archivo_salida)

    def descargar_mapa_riesgo_previsto_incendio(
            self, archivo_salida, dia=INCENDIOS_MANANA, area=PENINSULA):
        """
        Descarga una imagen con el mapa del riesgo previsto de incendio
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        :param dia: Día de consulta (+1, +2, +3)
        :param area: [Opcional] Área consultada (PENINSULA, BALEARES o CANARIAS)
        """
        url = MAPA_RIESGO_INCENDIOS_PREVISTO.format(dia, area)
        return self.download_image_from_url(url, archivo_salida)

    def descargar_mapa_riesgo_estimado_incendio(self, archivo_salida, area=PENINSULA):
        """
        Descarga una imagen con el mapa del riesgo estimado de incendio
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        :param area: [Opcional] Área consultada (PENINSULA, BALEARES o CANARIAS)
        """
        url = MAPA_RIESGO_INCENDIOS_ESTIMADO.format(area)
        return self.download_image_from_url(url, archivo_salida)

    def descargar_mapa_radar_nacional(self, archivo_salida):
        """
        Descarga una imagen con el mapa del radar por región
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        """
        url = RADAR_NACIONAL_API_URL
        return self.download_image_from_url(url, archivo_salida)

    def descargar_mapa_radar_regional(self, archivo_salida, region):
        """
        Descarga una imagen con el mapa del radar por región
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        :param region: Región consultada
        """
        url = RADAR_REGIONAL_API_URL.format(region)
        return self.download_image_from_url(url, archivo_salida)

    def descargar_mapa_rayos(self, archivo_salida):
        """
        Descarga una imagen con el mapa de rayos a nivel nacional
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        """
        url = MAPA_RAYOS_API_URL
        return self.download_image_from_url(url, archivo_salida)

    def descargar_mapa_satelite_sst(self, archivo_salida):
        """
        Descarga una imagen con el mapa del satélite (SST)
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        """
        url = SATELITE_SST
        return self.download_image_from_url(url, archivo_salida)

    def descargar_mapa_satelite_nvdi(self, archivo_salida):
        """
        Descarga una imagen con el mapa del satélite (NVDI)
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        """
        url = SATELITE_NVDI
        return self.download_image_from_url(url, archivo_salida)

    def descargar_productos_climatologicos(self, archivo_salida, anyo, decena):
        """
        Se obtiene, para la decema y el año pasados por parámetro, el Boletín
        Hídrico Nacional que se elabora cada diez días. Se presenta información
        resumida de forma distribuida para todo el territorio nacional de
        diferentes variables, en las que se incluye informaciones de la
        precipitación y la evapotranspiración potencial acumuladas desde el 1 de septiembre.
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        :param anyo: Año de consulta
        :param decena: Número de la decena de días que se va a consultar
        """
        if decena < 1 or decena > 36:
            raise Exception('Error: La decena tiene que ser un número entre 1 y 36')
        if decena < 10:
            decena = '0' + str(decena)
        url = PRODUCTOS_CLIMATOLOGICOS_API_URL.format(anyo, decena)
        return self.download_file_from_url(url, archivo_salida)

    def descargar_resumen_mensual_climatologico(self, archivo_salida, anyo, mes):
        """
        Resumen climatológico nacional, para el año y mes pasado por parámetro,
        sobre el estado del clima y la evolución de las principales variables
        climáticas, en especial temperatura y precipitación, a nivel mensual, estacional y anual.
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        :param anyo: Año de consulta
        :param mes: Mes de consulta
        """
        if mes < 1 or mes > 12:
            raise Exception('Error: Debes establecer un número de mes válido (1-12)')
        url = RESUMEN_CLIMATOLOGICO_MENSUAL_API_URL.format(anyo, mes)
        return self.download_file_from_url(url, archivo_salida)
