""" following scipts is the implementation of Local Outlier Factor approach 
for outlier detection in our project """

import numpy as np
from sklearn.neighbors import LocalOutlierFactor


class LOF(object):
    def __init__(self, data,n_neighbors):
        self.data = data
        self.n_neighbors = n_neighbors
        self.inliers = []
        self.anomalies = []
        
    def reshape(self,X):
        return np.array(X).reshape(-1,1)
    
    def run(self):
        clf = LocalOutlierFactor(n_neighbors=self.n_neighbors, metric='euclidean')
        reshapeData = self.reshape(self.data)
        y_pred = clf.fit_predict(reshapeData)            
        y_pred_score = clf.negative_outlier_factor_
    
        #Combine test data and prediction result
        self.data = list(zip(self.data,y_pred_score))
        
        #considering 0 to -2 as normal inliers
        #values close to -1 imply to be inliers
        for i in self.data:
            if i[1] <=0 and i[1] >=-2 :
                self.inliers.append(i[0])
            else:
                self.anomalies.append(i[0])
        return self.anomalies,self.inliers,y_pred_score,y_pred
    
    def trainModel(self):
        data = self.reshape(self.inliers)
        clf = LocalOutlierFactor(n_neighbors=self.n_neighbors, novelty=True,contamination=0.1)       
        clf.fit(data)
        return clf