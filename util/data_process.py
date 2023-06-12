import pandas as pd, numpy as np
from tqdm import tqdm
from time import sleep
from util.http_request import get_refurbishment_info, get_login_token
from util.data_visualization import set_plot_environment
import seaborn as sb
import matplotlib.pyplot as plt

tqdm.pandas(desc='pandas bar')
def get_MC_result(data):
        if data['是否报废']==2 and pd.isnull(data["返修时间"]):
            return 0
        else:
            return 1
        
def get_DC_result(data, token):
    #print(data["作业时间"])
    if data["MC返回"] == 0:
        return 0
    # print(data["缸体二维码"])
    # print(data["压检结果"])
    if  data['是否报废'] == 1:
        return 1
    if not pd.isnull(data["返修详细信息"]):
        if "150" in data["返修详细信息"]:
            #print(data["缸体二维码"])
            return get_refurbishment_info(data["缸体二维码"], token)
        else:
            #print("没有op150")
            return 1
    else : 
        return 0
def set_quality_class(data):
    return data["MC返回"]+data["DC实修"]  
        
class DataProcessUtil:

    def __init__(self, path1, path2):
        print("正在读取本地保存的两张数据表......")
        self.products_data = pd.read_excel(path1)
        self.process_data = pd.read_excel(path2)
       
    
    
        
    def get_process_data(self):
        """
        """
        tqdm.pandas(desc='进度：')
        # ----将两张初始表做一个做左连接查询，连接字段为缸体二维码编号
        print("正在将两张数据表做关联......")
        data = pd.merge(left=self.products_data, right=self.process_data, how = 'left', left_on='缸体二维码', right_on='缸体二维码')
        # ----数据过滤
        print("正在对待分析数据进行清洗......")
        data = data.dropna(axis = 0, how = "any", subset=["岗位号"])
        #data = data.dropna(axis =0, how = "any", subset=["F45销冷却水流量"])
        data = data.drop(labels=["F45销冷却水流量","F46销冷却水流量","F47销冷却水流量", "F48销冷却水流量", "缸孔销冷却水流量1","缸孔销冷却水流量2","缸孔销冷却水流量3", "缸孔销冷却水流量4", "F49销冷却水流量"],axis=1)
        #data = data.dropna(axis =1, how = "all")
        data = data.drop_duplicates( subset = "缸体二维码")
        # print(data.columns)
        data = data.drop(data.columns[[0,7,8,9,10,11,12,13,14]],axis = 1)
        #print(data.columns)
        print("清洗后的数据量为:"+str(len(data.index)))
        # -----设置MC返回值和DC实修值
        print("正在设置'MC是否返回'结果......")
        data.loc[:,"MC返回"] = data.progress_apply(get_MC_result, axis=1)
        token = get_login_token()
        print("正在设置'DC是否实修'结果......")
        data.loc[:,"DC实修"] = data.progress_apply(get_DC_result, args=(token,),axis=1)
        print("正在设置'质量等级'结果......")
        data.loc[:, "质量等级"] = data.progress_apply(set_quality_class, axis=1)
        return data
    

def statistic_products(data):
    columns = ['标签','统计数量', '均值', '标准差','方差', '最小值', '最大值','中位数', '偏度', '峰度']
    statistic_data = pd.DataFrame(columns =columns)
    for label in tqdm(data.columns[10:len(data.columns)-3]):
        mean = data.loc[:, label].mean()
        var = data.loc[:, label].var()
        std = data.loc[:, label].std()
        min = data.loc[:, label].min()
        max = data.loc[:, label].max()
        #mode = (data.loc[:, label].mode())[0]
        median = data.loc[:,label].median()
        skew = data.loc[:, label].skew()
        kurt = data.loc[:,label].kurt()
        num = len(data.index)
        append_data = pd.DataFrame( [[label, num, mean, std, var, min, max, median, skew, kurt]], columns = columns)
        statistic_data = pd.concat([statistic_data, append_data])
        sleep(0.01)
    statistic_data.set_index('标签', inplace=True)
    return statistic_data

def plot(statistic_data_path, parameter):
    set_plot_environment()
    statistic_data = pd.read_excel(statistic_data_path)
    pass
      

def outliers_filter(data):
    """异常值过滤器
    """
    for parameter in data.columns[10:len(data.columns)-3]:
        data_column = data.loc[:,parameter]
        # 上四分位数
        up_q = data_column.quantile(0.75)
        # 下四分位数
        low_q = data_column.quantile(0.25)
        # k=1.5是个经验值，根据整体数据的离散程度调节。一般范围[1.5, 3)
        dis = 1.5*(up_q - low_q)
        # 上边界
        up_limit = up_q + dis
        # 下边界
        low_limit = low_q - dis
        data_column[(data_column>=up_limit)|(data_column<=low_limit)] = np.nan
        data.loc[:,parameter] =data_column
        #print(data.loc[:,parameter])
    data.dropna(how='all', axis=1,inplace=True)
    return data

        
        
        
        