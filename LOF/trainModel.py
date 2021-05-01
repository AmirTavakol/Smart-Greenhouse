""" following scipts fetches raw data from database, train LOF model to detect outlier """
import numpy as np
import LOF
import pandas as pd
import dbconnection
import json

        
class Train(object):
    def __init__(self):
        pass
    #%%
    """
    fetch data from database
    sort them alphabetically
    and make a DataFrame
    """
    def fetch_data(self,trainInterval_h):
        select_train = dbconnection.db_connection()
        myresult = select_train.getSensorData(trainInterval_h)
        # temp = []
        # for result in myresult:
        #     if result[0] not in ["ANE","PLV1","PLV2","PLV3","WV"]:
        #         temp.append(result)
        # myresult = temp
        self.sensors = [x[0] for x in myresult]
        self.sensors = np.unique(self.sensors)
        self.sensors.sort()
        
        self.df = pd.DataFrame(myresult,columns=['sensor','value','timeStamp','ID'])
    #%%    
    """
    train the model using last trainInterval_h sensor data except the latest sensor data.
    using latest sensor data as test data in 'predictor.py'
    "ANE","PLV1","PLV2","PLV3","WV" are exempt from model training.
    output: trained model to be exploit in the next step by ecaluator.py
            and a json file containing train data to be stored in db
    """   
    def train(self):
        measurements = []
        tModels = []
        sensorNames= []
        tModels_dict ={}
        #seprate each sensor's measurement from another
        for sensor in self.sensors:
            locals()[str(sensor)] = self.df.loc[self.df['sensor'] == sensor]
            locals()[str(sensor)] = locals()[str(sensor)].reset_index(drop = True)
            locals()[str(sensor)] = locals()[str(sensor)][1:]
                        
            measure = (locals()[str(sensor)])   
            if sensor in ["ANE","PLV1","PLV2","PLV3","WV"]:
                scores = [1]*len(measure)
                measure['isOutlier'] = scores
                
            else:
                #number of neighbors to be sent to LOF
                #it has to be proportional to number of measurements
                n_neighbors = (len(measure)-2)
                
                #creating a LOF class object and pass dataset to it
                data = LOF.LOF(measure['value'],n_neighbors)
                            
                #outlier detection of current data set
                anomalies, inliers, _ , scores = data.run()
                
                #model training using remaining inliers from previous step
                tModel = data.trainModel()
                tModels.append(tModel)
                #make a dictionary with format {sensor: model}
                tModels_dict[sensor] = tModel
                                
                measure['isOutlier'] = scores
            measurements.append(measure)
        #save train data    
        toSend = self.toJson(measurements)
        saveData = dbconnection.db_connection()
            
            
        print("\n\n\n\nmodel trained!\n\n\n\n")
        return tModels_dict
    #%%
    def toJson(self,measurements):
                
        output_dict = {}
        output_list =[]
        
        for measure in measurements:
            for m in range(1,len(measure)+1):
                output_dict['sensor'] = measure['sensor'][m]
                output_dict['value'] = measure['value'][m]
                output_dict['timestamp']=measure['timeStamp'][m].isoformat()
                output_dict['ID'] = str(measure['ID'][m])
                if measure['isOutlier'][m] == 1:
                    output_dict['isOutlier'] = False
                else:
                    output_dict['isOutlier'] = True
                c = output_dict.copy()
                output_list.append(c)

        with open('train_input.json', 'w') as outfile: 
            json.dump(output_list, outfile, indent = 4)
            