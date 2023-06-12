import pandas as pd ,numpy as np ,seaborn as sns, matplotlib.pyplot as plt, os
from util.query_set import QuerySet
from util.console_interation import *
from util.data_process import DataProcessUtil, statistic_products


    
current_path = os.path.abspath(os.path.dirname(__file__))
save_path = os.path.join(current_path, "files/data.xlsx")
save_path1=os.path.join(current_path,"files/铸造产品分析.xlsx")
save_path2=os.path.join(current_path,"files/铸造压铸过程.xlsx")
statistic_data_save_path = os.path.join(current_path,"files/统计量分析结果.xls")
model_save_path = os.path.join(current_path,"files/model.pkl")
print("欢迎使用《DC压铸参数大数据分析》系统！")

new_query = ""
# -----查询参数设置-----------
for i in range(100):
    print("\n1. 获取指定条件的DC产品分析数据与DC压铸过程数据")
    print("2. 对DC产品分析和DC压铸过程数据进行数据处理")
    print("3. 分析压铸参数统计量特性")
    print("4. 数据可视化")
    print("5. 训练机器学习模型")
    print("6. logistic回归分析")
    print("7. 退出系统")
    select = input("\n请选择功能执行：")
    if select == "1":
        new_query = input_query_selcetions(save_path2)
        get_analysis_data(save_path1=save_path1, save_path2=save_path2, new_query=new_query)
    elif select == "2":
        data_process(save_path, save_path1, save_path2)
    elif select == "3":
        statistic_analaysis(save_path, statistic_data_save_path)
    elif select == "4":
        data_visualization_module(save_path)
    elif select == "5":
        train_model(save_path, model_save_path=model_save_path)
    elif select == "6":
        plot_logistic_regression_curve(save_path)
        pass
    else :
        break
    
    if(input("\n是否退出系统(y/n):")) == "y":
        break
    else:
        continue






