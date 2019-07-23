import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
data
lat = list(data["LAT"])
lon = list(data["LON"])
name = list(data["NAME"])
elev = list(data["ELEV"])

def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"

html = """<h4>Volcano information:</h4>
Name: <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location=[38, -99], zoom_start=6)

fgv = folium.FeatureGroup(name="Volcanoes")
fgp = folium.FeatureGroup(name="Population")


for lt, ln, nm, ev in zip(lat, lon, name, elev):
    iframe = folium.IFrame(html=html % (nm,nm, str(ev)), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius = 8, popup=folium.Popup(iframe), color=color_producer(ev), fill = True, fill_opacity = 0.6))

fgp.add_child(folium.GeoJson(data=(open("world.json", 'r', encoding = "utf-8-sig").read()),
style_function=lambda x: {"fillColor":"green" if x["properties"]["POP2005"] < 10000000
else "orange" if 10000000 <= x["properties"]["POP2005"] < 500000000 else "red"}))


map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map1.html")
