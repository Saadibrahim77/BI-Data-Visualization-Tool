# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 17:00:28 2021

@author: abdullah
"""

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from datetime import date, timedelta, datetime
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import seaborn as sns
import os
class CustomerSegmentation():
    


     def CustomerValues(self):
        #dropping all orders with customers' total spent <0 to make sure we are only dealing with actual customers
        #orders = pd.read_json('C:\\Users\\abdul\\.spyder-py3\\orders Data.json')
        orders = pd.read_csv(r'G:\Final Shehab\GP\GP\static\files\Orders.csv')
        orders = orders[['id','customer_id','total_amount','customer_name','created_date']]       

        #calculating today date and the customer's last order' datetime to get the Recency factor (withing 365 days)
        today_date = datetime.now()
        today_date = today_date.strftime("%Y-%m-%d %H:%M:%S")
        todaydatetime = datetime.strptime(today_date , "%Y-%m-%d %H:%M:%S")

        #caluclating number of days since last order date (Recency)
        recency = orders.sort_values(by = ['created_date'], ascending = False)    
        recency = orders.drop_duplicates(subset = ['customer_id'], keep = 'last').reset_index(drop = True)
        recency['created_date'] = pd.to_datetime(recency['created_date'], format = "%Y-%m-%d %H:%M:%S")

        for i in range(len(recency)):
            try:
                current = recency.iloc[i]['created_date']
                diff = todaydatetime - current
                recency.at[i, 'days_since_last_order'] = diff.days
            except:
                recency.at[i, 'days_since_last_order'] = -1
        recency = recency[['customer_id','days_since_last_order']]
        recency.columns = ["CustomerID", "Recency"]
        
        #caclulating number of orders per each customer in the 365 days time interval
        frequency = orders[['customer_id','created_date']]
        frequency = frequency.groupby("customer_id").created_date.count()
        frequency = pd.DataFrame(frequency)
        frequency = frequency.reset_index() 
        frequency.columns = ["CustomerID", "Frequency"]
        
        #calculating monetary value for each customer (total orders amount in 365 time interval)
        monetary = orders[['customer_id','created_date','total_amount']]
        monetary['total_amount'] = monetary['total_amount'].astype(float)
        monetary = monetary.groupby("customer_id").total_amount.sum()
        monetary = pd.DataFrame(monetary)
        monetary = monetary.reset_index() 
        monetary.columns = ["CustomerID", "Monetary"]
        
        #merging all 3 metrics RFM into one dataframe alongside with each customer id
        merging_temp = recency.merge(frequency, how = 'inner', on = 'CustomerID')
        rfm = merging_temp.merge(monetary, how = 'inner', on = 'CustomerID')
        
        #removing outliers
        rfm = rfm.drop(columns = {'CustomerID'})
        rfm = rfm[rfm['Frequency'] != 0]
        rfm = rfm[rfm['Monetary'] != 0]
        rfm = rfm[(np.abs(stats.zscore(rfm)) < 4).all(axis=1)]
             
        #normalizing values of RFM in order to iniate k-means clustering algorith
        scaler = MinMaxScaler()
        rfm_normalized = pd.DataFrame(scaler.fit_transform(rfm))
        rfm_normalized.columns = ['n_recenecy', 'n_frequency', 'n_monetary']
          
        #used to determine k by elbow detection
        '''
        SSE = []
        for k in range(0,10):
            kmeans = KMeans(n_clusters = k+1, random_state = 1231).fit(rfm_normalized)
            SSE.append(kmeans.inertia_)       
        sns.pointplot(x=list(range(1,11)), y = SSE)
        plt.show()
        '''

        model = KMeans(n_clusters = 4, random_state = 1231).fit(rfm_normalized)
        rfm_df = pd.DataFrame(scaler.inverse_transform(rfm_normalized))
        rfm_df.columns = rfm.columns
        rfm_df['CustomerID'] = rfm.index
        rfm_df['Cluster'] = model.labels_
        
        
        #used for cluster analysis (mean ,min ,max, standard deviation)
        '''
        cluster_analysis = rfm_df.groupby('Cluster').agg({'Recency':['mean','min','max','std'],'Frequency':['mean','min','max','std'],
                                       'Monetary':['mean','min','max','std']})
        '''
        
        rfm_df['Cluster'] = rfm_df['Cluster'].replace({1:'Promising', 2:'Champions', 3: 'Lost', 0:'At Risk'})      
        count = rfm_df['CustomerID'].groupby(rfm_df['Cluster']).count()
        count = count.reset_index()
        clusterlabels =count['Cluster'].tolist()
        clustersValues = count['CustomerID'].tolist()
        amount = rfm_df['Monetary'].groupby(rfm_df['Cluster']).sum()
        amount = amount.reset_index()
        amountLabels = amount['Cluster'].tolist()
        amountValues = amount['Monetary'].astype(int).tolist()
        return  rfm_df,clusterlabels,clustersValues,amountLabels,amountValues


#if __name__ == '__main__':
 #   orders,clusterlabels,clustersValues,amountLabels,amountValues= Segment_customers() 
    
    
    
    
    
    
    
    