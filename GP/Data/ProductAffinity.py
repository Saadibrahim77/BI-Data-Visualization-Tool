# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:33:23 2021

@author: abdullah
"""
import pandas as pd
import pyfpgrowth

class ProductAffinity(object):



      def GetProductValues(self):
        print("FLAG!: Affinity algorithm initated")
        orders_products = pd.read_csv(r'G:\Final Shehab\GP\GP\static\files\Orders_Products.csv')
        orders_products = orders_products[['id','order_id','product_id','shortname','price','created_date']]
        
        #forming orders_products table in the form of transactions and pass it to FP-growth function alongside with MIN Support
        step1 = orders_products[['order_id','product_id']]
        step2 = step1.groupby('order_id')['product_id'].apply(list).reset_index(name = 'products')
        transactions = step2['products']
        
        
        #performing a dictionary of products IDs and their name in order to map it later in Frequents_products and final rulesdf
        orders_pr = orders_products[['shortname','product_id']]
        orders_pr1 = orders_pr.drop_duplicates(subset = ['shortname','product_id'], keep = 'first')        
        products_dict = dict(zip(orders_pr1.product_id, orders_pr1.shortname))       

        patterns = pyfpgrowth.find_frequent_patterns(transactions, 100)  
        
        #splitting frequent itemsets IDs
        patternsdf = pd.DataFrame()
        counter = 0
        try:
            for key,value in patterns.items():  
                patternsdf.at[counter,'ID1'] = key[0]              
                if len(key) >=2 :
                    patternsdf.at[counter,'ID2'] = key[1]
                else:
                    patternsdf.at[counter,'ID2'] = float("NaN")
                if len(key) >= 3:                
                    patternsdf.at[counter,'ID3'] = key[2]
                else:
                    patternsdf.at[counter,'ID3'] = float("NaN")
                if len(key) >= 4: 
                    patternsdf.at[counter,'ID4'] = key[3]
                else:
                    patternsdf.at[counter,'ID4'] = float("NaN")           
                patternsdf.at[counter,'Number of Orders'] = value
                counter += 1  
        except:
            print("Frequent Products out of range!")
        
        #mapping each product id with its name (from the diciitonary) into frequent products 
        index = len(patternsdf.columns)
        if index == 2:           
            patternsdf['Product1'] = patternsdf.ID1.map(products_dict)
        elif index == 3:
            patternsdf['Product1'] = patternsdf.ID1.map(products_dict)
            patternsdf['Product2'] = patternsdf.ID2.map(products_dict)
        elif index == 4:
            patternsdf['Product1'] = patternsdf.ID1.map(products_dict)
            patternsdf['Product2'] = patternsdf.ID2.map(products_dict)
            patternsdf['Product3'] = patternsdf.ID3.map(products_dict)
        elif index == 5:
            patternsdf['Product1'] = patternsdf.ID1.map(products_dict)
            patternsdf['Product2'] = patternsdf.ID2.map(products_dict)
            patternsdf['Product3'] = patternsdf.ID3.map(products_dict)
            patternsdf['Product4'] = patternsdf.ID4.map(products_dict)
        elif index == 6:    
            patternsdf['Product1'] = patternsdf.ID1.map(products_dict)
            patternsdf['Product2'] = patternsdf.ID2.map(products_dict)
            patternsdf['Product3'] = patternsdf.ID3.map(products_dict)
            patternsdf['Product4'] = patternsdf.ID4.map(products_dict)
            patternsdf['Product5'] = patternsdf.ID5.map(products_dict)

        patternsdf = patternsdf.drop(columns = {'ID1','ID2','ID3','ID4'})

        #passing the frequent products to FP-growth fucntion alongside with the MIN Confidence probability
        rules = pyfpgrowth.generate_association_rules(patterns, 0.5)        
        rulesdf = pd.DataFrame.from_dict(rules,orient = 'index').reset_index()
        rulesdf.rename(columns = {'index':'Item/s 1', 0:'Product2_ID', 1:'Confidence Probability'}, inplace = True)
        
        #splitting and formating the final rules table, to have an integer index and mapped to the name of the product         
        for i in range(len(rulesdf)):
            current = rulesdf.iloc[i]['Item/s 1']
            try:                
                rulesdf.at[i,'Product11_ID'] = current[0]
                if len(current) >= 2:
                    rulesdf.at[i,'Product12_ID'] = current[1]   
                else:
                    rulesdf.at[i,'Product12_ID'] = float("NaN")  
                if len(current) >= 3:
                   rulesdf.at[i,'Product13_ID'] = current[2]
                else:
                    rulesdf.at[i,'Product13_ID'] = float("NaN") 
                #if len(current) >= 4:
                   #rulesdf.at[i,'Product14_ID'] = current[3] 
                #else:
                   #rulesdf.at[i,'Product14_ID'] = float("NaN") 
            except:
                 print("Rules' products out of range")
            try:
                current = rulesdf.iloc[i]['Product2_ID']
                rulesdf.at[i,'Product2_ID'] = current[0]
            except:
                rulesdf.at[i,'Product2_ID'] = float("NaN")
        temp = rulesdf[['Product2_ID','Confidence Probability']]
        rulesdf1 = rulesdf.drop(['Product2_ID','Confidence Probability','Item/s 1'], axis = 1)
        index = len(rulesdf1.columns)
        rulesdf1.insert(index, 'Product2_ID', temp.iloc[:, 0:1])
        rulesdf1.insert(index+1, 'Confidence Probability', temp.iloc[:, 1:2])
        
        #mapping each product id with its name (from the diciitonary) into rules dataframe
        index = len(rulesdf1.columns)
        if index == 3:           
            rulesdf1['Product11'] = rulesdf1.Product11_ID.map(products_dict)
            rulesdf1['Product2'] = rulesdf1.Product12_ID.map(products_dict)
        elif index == 4:
            rulesdf1['Product11'] = rulesdf1.Product11_ID.map(products_dict)
            rulesdf1['Product12'] = rulesdf1.Product12_ID.map(products_dict)
            rulesdf1['Product2'] = rulesdf1.Product2_ID.map(products_dict)
        elif index == 5:
            rulesdf1['Product11'] = rulesdf1.Product11_ID.map(products_dict)
            rulesdf1['Product12'] = rulesdf1.Product12_ID.map(products_dict)
            rulesdf1['Product13'] = rulesdf1.Product13_ID.map(products_dict)
            rulesdf1['Product2'] = rulesdf1.Product2_ID.map(products_dict)
        else:
            rulesdf1['Product11'] = rulesdf1.Product11_ID.map(products_dict)
            rulesdf1['Product12'] = rulesdf1.Product12_ID.map(products_dict)
            rulesdf1['Product13'] = rulesdf1.Product13_ID.map(products_dict)
            rulesdf1['Product14'] = rulesdf1.Product14_ID.map(products_dict) 
            rulesdf1['Product2'] = rulesdf1.Product2_ID.map(products_dict)
        rulesdf1 = rulesdf1.rename(columns = {'Product11':'Item1','Product12':'Item2','Product13':'Item3','Product2':'Recommended Item'})
        rulesdf1 = rulesdf1.drop(columns = {'Product11_ID','Product12_ID','Product13_ID','Product2_ID'})
        return patternsdf, rulesdf1
    

    
#if __name__ == '__main__':
 #   patterns, rules= ProductAffinity()
    
    
    