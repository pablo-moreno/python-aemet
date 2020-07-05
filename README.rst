============
Python AEMET
============
.. image:: https://img.shields.io/pypi/v/python-aemet
   :target: https://pypi.org/project/python-aemet
.. image:: https://img.shields.io/pypi/dm/python-aemet
   :target: https://pypi.org/project/python-aemet
.. image:: https://github.com/pablo-moreno/python-aemet/workflows/Upload%20Python%20Package/badge.svg
   :target: https://github.com/pablo-moreno/python-aemet/actions

Librería cliente de la API de datos de AEMET. Permite obtener y manejar la información de la API de datos abiertos de AEMET. Cuenta con una serie de modelos de datos y métodos preparados para poder utilizarlos de forma fácil y accesible. Además, permite descargar en archivos los mapas que genera y publica AEMET.

La información que recoge y utiliza esta librería es propiedad de la Agencia Estatal de Meteorología.

Instalación
============
Utiliza pip para instalar la librería:

.. code-block:: bash

    pip install python-aemet


API Key
=======

Obtén tu clave de API en la siguiente URL:

https://opendata.aemet.es/centrodedescargas/obtencionAPIKey


Usar la librería
=================

La clase principal de la librería es la clase Aemet.

.. code-block:: python

    from aemet import Aemet
    aemet_client = Aemet(api_key='your_api_key')

Instancia un objeto con la API key y tendrás acceso a todos los métodos.

Para más información, revisa la documentación

¿Dudas, sugerencias?
=====================

Para cualquier duda, sugerencia o mejora, siéntete libre de abrir una issue en el repositorio. No contesto a correos.
