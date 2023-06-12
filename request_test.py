import requests, json, pandas as pd
from time import sleep
from tqdm import tqdm
from math import ceil
from util.http_request import  get_login_token, get_dc_offline_product_info_page, get_dc_die_casting_info_page, export_get_dc_die_casting_info, get_refurbishment_info
from util.query_set import QuerySet
import os


# --------参数设置
castMachineNo = "2" # 压铸机号
cylinModel = "5R0" # 机种号
mouldNo = "1" # 模具号
start_date = "2021-01-01" #查询开始时间
end_date = "2022-12-31" # 查询结束时间
token = get_login_token()  # 使用api的token
current_path = os.path.abspath(os.path.dirname(__file__))
save_path = os.path.join(current_path, "files/data.xlsx")
save_path1=os.path.join(current_path,"files/铸造产品分析.xlsx")
save_path2=os.path.join(current_path,"files/铸造压铸过程.xls")
data_file = pd.ExcelWriter(os.path.join(current_path,"files/统计量分析结果.xlsx"))



# res = get_dc_offline_product_info_page(castMachineNo=castMachineNo, cylinModel=cylinModel, mouldNo=mouldNo, start_date=start_date, end_date=end_date, token=token)
# total_nums = int(res["data"]["total"] ) # 查询到的数据条数
# print('查询到的数据总条数：'+str(total_nums))
# last_page = ceil(total_nums/10) # 分页查询的总页数
# print('查询分页数目：'+str(last_page))
# total_data = []
# for page in tqdm(range(1, last_page+1)):
#     res = get_dc_offline_product_info_page(castMachineNo, cylinModel, mouldNo, start_date, end_date, token, page )
#     total_data = total_data+res["data"]["list"]
#     sleep(0.01)
# print(len(total_data))
# data_df = pd.DataFrame(total_data)
# data_df = data_df.sort_values(by = ['cylinbDcOnlineTime'])
# all_cylinb_date = data_df.loc[:,"cylinbDcOnlineTime"].values.tolist()
# print(all_cylinb_date[0])

# res = get_dc_die_casting_info_page(castMachineNo, cylinModel, mouldNo, start_date, end_date, token) 
# total_nums = int(res["data"]["total"] ) # 查询到的数据条数
# print('待查询的数据总条数：'+str(total_nums))
# last_page = ceil(total_nums/10) # 分页查询的总页数
# print('待查询分页数目：'+str(last_page))
# total_data = []

# df = export_get_dc_die_casting_info(castMachineNo=castMachineNo, cylinModel=cylinModel, mouldNo=mouldNo, start_date=start_date, end_date=end_date, token=token, save_path=save_path2)
# print(df)



