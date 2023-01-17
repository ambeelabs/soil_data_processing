from download_L2 import download_l2
from download_L3 import download_l3
from soil_processing import process_soil
import glob
import os


def process_l2(
    save=False,
    subset_cols=["ts", "soil_moisture_c1"],
    push_mongo=False,
    client_name="localhost",
    ttl=True,
):
    """
    Download and process l2 soil data
    Args:
    save: saves the processed data to csv if True,
    subset_cols: columns to subset for dropna,
    push_mongo: pushes to mongodb if True,
    client_name: name/url for mongodb, localhost by default,
    ttl: sets time to live for datetime index if True
    """
    download_l2()
    files = glob.glob("*.nc4")
    for file in files:
        process_soil(
            file,
            save=save,
            subset_cols=subset_cols,
            push_mongo=push_mongo,
            client_name=client_name,
            ttl=ttl,
        )
        try:
            os.remove(file)
        except Exception as e:
            print(e)


def process_l3(
    save=False,
    subset_cols=["ts", "soil_moisture_c1"],
    push_mongo=False,
    client_name="localhost",
    ttl=True,
):
    """
    Download and process l3 soil data
    Args:
    save: saves the processed data to csv if True,
    subset_cols: columns to subset for dropna,
    push_mongo: pushes to mongodb if True,
    client_name: name/url for mongodb, localhost by default,
    ttl: sets time to live for datetime index if True
    """
    download_l3()
    files = glob.glob("*.nc4")
    for file in files:
        process_soil(
            file,
            save=save,
            subset_cols=subset_cols,
            push_mongo=push_mongo,
            client_name=client_name,
            ttl=ttl,
        )
        try:
            os.remove(file)
        except Exception as e:
            print(e)
