""" following scipts runs corresponding functions and files to perfrom outlier detection operation """

import trainModel
import evaluator
import logging
import time
import dbconnection
import json

    
def train():
    logging.info('train model called')
    #train model
    train_data = trainModel.Train()
    train_data.fetch_data(trainInterval_h)
    train_data = train_data.train()
    
    #save train data in db
    saveToDB('train_input.json')
    
    return train_data

def test(train_data):
    logging.info('test model called')
    # test new input
    test_data = evaluator.predict(train_data)
    test_data.fetch_data()
    result = test_data.test()
    
    #save novelty detection result in db
    saveToDB('newdb_input.json')
    
    return result

def saveToDB(jsonName):
    with open(jsonName) as infile: 
        data = json.load(infile)
    saveData.saveFilteredData(data)
    
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s',filename="logfilename.log", level=logging.INFO)
    
    saveData = dbconnection.db_connection()
    
    #set intervals of training and testing   
    trainInterval_h = 8
    trainInterval_s = trainInterval_h*3600
    testInterval = 900
    
#%%    
    # uncomment 2 below lines if you want to run it only once to check
    model = train()
    test_data = test(model)

#%%
    '''
    every testInterval, latest measurements are used as
    test data and evaluated using latest trained model.
    A new model is updated every trainInterval_h 
    '''
    
    # start_time = time.time()
    # model = train()

    # while True:       
    #     now = time.time()
    #     if now - start_time >= trainInterval_s:
    #         model = train()
    #         start_time = time.time()
    #     test_data = test(model)
    #     saveData.saveFilteredData(test_data)
        
    #     time.sleep(testInterval)
                
        

