import os, pandas as pd
from util.data_process import DataProcessUtil, statistic_products

# def get_MC_result(data):
#         print("返回结果为空值："+str(pd.isnull(data["返修时间"])))
#         print("是否报废:"+str(data['是否报废'] ==2))
#         if (data['是否报废']==2) and (pd.isnull(data["返修时间"])):
#             return 0
#         else:
#             return 1
def set_quality_class(data):
    return data["MC返回"]+data["DC实修"]  

current_path = os.path.abspath(os.path.dirname(__file__))
save_path = os.path.join(current_path, "files/data.xlsx")
save_path1=os.path.join(current_path,"files/铸造产品分析.xlsx")
save_path2=os.path.join(current_path,"files/铸造压铸过程.xlsx")
#data_file = pd.ExcelWriter(os.path.join(current_path,"files/统计量分析结果.xlsx"))

# print("待分析数据正在保存中......")
# 
data = pd.read_excel(save_path)
data = data.dropna(axis =0, how = "any", subset=["F45销冷却水流量"])
data.to_excel(save_path)