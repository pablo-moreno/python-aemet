from aemet import *

aemet = Aemet(verbose=True)
aemet.descargar_mapa_rayos('rayos.jpg')
aemet.descargar_mapa_analisis('analisis.jpg')
aemet.descargar_mapa_satelite_sst('satelite-sst.jpg')
aemet.descargar_mapa_satelite_nvdi('satelite-nvdi.jpg')
aemet.descargar_mapa_radar_nacional('radar-nacional.jpg')
aemet.descargar_mapa_radar_regional('radar-regional.jpg', region='cc')
aemet.descargar_mapas_significativos('mapas-significativos.jpg')
aemet.descargar_mapa_riesgo_previsto_incendio('riesgo-incendios-previsto.jpg')
aemet.descargar_mapa_riesgo_estimado_incendio('riesgo-incendios-estimado.jpg')
