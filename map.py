import folium

from utils import geocoding

class Map:
  def __init__(self):
    fond = r'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png'
    self.carte = folium.Map(
      location=[46.5, 2.3],
      zoom_start=5.2, 
      tiles=fond, 
      attr='© OpenStreetMap © CartoDB'
      )
  
  def map(self, address_list):
    erreur = []
    for address in address_list:
      try:
        folium.Marker(
          list(geocoding(address).values()), popup=address, icon=folium.features.CustomIcon(
            "https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco,dpr_1/v1397184778/d8d5e0a2089418bbf5d7a28b5f7ba982.png",
            icon_size=(50, 35)
            )
        ).add_to(self.carte)
      except:
        erreur.append(f"Erreur sur {address}")
    return self.carte,erreur
