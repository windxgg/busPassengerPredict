#目录说明：

##source:
* CheckTrainData.py：查看原始数据
* DealTrainData.py：处理交易数据
* DealWeatherData.py：处理天气数据
* error.py：误差函数
* ExploreTrainData.py：交易数据探索绘图
* ExploreTrainWeather.py：交易数据关联天气数据探索绘图
* predict.py：预测20141225-20141231的客流
* TestDataResult.py：测试集生成
* TrainDataResult.py：训练集生成
* TrainModel.py：训练模型

##data:
由于大赛已经结束，咱们就把20141225-20141231的交易数据拿出来当作未知

* date_holiday.txt：日期节假日、工作日数据
* gd_line_desc.txt：比赛提供的公交线路信息数据
* gd_train_data.txt：比赛提供的原始交易数据
* gd_weather_report.txt：比赛提供的天气状况
* line6_passenger_hour_test.csv：20141225-20141231线路6的客流
* line11_passenger_hour_test.csv：20141225-20141231线路11的客流
* train_data.csv：去掉20141225-20141231的交易数据
* train_data_test.csv：20141225-20141231的交易数据，作为测试集

由于github对单个文件大小有限制，我把数据上传到了百度云盘
链接：https://pan.baidu.com/s/1vRsr_ur7fgtSz7GHzlALSw 密码：x1r4

##model:
存放训练好的模型