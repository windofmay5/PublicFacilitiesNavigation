# -*- coding:utf-8 -*-
#基于高德路径规划API开发服务半径计算方法，计算小区特定指标服务半径范围内的服务点个数
import arcpy
import os
#URL请求库
import requests
import random
import json
# Excel写入库
import xlwt
#XML解析库
try:
  import xml.etree.cElementTree as ET
except ImportError:
  import xml.etree.ElementTree as ET


#目录下判断是否为指定后缀文件
def endWith(s,*endstring):
        array = map(s.endswith,endstring)
        if True in array:
                return True
        else:
                return False


#读取shp属性表中xy坐标值
def readShpAttrLoc(path,xAttrName="x",yAttrName="y"):
    xyList = []
    with arcpy.da.SearchCursor(path, [xAttrName,yAttrName]) as cursor:
        for row in cursor:
            xyList.append([float(row[0]), float(row[1])])
    print(xyList)
    return xyList


def saveShpAttrPOICount(path,field_name,value_list):
    arcpy.AddField_management(path, field_name, "LONG")
    with arcpy.da.UpdateCursor(path, [field_name]) as cursor:
        for i,row in enumerate(cursor):
            row[0] = value_list[i]
            cursor.updateRow(row)


def requestDirectionAPI(start_x, start_y, end_x, end_y):
    walk_url = 'http://restapi.amap.com/v3/direction/walking?'
    key = 'key='+'87874adcc8ba2083e2497d17e937eaee'
    origin = "origin="+ str(round(start_x, 6)) + "," + str(round(start_y, 6))
    destination = "destination=" + str(round(end_x, 6)) + "," + str(round(end_y, 6))
    currentUrl = walk_url + origin + '&' + destination + '&' + key
    print(currentUrl)
    result = requests.get(currentUrl)
    js = result.json()
    time = int(js["route"]["paths"][0]["duration"])/60
    print(time)
    return time


def run(xq_path, poi_path, restrict_time):
    xq_xy = readShpAttrLoc(xq_path, "NewField_2", "NewField_3")
    poi_xy = readShpAttrLoc(poi_path, "NewField_2", "NewField_3")
    filed = os.path.basename(poi_path).split(".")[0]
    print(filed)
    count_list = []
    for xq_p in xq_xy:
        count = 0
        for poi_p in poi_xy:
            cost_time = requestDirectionAPI(xq_p[0], xq_p[1], poi_p[0], poi_p[1])
            if cost_time <= restrict_time:
                count += 1
        count_list.append(count)
    print(count_list)
    saveShpAttrPOICount(xq_path, filed, count_list)


# 主函数调用
if __name__ == "__main__":
    run(r"E:\work\wx\xq.shp", r"E:\work\wx\poi_clip\yl.shp", 30)



