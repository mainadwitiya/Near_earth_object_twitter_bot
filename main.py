#NeoWs API IMPLEMENTATION AND tWEEPY BOT
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("file.log")
formatter = logging.Formatter('%(asctime)s :: %(module)s :: %(levelname)s :: %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(f_format)
logger.addHandler(file_handler)
def logger_output(message,level=2):
   
    if level==1:
        logger.info(message)
    elif level==2:
        logger.info(message)
    elif level==3:
        logger.exception(message)

    return

import requests
import tweepy
from datetime import datetime
import pytz
from utils import measure_distance,get_relevant_data,measure_distance_case_haz
from configparser  import ConfigParser





parser = ConfigParser()
parser.read('config.ini')
APIKEY =str(parser.get('DEFAULT', 'TWITTER_APIKEY'))
APISECRET = str(parser.get('DEFAULT', 'APISECRET'))
ACCESS_TOKEN = str(parser.get('DEFAULT', 'ACCESS_TOKEN'))
ACCESS_TOKEN_SECRET = str(parser.get('DEFAULT', 'ACCESS_TOKEN_SECRET'))
demo_key=str(parser.get('NEOWS', 'API_KEY'))
feed_today=f'https://api.nasa.gov/neo/rest/v1/feed/today?detailed=true&api_key={demo_key}'
auth = tweepy.OAuthHandler(APIKEY, APISECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
UTC = pytz.utc
timeZ_Ny = pytz.timezone('America/New_York')
dt_Ny = datetime.now(timeZ_Ny)
utc_Ny = dt_Ny.astimezone(UTC)
date_ny_today=utc_Ny.strftime('%Y-%m-%d')
data = requests.get(feed_today).json()

def return_object_for_tweet():
    if potential_hazardous==True:
        if len(potential_hazardous_asteroid_dict)==1:
            object_id = next(iter(potential_hazardous_asteroid_dict))
            potential_hazardous_asteroid_dict1=potential_hazardous_asteroid_dict[object_id]
            #print(potential_hazardous_asteroid_dict1[0])
            return get_relevant_data(potential_hazardous_asteroid_dict1[0],potential_hazardous)
        else:
            closest_miss_distance_object=measure_distance_case_haz(potential_hazardous_asteroid_dict)
            object_id = next(iter(closest_miss_distance_object))
            return get_relevant_data(closest_miss_distance_object[0],potential_hazardous)
            
    else:
        closest_miss_distance_object=measure_distance(current_date_objects)
        object_id = next(iter(closest_miss_distance_object))
        return get_relevant_data(closest_miss_distance_object,potential_hazardous)

#--------------------------------------------------------------------------------------------------------------------------------

current_date_objects=data['near_earth_objects'][str(date_ny_today)]
potential_hazardous=False
potential_hazardous_asteroid_dict={}
for i in current_date_objects:
    if (i['is_potentially_hazardous_asteroid'])==True:
        key = i['id']
        if key not in potential_hazardous_asteroid_dict:
            potential_hazardous_asteroid_dict[key] = []
        potential_hazardous_asteroid_dict[key].append(i)
        potential_hazardous=True

       
tweet_data=return_object_for_tweet()


name=tweet_data['name_of_object']
min_dia=tweet_data['min_estimated_diametre_metres']
max_dia=tweet_data['max_estimated_diametre_metres']
hazardous=tweet_data['is_potential_hazardous']
miss_dist_km=tweet_data['miss_distance_in_km']
class_desc=tweet_data['orbit_class_description']
header=f'Near Earth Object for today.\nName - {name}\nMin & max diametre {min_dia,max_dia}mt\nPotential Hazardous-{hazardous}\nMiss Distance {miss_dist_km}kms\nClass- {class_desc}\n#NASA,#asteroid'
if len(header)>280:
    header=f'Near Earth Object for today.\nName - {name}\nMin and max diametre in mtrs {min_dia,max_dia}\nPotential Hazardous-{hazardous}\nMiss Distance in kms {miss_dist_km}\n#NASA,#asteroid'


post_result = api.update_status(status=header)
#print(post_result)
logger_output(f"Logging info{header}",level=1)