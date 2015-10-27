import pandas as pd
import numpy as np

df = pd.read_csv("pairs.csv")
db = pd.read_csv("latlong.csv")

def updateLat(port):
    port = db[db["Port"] == port]
    assert(port is not None)
    assert(port.shape == (1,3,))
    return port.iloc[0,1]

def updateLong(port):
    port = db[db["Port"] == port]
    assert(port is not None)
    assert(port.shape == (1,3,))
    return port.iloc[0,2]

def calcDistance(data):
    origin_lat = np.radians(data[0])
    origin_long = np.radians(data[1])
    dest_lat = np.radians(data[2])
    dest_long = np.radians(data[3])
    R = 6373. # in km
    dlon = dest_long - origin_long
    dlat = dest_lat - origin_lat
    a = (np.sin(dlat/2.))**2. + np.cos(origin_lat) * np.cos(dest_lat) * (np.sin(dlon/2))**2.
    c = 2 * np.math.atan2( np.sqrt(a), np.sqrt(1.-a) )
    d = R * c #(where R is the radius of the Earth)
    return d

df["Origin_lat"] = df["Origin"].apply(updateLat)
df["Origin_long"] = df["Origin"].apply(updateLong)
df["Dest_lat"] = df["Dest"].apply(updateLat)
df["Dest_long"] = df["Dest"].apply(updateLong)
df["Distance"] = df[["Origin_lat", "Origin_long", "Dest_lat", "Dest_long"]].apply(calcDistance, axis=1)
df = df.drop(["Origin_lat","Origin_long","Dest_lat","Dest_long"], axis=1)
df.to_csv("pairdistances.csv")
