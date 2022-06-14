import math 
import folium
import geocoder
import pandas as pd
from geopy import distance
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster

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
        output --> resi_mas_cercana (df)'''

    closest_dist = []
    resi_number = []
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
                    
                    closest_dist.append(aux)
                    resi_number.appent(j)
                    residencia.append(resis.iloc[resi_number[i]]['Residencia'])

                else: 
                    win = win
                    closest_dist.append('N/A')
                    resi_number.appent('N/A')
                    residencia.append('N/A')

            except:
                win = win

    resi_mas_cercana = pd.DataFrame(colegios['CENTRO'])
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
        output --> n_coles_cercanos (df) '''

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

                if lat_cole != ('N/A') and math.isnan(lat_cole) == False and lon_cole != 'N/A' and math.isnan(lon_cole) == False :

                    start, end = (lat_resi,lon_resi),(lat_cole,lon_cole)
                    aux = distance.distance(start, end).km
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

    return n_coles_cercanos

#############################################################################################################

def plot_map(colegios, resis, resi_mas_cercana, n_coles_cercanos):
    # create map
    plot_locations_map = folium.Map(location=[40.380708,-3.741548], zoom_start=7)

    marker_cluster = MarkerCluster(name="Colegios").add_to(plot_locations_map)

    for i in range(0,len(colegios)):
        try:
            dist_array = resi_mas_cercana['distance']
            resi_array = resi_mas_cercana['residencia']
            dist = round(dist_array[i],2)
            if dist <= 5:
                icon_path = "./images/book_icon.png"
                icon = folium.features.CustomIcon(icon_image=icon_path ,icon_size=(31,31))
                folium.Marker(
                    location=[colegios.iloc[i]['latitudes'],colegios.iloc[i]['longitudes']], 
                    popup= ( colegios.iloc[i]['CENTRO']+' Residencia mas cercana a: '+str(dist)+', '+ resi_array[i]), 
                    label =(colegios.iloc[i]['CENTRO']).lower() , 
                    icon = icon).add_to(marker_cluster)
            else:
                icon_path = "./images/book_icon.png"
                icon2 = folium.features.CustomIcon(icon_image=icon_path ,icon_size=(31,27))
                folium.Marker(
                    location=[colegios.iloc[i]['latitudes'],colegios.iloc[i]['longitudes']], 
                    popup= ( colegios.iloc[i]['CENTRO']+' Residencia mas cercana a: '+str(dist)+', '+ resi_array[i]), 
                    label =(colegios.iloc[i]['CENTRO']).lower(),
                    icon = icon2).add_to(marker_cluster)
        except: 
            x = i

    numero_coles = n_coles_cercanos['n. coles cercanos']

    for i in range(0,len(resis)):
        if resis.iloc[i]['Tipo'] != ('Centro menores con trastornos de salud mental, consucta y/o consumo de sustancias toxicas' or 'Recursos de Adolescentes' or 'Recursos de niños/niñas y adolescentes menores no acompañados'):
            try:
                name = resis.iloc[i]['Residencia'].upper()+' '+ str(numero_coles[i]) +', colegios a 5km o menos.'
                folium.Marker(
                    location=[resis.iloc[i]['latitudes'],resis.iloc[i]['longitudes']], 
                    popup=name, 
                    icon=folium.Icon(color='orange', icon_color='white', icon = 'home'), 
                    label =(resis.iloc[i]['Residencia']).lower()
                    ).add_to(plot_locations_map)
            except: 
                try:
                    folium.Marker(
                        location=[resis.iloc[i]['latitudes'],resis.iloc[i]['longitudes']], 
                        popup='No hay colegios a menos de 5km', 
                        icon=folium.Icon(color='orange', 
                        icon_color='white', icon = 'home'), 
                        label =(resis.iloc[i]['Residencia']).lower()
                        ).add_to(plot_locations_map)
                except: 
                    i = i 
                
    folium.LayerControl().add_to(plot_locations_map)
    
    return plot_locations_map

#############################################################################################################

# widget function allows to run this on IPYNB notebook (but not main.py or external HTML)
def plot_locations(address):
    # location address
    location = geocoder.osm(address)
    
    # latitude and longitude of location
    latlng = [location.lat, location.lng]
    
    colegios = pd.read_csv('./data/data_coles_complete_gm.csv', index_col=0)
    resis = pd.read_csv('./data/data_resis_complete_gm.csv')
    resi_mas_cercana = closest_residence(colegios, resis)
    n_coles_cercanos = number_close_schools(colegios, resis)
    # create map
    plot_locations_map = plot_map(colegios, resis, resi_mas_cercana, n_coles_cercanos)
    
    # marker
    folium.Marker(latlng, popup=str(address), tooltip='click').add_to(plot_locations_map)
    
    # display map
    display(plot_locations_map)