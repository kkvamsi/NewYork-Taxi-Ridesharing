from datetime import datetime
from math import radians, cos, sin, asin, sqrt

__author__ = 'vamsi'

import requests
import json
#via_list contains intermediate points in decreasing order from airport
#source contains the coordinates of airport
#destination contains the longest point coordinates
#this function is creates a url for grasshopper to get the details for via route
def create_via_request(via_list,sourcelat,sourcelong,destlat,destlong):
    request_string=''
    #'http://localhost:8989/route?point=41.8789%2C-87.6359&point=41.8916%2C-87.6045&vehicle=car'
    #http://localhost:8989/?point=jfk&point=manhattan&point=new%20jersey&locale=en-US&vehicle=car&weighting=fastest&elevation=false&layer=Omniscale
    via_string=''
    for each in via_list:
        #temp=[]
        #temp=each.split(',')
        via_string=via_string+each[6]+'%2C' #lat
        via_string=via_string+each[5]+'&point=' #long
    request_string='http://localhost:8989/route?point='+sourcelat+'%2C'+sourcelong+'&point='+via_string+destlat+'%2C'+destlong
    return request_string



def get_Time_Diff_seconds(destTime,sourceTime):
    #global_time_list.append(datetime.strptime(greatest_distance_request[1], "%Y-%m-%d %H:%M:%S")-datetime.strptime(greatest_distance_request[0], "%Y-%m-%d %H:%M:%S").total_seconds())
    time1=datetime.strptime(destTime, "%Y-%m-%d %H:%M:%S")
    time2=datetime.strptime(sourceTime, "%Y-%m-%d %H:%M:%S")
    return (time1-time2).total_seconds()




def call_graphhopper_api(request_string_to_grasshopper):
     r=requests.get(request_string_to_grasshopper)
     result=json.loads(r.text)
     #print(result)
     list_time_distance=[]
     if result is None:
         time_new=9999999999
         distance_new=9999999999
         list_time_distance.append(time_new)
         list_time_distance.append(distance_new)
         return list_time_distance
     if 'paths' not in result:
         time_new=9999999999
         distance_new=9999999999
         list_time_distance.append(time_new)
         list_time_distance.append(distance_new)

         return list_time_distance
     else:
         distance_new=result['paths'][0]['distance']
         time_new=result['paths'][0]['time']
         list_time_distance.append(time_new)
         list_time_distance.append(distance_new)
         #print(str(distance_new)+"->"+str(time_new))
         return list_time_distance

#checks for the feasibility of rides based on time taken for each ride
#returns true or false
def check_request_possibility(time_list):
    isPossible=True
    n=len(time_list)
    for i in range(0,n-1):
        if not (float(time_list[n-1])-float(time_list[i])<=0.5*(float(time_list[i]))):
            isPossible=False
            break
    return isPossible


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km

def fetch_waypoints_graphhopper(request):
    request=request+'&points_encoded=false'
    response=requests.get(request)
    waypoint_response=json.loads(response.text)
    waypoint_data=waypoint_response['paths'][0]['points']['coordinates']

    #if 'paths' in waypoint_data:

    return waypoint_data
    #else:
     #   print('----------------------------------null')
      #  x=[]
       # x.append([0,0])
        ##x=[[0,0]]
        #return x


if __name__=='__main__':

    waypoints=fetch_waypoints_graphhopper('http://localhost:8989/route?point=40.64658%2C-73.789749&point=40.713993%2C-74.00602&point=40.762081%2C-73.965797&point=40.73278%2C-73.984711&locale=en-US&vehicle=car&weighting=fastest&elevation=false&layer=Omniscale&calc_points=true&points_encoded=false')
    print(waypoints)
    # for each in waypoints:
    #     print(each)
    #print(check_request_possibility([30,35,40]))

    sourcelat='40.645362854003906'
    sourcelong='-73.776687622070313'
    destinationlat= '40.595260620117188'
    destinationlong='-73.964653015136719'
    list_via=['-73.781890869140625,40.644706726074219','-73.781890869140625,40.644706726074219']
    #reuest_string=create_via_request(list_via,sourcelat,sourcelong,destinationlat,destinationlong)
    #call_graphhopper_api(reuest_string)


