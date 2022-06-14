import pandas as pd
import folium
from functions import plot_map_1, plot_map_cluster

colegios = pd.read_csv('./data/data_coles_complete_gm.csv', index_col=0)
resis = pd.read_csv('./data/data_resis_complete_gm.csv', index_col=0)
resi_mas_cercana = pd.read_csv('./data/solos_resis_complete_gm.csv', index_col=0)
n_coles_cercanos = pd.read_csv('./data/n_coles_cercanos.csv', index_col=0)

# obtain a map with all points plotted
# no labels
m = plot_map_1(resis, colegios)
# m.save('mapV1.html')

# obtain a map with all resis plotted while schools are clustered and only visible when zoomed in 
# labels when locations are clicked- indicating which the nearest school or resi is and the distance
f = plot_map_cluster(resis, colegios)
# m.save('map2.html')

