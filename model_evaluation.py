# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 11:17:31 2019

@author: Administrator
"""
import pandas as pd
import datetime
        
def return_date(start_date= '2019-07-17',end_date='2019-07-23',alpha=0.4): 
    active_table = pd.read_csv('E:/UBiAi/fengkong/gas_station/active_table2.csv')
    active_table.date_id = pd.to_datetime(active_table.date_id,format='%Y%m%d') 
    start_date = pd.to_datetime(start_date,format='%Y-%m-%d')
    end_date = pd.to_datetime(end_date,format='%Y-%m-%d')
    # extract table in examine dates
    exam_t = active_table.loc[(active_table.date_id>=start_date)&(active_table.date_id<=end_date)]
    # convert table into dict with id as key
    id_dict = dict(list(exam_t.groupby('id'))) 
    # TF is filling & prediction true, TP is no filling & prediction true
    # FP is filling & prediction false, FN is no filling & prediction false       
    TF = {k: v for k, v in id_dict.items() if (sum(v.filling)==0)&(sum(v.prediction)==0)}            
    TP = {k: v for k, v in id_dict.items() if (sum(v.filling)>0)&(sum(v.prediction)>0)}   
    FP = {k: v for k, v in id_dict.items() if (sum(v.filling)==0)&(sum(v.prediction)>0)}
    FN = {k: v for k, v in id_dict.items() if (sum(v.filling)>0)&(sum(v.prediction)==0)}            
    # s1 = precision
    precision = len(TP)/(len(TP)+len(FP))
    recall = len(TP)/(len(TP)+len(FN))
    s1 = 2 / ((1 / precision) + (1 / recall))
    f_u = 0
    for k,v in TP.items():
        distance = v[v.filling==1].index[0] - v[v.prediction==1].index[0]
        f_u += 10/(10+distance**2)    
    s2 = f_u/len(TP)             
    S = alpha*s1 + (1-alpha)*s2
    print('The Presion is %f.' %S)
    return S

return_date()
