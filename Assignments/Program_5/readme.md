db name: world_data
collection names: airports, meteorites, volcanoes, earthquakes

bash file should be ble to be run with the following command:
    
    $ bash load_mongo.sh
    
Query 1 should run nicely (if incompletely) with the following command:
    
    $ python Query1.py DFW LAX 500
    
Query 2 should run nicely without command line parameters, but if more detailed control is desired, the following command should serve as an example:

    $ python Query2.py 
