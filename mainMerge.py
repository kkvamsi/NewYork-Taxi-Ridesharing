__author__ = 'vamsi'


# x=datetime.strptime('2015-01-01 00:15:52', "%Y-%m-%d %H:%M:%S")
# >>> y=datetime.strptime('2015-01-01 00:02:51', "%Y-%m-%d %H:%M:%S")
# >>> x-y
# datetime.timedelta(0, 781)
# >>> (x-y).total_seconds()
#

# (0)'start_time',(1)'drop_time',(2)'passengers',(3)'pickup_long',(4)'pickup_lat',(5)'drop_long',
# (6)'drop_lat',(7)'cost',(8)'distance',(9)'time',(10)'sector',(11)'rideID'
import collections
import postgres_conn
import helperMethods
import datetime


# global_time_list=[]
global_merged_list = []
# present_route_members_list=[]
present_route_request=''
walking_list=[]




def merge_trips(pooldata, from_stamp, to_stamp):
    global original_indiv_dist
    global distance_for_route
    global total_distance_merged
    distance_for_route=0
    total_distance_merged=0
    original_indiv_dist=0
    print("in main merge")
    print(len(pooldata))
    # print(pooldata)
    # for each in pooldata:
    #   print(each)

    unordered_dict = {}
    for each in pooldata:
        unordered_dict.update({each[11]: each})

    global_request_pool = collections.OrderedDict(
        sorted(unordered_dict.items(), key=lambda x: float(x[1][8]), reverse=True))

    while len(global_request_pool) > 0:
        for k in global_request_pool:
            print("greatest distance ID " + str(k))
            # print(global_request_pool[k])
            greatest_distance_key = k
            greatest_distance_request = global_request_pool[k]
            del global_request_pool[k]
            break
        present_route_request=''
        present_route_members_list = []
        present_route_members_list.append(greatest_distance_request)

        # generate a reequest to find time betwwen source and destination
        request_source_dest = create_param_graphhopper_req(present_route_members_list)
        time_for_source_dest = helperMethods.call_graphhopper_api(request_source_dest)[0]
        # print(time_for_source_dest/1000)
        time_for_source_dest = time_for_source_dest / 1000
        # adding distnace of first person to glaobla time list. this time list is used to check if a feasible path exists with vias

        # time_seconds=helperMethods.get_Time_Diff_seconds(str(greatest_distance_request[1]),str(greatest_distance_request[0]))
        global_time_list = []
        global_time_list.append(time_for_source_dest)
        ###print(global_time_list)
        nearest_neighbour_list=[]
        nearest_neighbour_list = postgres_conn.getnearest_destinations(greatest_distance_request[4],
                                                                       greatest_distance_request[5], from_stamp,
                                                                       to_stamp, greatest_distance_request[10])

        # print('Nearest neighbour list')
        # for ele in nearest_neighbour_list:
        #     print(ele)
        # print('End of nearest neighbour list')
        temp_counter = 0
        for each in nearest_neighbour_list:
            if each[1] == greatest_distance_key:
                del nearest_neighbour_list[temp_counter]
                break
            temp_counter = temp_counter + 1

        passenger = int(greatest_distance_request[2])
        temporary_route_members = []
        temporary_route_members.append(greatest_distance_request)

        while (passenger < 4 and len(nearest_neighbour_list) > 0):
            counter_temp=0

            nearest_neighbour_in_dict=[]
            for item in nearest_neighbour_list :
                if item[1] in global_request_pool:
                    #print(item)

                    nearest_neighbour = nearest_neighbour_list.pop(nearest_neighbour_list.index(item))

                    ###print("nearest neighbour is ->"+ str(nearest_neighbour[1]))
                    #nearest_neighbour_list.pop(0)
                    #print(nearest_neighbour)
                    nearest_neighbour_in_dict = global_request_pool[nearest_neighbour[1]]
                    #counter_temp=counter_temp+1
                    break
                else:
                     #nearest_neighbour_list[counter_temp]
                     nearest_neighbour_list.pop(nearest_neighbour_list.index(item))
                     #counter_temp=counter_temp+1

            if len(nearest_neighbour_in_dict)==0:

                ###print("in continue")
                break

            # for eachElement in nearest_neighbour_list:
            #     if eachElement[1] == global_request_pool[eachElement[1]][11]:
            #         nearest_neighbour = nearest_neighbour_list.pop(0)
            #         nearest_neighbour_in_dict = global_request_pool[nearest_neighbour[1]]
            #     else:
            #         nearest_neighbour_list.pop(0)
            temporary_route_members.append(nearest_neighbour_in_dict)
            req_string = create_param_graphhopper_req(temporary_route_members)
            #print(req_string)
            graphhopper_result=helperMethods.call_graphhopper_api(req_string)
            time_for_route_millisec = graphhopper_result[0]
            distance_for_route=graphhopper_result[1]
            time_for_route_sec = time_for_route_millisec / 1000

            temp_time_list = list(global_time_list)
            temp_time_list.append(time_for_route_sec)
            isPossible = helperMethods.check_request_possibility(temp_time_list)

            if isPossible:
                ###print("in possible")
                present_route_members_list.append(nearest_neighbour_in_dict)


                global_time_list.append(time_for_route_sec)
                present_route_request=req_string
                #print('possible->req_string')
                #print(present_route_request)
                # for eachGloval in global_request_pool:
                #     print(eachGloval)
                ###print("________________________________________")
                # delete nearest_neighbour_in_dict from global reqs lits
                ###print("deleting "+str(nearest_neighbour_in_dict[11]))
                #if(nearest_neighbour_in_dict[11] in global_request_pool):

                del global_request_pool[nearest_neighbour_in_dict[11]]
                ###print("deleted")
                passenger = passenger + int(nearest_neighbour_in_dict[2])
                nearest_neighbour_in_dict=[]

                # for eachGloval in global_request_pool:
                #     print(eachGloval)
                #print("________________________________________")

                ###for eachmemeber in temporary_route_members:
                    ###if eachmemeber[11]==2:
                       ### print("dummy statement")
                   ### print(eachmemeber[11])
                ###print(time_for_route_millisec / 1000)
                ###print(req_string)
                #print("--------------------------------------------------")


            else:
                ###print ("Not Possible ")
                del temporary_route_members[len(temporary_route_members) - 1]
                del temp_time_list[len(temp_time_list) - 1]


        #adding the presently feasible route to the global list
        ###print ("end of inner while")

        ##walking distance start
        # strategy<- assume that the walking distance accepted is 800 metres
        # fetch the route way points by calling the graphhopper request with vehicle=foot
        # calculate the distance between the points using haversine formula in global_pool_request and the way points which are less than 800 metres in distance
        #if the point is within specified distance then add the value to the present route
        #delete the request from the global_request_pool


        walking_list=list(present_route_members_list)
        if passenger<4 :
            while(passenger<=4):

                print('in the walking module')
                print(walking_list)
                #print(present_route_request)
                req_string_route=create_param_graphhopper_req(walking_list)
                #print(req_string_route)
                #make a call to the graphhopper module to get the way points
                waypoints_list=[]
                waypoints_list=helperMethods.fetch_waypoints_graphhopper(req_string_route)

                #print('waypoints')
                #print(waypoints_list)
                #for k,v in global_request_pool.items():
                 #   print(int(k)),print(v)

                for eachGlobalReq1 in global_request_pool:
                    if passenger<=4:
                        eachGlobalReq=global_request_pool[eachGlobalReq1]
                        for eachWaypoint in waypoints_list:
                            #print("present key ->"+str(eachGlobalReq1))
                            print(eachWaypoint)
                            #print(eachGlobalReq)
                            #print(eachWaypoint[0])
                            distance_waypt_globalPoolPt=helperMethods.haversine(float(eachWaypoint[0]),float(eachWaypoint[1]),float(eachGlobalReq[5]),float(eachGlobalReq[6]))
                            if(distance_waypt_globalPoolPt*1000<=400):
                                print("walking route on way found")
                                temp=list(eachGlobalReq)
                                present_route_members_list.append(temp)
                                passenger=passenger+int(eachGlobalReq[2])
                                del global_request_pool[eachGlobalReq[11]]
                                print("global request deleted as walking found")
                                break

                break



        for eachTrans in present_route_members_list:
            original_indiv_dist=original_indiv_dist+float(eachTrans[8])

        print("original distance->")
        print(original_indiv_dist)
        total_distance_merged=total_distance_merged+distance_for_route
        print('total merged distance->')
        print(total_distance_merged)
        print("present_route_members_list")
        print(present_route_members_list)
        global_merged_list.append(present_route_members_list)


    ###print(len(global_merged_list))
    ###print(global_merged_list)

