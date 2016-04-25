# get coordinates from http://boundingbox.klokantech.com/
prague="14.213219,50.027152,14.600487,50.179976"
brno="16.523609,49.140393,16.72308,49.241138"


export JAVA_OPTS="-Xmx6G -Xms1G -d64 -server"
export JAVACMD_OPTIONS="$JAVA_OPTS"

IFS=', ' read -r -a coords <<< "$prague"
osmosis/bin/osmosis --read-pbf "/home/kos/Downloads/czech-republic-latest.osm.pbf" --bounding-box left=${coords[0]} bottom=${coords[1]} right=${coords[2]}  top=${coords[3]} --mapfile-writer file="prague.osm.map" bbox="${coords[1]},${coords[0]},${coords[3]},${coords[2]}"

IFS=', ' read -r -a coords <<< "$brno"
osmosis/bin/osmosis --read-pbf "/home/kos/Downloads/czech-republic-latest.osm.pbf" --bounding-box left=${coords[0]} bottom=${coords[1]} right=${coords[2]}  top=${coords[3]} --mapfile-writer file="brno.osm.map"


