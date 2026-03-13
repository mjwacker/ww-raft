import folium
import json
from arcgis import GIS
from arcgis.features import FeatureLayer


# get the rivers from agol
gis = GIS()
rivers_layer = FeatureLayer(url="https://services7.arcgis.com/oF9CDB4lUYF7Um9q/ArcGIS/rest/services/North_America_Lakes_and_Rivers/FeatureServer/0", gis=gis)
#get the rivers we care about
rivers = rivers_layer.query(where="NameEn='Missouri River'", out_sr=4326)

m = folium.Map(location=(47.55, -110.215), tiles="cartodb positron", zoom_start=7)



geo_json = json.loads(rivers.to_geojson)

for feature in geo_json['features']:
    for coordinates in feature['geometry']['coordinates']:
        folium.PolyLine(
            locations=coordinates,
            color="#FF0000",
            weight=5,
            tooltip="Missouri",
        ).add_to(m)


m.save("index.html")