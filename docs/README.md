# Casos de uso de `python-aemet`

## Requisitos previos

### Instalar la librería `python-aemet`

- Tener `python3` instalado en el sistema: `which python`

- Instalar la librería en el local. Recomendamos el uso de un `virtualenv`.

   E.g. Instala `virtualenv`:

   ```bash
   pip install virtualenv
   ```

  Clona el repo `git clone git@github.com:pablo-moreno/python-aemet.git && cd python-aemet`

  Activa el `virtualenv`:

  ```bash
  virtualenv .venv
  source .venv/bin/activate
  ```

  Instala la librería

  ```bash
  pip install .
  ```

### Obtener la clave API

Obtén tu clave de API en la siguiente URL:

<https://opendata.aemet.es/centrodedescargas/obtencionAPIKey>

Y ponla en un fichero `aemet.key`

## Casos de uso

### Predicción de la temperatura máxima y mínima en un municipio concreto en los próximos días

```bash
aemet -p Madrid -f /path/a/la/clave/aemet.key
```

La salida:

```sh
Predicción de temperaturas para Madrid:

2021-04-03T00:00:00
Máxima: 20
Mínima: 10

2021-04-04T00:00:00
Máxima: 20
Mínima: 7

2021-04-05T00:00:00
Máxima: 22
Mínima: 7

2021-04-06T00:00:00
Máxima: 22
Mínima: 7

2021-04-07T00:00:00
Máxima: 19
Mínima: 4

2021-04-08T00:00:00
Máxima: 18
Mínima: 9

2021-04-09T00:00:00
Máxima: 20
Mínima: 10
```