def get_final_result():
    total_merges=0
    total_trans=0
    for gml in global_merged_list:
        total_merges=total_merges+1
        for i in gml:
            total_trans=total_trans+1
    result_merges=[]
    result_merges.append(total_merges)
    result_merges.append(total_trans)
    print('merge-Details')
    print('total_trans->'+str(total_trans))
    print('total_merges->'+str(total_merges))
    print('end-merge-details')
    return result_merges
    #print('total_trans->'+str(total_trans))
    #print('total_merges->'+str(total_merges))


                # temporary_route_members.reverse().pop()
                # temporary_route_members.reverse()
                # print()



                # for eachmemeber in temporary_route_members:
                #   print(eachmemeber[11])
                # print(time_for_route_millisec/1000)
                # print("--------------------------------------------------")
                # isPossible = create_param_graphhopper_req

                # if isPossible:
                #     present_route_members_list.append(nearest_neighbour_in_dict)
                #
                #
                #     time_seconds=helperMethods.get_Time_Diff_seconds(nearest_neighbour_in_dict[1],nearest_neighbour_in_dict[0])
                #     global_time_list.append(time_seconds)
                #     print(global_time_list)
                #
                #
                #
                #
                # else:
                #     temporary_route_members.pop(0)


                # print(temporary_route_members)











                # present_route_members_list.append(greatest_dist[0])


def create_param_graphhopper_req(temp_route_members):
    sourcelat = temp_route_members[0][4]
    sourcelong = temp_route_members[0][3]
    destlat = temp_route_members[0][6]
    destlong = temp_route_members[0][5]
    via_list = temp_route_members[1:]

    return helperMethods.create_via_request(via_list, sourcelat, sourcelong, destlat, destlong)

    times = helperMethods.call_graphhopper_api(req_string)

    if isPossible:
        print(req_string)
    return isPossible


if __name__ == '__main__':
    print()
    # test()
    # merge_trips()
