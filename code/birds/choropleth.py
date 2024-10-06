# Font choices: https://fontawesome.com/
#
# Boundarires of MA counties (shepefiles):
#   https://www.mass.gov/info-details/massgis-data-counties
#
# Shapefile -> GeoJson conversion: 
#   https://mapshaper.org/
#   https://github.com/mbloch/mapshaper/wiki/Command-Reference
#     mapshaper -proj wgs84 -simplify dp 20% -o COUNTIES_POLYM.json
#   GDAL's ogr2ogr command:
#     ogr2ogr -f GeoJSON -t_srs crs:84 COUNTIES_POLYM.geojson COUNTIES_POLYM.shp
#    
# US counties database: https://simplemaps.com/data/us-counties
#
# Style choices in folium follows CSS style properties.
#   https://www.w3schools.com/cssref/index.php
#   Font name choices (predefined names): https://www.w3.org/wiki/CSS/Properties/color/keywords
#

import csv, json, folium, folium.plugins, branca
from pprint import pprint
from branca.colormap import linear

# maCenter = (42.4072, -71.3824)
maCenter = (42.12, -71.73)

maCountyCenters = {}
with open("uscounties.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header
    for row in reader:
        if row[5] == "Massachusetts":
            maCountyCenters[row[1]] = (row[6],row[7])
            continue

countyNameToRecords = {}
with open("maCountyNameToRecords.json", mode="r") as f:
    countyNameToRecords = json.load(f)
print(f"Finished reading maCountyNameToRecords.json.")

obsList =[ countyNameToRecords[countyName]['totalObsCount'] for countyName in maCountyCenters.keys() ]
obsMax = max(obsList)
# colormap = linear.YlGn_09.scale(0, 1000)
# colormap = linear.Accent_06.scale(0, 1000)
# https://python-visualization.github.io/folium/latest/advanced_guide/colormaps.html
colormap = linear.OrRd_08.scale(0, obsMax)

maMap = folium.Map(location = maCenter, zoom_start = 9)

folium.GeoJson(
    "us-states.json",
    style_function = lambda geoJsonFeatures: {
        "color": "darkblue",
        "weight": 2,
        "fillOpacity": 0},
).add_to(maMap)

folium.GeoJson(
    "ma-counties.json",
    style_function = lambda geoJsonFeatures: {
        "color": "darkblue",
        "weight": 2,
        "fillColor":
            colormap(countyNameToRecords[geoJsonFeatures["properties"]["COUNTY"].lower().capitalize()]["totalObsCount"]),
        "fillOpacity": 0.5,
        },
).add_to(maMap)

colormap.caption = "# of Observations"
colormap.add_to(maMap)

for countyName, countyCenter in maCountyCenters.items():
    lat = float(countyCenter[0])
    lon = float(countyCenter[1])
    if countyName == "Norfolk":
        countyCenter = (lat-0.1, lon-0.15)
    if countyName == "Suffolk":
        countyCenter = (lat-0.05, lon+0.01)
    if countyName == "Middlesex":
        countyCenter = (lat+0.1, lon-0.1)
    if countyName == "Plymouth":
        countyCenter = (lat+0.05, lon+0.1)
    if countyName == "Bristol":
        countyCenter = (lat-0.05, lon-0.1)
    if countyName == "Hampden":
        countyCenter = (lat-0.09, lon-0.325)
    if countyName == "Berkshire":
        countyCenter = (lat+0.2, lon)
    if countyName == "Hampshire":
        countyCenter = (lat, lon-0.2)
    if countyName == "Franklin":
        countyCenter = (lat+0.1, lon)

    folium.Marker(
        countyCenter,
        popup = folium.Popup(
            html = f"<b>{countyName}, {countyNameToRecords[countyName]['totalObsCount']}</b><br>" +\
                   f"{countyNameToRecords[countyName]['records'][0]['comName']}<br>" +\
                   f"{countyNameToRecords[countyName]['records'][1]['comName']}<br>" +\
                   f"{countyNameToRecords[countyName]['records'][2]['comName']}",
            max_width=400, 
            show = True,
            sticky = True),
    ).add_to(maMap)

# lat, lon = maCountyCenters["Middlesex"]
# nearby = get_nearby_hotspots(apiKey, lat, lon, dist=10)
# print(len(nearby))

maMap.save("choropleth.html")




