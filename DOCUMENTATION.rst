Module aemet.models
===================

Classes
-------

`Aemet(api_key='', api_key_file='', headers={}, querystring={}, verbose=False)`
:

    ### Ancestors (in MRO)

    * aemet.models.AemetHttpClient

    ### Methods

    `descargar_mapa_analisis(self, archivo_salida)`
    :   Descarga una imagen con el mapa de análisis
        :param archivo_salida: Nombre del archivo en el que se va a guardar

    `descargar_mapa_radar_nacional(self, archivo_salida)`
    :   Descarga una imagen con el mapa del radar por región
        :param archivo_salida: Nombre del archivo en el que se va a guardar

    `descargar_mapa_radar_regional(self, archivo_salida, region)`
    :   Descarga una imagen con el mapa del radar por región
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        :param region: Región consultada

    `descargar_mapa_rayos(self, archivo_salida)`
    :   Descarga una imagen con el mapa de rayos a nivel nacional
        :param archivo_salida: Nombre del archivo en el que se va a guardar

    `descargar_mapa_riesgo_estimado_incendio(self, archivo_salida, area='p')`
    :   Descarga una imagen con el mapa del riesgo estimado de incendio
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        :param area: [Opcional] Área consultada (PENINSULA, BALEARES o CANARIAS)

    `descargar_mapa_riesgo_previsto_incendio(self, archivo_salida, dia=1, area='p')`
    :   Descarga una imagen con el mapa del riesgo previsto de incendio
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        :param dia: Día de consulta (+1, +2, +3)
        :param area: [Opcional] Área consultada (PENINSULA, BALEARES o CANARIAS)

    `descargar_mapa_satelite_nvdi(self, archivo_salida)`
    :   Descarga una imagen con el mapa del satélite (NVDI)
        :param archivo_salida: Nombre del archivo en el que se va a guardar

    `descargar_mapa_satelite_sst(self, archivo_salida)`
    :   Descarga una imagen con el mapa del satélite (SST)
        :param archivo_salida: Nombre del archivo en el que se va a guardar

    `descargar_mapas_significativos(self, archivo_salida, fecha='', ambito='esp', dia='a')`
    :   Descarga una imagen con los mapas significativos
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        :param fecha: Fecha
        :param ambito: Código de Comunidad Autónoma o de España
        :param dia: Código para fecha determinada [a, b, c, d, e, f]
        Ver MAPAS_SIGNIFICATIVOS_DIAS

    `descargar_productos_climatologicos(self, archivo_salida, anyo, decena)`
    :   Se obtiene, para la decema y el año pasados por parámetro, el Boletín
        Hídrico Nacional que se elabora cada diez días. Se presenta información
        resumida de forma distribuida para todo el territorio nacional de
        diferentes variables, en las que se incluye informaciones de la
        precipitación y la evapotranspiración potencial acumuladas desde el 1 de septiembre.
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        :param anyo: Año de consulta
        :param decena: Número de la decena de días que se va a consultar

    `descargar_resumen_mensual_climatologico(self, archivo_salida, anyo, mes)`
    :   Resumen climatológico nacional, para el año y mes pasado por parámetro,
        sobre el estado del clima y la evolución de las principales variables
        climáticas, en especial temperatura y precipitación, a nivel mensual, estacional y anual.
        :param archivo_salida: Nombre del archivo en el que se va a guardar
        :param anyo: Año de consulta
        :param mes: Mes de consulta

    `get_archivo_codigos_idema(self, archivo_salida)`
    :   Crea un archivo json con todos los registros de estaciones de IDEMA
        :param archivo_salida: Nombre del archivo de salida

    `get_contaminacion_fondo(self, estacion)`
    :

    `get_fecha_hoy(self)`
    :   Devuelve la fecha formateada en el formato que acepta AEMET

    `get_municipio(self, id_municipio)`
    :

    `get_observacion_convencional(self, estacion='', raw=False)`
    :   Devuelve un objeto de la clase Observacion con los datos de la consulta
        sobre una estación
        :param estacion: [Opcional] Id de la estación a consultar. Por defecto, estación de Madrid
        :param raw: [Opcional] Devuelve el resultado en formato json

    `get_prediccion(self, codigo_municipio, periodo='PERIODO_SEMANA', raw=False)`
    :   Devuelve un objeto de la clase Prediccion dado un código de municipio y
        un periodo de consulta.
        :param codigo_municipio: Código del municipio
        :param periodo: Periodo de tiempo a consultar, determinado por las constantes PERIODO_SEMANA (p.d.) y PERIODO_DIA
        :param raw: [Opcional] Devolver el resultado en formato json

    `get_prediccion_especifica_montanya(self, area, dia=-1, raw=False)`
    :   Predicción meteorológica para la zona montañosa que se pasa como parámetro
        (area) con validez para el día (día). Periodicidad de actualización: continuamente
        :param area: área de consulta
        :param dia: [Opcional] Día a consultar (0, +1, +2, +3)
        :param raw: [Opcional] Devolver el resultado en formato json

    `get_prediccion_especifica_playa(self, playa, raw=False)`
    :   La Predicción diaria de la playa que se pasa como parámetro.
        Establece el estado de nubosidad para unas horas determinadas, las 11 y
        las 17 hora oficial. Se analiza también si se espera precipitación en
        el entorno de esas horas, entre las 08 y las 14 horas y entre las 14 y 20 horas.
        :param playa: ID de la playa
        :param raw: [Opcional] Devuelve el resultado en formato json

    `get_prediccion_especifica_uvi(self, dia=0)`
    :   Predicción de índice de radiación UV máximo en condiciones de cielo
        despejado para el día seleccionado.
        :param dia: Día de consulta (0, 1, 2, 3, 4)

    `get_prediccion_maritima(self, tipo='costera', costa='', area='', raw=False)`
    :   Devuelve un objeto de la clase PrediccionMaritima dado un tipo de Predicción
        (TIPO_COSTERA por defecto o TIPO_ALTA_MAR) y un valor de costa o un valor de área
        :param tipo: Si es de COSTA o de ALTA MAR (definidos por las constantes TIPO_COSTERA y TIPO_ALTA_MAR)
        :param costa: Id de la costa
        :param area: Id del área
        :param raw: [Opcional] Devuelve el resultado en formato json

    `get_prediccion_nivologica(self, area)`
    :   Información nivológica para la zona montañosa que se pasa como parámetro (area)
        :param area: área de consulta (0: Pirineo Catalán 1: Pirineo Navarro y Aragonés)

    `get_prediccion_normalizada(self, ambito='nacional', dia='hoy', ccaa='', provincia='', fecha_elaboracion='')`
    :   Devuelve el texto elaborado por AEMET de la Predicción meteorológica para
        un determinado ámbito, día, Comunidad Autónoma, provincia y/o fecha de elaboración.
        :param ambito: ámbito a consultar para la Predicción (Constantes NACIONAL (p.d.), CCAA, PROVINCIA)
        :param dia: Día a consultar (Constantes HOY (p.d.), MANANA, PASADO_MANANA)
        :param ccaa: ID de la Comunidad Autónoma
        :param provincia: ID de la provincia
        :param fecha_elaboracion: Fecha de elaboración de la Predicción

    `get_valores_climatologicos_extremos(self, estacion, parametro='P')`
    :   Valores extremos para la estación y la variable (precipitación, temperatura y viento) pasadas por parámetro.
        Periodicidad: 1 vez al día.
        :param estacion: ID de la estación de IDEMA
        :param parametro: Valores de las constantes (VCP, VCT, VCV)

    `get_valores_climatologicos_mensuales(self, anyo, estacion, raw=False)`
    :   Devuelve un diccionario con la información de todas las estaciones
        :param anyo: Año de consulta
        :param estacion: ID de estación de IDEMA
        :param raw: [Opcional] Devuelve el resultado en formato json

    `get_valores_climatologicos_normales(self, estacion, raw=False)`
    :   Valores climatológicos normales (periodo 1981-2010) para la estación pasada por parámetro.
        Periodicidad: 1 vez al día.
        :param estacion: ID de la estación de IDEMA
        :param raw: [Opcional] Devuelve el resultado en formato json

