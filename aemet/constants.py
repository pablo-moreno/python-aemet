BASE_URL = 'https://opendata.aemet.es/opendata/api/'
API_KEY = open('api.key', 'r').read().strip()
WEEKLY_PREDICTION_API_URL = 'prediccion/especifica/municipio/diaria/'
DAILY_PREDICTION_API_URL = 'prediccion/especifica/municipio/horaria/'
PERIOD_WEEKLY = 0
PERIOD_DAILY = 1
TOWN_API_URL = 'maestro/municipios/'
