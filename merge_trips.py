__author__ = 'vamsi'
import  postgres_conn
import requests
def merge_trips(pooldata,from_stamp,to_stamp):
    # will get list of trips for a given poolsize
    merged_request = set()
    #(0)'start_time',(1)'drop_time',(2)'passengers',(3)'pickup_long',(4)'pickup_lat',(5)'drop_long',
    # (6)'drop_lat',(7)'cost',(8)'distance',(9)'time',(10)'sector',(11)'rideID'

    print("in merge trips")
    totalpooldata=[]

    #for item in pooldata:
       # print(item)

    # initialize a hash map with all sectors as keys
    sectorMap={}
    for i in range(1,8):
        sectorID='sector'
        sectorID=sectorID+str(i)
        #print(sectorID)
        sectorMap.update({sectorID:[]})
    sectorMap.update({'not in New York':[]})
    dist_sorted_entrymap={}
    #segregate all the entries that belong to a certain sector in the sectormap
    for eachitem in pooldata:
        sectorMap[eachitem[10]].append(eachitem)

    #testing if all the entries are satisfying the given condition according to above step
    #for k,v in sectorMap.items():
        #print(k+'->'+str(len(v)))

    #order the given transactions in a sector in the decreasing order of distance
    #eachsector is the sector in the map
    for eachsector,sectorlist in sectorMap.items():
        dist_sorted_entrymap[eachsector]=sorted(sectorlist,key=getkey,reverse=True)

    #checking if the given dict contains the sorted values according to distance
    for each_req_sector in dist_sorted_entrymap:
        x=dist_sorted_entrymap[each_req_sector]
        #for item in x:
        #print(x)

    # now take each sector from the sorted dict and check the next nearest destination from the present location
    #  in the sector .
    #check if the value can be merged with the existing trips
    del dist_sorted_entrymap['not in New York']
    for eachsector in dist_sorted_entrymap:
        print("in for loop")
        print(eachsector)
        #getnearest_destinations(longitude,latitude,from_stamp,to_stamp,sector)
        temporary_merged_list = []
        temporary_added_passengers=0
        #temporary_time_constraint=    # this is the minimum of the constraint times of all the requests added till now
        for each_req_sector in dist_sorted_entrymap[eachsector]:
 #           print("in inner for loop")
#            print(each[5]+'-' +each[6]+'-'+each[10])
            #here the code to be written for calling the nearest ride from the longest distance
            #Declaring variables for usage in the processing of one merged trip

            if(len(each_req_sector)<1 or each_req_sector[2]>3):
                continue

            if(each_req_sector[11] in merged_request):
                continue
            temporary_merged_list.append(each_req_sector[11])
            temporary_added_passengers=temporary_added_passengers+each_req_sector[2]

             # call the nearest neighbour in postgres_conn and receive the value returned as list of list
            nearest_neighbours=postgres_conn.getnearest_destinations(each_req_sector[5],each_req_sector[6],from_stamp,to_stamp,each_req_sector[10])
            # write code to find if a nearest neighbour can be merged 'via' route



        #print()
def getkey(item):
    return item[8]


def get_via_points():
    #r=requests.get('http://localhost:8989/route?point=41.8789%2C-87.6359&point=41.8916%2C-87.6045&vehicle=car')
    print("in get-via-points")




if __name__=='__main__':
    merge_trips()

 #(0)'start_time',(1)'drop_time',(2)'passengers',(3)'pickup_long',(4)'pickup_lat',(5)'drop_long',
    # (6)'drop_lat',(7)'cost',(8)'distance',(9)'time',(10)'sector',(11)'rideID'