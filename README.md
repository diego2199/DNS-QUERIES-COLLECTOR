# Analizador de Logs DNS y Envío de Datos a la API de Lumu

Este proyecto es un script en Python que analiza un archivo de log de consultas DNS, extrae datos relevantes como la IP del cliente, el host consultado y el timestamp, y luego envía estos datos a la API de Lumu en formato JSON. Adicionalmente, genera estadísticas sobre las IPs y los hosts procesados.

## Requisitos

- **Python 3.13**
- **Módulos de Python**:
  - `requests`: para hacer solicitudes HTTP a la API de Lumu.
  - `re`: para manejar expresiones regulares y procesar el archivo de log.
  - `datetime`: para manejar y convertir los formatos de fechas.
  - `collections.Counter`: para generar estadísticas.

Instala `requests` ejecutando:

```bash
py -m pip install requests

Configuración

Antes de ejecutar el script, define tus credenciales en el código:

LUMU_CLIENT_KEY: tu clave de cliente de Lumu.

COLLECTOR_ID: el ID de tu colector en Lumu.


Estas constantes permiten la autenticación y envío de datos a la API de Lumu.

Uso

Ejecución

Ejecuta el script de la siguiente manera:

python script.py <ruta_al_archivo_de_logs>

Donde <ruta_al_archivo_de_logs> es la ubicación del archivo de logs DNS que deseas analizar.

Ejemplo de Línea de Log

El script espera que el archivo de log tenga un formato similar a:

7-Jul-2022 16:35:16.603 consultas: información: cliente @ 0x55adcd6c47e0 190.242.62.142#23840 (asm-api-prod-geo-am-skype.trafficmanager.net): consulta: asm-api-prod-geo-am-skype.trafficmanager.net EN A +E(0)DC (172.20.101.44)

Funcionalidades Principales

1. parse_log:

Extrae y organiza la información del log.

Usa expresiones regulares para capturar la fecha y hora, la IP del cliente y el host consultado.

Convierte el formato de la fecha y hora a ISO 8601.



2. convert_to_iso:

Convierte una fecha en formato 7-Jul-2022 16:35:16.603 a 2022-07-07T16:35:16.603Z (ISO 8601).



3. send_data_in_chunks:

Envía los datos en fragmentos de 500 registros a la API de Lumu.

Verifica la respuesta y reporta cualquier error en el envío.



4. generate_statistics:

Genera un resumen de las IPs y hosts más comunes.

Muestra el total de registros y el porcentaje de ocurrencias de cada IP y host.




Ejemplo de Salida

Durante la ejecución, el script imprimirá mensajes como:

Confirmación de los datos de fecha y hora encontrados en cada línea del log.

Estadísticas de los clientes (IPs) y hosts más frecuentes.

Mensajes de error en caso de fallos al enviar los datos a la API.


Notas

Asegúrate de que el archivo de logs tenga el formato esperado para evitar problemas al analizar la información.

Si encuentras errores de autenticación o de formato de datos, revisa LUMU_CLIENT_KEY, COLLECTOR_ID y el formato de fechas en el log.


Créditos

Este script fue desarrollado como una herramienta de análisis de logs DNS y de envío de datos a la API de Lumu.
