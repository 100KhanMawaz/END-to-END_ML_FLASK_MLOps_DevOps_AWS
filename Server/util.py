import json
import pickle
import numpy as np

__location = None
__data_columns = None
__model = None

def get_estimated_price(total_sqft,bath,balcony,bhk,location):
    try:
        location_index = __data_columns.index(location.lower()) # In Numpy array we find like loc_index = np.where(x.columns==location)[0][0] but __data_columns is juts a python list so that's why here we find like this
    except:
        return print("Enter Correct location")

    arr = np.zeros(len(__data_columns))
    arr[0] = total_sqft
    arr[1] = bath
    arr[2] = balcony
    arr[3] = bhk
    arr[location_index] = 1
    return round(__model.predict([arr])[0],2) #since we are getting an array in return so basically [0] will get us 1st element in the array and we have only 1 element so why print as array. Also we are rounding our float data to 2 decimal places

def get_location_names():
    # by the time this function is called we have everything loaded in our __location variable
    load_saved_artifacts()
    return __location

def load_saved_artifacts():
    print("Loading Saved Artifacts...Start")
    global __data_columns  #we need to explicitely mention global otherwise it will create local variable
    global __location
    global __model

    with open("./Artifacts/columns.json",'r') as f:   #we are reading the file so we'll write r and it will loaded in a temporariry variable f
        __data_columns = json.load(f)['data_columns'] #since it is a JSON file we write json.load. Also inside the JSON file the particular Key we want to import is "data_columns" so we wrtie it explicitly
        __location = __data_columns[4:] #since our location starts with 4th Index so we are doing index slicing i.e starting from 4 take everything else

    with open("./Artifacts/Bangalore_house_prices_model.pickle",'rb') as f:     #since it is encoding in binary so we write read as binary i.e 'rb'
        __model = pickle.load(f) #since it is a Pickle file so we are doing Pickle.load

    print("Artifacts Loaded successfully")

if __name__ == '__main__':
    # We know the execution starts from main function so main function is calling load_saved_artifacts first then all the loading is done in global variables then we are calling get_location_names() which is just returning the __location and we printing it
    print(get_location_names())
    print(get_estimated_price(1000,3,3,3,'1st phase jp nagar'))
    print(get_estimated_price(1000, 2, 2, 2, '1st phase jp nagar'))
    print(get_estimated_price(1000, 2, 2, 2, '10th phase jp nagar'))
    print(get_estimated_price(1000, 2, 2, 2, 'iske upar wala bhi galat location ye bhi galat location'))
