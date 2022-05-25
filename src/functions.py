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

def get_coordinates_geolocator(df, street_column, postal_code):
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