import requests, json, pandas as pd
from math import ceil
from util.http_request import get_dc_offline_product_info_page, get_dc_die_casting_info_page, export_get_dc_die_casting_info
from time import sleep
from tqdm import tqdm
def get_login_token():
    """
    获取账户的token
    : return : 返回token字符串
    """
    login_url = "https://qdap.ghac.cn/mojo-gateway/gahc/ad/toLogin"
    login_data={"username": "liufan", "password": "19981015@LF"}
    res = requests.post(url=login_url, data=login_data)
    login_token=json.loads(res.text)
    return login_token['access_token']

class QuerySet:
    castMachineNo = "" # 压铸机号
    cylinModel = "" # 机种号
    mouldNo = "" # 模具号
    start_date = "" #查询开始时间
    end_date = "" # 查询结束时间
    token = ""   # 使用api的token
    dc_online_start_date = "" # DC压铸开始时间
    dc_online_end_date = "" # Dc压铸结束时间
    dc_die_casting_data_save_path = ""
    
    def __init__(self, castMachineNo, cylinModel, mouldNo, start_date, end_date, save_path):
      self.castMachineNo = castMachineNo
      self.cylinModel = cylinModel
      self.mouldNo =mouldNo
      self.start_date = start_date
      self.end_date = end_date
      self.token = get_login_token()
      self.dc_die_casting_data_save_path = save_path
    
    def get_dc_offline_products_info(self):
        """_获取DC下线产品信息_
        
        """
        res = get_dc_offline_product_info_page(castMachineNo=self.castMachineNo, cylinModel=self.cylinModel, mouldNo=self.mouldNo, start_date=self.start_date, end_date=self.end_date, token=self.token)
        total_nums = int(res["data"]["total"] ) # 查询到的数据条数
        print('待查询的数据总条数：'+str(total_nums))
        last_page = ceil(total_nums/100) # 分页查询的总页数
        print('待查询分页数目：'+str(last_page))
        total_data = []
        print("开始进行查询")
        for page in tqdm(range(1, last_page+1)):
            res = get_dc_offline_product_info_page(castMachineNo=self.castMachineNo, cylinModel=self.cylinModel, mouldNo=self.mouldNo, start_date=self.start_date, end_date=self.end_date, token=self.token,page=page )
            total_data = total_data+res["data"]["list"]
            sleep(0.01)
        print("查询完成！已查询到的数据数目为："+str(len(total_data)))
        data_df = pd.DataFrame(total_data)
        data_df = data_df.sort_values(by = ['cylinbDcOnlineTime'])
        data_df = data_df.dropna(axis=0, how = 'any' ,subset='cylinbDcOnlineTime')
        all_cylinb_date = data_df.loc[:,"cylinbDcOnlineTime"].values.tolist()
        self.dc_online_start_date = all_cylinb_date[0]
        self.dc_online_end_date = all_cylinb_date[len(all_cylinb_date)-1]
        data_df = data_df.loc[:,["cylinbCode", "cylinbDcOnlineTime","cylinbDcOfflineTime","isScrap","dcCylinbRepairTime","dcRepairDesc"]]
        data_df.columns = ["缸体二维码", "DC上线时间", "DC下线时间","是否报废", "返修时间","返修详细信息"]
        return data_df
    
    
    def export_all_dc_die_casting_info(self):
        """导出所有需要查询的DC压铸过程数据"""
        print("查询缸体的压铸时间段"+self.dc_online_start_date+" - "+self.dc_online_end_date)
        # ------------获取需要导出的数据数目
        res = get_dc_die_casting_info_page(castMachineNo=self.castMachineNo, cylinModel=self.cylinModel, mouldNo=self.mouldNo, start_date=self.dc_online_start_date, end_date=self.dc_online_end_date, token=self.token)
        total_nums = int(res["data"]["total"])
        print("待查询的数据总条数"+str(total_nums))
        query_loops = ceil(total_nums/10000)
        print("开始进行查询......")
        df = pd.DataFrame()
        for loop in tqdm(range(1, query_loops+1)):
            if loop == 1:
                df = export_get_dc_die_casting_info(self)
                df = df.sort_values(by = ["作业时间"])
            else: 
                all_cylinb_date = df.loc[:,"作业时间"].values.tolist()
                self.dc_online_end_date = all_cylinb_date[0]
                df = pd.concat([df, export_get_dc_die_casting_info(self)])
                df = df.sort_values(by = ["作业时间"])
                #print(df.loc[:,"作业时间"])
                #print("查询到的总条数"+str(len(df)))
            sleep(0.01)
        df = df.drop_duplicates( subset = "缸体二维码")
        print("查询到的总条数"+str(len(df)))
        return df