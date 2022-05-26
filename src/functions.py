import math 
from geopy import distance
from geopy.geocoders import Nominatim

#############################################################################################################
# Dos funciones que encuentran la latitude y longitude segun la calle y el codigo postal 
# Two functions that find the latitude and longitude according to street name and postcode
def get_coordinates_google(df, street_column, postal_code):

    ''' Utilizando la API de Google Map 
        Using the Google Maps API
        
        input --> df (data frame), street_column
        '''

    latitudes = []
    longitudes = []
    for i in range(0,len(df)):
        try: 
            address = df.iloc[i][street_column]+', Madrid, '+str(df.iloc[i][postal_code])
            response = map_client.geocode(address)
            latitudes.append(response[0]['geometry']['location']['lat'])
            longitudes.append(response[0]['geometry']['location']['lng'])
        except: 
            latitudes.append('N/A')
            longitudes.append('N/A')

    return latitudes, longitudes

def get_coordinates_geolocator(df, street_column, postal_code, geolocator = Nominatim(user_agent="project")):
    latitudes = []
    longitudes = []
    for i in range(0,len(df)):
        try: 
            x = geolocator.geocode(df.iloc[i][street_column]+', Madrid, '+df.iloc[i][postal_code]).point
            latitudes.append(x[0])
            longitudes.append(x[1])
        except: 
            latitudes.append('N/A')
            longitudes.append('N/A')

    return latitudes, longitudes

#############################################################################################################

def closest_residence(colegios, resis):

    ''' Calculate the distance between schools and resis
        find the closest resi to each school
        Calcula las distancias entre las resis y los colegios
        encuentra la resi mas cercana de cada colegio
        
        input --> colegios (df), resis (df)
        output --> '''

    closest_dist = list(range(0,len(colegios)))
    resi_number = [0] * len(colegios)
    residencia = []

    for i in range(0, len(colegios)):
        win = 1000000
        for j in range(0, len(resis)):

            lat_resi = resis.iloc[j]['latitudes']
            lon_resi = resis.iloc[j]['longitudes']
            lat_cole = colegios.iloc[i]['latitudes']
            lon_cole = colegios.iloc[i]['longitudes']

            start, end = (lat_resi,lon_resi),(lat_cole,lon_cole)

            try:
                aux = distance.distance(start, end).km

                if aux < win :
                    win = aux 
                    
                    closest_dist[i] = aux
                    resi_number[i] = j
                    residencia.append(resis.iloc[resi_number[i]]['Residencia'])

            except:
                win = win

        resi_mas_cercana = colegios['CENTRO']
        resi_mas_cercana['distance'] = closest_dist
        resi_mas_cercana['n. resi'] = resi_number
        resi_mas_cercana['residencia'] = residencia

        return resi_mas_cercana

def number_close_schools(colegios, resis):

    ''' Calculate the distance between schools and resis
        find all resis <= 5 km to a school
        Calcula la distancia entre los coles y las resis
        devuelve cuantos coles estan a 5km o menos de cada resi
        
        input --> colegios (df) resis (df)
        output --> '''

    close_schools_dist = []
    close_schools = []

    for p in range(0, len(resis)):

        lat_resi = resis.iloc[p]['latitudes']
        lon_resi = resis.iloc[p]['longitudes']

        close_schools.append([])
        close_schools_dist.append([])

        if math.isnan(lat_resi) == False and math.isnan(lon_resi) == False:

            for q in range(0, len(colegios)):
                
                lat_cole = colegios.iloc[q]['latitudes']
                lon_cole = colegios.iloc[q]['longitudes']

                if lat_cole != 'N/A' and lon_cole != 'N/A':

                    start, end = (lat_resi,lon_resi),(lat_cole,lon_cole)
                    try: 
                        aux = distance.distance(start, end).km
                    except: 
                        print(p,q,start,end)

                    if aux <= 5:
                        close_schools[p].append(q)
                        close_schools_dist[p].append(aux)
                    else: 
                        continue

                else: continue
        else: 
            continue

        numero_coles = []
        for i in range(0, len(close_schools)):
            numero_coles.append(len(close_schools[i]))

        n_coles_cercanos = resis['Residencia']
        n_coles_cercanos['n. coles cercanos'] = numero_coles

