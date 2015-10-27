import pandas as pd
import numpy as np

df = pd.read_csv("../2007_shortened_weather.csv")
db = pd.read_csv("latlong.csv")
pairdb = pd.read_csv("pairdistances.csv")

latdict = pd.Series(db.Latitude.values,index=db.Port).to_dict()
longdict = pd.Series(db.Longtitude.values,index=db.Port).to_dict()

pairdb["Ports"] = pairdb["Origin"] + "," + pairdb["Dest"]
pairdict = pd.Series(pairdb.Distance.values,index=pairdb.Ports).to_dict()


def updateLat(port):
    return latdict[port]

def updateLong(port):
    return longdict[port]

def updateDistance(data):
    return pairdict[data[0]+","+data[1]]

print "Start"
df["OriginLat"] = df["Origin"].apply(updateLat)
print "OriginLat done"
df["OriginLong"] = df["Origin"].apply(updateLong)
print "OriginLong done"
df["DestLat"] = df["Dest"].apply(updateLat)
print "DestLat done"
df["DestLong"] = df["Dest"].apply(updateLong)
print "DestLong done"
df["Distance"] = df[["Origin", "Dest"]].apply(updateDistance, axis=1)
print "Distance done"

df.to_csv("2007_shortened_weather_distances.csv")
