import os
from pathlib import Path

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = str(Path.home())
AEMET_DIR = os.path.join(HOME_DIR, '.aemet')

if not os.path.exists(AEMET_DIR):
    # Create ~/.aemet config dir
    os.mkdir(os.path.join(HOME_DIR, '.aemet'))
API_KEY_FILE = os.path.join(HOME_DIR, '.aemet', 'api.key')
try:
    API_KEY = open(API_KEY_FILE, 'r').read().strip()
except:
    API_KEY = ''

# Endpoints
BASE_URL = 'https://opendata.aemet.es/opendata/api'
MUNICIPIOS_API_URL = BASE_URL + '/maestro/municipios/'
MUNICIPIOS_DETALLE_API_URL = BASE_URL + '/maestro/municipio/{}'  # id
PREDICCION_SEMANAL_API_URL = BASE_URL + '/prediccion/especifica/municipio/diaria/'
PREDICCION_POR_HORAS_API_URL = BASE_URL + '/prediccion/especifica/municipio/horaria/'
PREDICCION_NORMALIZADA_API_URL = BASE_URL + '/prediccion/{}/{}/{}'
PREDICCION_MARITIMA_ALTA_MAR_API_URL = BASE_URL + '/prediccion/maritima/altamar/area/{}'
PREDICCION_MARITIMA_COSTERA_API_URL = BASE_URL + '/prediccion/maritima/costera/costa/{}'
PREDICCION_ESPECIFICA_MONTANYA_API_URL = BASE_URL + '/prediccion/especifica/montaña/pasada/area/{}'
PREDICCION_ESPECIFICA_MONTANYA_DIA_API_URL = BASE_URL + '/prediccion/especifica/montaña/pasada/area/{}/dia/{}'
PREDICCION_ESPECIFICA_PLAYA_API_URL = BASE_URL + '/prediccion/especifica/playa/{}/'
PREDICCION_ESPECIFICA_UVI_API_URL = BASE_URL + '/prediccion/especifica/uvi/{}'
PREDICCION_NIVOLOGICA_API_URL = BASE_URL + '/prediccion/especifica/nivologica/{}'  # 0 / 1
ESTACIONES_EMA_API_URL = BASE_URL + '/valores/climatologicos/inventarioestaciones/todasestaciones'
VALORES_CLIMATOLOGICOS_NORMALES = BASE_URL + '/valores/climatologicos/normales/estacion/{}'
VALORES_CLIMATOLOGICOS_EXTREMOS = BASE_URL + '/valores/climatologicos/valoresextremos/parametro/{}/estacion/{}'
VALORES_CLIMATOLOGICOS_MENSUALES = BASE_URL + '/valores/climatologicos/mensualesanuales/datos/anioini/{}/aniofin/{}/estacion/{}'
VALORES_CLIMATOLOGICOS_DIARIOS = BASE_URL + '/valores/climatologicos/diarios/datos/fechaini/{}/fechafin/{}/estacion/{}'
PRODUCTOS_CLIMATOLOGICOS_API_URL = BASE_URL + '/productos/climatologicos/balancehidrico/{}/{}/'
RESUMEN_CLIMATOLOGICO_MENSUAL_API_URL = BASE_URL + '/productos/climatologicos/resumenclimatologico/nacional/{}/{}/'
OBSERVACION_CONVENCIONAL_API_URL = BASE_URL + '/observacion/convencional/todas/'
OBSERVACION_CONVENCIONAL_ESTACION_API_URL = BASE_URL + '/observacion/convencional/datos/estacion/{}/'
MAPA_RIESGO_INCENDIOS_ESTIMADO = BASE_URL + '/incendios/mapasriesgo/estimado/area/{}'
MAPA_RIESGO_INCENDIOS_PREVISTO = BASE_URL + '/incendios/mapasriesgo/previsto/dia/{}/area/{}'
MAPA_ANALISIS_API_URL = BASE_URL + '/mapasygraficos/analisis/'
MAPAS_SIGNIFICATIVOS_FECHA_API_URL = BASE_URL + '/mapasygraficos/mapassignificativos/fecha/{}/{}/{}/'
MAPAS_SIGNIFICATIVOS_API_URL = BASE_URL + '/mapasygraficos/mapassignificativos/{}/{}/'
MAPA_RAYOS_API_URL = BASE_URL + '/red/rayos/mapa/'
RADAR_NACIONAL_API_URL = BASE_URL + '/red/radar/nacional'
RADAR_REGIONAL_API_URL = BASE_URL + '/red/radar/regional/{}'
SATELITE_SST = BASE_URL + '/satelites/producto/sst/'
SATELITE_NVDI = BASE_URL + '/satelites/producto/nvdi/'
CONTAMINACION_FONDO_ESTACION_API_URL = BASE_URL + '/red/especial/contaminacionfondo/estacion/{}/'

# Params
MAPAS_SIGNIFICATIVOS_DIAS = {
    'HOY_0_12': 'a',
    'HOY_12_24': 'b',
    'MANANA_0_12': 'c',
    'MANANA_12_24': 'd',
    'PASADO_MANANA_0_12': 'e',
    'PASADO_MANANA_12_24': 'f'
}
VCP, VCT, VCV = 'P', 'T', 'V'
TIPO_COSTERA, TIPO_ALTA_MAR = 'costera', 'altamar'
PERIODO_SEMANA, PERIODO_DIA = 'PERIODO_SEMANA', 'PERIODO_DIA'
INCENDIOS_MANANA, INCENDIOS_PASADO_MANANA, INCENDIOS_EN_3_DIAS = range(1, 4)
PENINSULA, CANARIAS, BALEARES = 'p', 'c', 'b'
NACIONAL, CCAA, PROVINCIA = 'nacional', 'ccaa', 'provincia'
HOY, MANANA, PASADO_MANANA, MEDIO_PLAZO, TENDENCIA = 'hoy', 'manana', 'pasadomanana', 'medioplazo', 'tendencia'
