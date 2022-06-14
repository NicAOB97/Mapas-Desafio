# Script used to process raw school data 
# csv of primary schools and secondary schools obtained from madrid gov website
# cleans and saves all data into new csv

import pandas as pd 
from functions import process_names, get_coordinates, closest_residence, number_close_schools

# Processing csv's and saving (rewriting old)
df_primaria = pd.read_csv('./data/centros_primaria.csv', sep= ';', encoding='Latin-1')
df_secundaria = pd.read_csv('./data/centros_secundaria.csv', sep= ';', encoding='Latin-1')

resis = pd.read_csv('./data/resis_complete_gm.csv')

# Setting column names
# Indicando el nombre de las columnas
new_header = df_primaria.iloc[0]
df_primaria = df_primaria[1:]
df_secundaria = df_secundaria[1:]
df_primaria.columns = new_header
df_secundaria.columns = new_header

# adding 'Type School' column
# añadiendo columna de 'Tipo de cole'
df_primaria['TIPO'] = 'Primaria'
df_secundaria['TIPO'] = 'Secundaria'

# dataframe cleaning
# limpieza del dataframe
df_primaria.drop(['Unnamed: 14', 'Unnamed: 15'], inplace=True, axis=1)
df_secundaria.drop(['Unnamed: 14', 'Unnamed: 15'], inplace=True, axis=1)

# re-saving csv
# guardando cav
df_primaria.to_csv('./data/centros_primaria.csv')
df_secundaria.to_csv('./data/centros_secundaria.csv')

# creating complete list of schooles (concatenating)
# concatenando para obtenes listado completo de colegios
colegios = pd.concat([df_primaria,df_secundaria], axis = 0 )

# cleans street names (function which removes S/N)
# limpieza del nombre de las calles (funcion que quita S/N)
colegios = process_names(colegios)

# get coordinates
# encuentra las coordenadas
latitudes, longitudes = get_coordinates(colegios, 'calle', 'CODIGO POST.') 
colegios['latitudes'] = latitudes
colegios['longitudes'] = longitudes

latitudes, longitudes = get_coordinates(resis, 'Calle', 'CP')
resis['latitudes'] = latitudes
resis['longitudes'] = longitudes


# distances
# distancias 
resi_mas_cercana = closest_residence(colegios, resis)
n_coles_cercanos = number_close_schools(colegios, resis)

# saving
# guardando 
resis.to_csv('./data/data_resis_complete.csv')
colegios.to_csv('./data/data_coles_complete.csv')


