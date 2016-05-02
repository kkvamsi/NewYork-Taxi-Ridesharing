__author__ = 'vamsi'
import merge_trips
import sqlite_import
import pandas as pd
from datetime import datetime
import mainMerge
def import_dataframe(poolsize):
        result_list_counter=0
        poolsize=str(poolsize)+'min'
        #change to 13 after total data is available
        for month in range(2,3):
            total_merges_month=0
            total_trans_month=0
            month_data=sqlite_import.import_month_data(month)
            df=pd.DataFrame(month_data,columns=['start_time','drop_time','passengers','pickup_long','pickup_lat','drop_long','drop_lat','cost','distance','time','sector','rideID'])
            df['start_time'] = pd.to_datetime(df['start_time'])
            df['drop_time'] = pd.to_datetime(df['drop_time'])

            df.index=df['start_time']

            if month<10:
                month=str(0)+str(month)
            elif month>=10 and month<13:
                month=str(month)

            if month=='01':
                param1='2015-'+(month)+'-01'
                param2 = '2015-' +(month)+'-31'
            elif month=='02':
                param1='2015-'+(month)+'-01'
                param2 = '2015-' +(month)+'-28'
            elif month=='03':
                param1='2015-'+str(month)+'-01'
                param2 = '2015-' +(month)+'-31'
            elif month=='04':
                param1='2015-'+str(month)+'-01'
                param2 = '2015-' +(month)+'-30'
            elif month=='05':
                param1='2015-'+str(month)+'-01'
                param2 = '2015-' +(month)+'-31'
            elif month=='06':
                param1='2015-'+str(month)+'-01'
                param2 = '2015-' +(month)+'-30'
            elif month=='07':
                param1='2015-'+str(month)+'-01'
                param2 = '2015-' +(month)+'-31'
            elif month=='08':
                param1='2015-'+str(month)+'-01'
                param2 = '2015-' +(month)+'-31'
            elif month=='09':
                param1='2015-'+str(month)+'-01'
                param2 = '2015-' +(month)+'-30'
            elif month=='10':
                param1='2015-'+str(month)+'-01'
                param2 = '2015-' +(month)+'-31'
            elif month=='11':
                param1='2015-'+str(month)+'-01'
                param2 = '2015-' +(month)+'-30'
            elif month=='12':
                param1='2015-'+str(month)+'-01'
                param2 = '2015-' +(month)+'-31'
            print(str(month))



            rng=pd.date_range(param1,param2,freq=poolsize)
                #print(len(rng))
            #print(rng)
            count=0
            if month=='02':
                exit_condition=5376#7900
            else:
                exit_condition=5952#8594
            l=180
            # for i in range(0,len(rng)):
            #     print(rng[i])

            #for l in range(180,8594):
            while l<=exit_condition:
                print("lvalue->"+str(l))
                x=1
                print("l value->"+str(l)+"->"+str(rng[l])+ " ->" +str(rng[l+x]))

                prev=l
                while x<=2:
                    print("-----------------------------------------")
                    print(x)

                    print(str(rng[prev]),str(rng[l+x]))

                    print("-----------------------------------------")
                    pooldata=df[rng[l]:rng[l+x]].values.tolist()
                    result_merges=mainMerge.merge_trips(pooldata,str(rng[prev]),str(rng[l+x]))

                    prev=l+x
                    x=x+1
                l=l+288
                #break





            print(total_merges_month)
            print(total_trans_month)

            print("month wise result,"+month)
            result_arrray=mainMerge.get_final_result()
            month_wise_results=[]
            month_wise_results.append(result_arrray)
            #result_list_counter=result_list_counter+1

            print("total merges")
            print(result_arrray[0])
            print("total transcations")
            print(result_arrray[1])
            #break

                #need to call merge algo with list as parameter from here
            #print(count)



            #print(range_result)
            # for day in range(1,31):
            #     for hour in range(0,24):
            #         minute_from=0
            #         minute_to=poolsize-1
            #         minute=0
            #         while minute<=60/poolsize:
            #             poolsize_data=pd.DataFrame.between_time(minute_from,minute_to)
            #             minute_from=minute_from+poolsize
            #             minute_to=minute_to+poolsize
            #             minute=minute+1




        #input_data= pd.read_csv('/home/vamsi/Databases_sqlLite/taxi_extract_2015_yellow_mar_3.csv')
        #input_data=pd.read(month_data)





import_dataframe(5)



