# get coordinates from http://boundingbox.klokantech.com/
prague="14.213219,50.027152,14.600487,50.179976"
brno="16.523609,49.140393,16.72308,49.241138"
vienna="16.2565040588,48.1516571954,16.5438652039,48.2875335252"
brno_country="15.2545166016,48.6038576082,18.2427978516,49.8308962883"
krakow="19.777279,49.980371,20.122833,50.126741"
budapest="18.9079856873,47.4242547826,19.1980934143,47.5773363327"
dresden="13.606911,50.848874,14.266777,51.105678"
amsterdam="4.5751190186,52.2937824187,5.0173187256,52.6851240169"
bologna="11.1178207397,44.3852193805,11.5298080444,44.5899781896"
rimini="12.2706985474,43.8820573039,12.9312515259,44.2004203906"

export JAVA_OPTS="-Xmx6G -Xms1G -d64 -server"
export JAVACMD_OPTIONS="$JAVA_OPTS"

#IFS=', ' read -r -a coords <<< "$prague"
#osmosis/bin/osmosis --read-pbf "/home/kos/Downloads/czech-republic-latest.osm.pbf" --bounding-box left=${coords[0]} bottom=${coords[1]} right=${coords[2]}  top=${coords[3]} --mapfile-writer file="prague.osm.map" bbox="${coords[1]},${coords[0]},${coords[3]},${coords[2]}"

#IFS=', ' read -r -a coords <<< "$brno"
#osmosis/bin/osmosis --read-pbf "/home/kos/Downloads/czech-republic-latest.osm.pbf" --bounding-box left=${coords[0]} bottom=${coords[1]} right=${coords[2]}  top=${coords[3]} --mapfile-writer file="brno.osm.map"

#IFS=', ' read -r -a coords <<< "$vienna"
#osmosis/bin/osmosis --read-pbf "/home/kos/Downloads/austria-latest.osm.pbf" --bounding-box left=${coords[0]} bottom=${coords[1]} right=${coords[2]}  top=${coords[3]} --mapfile-writer file="vienna.osm.map"

#IFS=', ' read -r -a coords <<< "$brno_country"
#osmosis/bin/osmosis --read-pbf "/home/kos/Downloads/czech-republic-latest.osm.pbf" --bounding-box left=${coords[0]} bottom=${coords[1]} right=${coords[2]}  top=${coords[3]} --mapfile-writer file="brno.country.osm.map" bbox="${coords[1]},${coords[0]},${coords[3]},${coords[2]}"

#IFS=', ' read -r -a coords <<< "$krakow"
#osmosis/bin/osmosis --read-pbf "/home/kos/Downloads/poland-latest.osm.pbf" --bounding-box left=${coords[0]} bottom=${coords[1]} right=${coords[2]}  top=${coords[3]} --mapfile-writer file="krakow.osm.map" bbox="${coords[1]},${coords[0]},${coords[3]},${coords[2]}"

#IFS=', ' read -r -a coords <<< "$budapest"
#osmosis/bin/osmosis --read-pbf "/home/kos/Downloads/hungary-latest.osm.pbf" --bounding-box left=${coords[0]} bottom=${coords[1]} right=${coords[2]}  top=${coords[3]} --mapfile-writer file="budapest.osm.map" bbox="${coords[1]},${coords[0]},${coords[3]},${coords[2]}"

#IFS=', ' read -r -a coords <<< "$amsterdam"
#osmosis/bin/osmosis --read-pbf "/home/kos/Downloads/netherlands-latest.osm.pbf" --bounding-box left=${coords[0]} bottom=${coords[1]} right=${coords[2]}  top=${coords[3]} --mapfile-writer file="netherlands.osm.map" bbox="${coords[1]},${coords[0]},${coords[3]},${coords[2]}"

IFS=', ' read -r -a coords <<< "$bologna"
osmosis/bin/osmosis --read-pbf "/home/kos/Downloads/italy-latest.osm.pbf" --bounding-box left=${coords[0]} bottom=${coords[1]} right=${coords[2]}  top=${coords[3]} --mapfile-writer file="bologna.osm.map" bbox="${coords[1]},${coords[0]},${coords[3]},${coords[2]}"

IFS=', ' read -r -a coords <<< "$rimini"
osmosis/bin/osmosis --read-pbf "/home/kos/Downloads/italy-latest.osm.pbf" --bounding-box left=${coords[0]} bottom=${coords[1]} right=${coords[2]}  top=${coords[3]} --mapfile-writer file="rimini.osm.map" bbox="${coords[1]},${coords[0]},${coords[3]},${coords[2]}"



#IFS=', ' read -r -a coords <<< "$dresden"
#osmosis/bin/osmosis \
#    --read-pbf "/home/kos/Downloads/sachsen-latest.osm.pbf" \
#    --bounding-box left=${coords[0]} bottom=${coords[1]} right=${coords[2]}  top=${coords[3]} \
#    --mapfile-writer file="dresden.osm.map"


