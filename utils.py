import requests
def download_image(url, image_file_path):
    r = requests.get(url, timeout=4.0)
    if r.status_code != requests.codes.ok:
        assert False, 'Status code error: {}.'.format(r.status_code)

    with Image.open(io.BytesIO(r.content)) as im:
        im.save(image_file_path)
    return image_file_path


def measure_distance(objects):
    # miss distance in km -(i['close_approach_data'][0]['miss_distance']['kilometers'])
    # miss distance in astronomical -(i['close_approach_data'][0]['miss_distance']['astronomical'])
    list_miss_distance=[]
    for i in objects:
        list_miss_distance.append(i['close_approach_data'][0]['miss_distance']['astronomical'])
    closest_distance=min(list_miss_distance)
    closest_distance_index=list_miss_distance.index(closest_distance)
    return objects[closest_distance_index]


def measure_distance_case_haz(objects):
    # miss distance in km -(i['close_approach_data'][0]['miss_distance']['kilometers'])
    # miss distance in astronomical -(i['close_approach_data'][0]['miss_distance']['astronomical'])
    list_miss_distance=[]
    for key,val in objects.items():
        list_miss_distance.append(val[0]['close_approach_data'][0]['miss_distance']['astronomical'])
    closest_distance=min(list_miss_distance)
    closest_distance_index=list_miss_distance.index(closest_distance)
    id_of_closest_miss_object=list(objects.keys())[closest_distance_index]

    return objects[id_of_closest_miss_object]





def get_relevant_data(closest_miss_distance_object,potential_hazardous):
    relevant_data_dict=dict()
    relevant_data_dict['name_of_object']=closest_miss_distance_object['name']
    relevant_data_dict['min_estimated_diametre_metres']=closest_miss_distance_object['estimated_diameter']['meters']['estimated_diameter_min']
    relevant_data_dict['max_estimated_diametre_metres']=closest_miss_distance_object['estimated_diameter']['meters']['estimated_diameter_max']
    relevant_data_dict['miss_distance_in_km'] =closest_miss_distance_object['close_approach_data'][0]['miss_distance']['kilometers']
    relevant_data_dict['orbit_class_description']=closest_miss_distance_object['orbital_data']['orbit_class']['orbit_class_description']
    relevant_data_dict['is_potential_hazardous']=potential_hazardous
    return relevant_data_dict
    #name_of_object,min_estimated_diametre_metres,max_estimated_diametre_metres,miss_distance_in_km,orbit_class_description


