import folium
from arcgis import GIS
from arcgis.features import FeatureLayer
import pandas
gis = GIS()

rivers_layer = FeatureLayer(url="https://services7.arcgis.com/oF9CDB4lUYF7Um9q/ArcGIS/rest/services/North_America_Lakes_and_Rivers/FeatureServer/0", gis=gis)
#get the rivers we care about
rivers = rivers_layer.query(where="NameEn='Missouri River'")
rivers_sdf = rivers.sdf
print(rivers_sdf)








m = folium.Map(location=(47.55, -110.215), tiles="cartodb positron", zoom_start=7)
m.save("index.html")