# Sample script by Hector Muro for retrieving data from the AgroDataCube

import requests
import json
import geojson
import os
import csv
from shapely.geometry import shape

####Read coordinates, send coordinates, retrieve id, send id's, retrieve information
def read_write(input_path,output_path):
    with open(input_path, 'r') as csvfile:
        coord_reader = csv.reader(csvfile, delimiter=',')
        data = list(coord_reader)
        row_count = len(data)
        with open(output_path,'w') as outputfile:
            writer = csv.writer(outputfile, delimiter=',')
            header = ["csv_id","Field_ID","Year","NDVI_value","NDVI_datum","ahn_mean","ahn_stddev","ahn_min","ahn_max", "Risico Code","BDgem_BDmax","POR/40",
                    "crop_name","area","station1_id","dist_station1","station2_id","dist_station2","station3_id","dist_station3","station4_id",
                    "dist_station4","station5_id","dist_station5","geometry_wkt"] #Crop Types, Soil Types
            writer.writerow(header)

            for i in range(1,row_count):
                id_csv = data[i][1]
                x = data[i][5]
                y = data[i][6]
                risico_code = data[i][64]
                bdgem = data[i][39]
                por_40 = data[i][36]
                url = "https://agrodatacube.wur.nl/api/v2/rest/fields?output_epsg=28992&page_offset=0&year=2017&geometry=POINT({} {})&epsg=28992".format(x,y)
                #"https://agrodatacube.wur.nl/api/v2/rest/fields?output_epsg=28992&page_size=25&page_offset=0&year=2017&geometry=POINT(127212.5 495887.5)&epsg=28992"
                response = requests.get(url)
                fields = geojson.loads(response.content)#This feature collection contains
                for i in range(len(fields['features'])): #i is 0 to 5 (every year)
                    year = fields['features'][i]['properties']['year']
                    print(year)
                    fieldid = fields['features'][i]['properties']['fieldid'] #Now, with the fieldId we have to make another call

                    url_ahn = "https://agrodatacube.wur.nl/api/v2/rest/fields/{}/ahn?page_size=25&page_offset=0".format(fieldid)
                    response_ahn = requests.get(url_ahn)
                    ahn_values = geojson.loads(response_ahn.content)
                    mean = 0
                    sttdev = 0
                    min_ = 0
                    max_ = 0
                    # print(fieldid)
                    for i in range(len(ahn_values['features'])):
                        #Some fields have a null AHN value.
                        try:
                            mean += ahn_values['features'][i]['properties']['mean']
                            sttdev += ahn_values['features'][i]['properties']['stddev']
                            min_ += ahn_values['features'][i]['properties']['min']
                            max_ += ahn_values['features'][i]['properties']['max']
                        except:
                            pass

                    ahn_mean = mean/len(ahn_values['features'])
                    ahn_stddev = sttdev/len(ahn_values['features'])
                    ahn_min = min_/len(ahn_values['features'])
                    ahn_max = max_/len(ahn_values['features'])

                    url_crop = "https://agrodatacube.wur.nl/api/v2/rest/fields/{}?output_epsg=28992&page_offset=0".format(fieldid)
                    response_crop = requests.get(url_crop, headers={"token":"<your token>"})
                    crop_values = geojson.loads(response_crop.content)

                    crop_name = crop_values['features'][0]['properties']['crop_name']
                    area = crop_values['features'][0]['properties']['area']

                    #Write geometry as a WKT.
                    geometry_json = crop_values['features'][0]['geometry']
                    geom_shapely = shape(geometry_json)
                    geometry_wkt = geom_shapely.wkt

                    url_meteo = "http://agrodatacube.wur.nl/api/v1/rest/fields/{}/meteostations?output_epsg=28992&page_offset=0".format(fieldid)
                    response_meteo = requests.get(url_meteo,headers={"token":"<your token>"})
                    meteo_values = geojson.loads(response_meteo.content)
                    station1_id = meteo_values['features'][0]['properties']['meteostationid']
                    dist_station1 = meteo_values['features'][0]['properties']['distance']
                    station2_id = meteo_values['features'][1]['properties']['meteostationid']
                    dist_station2 = meteo_values['features'][1]['properties']['distance']
                    station3_id = meteo_values['features'][2]['properties']['meteostationid']
                    dist_station3 = meteo_values['features'][2]['properties']['distance']
                    station4_id = meteo_values['features'][3]['properties']['meteostationid']
                    dist_station4 = meteo_values['features'][3]['properties']['distance']
                    station5_id = meteo_values['features'][4]['properties']['meteostationid']
                    dist_station5 = meteo_values['features'][4]['properties']['distance']

                    url_ndvi = "https://agrodatacube.wur.nl/api/v2/rest/fields/{}/ndvi?output_epsg=28992&page_offset=0".format(fieldid)
                    response_ndvi = requests.get(url_ndvi,headers={"token":"<your token>"})
                    ndvi_values = geojson.loads(response_ndvi.content)
                    for i in range(len(ndvi_values['features'])):
                        ndvi_val = ndvi_values['features'][i]['properties']['ndvi_value']
                        ndvi_datum = ndvi_values['features'][i]['properties']['datum']
                        row = [id_csv,fieldid,year,ndvi_val,ndvi_datum,ahn_mean,ahn_stddev,ahn_min,ahn_max,risico_code,
                                bdgem,por_40,crop_name,area,station1_id,dist_station1,station2_id,dist_station2,
                                station3_id,dist_station3,station4_id,dist_station4,station5_id,dist_station5,geometry_wkt]
                        writer.writerow(row)
    # https://agrodatacube.wur.nl/api/v1/rest/fields/402117/soilparams?output_epsg=28992&page_size=25&page_offset=0

###ZIP coodes
###The API only returns 50 max, so I have do nit in QGIS.
def zip_codes():
    url_zipcodes = 'https://agrodatacube.wur.nl/api/v2/rest/regions/postalcodes?&output_epsg=28992&page_offset=0'
    response_zipcodes = requests.get(url_zipcodes,headers={"token":"<your token>"})
    zip_codes_api = geojson.loads(response_zipcodes.content)
    zip_codes = []
    for i in range(len(zip_codes_api['features'])):
        zip_codes += [[zip_codes_api['features'][i]['properties']['postcode']],[zip_codes_api['features'][i]['geometry']]]
    return zip_codes

if __name__ == '__main__':
    ##Here there must be the relative paths to the input data and where the data should be stored.
    read_write("","")
    # read_write('/home/hectormauer/Desktop/AgroDataCubeSprint/data_nograss.csv','/home/hectormauer/Desktop/AgroDataCubeSprint/data_nograss_fields.csv')
