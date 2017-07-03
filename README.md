# google_kml_to_locus_gpx
Convert google kml to gpx format with locus extensions

## checkout and compile CutyCapt
```
sudo apt-get install qt5-default qt5-qmake libqt5svg5-dev libqt5webkit5-dev

svn checkout svn://svn.code.sf.net/p/cutycapt/code/ cutycapt-code
cd cutycapt-code/CutyCapt
qmake
make

```

## set env 
```
export CUTYCAPT=<path to cuty-capt directory>
```

## run
```
python locus__kml_to_gpx.py -i doc.kml  -o out.gpx
```

# UPD

mapsforge-map-writer-0.6.0.jar
Osmosis Version 0.44.1

