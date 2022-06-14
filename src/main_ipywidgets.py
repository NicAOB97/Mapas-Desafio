import pandas as pd
import ipywidgets
from functions import closest_residence, number_close_schools, plot_locations

colegios = pd.read_csv('./data/data_coles_complete_gm.csv', index_col=0)
resis = pd.read_csv('./data/data_resis_complete_gm.csv', index_col=0)

resi_mas_cercana = closest_residence(colegios, resis)
n_coles_cercanos = number_close_schools(colegios, resis)

# text widget
address_text_box = ipywidgets.Text(value='', placeholder='escribe aqui', description='dirección:')
# interaction between widget and function  
ipywidgets.interact_manual(plot_locations, address = address_text_box)