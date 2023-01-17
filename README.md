# README #

These scripts download nc4 soil satellite data from NASA LPRM_AMSR2_DS_SOILM and process it. 
You can save the processed data to a csv file or you can push it to mongodb(local/srv).

### How do I get set up? ###

* Install packages from requirements.txt
* Install external dependency for shapely in case of error https://shapely.readthedocs.io/en/stable/installation.html
* Dependencies


### Example Usage ###

#### Download and process Level 2 data ####
```
from main import process_l2

process_l2(save=True, push_mongo=True, ttl=True)
```

#### Download and process Level 3 data ####
```
from main import process_l3

process_l3(save=True, push_mongo=True, ttl=True)
```

#### Download Level 2 data ####
```
from download_L2 import download_l2

download_l2()
```

#### Download Level 3 data ####
```
from download_L2 import download_l3

download_l3()
```

#### Download 1 year historical data and process ###
```
from download_yearly import download_yearly
from soil_processing import process_soil
import glob

download_yearly(2022)
files = glob.glob("*.nc4")
for file in files:
	process_soil(
	    file,
	    save=True,
	)
```
