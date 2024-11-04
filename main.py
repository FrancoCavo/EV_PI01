from fastapi import FastAPI
import pandas as pd
from urllib.parse import unquote

app = FastAPI()

#En local usamos la siguiente lectura de archivo:
#movies_funcion = pd.read_parquet('../EV_PI01\movies_funcion.parquet')

#En Render usamos la siguiente:
movies_funcion = pd.read_parquet('movies_funcion.parquet')

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
def cantidad_filmaciones_mes(Mes: int):
    lanzamientos_por_mes = len(movies_funcion[movies_funcion['month'] == Mes])
    #return print('En el mes', Mes,'hubo', lanzamientos_por_mes,'lanzamientos.') --> Esta opcion no la usamos, 
    # ya que el print sirve solo para retornar en la terminal.
    return {"mes": Mes, "lanzamientos": lanzamientos_por_mes}

#Endpoint 2
@app.get("/Dia/{Dia}")
def cantidad_filmaciones_dia(Dia:str):
    Dia_traducido = dias_dicc[Dia.lower()]
    lanzamientos_por_dia = len(movies_funcion[movies_funcion['day'] == Dia_traducido])
    return {"dia": Dia, "lanzamientos": lanzamientos_por_dia}

#Endpoint 3
#@app.get("/titulo/{titulo_de_la_filmacion}")
@app.get("/titulo/")
def score_titulo(titulo_de_la_filmacion: str):
    # Filtrar las filas que coinciden con el titulo
    titulo_de_la_filmacion = titulo_de_la_filmacion.lower()
    filtro = movies_funcion[movies_funcion['title'].str.lower() == titulo_de_la_filmacion]

    # Verificar si el filtro no esta vacio
    if not filtro.empty:
        Titulo = filtro['title'].iloc[0]
        Year = filtro['year'].iloc[0]
        Popularity = filtro['popularity'].iloc[0]
        return {"Titulo": Titulo, "Ano de lanzamiento": str(Year), 'Puntaje': str(Popularity)}
    else:
        return {"error": "No se encontro titulo"}

#Endpoint 4

#Sistema de recomendacion
@app.get("/titulo_recomendacion/")
def recomendacion( titulo: str ):
    # Hacemos que al titulo no le influyan las mayusculas
    titulo = titulo.lower()
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
    return ('Recomendaciones: 1)'{lista[0]}, '2)'{lista[1]}, '3)'{lista[2]}, '4)'{lista[3]}, '5)'{lista[4]})