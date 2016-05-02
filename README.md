#NewYork-Taxi-Ridesharing
Team-8 submission

 To run the code locally, please follow these steps:

- Below are the steps to run the source code to perform more trials and conduct simulations for all the algorithms:
    The steps to use this API is :
- Download the Java based implementation from the following link:
    https://github.com/graphhopper/graphhopper/blob/0.6/docs/web/quickstart.md

Follow the instructions in this link and use the New York based OSM instead of the default instructions used in the Graphhopper Page.
- The New York OSM file can be obtained from :
  http://download.geofabrik.de/north-america/us/new-york.html

Change the configurations:
- Need to change the configuration file to enable walking based calculations to the calculations:
- Navigate to config-example.properties file in Graphhopper folder and change : graph.flagEncoders=car , add foot to this statement.
- Start GraphHopper by using this command in Command Prompt or teminal: 
java -jar *.jar jetty.resourcebase=webapp config=config-example.properties osmreader.osm=new-york-latest.osm

- Please note that Graphhopper must be running all the time while algorithm is running.

- Download PostgreSQL with GIS and SQLite. Additionally, download SQLite Browser.
Set up a username and password in PostgreSQL.

- Import taxishare_post.sql file in PostgreSQL and taxi_data.db file in   SQLite.
The database related dumps are available from https://drive.google.com/open?id=0BworjGnztGcSR1pUdkV0cTRfSlk.

- Import the downloaded files from Google Drive and uncompress them.Import them into Postgres and SQLite having corresponding names as their file names

- Open the Source folder in any Python IDE configured to Python 3.4.

- Change the path of the sql file located and also username and password of PostgreSQL database in postgres_conn.py file.

- Similarly, change the path of the db file located in sqlite_import.py file.

- In getPandas.py file, in Line 17 change the month you would like to run the experiment for,
    Eg: For Jan (1,2) , Jan to April (1,5).
  Change the parameter for pool size in line - 146.  eg.(5,10,15,20 poolsizes)

