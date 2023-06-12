import requests, json, os, pandas as pd

def get_login_token():
    """
    获取账户的token
    : return : 返回token字符串
    """
    login_url = "https://qdap.ghac.cn/mojo-gateway/gahc/ad/toLogin"
    login_data={"username": "liufan", "password": "19981015@LF"}
    res = requests.post(url=login_url, data=login_data)
    login_token=json.loads(res.text)
    #print(login_token['access_token'])
    return login_token['access_token']

def get_refurbishment_info(cylinbCode ,token):
    """
    获取缸体在op150岗位返修结果
    : param cylinbCode: 查询缸体序列号
    : return: Number 如果缸体返修结果为“合格误判”返回0; 反之返回1
    """
    query_url="https://qdap.ghac.cn/mojo-gateway/gahc/process/info/info"
    header={"Authorization": "bearer "+token}
    query_data={"sectionId" : "1512725475130322946", 
                "positNo" : "OP_150", 
                "keyType":"1", 
                "cylinbCode": cylinbCode}
    res = requests.get(query_url, headers=header, params = query_data)
    #print(res.json())
    data= res.json()["data"]["tableData"][0]
    for item in data:
        if item["ngitem_repair_result_code"] != "合格误判":
            return 1
    return 0
    
def get_dc_offline_product_info_page(castMachineNo, cylinModel, mouldNo, start_date, end_date, token, page =1):
    """获取DC下线产品数据
    """
    header={"Authorization": "bearer "+token}
    query_url ="https://qdap.ghac.cn/mojo-gateway/gahc/engine/info/customQueryPage"
    conditionList =[{"comparison":"eq","fieldName":"cylinb_model","join":"and", "values":"R0J"if cylinModel== "5R0" else "59B" },
            {"comparison":"eq","fieldName":"cast_machine_no","join":"and","values":castMachineNo},
            {"comparison":"eq","fieldName":"mould_no","join":"and","values":mouldNo}]
    if mouldNo == "all":
        conditionList.pop()
    query_data={"conditionList":conditionList,
        "startDcCylinbOfflineTime":start_date,
        "endDcCylinbOfflineTime":end_date,
        "sectionType":"dc",
        "page":page,
        "limit": 100}
    res = requests.post(url=query_url, json=query_data,headers=header)
    return res.json()

def get_dc_die_casting_info_page(castMachineNo, cylinModel, mouldNo, start_date, end_date, token, page =1):
    """获取DC铸造过程分页信息"""      
    header={"Authorization": "bearer "+token}
    if(mouldNo != "all"):
        like_value = cylinModel+mouldNo+castMachineNo
        conditionList=[{"comparison":"like","fieldName":"cylinb_code","join":"and","values":like_value}]
    else:
        like_value = cylinModel
        conditionList=[{"comparison":"like","fieldName":"cylinb_code","join":"and","values":like_value}]
    query_url = "https://qdap.ghac.cn/mojo-gateway/gahc/process/info/union"
    query_data = {"positNos":"",
        "positNames":"压铸",
        "sectionId":"1512725475130322946",
        "paramIds":"",
        #"paramIds":"1557665197525590017,1557665167360155650,1557665163656585218,1557665164189261826,1557665166290608130,1557665166835867650,1557665171655122946,1557665172162633730,1557665176608595969,1557665177132883969,1557665178701553665,1557665179217453058,1557665180257640450,1557642561244430337,1557665181255884802,1557665181792755713,1557665182300266498,1557665182820360193,1557665183353036801,1557642561617723394,1557665183873130498,1557665184351281153,1557665185018175489,1557665185529880578,1557665186037391362,1557642561999405058,1557665186549096449,1557665187060801538,1557665187522174977,1557665193599721474,1557642563182198785,1557665189774516225,1557665190294609922,1557665190839869442,1557665191389323266,1557665194128203777",
        "conditionList":[{"comparison":"like","fieldName":"cylinb_code","join":"and","values":like_value,"key":1680505921253}],
        "startDate":start_date,
        "endDate":end_date,
        "page":page,
        "limit":10,
        "orderField":"",
        "order":""}
    #print(query_data)
    res = requests.post(url=query_url, json=query_data,headers=header)
    return res.json()

def export_get_dc_die_casting_info(query_set):
    """导出DC压铸过程信息"""
    header={"Authorization": "bearer "+query_set.token}
    if(query_set.mouldNo != "all"):
        like_value = query_set.cylinModel+query_set.mouldNo+query_set.castMachineNo
        conditionList=[{"comparison":"like","fieldName":"cylinb_code","join":"and","values":like_value}]
    else:
        like_value = query_set.cylinModel
        conditionList=[{"comparison":"like","fieldName":"cylinb_code","join":"and","values":like_value}]
    query_url = " https://qdap.ghac.cn/mojo-gateway/gahc/process/info/customQueryExport"
    query_data = {"positNos":"",
        "positNames":"压铸",
        "sectionId":"1512725475130322946",
        "paramIds":"1557665197525590017,1557665167360155650,1557665163656585218,1557665164189261826,1557665164705161218,1557642559352799234,1557665165195894785,1557665165770514434,1557665166290608130,1557665166835867650,1557665168396148738,1557665168958185473,1557665169511833602,1557665170065481730,1557665170556215297,1557665171655122946,1557665172162633730,1557665176608595969,1557665177132883969,1557642560875331586,1557665178701553665,1557665179217453058,1557665179733352449,1557665180257640450,1557665180739985410,1557642561244430337,1557665181255884802,1557665181792755713,1557665182300266498,1557665182820360193,1557665183353036801,1557642561617723394,1557665183873130498,1557665184351281153,1557665185018175489,1557665185529880578,1557665186037391362,1557642561999405058,1557665186549096449,1557665187060801538,1557665187522174977,1557665205687705602,1557665206170050562,1557665206711115778,1557665207227015169,1557665208682438657,1557665209210920961,1557665209726820354,1557665210272079873,1557665193599721474,1557665194128203777,1557665194644103170,1557642563182198785,1557665189774516225,1557665190294609922,1557665190839869442,1557665191389323266,1557665207730331649", 
        "conditionList":[{"comparison":"like","fieldName":"cylinb_code","join":"and","values":like_value,"key":1680505921253}],
        "startDate":query_set.dc_online_start_date,
        "endDate":query_set.dc_online_end_date,}
    #print("时间段:"+query_set.dc_online_start_date+" - "+query_set.dc_online_end_date)
    res = requests.post(url=query_url, json=query_data,headers=header)
    with open(query_set.dc_die_casting_data_save_path, 'wb') as f:
        f.write(res.content)
    df = pd.read_excel(query_set.dc_die_casting_data_save_path)
    #print(df)
    return df
    


