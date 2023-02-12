import folium

from utils import geocoding

class Map:
  def __init__(self):
    fond = r'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}' #https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png'
    self.carte = folium.Map(
      location=[46.2276, 2.2137],
      zoom_start=7, 
      tiles=fond, 
      attr='Custom tiles'
      )

  def map(self, address_list):
    erreur = []
    for address in address_list:
      try:
        folium.Marker(
          list(geocoding(address).values()), popup=address, icon=folium.features.CustomIcon(
            "https://www.promenadesdebretigny.fr/wp-content/uploads/2019/06/basic-fit.png",
            icon_size=(50*2.5, 35*2.5)
            )
        ).add_to(self.carte)
      except:
        erreur.append(f"Erreur sur {address}")
    return self.carte,erreur
