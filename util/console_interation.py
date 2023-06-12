from util.query_set import QuerySet
from util.data_visualization import Data_Visualization_util
from util.data_process import DataProcessUtil, statistic_products, outliers_filter
from util.LogisticRegressionAnalysis import LogisticRegressionAnalysis, binary_lr_analysis
import pandas as pd, xlwt

def input_query_selcetions(save_path):
    """设置查询条件功能模块
    return : 返回QuerySet对象
    """
    print("\n------步骤1：设置分析数据的范围------\n")
    print("请选择压铸机号: \n 1: 1#压铸机 \n 2: 2#压铸机")
    castMachineNo = input("\n输入:")
    print("\n请输入模具类型:\n1.5R0\n2.59B")
    cylinModel = "5R0" if input("\n输入：") == "1" else "59B"
    if(cylinModel == "5R0"):
        print("\n请输入模具号:\n1. 1号模\n2. 2号模\n3. 3号模\n4. 4号模\n5. 5号模\n6. 6号模\n7. 全部")
        temp = input("请输入：")
        mouldNo = "all"if temp == "7" else temp
    else:
        print("\n请输入模具号:\n1. 1号模\n2. 2号模\n3. 全部\n")
        temp = input("请输入：")
        mouldNo = "all"if temp == "3" else temp
    start_date = input("\n请输入开始时间:")
    end_date = input("请输入结束时间:")
    return QuerySet(castMachineNo, cylinModel, mouldNo, start_date, end_date, save_path)

def data_visualization_module(save_path):
    """数据可视化功能模块

    Args:
        save_path: 待分析数据文件存储路径
    """
    print("\n-------数据可视化功能模块-------\n")
    print("正在读取本地待分析数据文件......")
    data = pd.read_excel(save_path)
    data0 = data.query("质量等级 == 0 ")
    data1 = data.query("质量等级 == 1 ")
    data2 = data.query("质量等级 == 2 ")
    data_visualization_util = Data_Visualization_util(data, data0, data1, data2)
    for i in range(1000):
        print("请选择要分析的参数：")
        index = 0
        for parameter in data.columns[9:len(data.columns)-3]:
            index = index+1
            print(index, ":",parameter)
        select2 = input("请输入：")
        select_parameter = data.columns[int(select2)+8]
        data_visualization_util.plot_distribution_curve(select_parameter)
        if input("是否继续查看其他压铸参数？(y/n):\n") =="y":
            continue
        else:
            break

def get_analysis_data(save_path1, save_path2, new_query):
    """从大数据平台获取数据功能模块

    Args:
        save_path1 (_string_): _DC下线产品分析文件存储路径_
        save_path2 (_string_): _DC压铸过程文件存储路径_
        new_query (_object_): Query_set对象
    """
    print("\n------步骤2：从大数据平台获取DC产品分析数据和压铸过程数据")
    print("正在从大数据平台获取DC产品分析数据......")
    dc_offline_product_data = new_query.get_dc_offline_products_info()
    print("将获取到的数据保存到本地......")
    dc_offline_product_data.to_excel(save_path1)   
    print("DC产品分析数据已成功保存！")

    print("正在从大数据平台获取DC压铸过程数据......")
    dc_die_casting_data = new_query.export_all_dc_die_casting_info()
    print("将获取到的数据保存到本地......")
    dc_die_casting_data .to_excel(save_path2)
    print("DC压铸过程数据已成功保存！\n")

def data_process(save_path, save_path1, save_path2):
    """_DC下线与压铸过程数据处理_

    Args:
        save_path (_string_): _处理后的数据存储路径_
        save_path1 (_string_): _DC下线产品分析文件存储路径_
        save_path2 (_string_): _DC压铸过程文件存储路径_
    """
    dp = DataProcessUtil(save_path1, save_path2)
    data = dp.get_process_data()
    print("待分析数据正在保存中......")
    data.to_excel(save_path)
    pass 

def statistic_analaysis(save_path, statistic_data_save_path):
    """_对待分析数据文件进行统计量分析_

    Args:
        save_path (_string_): _待分析数据文件路径_
        statistic_data_save_path (_type_): _统计量分析数据文件存储路径_
    """
    print("正在读取本地数据文件......")
    data = pd.read_excel(save_path)
    #statistic_data_file = pd.ExcelWriter(statistic_data_save_path)
    print("正在分析MC返回为0的产品压铸参数统计量...")
    data0 = data.query("MC返回 == 0 ")
    statistic_MC_return0_data = statistic_products(data0)
    #statistic_MC_return0_data.to_excel(statistic_data_file, sheet_name="质量等级为0")
    print("正在分析MC返回为1且DC实修为0的产品压铸参数统计量...")
    data1 = data.query("MC返回 == 1 and DC实修 == 0")
    statistic_dc_do0_data = statistic_products(data1)
    #statistic_dc_do0_data.to_excel(statistic_data_file, sheet_name="质量等级为1")
    print("正在分析MC返回为1且DC实修为1的产品压铸参数统计量...")
    data2 = data.query("MC返回 == 1 and DC实修 == 1")
    statistic_dc_do1_data = statistic_products(data2)
    #statistic_dc_do1_data.to_excel(statistic_data_file, sheet_name="质量等级为2")
    col =  statistic_MC_return0_data.columns
    statistic_data = pd.DataFrame()
    statistic_data.index = statistic_dc_do0_data.index
    for index in range(0, len(statistic_dc_do0_data.columns)):
        print("质量0 "+col[index])
        statistic_data.loc [:,"质量0 "+col[index]]= statistic_MC_return0_data.loc[:,col[index]]
        statistic_data .loc[:,"质量1 "+col[index]]= statistic_dc_do0_data.loc[:,col[index]]
        statistic_data.loc[:, "质量2 "+col[index]] = statistic_dc_do1_data.loc[:,col[index]]
        pass
    statistic_data.to_excel(statistic_data_save_path)
    print("分析完成！")
    return 
    #statistic_data_file.close()

def train_model(save_path, model_save_path):
    lr = LogisticRegressionAnalysis(save_path, model_save_path)
    lr.create_model()

def plot_logistic_regression_curve(data_path):
    """_绘制二元逻辑回归曲线_

    Args:
        data_path (_type_): _description_
    """
    print("正在读取待分析数据......")
    data = pd.read_excel(data_path)
    print("正在过滤待分析数据异常值")
    data = outliers_filter(data)
    for i in range(1000):
        print("请选择要分析的参数：")
        index = 0
        for parameter in data.columns[10:len(data.columns)-3]:
            index = index+1
            print(index, ":",parameter)
        select2 = input("请输入：")
        select_parameter = data.columns[int(select2)+9]
        print(select_parameter)
        binary_lr_analysis(data, select_parameter)
        if input("是否继续查看其他压铸参数？(y/n):\n") =="y":
            continue
        else:
            break
    pass