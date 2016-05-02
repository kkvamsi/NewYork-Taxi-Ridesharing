__author__ = 'vamsi'

from datetime import datetime
str(datetime.now())
import beatrix


#get the handle for csv data and read them into a list. Return the list
def fetch_csv_data():
    print(str(datetime.now()))
    input_handle=open('/home/vamsi/Databases_sqlLite/taxi_extract_2015_yellow_jan_1_sorted.csv','r')
    output=open('/home/vamsi/Databases_sqlLite/taxi_extract_2015_yellow_jan_1_processed.csv','w')
    total_month_data=[]
    sector1=[(-73.767014,40.639488),
(-73.729248,40.644699),
(-73.717575,40.824202),
(-73.756714,40.840827),
(-73.765640,40.638446)]
    sector2=[(-73.861084,40.901058),
(-73.784866,40.659285),
(-73.765640,40.641573),
(-73.756027,40.886524),
(-73.769760,40.906767),
(-73.859711,40.901058)]
    sector3=[(-73.769073,40.639488),
(-73.796539,40.632193),
(-73.942795,40.876661),
(-73.914642,40.903134),
(-73.862457,40.900020),
(-73.774567,40.634278)]
    sector4=[(-73.771133,40.632714),
(-73.800659,40.631151),
(-73.970261,40.745176),
(-73.969574,40.723844),
(-73.983994,40.706669),
(-74.022446,40.699902),
(-74.016953,40.742575),
(-73.998413,40.778982),
(-73.980560,40.794578),
(-73.966141,40.822124),
(-73.959274,40.837710),
(-73.950348,40.863160),
(-73.943481,40.874584),
(-73.794479,40.630109)]
    sector5=[(-73.765640,40.633757),
(-73.804092,40.631151),
(-73.966827,40.741014),
(-73.968201,40.721242),
(-73.979874,40.707710),
(-73.996353,40.703025),
(-74.021759,40.698340),
(-74.029312,40.683242),
(-74.033432,40.675951),
(-74.034805,40.658764),
(-73.951035,40.646783),
(-73.868637,40.642615),
(-73.763580,40.633236)]
    sector6=[(-73.774567,40.631151),
(-73.856964,40.640530),
(-73.880310,40.641573),
(-73.944855,40.644699),
(-73.967514,40.647304),
(-74.033432,40.657201),
(-74.077377,40.650950),
(-74.137115,40.641051),
(-74.169388,40.641573),
(-74.206467,40.623334),
(-74.222260,40.563895),
(-74.247665,40.520585),
(-74.255905,40.501269),
(-74.240799,40.495004),
(-74.220886,40.495004),
(-74.189301,40.511189),
(-74.118576,40.536764),
(-74.072571,40.567024),
(-74.038925,40.601441),
(-74.008026,40.572762),
(-73.985367,40.570154),
(-73.937302,40.569632),
(-73.915329,40.577456),
(-73.899536,40.599356),
(-73.879623,40.613431),
(-73.881683,40.626982),
(-73.865891,40.633757),
(-73.859024,40.633757),
(-73.818512,40.629067),
(-73.771133,40.631672) ]
    sector7=[(-73.769760,40.631151),
(-73.948975,40.553461),
(-73.942795,40.534677),
(-73.795166,40.561808),
(-73.777313,40.583192),
(-73.726501,40.603005),
(-73.699036,40.638967),
(-73.723755,40.648866),
(-73.768387,40.629067)]

    for trans in input_handle:
        #print(trans)
        each_day_list=[]
        each_day_data_temp=trans.split(',')
        #adding required data from the original data set to the list
        storage=''
        each_day_list.append(each_day_data_temp[1].strip())
        each_day_list.append(each_day_data_temp[2].strip())
        each_day_list.append(each_day_data_temp[3].strip())
        each_day_list.append(each_day_data_temp[5].strip())
        each_day_list.append(each_day_data_temp[6].strip())
        each_day_list.append(each_day_data_temp[9].strip())
        each_day_list.append(each_day_data_temp[10].strip())
        each_day_list.append(each_day_data_temp[18].strip())

        #calculate and add the distance to the list
        distance=beatrix.getDistance(each_day_data_temp[6],each_day_data_temp[5],each_day_data_temp[10],each_day_data_temp[9])

        if distance[0]> 0 and distance[1]>0:
            each_day_list.append(distance[0])
            each_day_list.append(distance[1])
        else:
            continue
        #identify the sector of the given coordinate

        y1=float(each_day_data_temp[9])
        y2=float(each_day_data_temp[10])
        sectorID=''
        if beatrix.point_in_poly(y1,y2,sector1):
            sectorID='sector1'
        elif  beatrix.point_in_poly(y1,y2,sector2):
            sectorID='sector2'
        elif beatrix.point_in_poly(y1,y2,sector3):
            sectorID='sector3'
        elif beatrix.point_in_poly(y1,y2,sector4):
            sectorID='sector4'
        elif beatrix.point_in_poly(y1,y2,sector5):
            sectorID='sector5'
        elif beatrix.point_in_poly(y1,y2,sector6):
            sectorID='sector6'
        elif beatrix.point_in_poly(y1,y2,sector7):
            sectorID='sector7'
        else :
            sectorID='not in New York'

        each_day_list.append(sectorID)

        #each_day_list.append(each_day_list)
        #storage=each_day_data_temp[1].strip()+','+each_day_data_temp[2].strip()
        total_month_data.append(each_day_list)
        for eachitem in each_day_list:
            storage=storage+str(eachitem)+','
        storage=storage.strip(',')
        storage=storage+'\n'

        #storage.strip(',')


        #print(storage)
        output.write(storage)
    print(str(datetime.now()))
    #for element in total_month_data:
     #   output.write(element)
    #print(total_month_data)


