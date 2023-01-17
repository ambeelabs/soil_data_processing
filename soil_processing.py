import xarray as xr
import geopandas
from pymongo import MongoClient, GEOSPHERE, DESCENDING
import shapely.geometry
from pymongo.errors import BulkWriteError


def process_soil(
    filename,
    save=False,
    subset_cols=["ts", "soil_moisture_c1"],
    push_mongo=False,
    client_name="localhost",
    ttl=True,
):
    """
    Function to process soil data from NASA LPRM AMSR2 satellite.

    params:
    filename: name of the .nc4 file
    save: saves the dataframe in csv file if True
    subset_cols: columns to subset for dropna
    push_mongo: If True, data is pushed to mongodb (local client by default)
    client_name: If data needs to be pushed to remote client, the url can be passed in pymongo compatible format (srv url for example)
    ttl: Sets time to live for scantime, True by default.
    """
    nc = xr.open_dataset(filename)
    try:
        df = nc.to_dataframe().reset_index(drop=True)
        df = df[
            [
                "Longitude",
                "Latitude",
                "ts",
                "soil_moisture_c1",
                "soil_moisture_c2",
                "soil_moisture_x",
                "scantime",
            ]
        ]
    except:
        df = nc.to_dataframe().reset_index()
        df = df[
            [
                "Longitude",
                "Latitude",
                "ts",
                "soil_moisture_c1",
                "soil_moisture_c2",
                "soil_moisture_x",
                "scantime",
            ]
        ]
    df = df.dropna(subset=subset_cols)
    if df.shape[0] == 0:
        print("Data Empty")
        quit()
    else:
        print(df.head())
    # Convert K to Celsius
    df["soil_temperature"] = df["ts"].apply(lambda x: x - 273.15)
    if push_mongo == True:
        # Convert to Geopandas dataframe to get point object
        gdf = geopandas.GeoDataFrame(
            df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude)
        )
        # Convert to GEOJSON
        gdf["loc"] = gdf["geometry"].apply(lambda x: shapely.geometry.mapping(x))
    df_filename = filename.split(".")[0] + ".csv"
    if save == True:
        df.to_csv(df_filename, index=False)
    if push_mongo == True:
        # Create Connection
        if client_name == "localhost":
            client = MongoClient("localhost", 27017)
        else:
            client = MongoClient(client_name, maxPoolSize=5)
        db = client.satellite_data
        collection = db.soil
        # Create Geospatial index
        collection.create_index([("loc", GEOSPHERE)])
        # Create a TTL index
        if ttl == True:
            collection.create_index(
                [("scantime", DESCENDING)], expireAfterSeconds=7776000
            )
        else:
            collection.create_index([("scantime", DESCENDING)])
        print("connection_created")
        del gdf["Latitude"], gdf["Longitude"], gdf["geometry"]
        # Convert Geodataframe to dictionary
        data = gdf.to_dict(orient="records")
        # Insert Data
        try:
            collection.insert_many(data)
        except BulkWriteError as bwe:
            print(bwe.details)
            raise
        # Close Connection
        client.close()
        print("Inserted")
