__author__ = 'vamsi'

import json
#import postgres_conn
import operator
from collections import defaultdict
import requests
#/home/vamsi/Desktop/taxi_dbms/nyctaxisub.csv


def getData_fromDB(pool_size,customers_willing_walk):
    print('in getdata from db')

def mergeTrips(pool_size,):
    print('in merge Trips')


def getDistance(plat,plong,dlat,dlong):
    requestString='http://localhost:8989/route?point='+str(plat)+'%2C'+str(plong)+'&point='+str(dlat)+'%2C'+str(dlong)+'&vehicle=car'
    #print(requestString)
    #r=requests.get('http://localhost:8989/route?point=41.8789%2C-87.6359&point=41.8916%2C-87.6045&vehicle=car')
    r=requests.get(requestString)

    res=json.loads(r.text)

    return_list=[]
    if('paths' in res):
        return_list.append(res['paths'][0]['distance'])
        return_list.append(res['paths'][0]['time'])
        return return_list
    else:
        return_list.append(-250)
        return_list.append(-250)
        return return_list
    #http://localhost:8989/route?point=41.8789%2C-87.6359&point=41.8916%2C-87.6045&vehicle=foot&points_encoded=false&instructions=false
    #http://localhost:8989/info




#Used to label the given points based on different sectors
def clustering():
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

    entryMap={} #contains the list of transactions categorized by each sector -> key -> sectornumber; value->list of all transactions for each sector

    for i in range(1,8):
        sectorID='sector'
        sectorID=sectorID+str(i)
        print(sectorID)
        entryMap.update({sectorID:[]})
    entryMap.update({'not in New York':[]})
    sectorlist=[]
    sectorlist.append("sector1")
    sectorlist.append("sector2")
    sectorlist.append("sector3")
    sectorlist.append("sector4")
    sectorlist.append("sector5")
    sectorlist.append("sector6")
    sectorlist.append("sector7")

    sourcedata=open('/home/vamsi/Databases_sqlLite/taxi_extract_2015_yellow_mar_3_sorted.csv','r')
    for trans in sourcedata:
        x=trans.split(',')
        y1=float(x[9])
        y2=float(x[10])



        if point_in_poly(y1,y2,sector1):
            entryMap['sector1'].append(trans)
        elif point_in_poly(y1,y2,sector2):
            entryMap['sector2'].append(trans)
           # print('sector2')
        elif point_in_poly(y1,y2,sector3):
            entryMap['sector3'].append(trans)
            # print('sector3')
        elif point_in_poly(y1,y2,sector4):
            x=entryMap['sector4']
            x.append(trans)
            #print('sector4')
        elif point_in_poly(y1,y2,sector5):
            entryMap['sector5'].append(trans)
            #print('sector5')
        elif point_in_poly(y1,y2,sector6):
            entryMap['sector6'].append(trans)
            #print('sector6')
        elif point_in_poly(y1,y2,sector7):
            entryMap['sector7'].append(trans)
            #print('sector7')
        else :
            entryMap['not in New York'].append(trans)
            #print('not in New York')

    for k,v in entryMap.items():
        print(k,len(v))


#not used in the implementation
def sort_date_time():
    reference=open('/home/vamsi/Documents/Spring2016/DBMS/TaxiSharing/dataset_taxisharing/trip_data_1_output.csv','r')
    output= open('/home/vamsi/Documents/Spring2016/DBMS/TaxiSharing/dataset_taxisharing/trip_data_1_output_sorted.csv','w')
    x=[]
    for trans in reference:
        x.append(trans)

    x.sort(key=operator.itemgetter(1))

    for each in x:
        output.write(each)




def sample():
    count=0
    with  open('/home/vamsi/Downloads/yellow_tripdata_2015-01.csv','r') as sample_data:

        for trans in sample_data:
            count=count+1
            print(trans)
            if count>10:
                break


def extract_rides_from_airport():
   i=0
   k=0
   output= open('/home/vamsi/Documents/Spring2016/DBMS/TaxiSharing/dataset_taxisharing/extracts/trip_data_5_output.csv','w')
   #with  open('/home/vamsi/Documents/Spring2016/DBMS/TaxiSharing/dataset_taxisharing/trip_data_2.csv','r') as taxi:

   poly=[
(-73.822117,40.659676),
(-73.818512,40.660717),
(-73.811302,40.660327),
(-73.811131,40.662280),
(-73.807182,40.663322),
(-73.803062,40.664233),
(-73.798428,40.663843),
(-73.790359,40.662931),
(-73.780746,40.660717),
(-73.773365,40.657983),
(-73.766499,40.654988),
(-73.760834,40.651211),
(-73.755169,40.647304),
(-73.748989,40.642224),
(-73.751907,40.636362),
(-73.760147,40.632063),
(-73.766155,40.628155),
(-73.771820,40.625940),
(-73.782120,40.626200),
(-73.784351,40.622161),
(-73.788643,40.622943),
(-73.782806,40.629067),
(-73.786411,40.632063),
(-73.792419,40.636362),
(-73.802032,40.640530),
(-73.813534,40.644568),
(-73.819542,40.648085),
(-73.821774,40.652383),
(-73.822117,40.659285)]

   with  open('/home/vamsi/Downloads/yellow_tripdata_2015-05.csv','r') as taxi:

    for trans in taxi:
        x=trans.split(',')
        k=k+1
        #if x[5].startswith('-73.77') and x[6].startswith('40.63'):   #jfk 40.63,-73.77
        if k>1:
            y1=float(x[5])
            y2=float(x[6])

            if point_in_poly(y1,y2,poly):
                output.write(trans)
            #print(trans)
        #print(x)
        #print(x[11]+"->"+x[10])
        #print(type(trans[10]))
        #i=i+1
        #if(i==30000):
         #  break

def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside


#x=getDistance(40.639488,-73.767014,40.636362,-73.792419)
#print(str(x))
#clustering()
#extract()
#sample()
#sort_date_time()

