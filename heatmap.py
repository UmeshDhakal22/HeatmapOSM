#import all the necessary libraries
import requests
import pandas as pd
import json
from geojson import FeatureCollection
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
from folium.plugins import MarkerCluster

#This is the url to the static feature collected 
url='https://tileboundaries.baato.io/admin_boundary/pois.json'

#read the url in json format
response=requests.get(url)
data=response.json()
data=json.dumps(data, indent=4)
data=json.loads(data)

#get the necessary features from the data
features = data["features"]
extracted_data = []
for feature in features:
    properties = feature["properties"]
    geometry = feature["geometry"]

    extracted_data.append({
        "type": feature["type"],
        "amenity": properties.get("amenity", None),
        "classa": properties.get("class", None),
        "name": properties.get("name", None),
        "longitude": geometry["coordinates"][0],
        "latitude": geometry["coordinates"][1],
        "geometry_type": geometry["type"]
    })

#change the data into a Dataframe
df=pd.DataFrame(extracted_data)

#see the counts of each value in a class feature
class_counts=df['classa'].value_counts()
print(class_counts)

#bar graph of the count
class_counts.plot(kind='bar')
plt.show()

#reading the geojson file, please replace it with your geojson file
with open('geo.geojson') as f:
    data = json.load(f)
    geojson_map = FeatureCollection(data['features'])

#removing all the empty values from the classa column
a=df.dropna(subset=['classa'])

#making the cluster map
m = folium.Map()
marker_cluster = MarkerCluster().add_to(m)
for index, row in a.iterrows():
    latitude = row['latitude']
    longitude = row['longitude']
    name=row['name']
    classa = row['classa']

    marker = folium.Marker([latitude, longitude])
    popup_message = f'Name: {name}'
    folium.Popup(popup_message).add_to(marker)
    marker_cluster.add_child(marker)

folium.GeoJson('geo.geojson').add_to(m) 
m.save('class.html')

#making the heatmap
m_heatmap = folium.Map()
locations = df[['latitude', 'longitude']].values
heat_map = HeatMap(locations).add_to(m_heatmap)
folium.GeoJson('geo.geojson').add_to(m_heatmap)  
m_heatmap.save('heat_map.html')




