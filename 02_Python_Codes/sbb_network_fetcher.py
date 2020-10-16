import pySBB
import datetime
import numpy as np
import pandas as pd
import requests 


def con_gen(start_data,end_date,station_array):
     
    time_array = np.arange(np.datetime64(start_data), np.datetime64(end_date),step=7)
    time_array = np.datetime_as_string(time_array)
    
    station_time_combis = [(x,y,time) for x in station_array for y in station_array for time in time_array if x != y]
    
    return list(station_time_combis)

def sbb_station_list_gen(connections):
    objects = []
    for connection in connections:
        for i in connection.sections:
            for passlist in i.journey.passList:
            
                station = passlist.station
                arrival = passlist.arrival
                departure = passlist.departure
                lat = station.coordinate.x
                lon = station.coordinate.y
            
                objects.append([str(station),str(arrival),str(departure),lat,lon])
     
    
    for i,objec in enumerate(objects):
        try:
            if objects[i][2] == str(None) and objects[i][1] != str(None):
                objec.append("end-station")
            
            elif objects[i][1] == str(None) and objects[i][2] == str(None):
                objec.append(objects[i+1][0])
                
            else:
                
                objec.append(objects[i+1][0])
        
        except:
            ""
        
        
    return objects

def get_the_sbb_network(station_time_combis):
    stationlist = []
    times = ["00:00","09:00","13:00","17:00","21:00"]
    
    for combi in station_time_combis:
        for time in times:
            try:
                connection = pySBB.get_connections(str(combi[0]), str(combi[1]), limit=15, date = str(combi[2]), time = time)
            
                stationlist = stationlist + sbb_station_list_gen(connection)
            except:
                ""
        
    return stationlist


if __name__ == "__main__":

    comb = con_gen("2020-03-09","2020-05-05",["Basel","Zürich","Luzern","Bern","Genf","Locarno","Davos"])

    print(comb)

    print("start")
    network = get_the_sbb_network(comb)
    print("end")

    df = pd.DataFrame(network,columns =['from', 'arrival',"departure","lat","lon","to"]) 


    df.to_csv(r"sbb_network_output.csv",encoding="utf-8")