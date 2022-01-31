############################
# Insert your imports here
import os
import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np

############## filtering data by current time, return as a dataframe #################
def filter_mempool_data(mempool_data,current_time):
    df = mempool_data    #insert the csv data into the dataframe
    new_df = df.drop(df[(current_time <= df['time']) | (current_time > df['removed'])].index)
    return new_df

############## creating a list of transactions that entered the block #################
def greedy_knapsack(block_size, all_pending_transactions):

    all_pending_transactions['ratio'] = all_pending_transactions['fee']/all_pending_transactions['size']
    tx_list = []
    size_limit = 0
    new_df = all_pending_transactions.sort_values(by=["ratio","TXID"], ascending=[0,1])
    del all_pending_transactions['ratio']

    for data in new_df.itertuples():
        cur_size = data.size
        if size_limit + cur_size > block_size:
            continue
        else:
            tx_list.append(data.TXID)
            size_limit = size_limit + cur_size

    return tx_list

def evaluate_block(tx_list, all_pending_transactions):

    x = ((all_pending_transactions[all_pending_transactions['TXID'].isin(tx_list)])['fee'].sum())
    return x

# return a dict of tx_id as keys, for each tx_id its VCG price in satoshi]
def VCG_prices(block_size, tx_list, all_pending_transactions):
    vcg = {}
    count = 0
    for tx in tx_list:

        count += 1
        v2_df = all_pending_transactions.copy()
        v2_df.drop(v2_df.loc[v2_df['TXID'] == tx].index,inplace=True)
        #v2_df = all_pending_transactions[all_pending_transactions['TXID'] != tx].copy()
        v2_list = greedy_knapsack(block_size, v2_df)
        v2 = evaluate_block(v2_list,all_pending_transactions)

        v1_size = block_size - ((all_pending_transactions.loc[all_pending_transactions['TXID'] == tx])["size"].values[0])
        v1_list = greedy_knapsack(v1_size, v2_df)
        v1 = evaluate_block(v1_list,all_pending_transactions)
        vcg[tx] = v2 - v1

    return vcg

def blocks_by_time_1510266000():
    return {1510261800,
            1510262800,
            1510263100,
            1510264600,
            1510264700,
            1510265400,
            1510265600,
            1510265900,
            1510266200,
            1510266500
            }
def blocks_after_time_1510266000():
    block_times = {1510266190,1510266490,1510267250,1510267730,1510267834,1510269386,1510269627,1510270136,1510275909
,1510277772
}
    return block_times
####part B
def load_my_TXs(my_TXs_full_path):
    my_tx = pd.read_csv(my_TXs_full_path)
    return my_tx

class BiddingAgent:
    def __init__(self, time_begin_lin, time_end_lin, block_size):
        self.time_begin_lin = time_begin_lin
        self.time_end_lin = time_end_lin
        self.block_size = block_size

class SimpleBiddingAgent(BiddingAgent):
    def bid(self, TX_min_value, TX_max_value, TX_size, current_mempool_data, current_time):
        mid_value = (TX_min_value + TX_max_value) / 2
        bid = mid_value
        if TX_size > 1000:
            bid = bid * 1.2
        return bid
class ForwardBiddingAgent(BiddingAgent):
    def bid(self, TX_min_value, TX_max_value, TX_size, current_mempool_data, current_time):
        current_mempool_data['ratio'] = current_mempool_data['fee'] / current_mempool_data['size']
        mempool_by_ratio = current_mempool_data.sort_values(by=["ratio"], ascending=[False])  #mempool sort by ratio (high to low)
        #mempool_by_ratio['index'] = np.arange(len(mempool_by_ratio))
        min_size = current_mempool_data['size'].min()

        gu_dic = {}
        max_gu = 0
        for z in range(5, 1000, 5):  # iter over z (0 to 1000) in legs of 5
            size_limit = 0
            block_count = 0

            df = mempool_by_ratio.copy()
            while True:
                ratio_list, tx_list = self.block(df,min_size,z)
                df = df[~df['TXID'].isin(tx_list)]
                mm = min(ratio_list)
                if z > mm:
                    break
                block_count += 1

            t_z = block_count * 60
            if t_z > self.time_end_lin:  g_u = 0
            elif t_z < self.time_begin_lin: g_u = TX_max_value - z * TX_size
            else:
                g_u = TX_max_value - ((t_z - self.time_begin_lin) / (self.time_end_lin - self.time_begin_lin)) * (TX_max_value - TX_min_value) - z * TX_size

            gu_dic[g_u] = [z,t_z]

        utility_if_z = key = (max(gu_dic, key=int))
        bid_best_z = (gu_dic[key])[0] * TX_size
        time_if_z = (gu_dic[key])[1]

        if utility_if_z == 0:
            bid_best_z = -1
            time_if_z =-1
        #print( bid_best_z, time_if_z, utility_if_z)
        return bid_best_z, time_if_z, utility_if_z


    def block(self,df,min_size,z):
        size_limit = 0
        #last_ratio =0
        tx_list = []
        ratio_list= []
        for data in df.itertuples():
            if self.block_size - size_limit < min_size: break
            cur_size = data.size
            if size_limit + cur_size > self.block_size:
                continue
            else:
                size_limit = size_limit + cur_size
                ratio_list.append(data.ratio)
                tx_list.append(data.TXID)
        return ratio_list, tx_list


class CompetitiveBiddingAgent(BiddingAgent):
    def bid(self, TX_min_value, TX_max_value, TX_size, current_mempool_data, current_time):
        ## IMPLEMENT for competitive part ##

        bid_competitive=0

        return bid_competitive

def write_file_ForwardAgent(tx_num,time_list,bid,utility_list):
    """writing lists to a csv files"""
    filename = 'hw2_ForwardAgent.csv'
    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        fieldnames2 = ["Index","Time", "Bid", "Utility"]
        writer.writerow(fieldnames2)
        for i in range(len(utility_list)):
            writer.writerow([tx_num[i],time_list[i], bid[i], utility_list[i]])
def write_file_CompetitiveAgent(tx_num,competitive_bid):
    """writing lists to a csv files"""
    filename = 'hw2_CompetitiveAgent.csv'
    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        fieldnames2 = ["Index","Bid"]
        writer.writerow(fieldnames2)
        for i in range(len(competitive_bid)):
            writer.writerow([tx_num[i],competitive_bid[i]])