# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 11:52:39 2019

@author: Administrator
"""
import pandas as pd
import random
import math
from operator import itemgetter

class UserBasedCF():
    # 初始化相关参数
    def __init__(self):
        # 找到与目标用户兴趣相似的20个用户，为其推荐10部电影
        self.n_sim_user = 5
        self.n_rec_station = 1

        # 将数据集划分为训练集和测试集
        self.trainSet = {}
        self.testSet = {}

        # 用户相似度矩阵
        self.user_sim_matrix = {}
        self.station_count = 0

        print('Similar user number = %d' % self.n_sim_user)
        print('Recommneded station number = %d' % self.n_rec_station)


    # 读文件得到“用户-电影”数据
    def get_dataset(self, filename, pivot=0.9):
        # read in file
        gas_fuel = pd.read_csv(gas_site)
        gas_fuel.vid = gas_fuel.vid.apply(str)
        
        # convert gas station names into id
        station_id = gas_fuel.groupby(['gas_station']).count().reset_index().reset_index()
        df = pd.merge(gas_fuel,station_id,how='left',on='gas_station')
        user_gs_list = df.loc[:,['vid_x','index']].rename(columns={'vid_x':'user','index':'gas_station'})
        
        # score for user-station
        user_gs_list['score'] = 0
        user_gs_score = user_gs_list.groupby(['user','gas_station']).count()
        user_gs_score = user_gs_score.reset_index()
        
        # score to level: count/sum(count) in 0-25% -> 1,25%-50 -> 2, etc.
        user_gs_score['sum'] = user_gs_score.groupby(['user'])['score'].transform(sum)
        user_gs_score['percent'] = user_gs_score['score']/user_gs_score['sum']
        def percent_to_level(df,column='percent'):
            if df[column] <= 0.25:
                return 1
            elif 0.25 < df[column] <= 0.5:
                return 2
            elif 0.5 < df[column] <= 0.75:
                return 3
            else:
                return 4
        user_gs_score['level'] = user_gs_score.apply(percent_to_level,axis=1)   
        user_gs_score = user_gs_score.loc[:,['user','gas_station','level']]
        #print(user_gs_score)
        
        
        #split train and test set
        trainSet_len = 0
        testSet_len = 0
        for index,row in user_gs_score.iterrows():
            user, gas_station, level = row['user'],row['gas_station'],row['level']
            if random.random() < pivot:
                self.trainSet.setdefault(user, {})
                self.trainSet[user][gas_station] = level
                trainSet_len += 1
            else:
                self.testSet.setdefault(user, {})
                self.testSet[user][gas_station] = level
                testSet_len += 1
        print('Split trainingSet and testSet success!')
        print('TrainSet = %s' % trainSet_len)
        print('TestSet = %s' % testSet_len)


    # 计算用户之间的相似度
    def calc_user_sim(self):
        # 构建“加油站-用户”倒排索引
        # key = stationID, value = list of userIDs who have seen this station
        print('Building gas_station-user table ...')
        station_user = {}
        for user, gas_station in self.trainSet.items():
            for gs in gas_station:
                if gs not in station_user:
                    station_user[gs] = set()
                station_user[gs].add(user)
        print('Build gas_station-user table success!')

        self.station_count = len(station_user)
        print('Total station number = %d' % self.station_count)

        print('Build user co-rated stations matrix ...')
        for station, users in station_user.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    self.user_sim_matrix.setdefault(u, {111111})
                    self.user_sim_matrix[u].setdefault(v, 0)
                    self.user_sim_matrix[u][v] += 1
        print('Build user co-rated stations matrix success!')

        # 计算相似性
        print('Calculating user similarity matrix ...')
        for u, related_users in self.user_sim_matrix.items():
            for v, count in related_users.items():
                self.user_sim_matrix[u][v] = count / math.sqrt(len(self.trainSet[u]) * len(self.trainSet[v]))
        print('Calculate user similarity matrix success!')


    # 针对目标用户U，找到其中最相似的K个用户，产生N个推荐
    def recommend(self, user):
        K = self.n_sim_user
        N = self.n_rec_station
        rank = {}
        user = '817112100087929'
        visited_station = self.trainSet[user]
        v = '817112100153283'
        # v=similar user, wuv=similar factor
        for v, wuv in sorted(self.user_sim_matrix[user].items(), key=itemgetter(1),
                             reverse=True)[0:K]:
            for station in self.trainSet[v]:
                if station in visited_station:
                    continue
                rank.setdefault(station, 0)
                rank[station] += wuv
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]


    # 产生推荐并通过准确率、召回率和覆盖率进行评估
    def evaluate(self):
        print("Evaluation start ...")
        N = self.n_rec_station
        # 准确率和召回率
        hit = 0
        rec_count = 0
        test_count = 0
        # 覆盖率
        all_rec_station = set()

        for i, user in enumerate(self.trainSet):
            print(i,user)
            test_station = self.testSet.get(user, {})
            rec_station = self.recommend(user)
            for station, w in rec_station:
                if station in test_station:
                    hit += 1
                all_rec_station.add(station)
            rec_count += N
            test_count += len(test_station)

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_station) / (1.0 * self.station_count)
        print('precisioin=%.4f\trecall=%.4f\tcoverage=%.4f' % (precision, recall, coverage))


if __name__ == '__main__':
    gas_site = 'E:/UBiAi/fengkong/gas_station/parking_site.csv'
    userCF = UserBasedCF()
    userCF.get_dataset(gas_site, pivot=0.9)
    userCF.calc_user_sim()
    userCF.evaluate()


test1 = userCF.trainSet['817112100154380']
userCF.recommend('817112100154380')
for i, user in enumerate(userCF.trainSet):
    print(i,user)
    