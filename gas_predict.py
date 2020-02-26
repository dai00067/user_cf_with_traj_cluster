# -*- coding: utf-8 -*-0
"""
Created on Fri Jul 19 10:55:31 2019

@author: zoed0
"""
#for all stay points between (i-1)th_Sun and (i)th_Sun:
#   detect_fill_point_func
#   if fill_point is true:
#       if len(fill_point) == 1:
#           return fill_point.miles
#           enter predict_next_fill_func
#       else:
#           user data transferred into active_user table and \
#           further refilling habits being analyzed 
#   else:

import pandas as pd
import numpy as np
import datetime
        
def return_date(user_id=87622,check_date= '2019-07-16'): 
    active_table = pd.read_csv('C:/Users/zoed0/Desktop/UBiAi/fengkong/gas_station/active_table.csv')
    active_table.date_id = pd.to_datetime(active_table.date_id,format='%Y%m%d') 
    check_date = pd.to_datetime(check_date,format='%Y-%m-%d')
    user1 = active_table[active_table.id == user_id]
    user1 = user1.set_index('date_id')
    active_driver = []       
    last_checkpt = check_date + datetime.timedelta(-7)
    
    points = user1[last_checkpt:check_date] #days a week before check_point
    count_filling = sum(points.filling)
    if (count_filling <= 0):
        pass
    elif (count_filling >1):
        active_driver.append(user1)
        print('active driver!')
    elif (count_filling == 1):
        fill_date = list(points[points.filling==1].index)[0]               
        #加完油后到check point消耗的油量
        after_fill = points[(points.index-fill_date).days>0].loc[:,'fuel_consumption']
        runned_mile = sum(after_fill)
        #预测的下周油量
        next_firstday = check_date + datetime.timedelta(1)
        comsup = user1[next_firstday:].fuel_consumption
        pred_mile = sum(comsup)       
        full_tank = 55
        if (full_tank - runned_mile - pred_mile) > 1/3*full_tank:
            pass
        else:
            next_week = comsup.tolist()
            next_week = np.cumsum(next_week)
            itemindex = np.argwhere(np.array(next_week)>(2/3*full_tank-runned_mile))[0]
            remind_date = check_date + datetime.timedelta(itemindex)
            return remind_date
