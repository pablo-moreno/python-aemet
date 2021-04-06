# Casos de uso de `python-aemet`

## Requisitos previos

### Instalar la librería `python-aemet`

- Tener `python3` instalado en el sistema: `which python`

- Instalar la librería en el local. Recomendamos el uso de un `virtualenv` o un gestor
de entornos como `pyenv`.

  Instala la librería

  ```bash
  pip install python-aemet
  ```

### Obtener la clave API

Obtén tu clave de API en la siguiente URL:

<https://opendata.aemet.es/centrodedescargas/obtencionAPIKey>

Y ponla en un fichero `aemet.key`

## Casos de uso

### Predicción de la temperatura máxima y mínima en un municipio concreto en los próximos días

```bash
aemet -p Huelva -f /path/a/la/clave/aemet.key
```

La salida:

```sh
Predicción de temperaturas para Huelva:

2021-04-04T00:00:00
Máxima: 23
Mínima: 12

2021-04-05T00:00:00
Máxima: 22
Mínima: 13

2021-04-06T00:00:00
Máxima: 25
Mínima: 11

2021-04-07T00:00:00
Máxima: 25
Mínima: 13

2021-04-08T00:00:00
Máxima: 23
Mínima: 12

2021-04-09T00:00:00
Máxima: 21
Mínima: 12

2021-04-10T00:00:00
Máxima: 21
Mínima: 13
```
