db name: world_data
collection names: airports, meteorites, volcanoes, earthquakes

bash file should be ble to be run with the following command:
    
    $ bash load_mongo.sh
    
Query 1 should run nicely (if incompletely) with the following command:
    
    $ python Query1.py DFW LAX 500
    
Query 2 should run nicely without command line parameters, but if more detailed control is desired, the following command should serve as an example:

    $ python Query2.py volcanoes Altitude 1000 min 0 1000 -160.0,75.0

Please note: due to non-robust input validation and error checking, there are a good many queries that can break this particular program.

Query 3 has issues with Earthquakes and Meteorites due to the large amount of entries in those files, but should work fine with the following query:

    $ python Query3.py volcanoes 10 100
