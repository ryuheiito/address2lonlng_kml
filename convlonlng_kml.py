import requests
import urllib
import csv

# 住所格納リストの作成
address_list = []
latlng_list = []
latlist = []
lnglist = []
outputlist = []
name = []

# csv読み込み
with open('input/住所.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        address_list.append(row[1])
        name.append(row[2])

address_num = len(address_list)

for i in range(address_num):
    print(address_list[i])

# 緯度経度の検索
for i in range(1, address_num):
    address = address_list[i]
    makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
    s_quote = urllib.parse.quote(address)
    response = requests.get(makeUrl + s_quote)
    print(response.json()[0]["geometry"]["coordinates"])  # [経度,緯度]
    latlng_list.append(response.json()[0]["geometry"]["coordinates"])

# 緯度と経度に取り出し
for i in range(0, address_num - 1):
    latlist.append(latlng_list[i][1])

for i in range(0, address_num - 1):
    lnglist.append(latlng_list[i][0])

del address_list[0]
del name[0]

# 書き出し
with open('output/output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["住所", "緯度", "経度", "建物名"])
    for i in range(0, address_num - 1):
        writer.writerow([address_list[i], latlist[i], lnglist[i], name[i]])

# KMLファイルの出力
for i in range(0, address_num - 1):
    kml_filename = f'kml_output/{name[i]}.kml'
    with open(kml_filename, 'w') as kml_file:
        kml_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        kml_file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        kml_file.write('<Placemark>\n')
        kml_file.write(f'  <name>{name[i]}</name>\n')
        kml_file.write('  <Point>\n')
        kml_file.write(f'    <coordinates>{lnglist[i]},{latlist[i]},0</coordinates>\n')
        kml_file.write('  </Point>\n')
        kml_file.write('</Placemark>\n')
        kml_file.write('</kml>\n')
