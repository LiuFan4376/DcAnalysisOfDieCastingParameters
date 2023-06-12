import os , pandas as pd, joblib, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler,RobustScaler
from util.data_visualization import set_plot_environment
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.model_selection import train_test_split

class LogisticRegressionAnalysis:
    
    def __init__(self, save_path, model_save_path):
      self.save_path = save_path
      self.model_save_path = model_save_path
      
    def create_model(self):
        print("正在读取训练数据......")
        data = pd.read_excel(self.save_path)
        trianing_data_x = data.drop(data.columns[range(-3, 10)],axis = 1)
        trianing_data_y = data.loc[:,"MC返回"]
        transfer = RobustScaler()
        trian_x = transfer.fit_transform(trianing_data_x)
        model = LogisticRegression(max_iter=3000, solver='liblinear', penalty='l2', C =0.5)
        model.fit(trian_x,trianing_data_y)
        print("模型训练完成")
        coef = pd.DataFrame({'var' : pd.Series(trianing_data_x.columns),
                        'coef_abs' : abs(pd.Series(model.coef_[0].flatten()))
                        })
        coef = coef.sort_values(by="coef_abs", ascending=False)
        print("训练参数影响因子：")
        print(coef)
        predict_y = model.predict(trianing_data_x)
        print(classification_report(trianing_data_y, predict_y))  
        joblib.dump(model, self.model_save_path)
        print("训练模型已保存")
        return
def  binary_lr_analysis(data , parameter):
    set_plot_environment()
    data = data.loc[:,[parameter, "MC返回", "DC实修"]]
    data.dropna(how='any', axis=0,inplace=True)
    trianing_data_x = data.loc[:, parameter]
    min = trianing_data_x.min()
    max = trianing_data_x.max()
    trianing_data_y = data.loc[:,"DC实修"]
    X_train,X_test,Y_train,Y_test = train_test_split(trianing_data_x,trianing_data_y,train_size=0.8)
    # -----------二、将 训练数据 和 测试数据 用散点图表示出来
    plt.scatter(X_train,Y_train,color='b',label='train data')
    #plt.scatter(X_test,Y_test,color='r',label='teat data')
    #plt.legend(loc=2)
    plt.xlabel('压铸参数计测值')
    plt.ylabel('品质质量')
    plt.show()

    # ------------------ 三、建立训练模型
    # 引入逻辑回归算法，并创建逻辑回归模型
    model = LogisticRegression()
    model = LogisticRegression(max_iter=3000, solver='liblinear', penalty='l2', C =0.5)
    '''
    sklearn 要求输入的特征为：二维数组类型，目前只有一个特征，要用 reshape 转换成 二维数组类型；
    reshape(-1,1) 就是改变成 1列的数组，这个数组的长度是根据原始数组的大小自动形成的。
    '''
    X_train = X_train.values.reshape(-1,1)
    X_test = X_test.values.reshape(-1,1)
    model.fit(X_train,Y_train)
    print("Class:",model.classes_)
    print("Coef:",model.coef_)
    print("intercept",model.intercept_)
    print("n_iter",model.n_iter_)

    # 2.4 为了更深刻理解逻辑函数，根据逻辑回归函数及回归方程计算逻辑函数y值
    # 截距
    a = model.intercept_[0]
    # 回归系数
    b = model.coef_[0][0]
    x = np.arange(0.5*min,1.5*max,0.01)
    z = a+b*x
    y_pred = 1/(1+np.exp(-z))
    #y_range = 1/(1+np.exp(-(intercept+coef*x_range)))

    sb.lineplot(x=x, y=y_pred)
    plt.vlines(min, 0, 1, '#b2996e', '--', label='下限:'+str(min)) # 下图中垂直的棕色的线
    plt.vlines(max, 0, 1, 'r', '--', label='上限:'+str(max)) # 下图中垂直的棕色的线
    plt.legend()
    plt.xlabel(parameter)
    plt.ylabel('MC返回概率')
    plt.show() 