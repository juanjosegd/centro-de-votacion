# centro-de-votacion

✅ Requisitos Previos
Tener Python 3 instalado en tu equipo.

Instalar las bibliotecas necesarias ejecutando:

bash
Copiar
Editar
pip install pandas matplotlib
▶️ Cómo Ejecutar
Clona el repositorio o descarga todos los archivos del proyecto.

Asegúrate de estar en la carpeta donde se encuentra aactividaad8.py.

Abre una terminal y ejecuta el archivo con:

bash
Copiar
Editar
python aactividaad8.py
🗃️ Archivos Planos Requeridos
votantes.csv
Archivo en formato CSV con los datos de los votantes. Debe tener las siguientes columnas:

Ejemplo de contenido:
resultados.json
Archivo JSON con los resultados de votación. Debe contener una lista de objetos con las siguientes claves:

candidato: Nombre del candidato.

votos: Número de votos recibidos.


🧠 Funcionalidades Principales
Registro de jurados por salón, mesa y botón.

Carga de votantes desde votantes.csv.

Registro de asistencia con validación de fecha.

Carga de resultados desde archivo .json.

Búsqueda de jurados y votantes por número de cédula.

Estadísticas y análisis de resultados con pandas.

Generación de gráficos automáticos con matplotlib.

💾 Guardado y Carga
Puedes guardar la estructura del centro de votación (jurados) en el archivo estructura.txt.

Esta estructura puede ser consultada más adelante (aunque en esta versión no hay carga automática de estructura desde archivo).
