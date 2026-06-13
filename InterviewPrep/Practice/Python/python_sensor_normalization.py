readings = [
    {"device_id": "d001", "timestamp": 1701000001, "temperature": 72.5, "humidity": 45.2, "pressure": 1013.1},
    {"device_id": "d002", "timestamp": 1701000002, "temperature": 68.1, "humidity": None, "pressure": 1012.4},
    {"device_id": "d001", "timestamp": 1701000003, "temperature": 75.3, "humidity": 48.1, "pressure": None},
    {"device_id": "d003", "timestamp": 1701000004, "temperature": 90.2, "humidity": 62.3, "pressure": 1015.2},
    {"device_id": "d002", "timestamp": 1701000005, "temperature": 69.4, "humidity": 44.8, "pressure": 1011.9},
    {"device_id": "d001", "timestamp": 1701000006, "temperature": 71.8, "humidity": 46.5, "pressure": 1013.8},
]

# 1. DEFINE -- "We need to go through, normalize the data into 0-1 scaling within 4 decimal spaces (i.e. lowest value = 0, highest = 1, everything else in between), ignore anything reading that has any missing fields, and return all the normalized data in a {device_id, timestamp, temperature, humidity, pressure} format."
# 2. EXPECTED OUTPUT:[
#     {"device_id": "d001", "timestamp": 1701000001, "temperature": 0.1490, "humidity": 0.0229, "pressure": .3636},
#     {"device_id": "d003", "timestamp": 1701000004, "temperature": 1.0, "humidity": 1.0, "pressure": 1.0},
#     {"device_id": "d002", "timestamp": 1701000005, "temperature": 0.0, "humidity": 0.0, "pressure": 0.0},
#     {"device_id": "d001", "timestamp": 1701000006, "temperature": 0.1154, "humidity": 0.0971, "pressure": .5756},
# ]

# min-max normalization "feature scaling"
# pressure = x(scaled) = (x - xmin)/(xmax-xmin) = (x - 1011.9)/3.3
# humidity = (x - 44.8)/17.5 
# temp = (x - 69.4)/20.8 = 

# 3. CONSTRAINTS --
# 4. MVP -- 
# 5. BREAK IT --

def data_norm(readings):
    norm_reading = []
    min_temp, max_temp = float('inf'), float('-inf')
    min_hum, max_hum = float('inf'), float('-inf')
    min_pres, max_pres = float('inf'), float('-inf')

    #check for incompelte data
    if not readings:
        print("Insufficient data")
        return[]
    
    #gathering relevant data and putting into appropriate format
    for record in readings:
        temp_1 = record['temperature']
        hum_1 = record['humidity']
        pres_1 = record['pressure']
        
        if temp_1 is None or hum_1 is None or pres_1 is None:
            continue
        else:
            clean_read = {"device_id": record['device_id'], "timestamp": record['timestamp'], "temperature": temp_1, "humidity": hum_1, "pressure": pres_1}
            norm_reading.append(clean_read)

            # check min max temperatures
            if temp_1 < min_temp:
                min_temp = temp_1
            if temp_1 > max_temp:
                max_temp = temp_1
            
            #check min max humidity
            if hum_1 < min_hum:
                min_hum = hum_1
            if hum_1 > max_hum:
                max_hum = hum_1
            
            #check min max pressure
            if pres_1 < min_pres:
                min_pres = pres_1
            if pres_1 > max_pres:
                max_pres = pres_1
    index = 0

    for record in norm_reading:
        result_temp = min_max_calc(min_temp, max_temp, record['temperature'])
        record['temperature'] = result_temp

        result_hum = min_max_calc(min_hum, max_hum, record['humidity'])
        record['humidity'] = result_hum
        
        result_pres = min_max_calc(min_pres, max_pres, record['pressure'])
        record['pressure'] = result_pres

    return norm_reading
    
def min_max_calc(min_val, max_val, x):
    denom = max_val - min_val
    numer = x - min_val
    
    if min_val == max_val:
        return 0.0
    else:
        value = numer/denom
        result = round(value, 4)
        return result
    
print(data_norm(readings))
