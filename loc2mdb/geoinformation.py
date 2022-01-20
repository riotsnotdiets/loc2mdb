# to get the correct geojson file:
#
# 1. go to https://bundeswahlleiter.de/bundestagswahlen/2021/wahlkreiseinteilung/downloads.html
#
# 2. make sure you have the correct bundestagswahl, change if needed
#
# 3. download: "Shapefile (SHP) - Geometrie der Wahlkreise in geografischen Koordinaten
#    (Angabe in Länge- und Breitengrad, Datum WGS84) nicht generalisiert as ZIP (2021 was 5.8 MB)"
#
# 4. use a free tool like https://mygeodata.cloud/converter/shp-to-geojson to translate
#    Geometrie_Wahlkreise_xxDBT_geo.shp to Geometrie_Wahlkreise_xxDBT_geo.shp
#    (xx is the Wahlperiode, for 2021 xx = 20, 2025 should be 21)