def correction_sector_ID():

    sector1=[(-73.767014,40.639488),
(-73.729248,40.644699),
(-73.717575,40.824202),
(-73.756714,40.840827),
(-73.765640,40.638446)]
    sector2=[(-73.861084,40.901058),
(-73.784866,40.659285),
(-73.765640,40.641573),
(-73.756027,40.886524),
(-73.769760,40.906767),
(-73.859711,40.901058)]
    sector3=[(-73.769073,40.639488),
(-73.796539,40.632193),
(-73.942795,40.876661),
(-73.914642,40.903134),
(-73.862457,40.900020),
(-73.774567,40.634278)]
    sector4=[(-73.771133,40.632714),
(-73.800659,40.631151),
(-73.970261,40.745176),
(-73.969574,40.723844),
(-73.983994,40.706669),
(-74.022446,40.699902),
(-74.016953,40.742575),
(-73.998413,40.778982),
(-73.980560,40.794578),
(-73.966141,40.822124),
(-73.959274,40.837710),
(-73.950348,40.863160),
(-73.943481,40.874584),
(-73.794479,40.630109)]
    sector5=[(-73.765640,40.633757),
(-73.804092,40.631151),
(-73.966827,40.741014),
(-73.968201,40.721242),
(-73.979874,40.707710),
(-73.996353,40.703025),
(-74.021759,40.698340),
(-74.029312,40.683242),
(-74.033432,40.675951),
(-74.034805,40.658764),
(-73.951035,40.646783),
(-73.868637,40.642615),
(-73.763580,40.633236)]
    sector6=[(-73.774567,40.631151),
(-73.856964,40.640530),
(-73.880310,40.641573),
(-73.944855,40.644699),
(-73.967514,40.647304),
(-74.033432,40.657201),
(-74.077377,40.650950),
(-74.137115,40.641051),
(-74.169388,40.641573),
(-74.206467,40.623334),
(-74.222260,40.563895),
(-74.247665,40.520585),
(-74.255905,40.501269),
(-74.240799,40.495004),
(-74.220886,40.495004),
(-74.189301,40.511189),
(-74.118576,40.536764),
(-74.072571,40.567024),
(-74.038925,40.601441),
(-74.008026,40.572762),
(-73.985367,40.570154),
(-73.937302,40.569632),
(-73.915329,40.577456),
(-73.899536,40.599356),
(-73.879623,40.613431),
(-73.881683,40.626982),
(-73.865891,40.633757),
(-73.859024,40.633757),
(-73.818512,40.629067),
(-73.771133,40.631672) ]
    sector7=[(-73.769760,40.631151),
(-73.948975,40.553461),
(-73.942795,40.534677),
(-73.795166,40.561808),
(-73.777313,40.583192),
(-73.726501,40.603005),
(-73.699036,40.638967),
(-73.723755,40.648866),
(-73.768387,40.629067)]

    k=0
    input=open('/home/vamsi/Databases_sqlLite/taxi_extract_2015_yellow_mar_3_processed.csv','r')
    output=open('/home/vamsi/Databases_sqlLite/correct/taxi_extract_2015_yellow_mar_3_processed_corrected.csv','w')
    for item in input:
        if k==0:
            k=k+1
            continue


        x=item.split(',')
        #print(x[5]+"---"+x[6])
        y1=float(x[5])
        y2=float(x[6])
        sectorID=''
        if beatrix.point_in_poly(y1,y2,sector1):
            sectorID='sector1'
        elif  beatrix.point_in_poly(y1,y2,sector2):
            sectorID='sector2'
        elif beatrix.point_in_poly(y1,y2,sector3):
            sectorID='sector3'
        elif beatrix.point_in_poly(y1,y2,sector4):
            sectorID='sector4'
        elif beatrix.point_in_poly(y1,y2,sector5):
            sectorID='sector5'
        elif beatrix.point_in_poly(y1,y2,sector6):
            sectorID='sector6'
        elif beatrix.point_in_poly(y1,y2,sector7):
            sectorID='sector7'
        else :
            sectorID='not in New York'

        x[10]=sectorID
        storage=''
        for eachitem in x:
            storage=storage+str(eachitem)+','
        storage=storage.strip(',')
        storage=storage+'\n'

        output.write(storage)



correction_sector_ID()
#fetch_csv_data()