`AemetHttpClient(api_key='', api_key_file='', headers={}, querystring={}, verbose=False)`
:

    ### Descendants

    * aemet.models.Aemet

    ### Static methods

    `guardar_clave_api()`
    :

    ### Methods

    `download_file_from_url(self, url, out_file)`
    :   Creates a new file with the content of the image response from an url
        :param url: The URL
        :param out_file: Image filename

    `download_image_from_url(self, url, out_file)`
    :   Creates a new file with the content of the image response from an url
        :param url: The URL
        :param out_file: Image filename

    `get_api_key(self)`
    :

    `get_headers(self)`
    :

    `get_querystring(self)`
    :

    `get_request_data(self, url, todos=False)`
    :   Returns the JSON formatted request data

    `get_request_normalized_data(self, url)`
    :   Return the request raw content data

    `set_api_key(self, api_key)`
    :

    `set_headers(self, headers)`
    :

    `set_querystring(self, querystring)`
    :

`Estacion(altitud, indicativo, provincia, longitud, nombre, latitud, indsinop)`
:

    ### Static methods

    `buscar_estacion(nombre, api_key)`
    :   Devuelve un array de Estaciones que contienen el nombre pasado por parámetro
        :param nombre: Nombre de la estación
        :param api_key: Clave API

    `get_estaciones(api_key)`
    :   Devuelve un diccionario con la información de todas las estaciones

`Municipio(cod_auto, cpro, cmun, dc, nombre)`
:

    ### Class variables

    `MUNICIPIOS`
    :

    `f`
    :

    ### Static methods

    `buscar(nombre)`
    :   Devuelve una lista con los resultados de la búsqueda
        :param nombre: Nombre del municipio

    `from_json(data)`
    :

    `get_municipio(id)`
    :

    ### Methods

    `get_codigo(self)`
    :

`Observacion(idema, lon, lat, fint, prec, alt, vmax, vv, dv, dmax, ubi)`
:

    ### Static methods

    `from_json(data, multiple=False)`
    :

`Prediccion(provincia, version, id, origen, elaborado, prediccion, nombre)`
:

    ### Static methods

    `from_json(data, periodo)`
    :

    ### Methods

    `ver(self)`
    :

`PrediccionDia(uv_max=0, racha_max=(), fecha='', sens_termica=(), humedad_relativa=(), temperatura=(), estado_cielo=(), cota_nieve_prov=(), viento=(), prob_precipitacion=())`
:

    ### Static methods

    `from_json(data)`
    :

    ### Methods

    `get_temperatura_maxima(self)`
    :

    `get_temperatura_minima(self)`
    :

    `ver(self)`
    :

`PrediccionMaritima(origen=None, aviso=None, situacion=None, prediccion=None, tendencia=(), id='', nombre='', tipo='costera')`
:

    ### Static methods

    `from_json(data, tipo)`
    :

`PrediccionPorHoras(estadoCielo=(), precipitacion=(), vientoAndRachaMax=(), ocaso='', probTormenta=(), probPrecipitacion=(), orto='', humedadRelativa=(), nieve=(), probNieve=(), fecha='', temperatura=(), sensTermica=())`
:

    ### Static methods

    `from_json(data)`
    :

