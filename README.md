#NewYork-Taxi-Ridesharing
Team-8 submission

<b>Links for obtaining the database files in zipped format:https://drive.google.com/open?id=0BworjGnztGcSR1pUdkV0cTRfSlk</b>
<ul>
<li>Please note that access to this file restricted to people with UIC domain login</li><br>
<li>Also note that the files are large and need to be uncompressed for further usage</li>
</ul>

The steps to use this API is :
Download the Java based implementation from the following link:
https://github.com/graphhopper/graphhopper/blob/0.6/docs/web/quickstart.md

Follow the instructions in this link and use the New York based OSM instead of the default instructions used in the Graphhopper Page.
The New York OSM file can be obtained from :
http://download.geofabrik.de/north-america/us/new-york.html

Change the configurations:
Need to change the configuration file to enable walking based calculations to the calculations:
Navigate to config-example.properties file in Graphhopper folder and change : graph.flagEncoders=car , add foot to this statement.
Start GraphHopper by using this command in Command Prompt or teminal: 
java -jar *.jar jetty.resourcebase=webapp config=config-example.properties osmreader.osm=new-york-latest.osm

Please note that Graphhopper must be running all the time while algorithm is running.


