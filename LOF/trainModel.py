""" following scipts fetches raw data from database, train LOF model to detect outlier """
import numpy as np
import LOF
import pandas as pd
import dbconnection

        
class Train(object):
    def __init__(self):
        pass
    #%%
    """
    fetch data from database
    sort them alphabetically
    and make a DataFrame
    "ANE","PLV1","PLV2","PLV3","WV" are exempt 
    """
    def fetch_data(self,trainInterval_h):
        select_train = dbconnection.db_connection()
        myresult = select_train.getSensorData(trainInterval_h)
        temp = []
        for result in myresult:
            if result[0] not in ["ANE","PLV1","PLV2","PLV3","WV"]:
                temp.append(result)
        myresult = temp
        self.sensors = [x[0] for x in myresult]
        self.sensors = np.unique(self.sensors)
        self.sensors.sort()
        
        self.df = pd.DataFrame(myresult,columns=['sensor','value','timeStamp','ID'])
    #%%    
    """
    train the model using last 8h sensor data except the latest sensor data
    using latest sensor data as test data in 'predictor.py'
    output: trained model
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
            measurements.append(locals()[str(sensor)])
            
            measure = (locals()[str(sensor)])   
            
            #number of neighbors to be sent to LOF
            #it has to be proportional to number of measurements
            n_neighbors = (len(measure)-2)
            
            #creating a LOF class object and pass dataset to it
            data = LOF.LOF(measure['value'],n_neighbors)
                        
            #outlier detection of current data set
            anomalies, inliers,_ = data.run()
            
            #model training using remaining inliers from previous step
            tModel = data.trainModel()
            tModels.append(tModel)
            #make a dictionary with format {sensor: model}
            tModels_dict[f'{sensor}'] = tModel
            
        print("\n\n\n\nmodel trained!\n\n\n\n")
        return tModels_dict
