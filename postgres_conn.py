__author__ = 'vamsi'


import psycopg2

# load the psycopg extras module
import psycopg2.extras

# Try to connect
def getnearest_destinations(longitude,latitude,from_stamp,to_stamp,sector):

#try:
    conn=psycopg2.connect("dbname='taxidata' user='vamsi' password='2311'")
#except:
#print ("I am unable to connect to the database.")

# If we are accessing the rows via column name instead of position we
# need to add the arguments to conn.cursor.
    ref_point=str(longitude)+' '+str(latitude)

    #print(ref_point)

    if(sector == 'sector1'):
        sector = 'sector = \'sector1\' or sector = \'sector2\''
    elif(sector == 'sector2'):
        sector = 'sector = \'sector1\' or sector=\'sector2\' or sector=\'sector3\''
    elif(sector == 'sector3'):
        sector = 'sector = \'sector2\' or sector=\'sector3\' or sector=\'sector4\''
    elif(sector == 'sector4'):
        sector = 'sector = \'sector3\' or sector=\'sector4\' or sector=\'sector5\''
    elif(sector == 'sector5'):
        sector = 'sector = \'sector4\' or sector=\'sector5\' or sector=\'sector6\''
    elif(sector == 'sector6'):
        sector = 'sector = \'sector5\' or sector=\'sector6\' or sector=\'sector7\''
    elif(sector == 'sector7'):
        sector = 'sector = \'sector6\' or sector = \'sector7\''


    query_string="""SELECT
ST_Distance(ST_GeomFromText('POINT("""+ref_point+""")', 4326), taxi_data.dropoff) AS planar_degrees,
ride_id,dropoff_longitude,dropoff_latitude,pickup_datetime,sector
FROM taxi_data where ("""+sector+""") and pickup_datetime between '"""+from_stamp+"""' and '"""+to_stamp+"""'
 ORDER BY planar_degrees ASC
LIMIT 100"""
    #print(query_string)


    #query_string='SELECT ST_Distance(ST_GeomFromText(POINT('+ref_point+'), 4326), taxi_data.dropoff) AS planar_degrees, ride_id,dropoff_longitude,dropoff_latitude FROM taxi_data ORDER BY planar_degrees ASC LIMIT 100;)'
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        #cur.execute("SELECT ST_Distance(ST_GeomFromText('POINT('+ref_point+')', 4326), taxi_data.dropoff) AS planar_degrees, ride_id,dropoff_longitude,dropoff_latitude FROM taxi_data ORDER BY planar_degrees ASC LIMIT 100;")
        cur.execute(query_string)
    except:
        print ("I can't SELECT from bar")

#
# Note that below we are accessing the row via the column name.

    rows = cur.fetchall()
    return rows
    #for row in rows:
     #   print(row)

if __name__=='main':
    getnearest_destinations(-73.9646530151367 , 40.5952606201172,'2015-01-01 00:00:00','2015-01-01 00:05:00','sector4')





## for back up only
# query_string1="""SELECT
# ST_Distance(ST_GeomFromText('POINT("""+ref_point+""")', 4326), taxi_data.dropoff) AS planar_degrees,
# ride_id,dropoff_longitude,dropoff_latitude,ride_id,dropoff_longitude,dropoff_latitude,pickup_datetime,sector
# FROM taxi_data where sector='"""+sector+"""' and pickup_datetime between '"""+from_stamp+"""' and '"""+to_stamp+"""'
#  ORDER BY planar_degrees ASC
# LIMIT 100"""

