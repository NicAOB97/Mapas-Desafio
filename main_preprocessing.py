import pandas as pd 

# Processing csv's and saving (rewriting old)
df_primaria = pd.read_csv('centros_primaria.csv', sep= ';', encoding='Latin-1')
df_secundaria = pd.read_csv('centros_secundaria.csv', sep= ';', encoding='Latin-1')

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
df_primaria.to_csv('centros_primaria.csv')
df_secundaria.to_csv('centros_secundaria.csv')

# creating complete list of schooles (concatenating)
# concatenando para obtenes listado completo de colegios
colegios = pd.concat([df_primaria,df_secundaria], axis = 0 )

# saving
# guardando 
colegios.to_csv('colegios.csv')


