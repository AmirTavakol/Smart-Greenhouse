"""following script gets latest traiend model and evaluate test_data as either 'inlier' or 'outlier' for each sensor"""
import numpy as np
import datetime
import pandas as pd
import logging
import json
import sys
import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import dbconnection

class predict(object):
    def __init__(self,model):
        self.model = model
    #%%
    """
    fetch data from database
    sort them alphabetically
    and make a DataFrame
    """       
    def fetch_data(self):
        #fetch data from db
        select_test = dbconnection.db_connection()
        myresult = select_test.getDataLastEpoch()
        
        self.sensors = [x[0] for x in myresult]
        self.sensors = np.unique(self.sensors)
        self.sensors.sort()
        
        self.df = pd.DataFrame(myresult,columns=['sensor','value','timeStamp','ID'])
        self.df = self.df.sort_values('sensor')
    #%%
    """
    using latest sensor data as test data
    output: a json file containing new measurements 
    wit a new entry for each, 'isOutlier' which is
    either True or False
    """      
    def test(self):
        logging.basicConfig(format='%(asctime)s - %(message)s',filename="logfilename.log", level=logging.INFO)
        return_data =[]
        for i,sensor in enumerate(self.sensors):
            
            locals()[str(sensor)+ "_test" ] = self.df.loc[self.df['sensor'] == sensor]
            locals()[str(sensor)+ "_test" ] = locals()[str(sensor+ "_test")].iloc[0]
            
            #excluding "ANE","PLV1","PLV2","PLV3","WV"
            test_data = locals()[str(sensor)+ "_test" ]
            test_value = np.array(test_data['value']).reshape(-1,1)
            if sensor in ["ANE","PLV1","PLV2","PLV3","WV"]:
                isOutlier = False
                status = 'inlier'
                test_data['isOutlier'] = isOutlier
                return_data.append(test_data)
            else:
                #giving test data to LOF trained model to evaluate                
                outlierDetector = self.model[sensor].score_samples(test_value)
                
                if outlierDetector <=1 and outlierDetector >=-3:
                    isOutlier = False
                    status = 'inlier'
                else:
                    isOutlier =True
                    status = "outlier"
                test_data['isOutlier'] = isOutlier
                return_data.append(test_data)
            
            print(f"for sensor {test_data['sensor']}, new input {test_value[0][0]} detected as: {status}")
            logging.info(f"for sensor {test_data['sensor']}, new input {test_value[0][0]} detected as: {status}")
        print(f"<==================== {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} ===================>")
        
        returnJson = self.toJson(return_data)
        return returnJson
    #%%
    '''
    make a json file to be submitted into new database
    '''
    def toJson(self,new_input):
        output_dict = {}
        output_list =[]
        
        for i in new_input:
            output_dict['sensor'] = i[0]
            output_dict['value'] = i[1]
            output_dict['timestamp']=i[2].isoformat()
            output_dict['ID'] = str(i[3])
            output_dict['isOutlier'] = i[4]
            c = output_dict.copy()
            output_list.append(c)
        
        with open('newdb_input.json', 'w') as outfile:
            json.dump(output_list, outfile, indent = 4)
        return json.dumps(output_list)