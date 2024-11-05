PROYECTO INDIVIDUAL Nro 1 - SISTEMA DE RECOMENDACION DE PELICULAS

El siguiente proyecto, consiste en realizar 6 funciones de consulta y 1 sistema de recomendacion de peliculas en base a un dataset proporcionado. Este sistema se ejecuta en una API (FastAPI) y se hace un deploy en Render.

Funciones de consulta:

- Endpoint1 - Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.
- Endpoint2 - Se ingresa un día en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en día consultado en la totalidad del dataset.
- Endpoint3 - Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.
- Endpoint4 - Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.
- Endpoint5 - Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, la cantidad de películas que en las que ha participado y el promedio de retorno. La definición no deberá considerar directores.
- Endpoint6 - Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.
- Sistema de recomendacion: Se ingresa el nombre de una película y te recomienda las similares en una lista de 5 valores.

TABLA DE CONTENIDOS

- Descripcion
- Documentos
- Datos de interes

DESCRIPCION

Para llevar a cabo este proyecto, fue necesario hacerlo en distintas etapas. Proceso de ETL_1 y ETL_2, EDA + Generacion de modelo, Creacion de funciones de consultas y deploy en Render.

Proceso ETL_1

En esta etapa se realizo una limpieza general y segun las solicitudes del enunciado. A partir del dataset 'credits' se generaron dos datasets, 'credits_crew' y 'credits_cast', para no generar un solo archivo dada la cantidad de datos que contiene. Para el dataset 'movies' se genero el archivo 'movies_con_etl' que luego es consumido por el proceso de ETL_2. Los archivos generados se guardaron en formato parquet para optimizar el rendimiento de Render. 

Proceso ETL_2

Este segundo proceso de ETL se lleva a cabo para poder dejar solo los datos que necesitan las funciones de consulta (Endpoints). Este proceso de optimizacion nos es util para agilizar el deploye en Render. De este proceso se obtiene el archivo 'movies_funcion' que se utiliza para el consumo de la API.

EDA + Generacion de modelo

Para la generacion del modelo, fue necesario hacer un analisis y exploracion de los datos que se obtuvieron a partir del ETL. El sistema elegido para hacer la recomendacion fue la Similitud del Coseno. 

Este modelo requiere que le proporcionemos datos que nos permitan comparar anguloes entre vectores (generados con TF-IDF Vectorizer) entre las diferentes peliculas. La relacion esta dada entre '0' y '1', siendo '1' una similitud exacta y '0' una similitud nula entre vectores.
Se tienen en cuenta los siguientes criterios:

- Los valores a vectorizar seran los que contiene la columna 'overview', ya que esta posee informacion detallada de cada pelicula.
- Por ser render una aplicacion que nos limita la capacidad de computo, se reduce el dataset de consulta a solo 4000 filas.
- Las 4000 filas son seleccionadas en base a peliculas que contienen el numero de votos que permita hacer representable el valor de popularidad.

En este proceso se generan los datos 'movies_modelo_recortado' y 'similitud_coseno_df' que luego son consumidos por la funcion en la API.

Creacion de funciones de consultas y deploy en Render

La ultima etapa consiste en crear el archivo main.py que tiene todo lo necesario para hacer funcionar a las funciones de consulta y el sistema de recomendacion. 

Link para deploy en render: https://ev-pi01.onrender.com (recordar agregar /docs para visualizar las funciones)

DOCUMENTOS

En el repositorio vamos a encontrar los siguiente archivos:

ETL_1 y ETL_2: Notebooks con el paso a paso de los procesos de ETL.

EDA_Modelo_ML: Notebook con el paso a paso del analisis y creacion de los datos para el sistema de recomendacion.

movies_funcion.parquet: Datos en formato parquet para el consumo de las funciones de consulta.

movies_modelo_recortado.parquet y similitud_coseno_df.parquet: Datos en formato parquet para el consumo del sistema de recomendacion.

main.py: Contiene las funciones para el deploy en la API.

DATOS DE INTERES

Datasets originales: https://drive.google.com/drive/folders/1X_LdCoGTHJDbD28_dJTxaD4fVuQC9Wt5
