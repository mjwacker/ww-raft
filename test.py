import folium
import json
from arcgis import GIS
from arcgis.features import FeatureLayer


# get the rivers from agol
gis = GIS()
rivers_layer = FeatureLayer(url="https://services7.arcgis.com/oF9CDB4lUYF7Um9q/ArcGIS/rest/services/North_America_Lakes_and_Rivers/FeatureServer/0", gis=gis)
#get the rivers we care about
rivers = rivers_layer.query(where="NameEn IN ('Missouri River', 'Flathead River',"
                                  " 'Middle Fork Flathead River', 'Two Medicine River',"
                                  " 'Gallatin River', 'Yellowstone River', 'Blackfoot River')",
                            out_sr=4326)

m = folium.Map(location=(47.55, -110.215), tiles="cartodb positron", zoom_start=7)



geo_json = json.loads(rivers.to_geojson)


# these f'n coordinates are inverted...
for feature in geo_json['features']:

    title = feature['properties']['NameEn']
    html = f"""
    <h1>{title}<h2>
    <p>The {title} is a river</p>
    """
    for coordinates in feature['geometry']['coordinates']:
        print(coordinates)
        swapped_coordinates = [(y, x) for x, y in coordinates]
        folium.PolyLine(
            smooth_factor=5,
            locations=[swapped_coordinates],
            color="#4053DF",
            weight=5,
            tooltip=title,
            popup=html
        ).add_to(m)


m.save("index.html")