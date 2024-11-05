from fastapi import FastAPI
import pandas as pd
from urllib.parse import unquote

app = FastAPI()

movies_funcion = pd.read_parquet('movies_funcion.parquet')

#Diccionario a usar en el Endpoint 1.
mes_dicc = { 
    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6, 'julio': 7, 
    'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12 
    }

#Diccioniario para usar en el Endpoint 2.
dias_dicc = { 
    'lunes': 'Monday', 'martes': 'Tuesday', 'miercoles': 'Wednesday', 'jueves': 'Thursday', 
    'viernes': 'Friday', 'sabado': 'Saturday', 'domingo': 'Sunday' 
    }

#Datos a usar en el sistema de recomendacion
similitud_coseno_df = pd.read_parquet('similitud_coseno_df.parquet')
similitud_coseno_arr = similitud_coseno_df.values
movies_modelo_recortado = pd.read_parquet('movies_modelo_recortado.parquet')

#Endpoint 1
@app.get("/Mes/{Mes}")
def cantidad_filmaciones_mes(Mes:str):
    num_mes = mes_dicc[Mes.lower()]
    lanzamientos_por_mes = len(movies_funcion[movies_funcion['month'] == num_mes])
    return (f'En el mes de {Mes} se hicieron {lanzamientos_por_mes} lanzamientos')

#Endpoint 2
@app.get("/Dia/{Dia}")
def cantidad_filmaciones_dia(Dia:str):
    Dia_traducido = dias_dicc[Dia.lower()]
    lanzamientos_por_dia = len(movies_funcion[movies_funcion['day'] == Dia_traducido])
    return (f'En el dia {Dia} se hicieron {lanzamientos_por_dia} estrenos.')

#Endpoint 3
@app.get("/titulo_para_estreno/")
def score_titulo(titulo_de_la_filmacion: str):
    # Filtrar las filas que coinciden con el titulo
    titulo_de_la_filmacion = titulo_de_la_filmacion.lower()
    filtro = movies_funcion[movies_funcion['title'].str.lower() == titulo_de_la_filmacion]

    # Verificar si el filtro no esta vacio
    if not filtro.empty:
        Titulo = filtro['title'].iloc[0]
        Year = filtro['release_year'].iloc[0]
        Popularity = filtro['popularity'].iloc[0]
        return (f'La pelicula {Titulo}, fue estrenada en el año {Year} y tiene un puntaje de {Popularity}')
    else:
        return ("Error, no se encontro titulo")

#Endpoint 4
@app.get("/titulo_para_cuenta_votos/")
def votos_titulo( titulo_de_la_filmacion ):
    titulo_de_la_filmacion = titulo_de_la_filmacion.lower()
    filtro = movies_funcion[movies_funcion['title'].str.lower() == titulo_de_la_filmacion]

    # Verificar si el filtro no esta vacio
    if not filtro.empty:
        Titulo = filtro['title'].iloc[0]
        Cant_votos = filtro['vote_count'].iloc[0]
        Prom_votos = filtro['vote_average'].iloc[0]
        if Cant_votos >= 2000:
            return (f'La pelicula {Titulo}, cuenta con un total de {Cant_votos} valoraciones, con un promedio de {Prom_votos}')
        else:
            return (f'La pelicula {Titulo} no cumple con el minimo de 2000 valoraciones')
    else:
        return ("Error, no se encontro titulo")

#Endpoint 5
@app.get("/nombre_actor/")
def get_actor( nombre_actor: str ):
    return ('Enpoint en desarrollo')

#Endpoint 6
@app.get("/nombre_actor/")
def get_director( nombre_director: str ):
    return ('Enpoint en desarrollo')

#Sistema de recomendacion
@app.get("/titulo_recomendacion/")
def recomendacion( titulo: str ):
    # Hacemos que al titulo no le influyan las mayusculas
    titulo = titulo.lower()
    # Aseguramos que el titulo se encuentre dentro del dataset o en caso contrario, nos de aviso
    if not movies_modelo_recortado[movies_modelo_recortado['title'].str.lower() == titulo].empty:
        # Buscamos cual es el indice que le corresponde al titulo elegido para buscarlo en la matriz de similitud
        indice = movies_modelo_recortado[movies_modelo_recortado['title'].str.lower() == titulo].index.values[0]
        # Para el indice dado, encontramos cuales son los valores de similitud de coseno comparando con todas las peliculas
        similitud = similitud_coseno_arr[indice]
        # Ordenamos y truncamos para las primeras 5 mejores relaciones encontradas (sin contar la peli elegida) 
        # y nos devuelven los indices
        indices_similares = similitud.argsort()[::-1][1:6]
        # Ahora tenemos que ver que titulos tienen esos indices encontrados
        lista = []
        for i in indices_similares:
            recomendacion = movies_modelo_recortado['title'].iloc[i]
            lista.append(recomendacion)
        return (f'Recomendaciones: 1) {lista[0]}, 2) {lista[1]}, 3) {lista[2]}, 4) {lista[3]}, 5) {lista[4]}')
    else:
        return ("Error, no se encontro titulo")