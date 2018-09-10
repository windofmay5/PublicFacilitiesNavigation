# -*- coding: utf-8 -*-
import requests
import xlwt

base_url = "http://restapi.amap.com/v3/place/text?"
key = "*****"

type = "17"
#城市
city = "320211"
path = r"E:\工作\tool\amapPOISearch\temp.xls"

index = 0
workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('sheet1',cell_overwrite_ok=True)

for page in range(1, 46):
    requests_url = base_url+"key="+key+"&types="+type+"&city="+city+"&page="+str(page)
    print(requests_url)
    result = requests.get(requests_url)
    js = result.json()
    for i,item in enumerate(js["pois"]):
        item_name = item["name"]
        item_type = item["type"]
        print(item["location"])
        location_x = item["location"].split(",")[0]
        location_y = item["location"].split(",")[1]
        worksheet.write(index, 0, item_name)
        worksheet.write(index, 1, item_type)
        worksheet.write(index, 2, location_x)
        worksheet.write(index, 3, location_y)
        index += 1
workbook.save(path)





