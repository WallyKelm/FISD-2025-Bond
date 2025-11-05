import geopandas
import geodatasets
import matplotlib.pyplot as plt
import folium

## Precinct data from https://data.capitol.texas.gov/dataset/precincts
precincts = geopandas.read_file("Precincts")
# Filter to FISD precincts in Galveston County
fisd = precincts[precincts["CNTY"]==167][precincts["PREC"].isin(["0356","0357","0460","0461","0462","0492","0495"])]
fisd = fisd[["PREC",'geometry']]
fisd.rename({"PREC":"Precinct"})

# Add election data from: https://results.enr.clarityelections.com/TX/Galveston/125146/web.345435/#/detail/8
# Valid as of Nov 5, 2025 11:20 AM
fisd["Registered Voters"] = [3654, 4684, 3399, 4111, 3679, 1722, 2471]
fisd["For"] = [228, 443, 475, 410, 363, 363,280]
fisd["Against"] = [523, 1014, 1204, 1013, 1039, 1001, 725]
fisd["Total"] = [751, 1457, 1679, 1423, 1402, 1364, 1005]
fisd["Turnout"] = ['30.4%', '30.4%', '28.3%', '28.8%', '25.9%', '26.6%', '27.9%']
fisd["Margin"] = ((fisd["For"] - fisd["Against"]) / fisd["Total"]).apply(lambda x: f"{x:.1%}")

# Create map file
map = fisd.explore()

# Define the map title using HTML
map_title = "FISD 2025 Bond Election Results for Proposition A"
title_html = f'''
             <h3 align="center" style="font-size:20px"><b>{map_title}</b></h3>
             '''
source_link = "https://results.enr.clarityelections.com/TX/Galveston/125146/web.345435/#/detail/8"
			 
source_html = f'''
			<h2 align="center" style="font-size:16px"><a href={source_link} target="_blank">Election Results Source</a></h2>
			'''

# Add the title HTML to the map
map.get_root().html.add_child(folium.Element(title_html))
map.get_root().html.add_child(folium.Element(source_html))
map.save("fisd_2025_precincts.html")