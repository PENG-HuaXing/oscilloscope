## WaveForm

这个类是波形信号类，拥有两种初始化方法，其一是使用numpy的时间和幅值进行初始化，其二是通过读取csv波形数据文件进行初始化。 若是波形数据是其他的格式，可以使用DataSetTool中读取文件功能将数据转化成为numpy形式，因此后续如果有其他类型的波形数据需要读取，直接在DataSetTool内增加新的类即可。

WaveForm类的成员变量有`self.time（时间序列）`，`self.ampl（幅值序列）`，`self.bound1（时间边界值1）`，`self.bound2（时间边界值2）`，`self.delta_time（时间步长）`

WaveForm类的成员函数

+ `_value2index`：将输入的时间数值转化为时间序列最近的索引
+ `_interval2index`：将输入的时间区间转化为时间序列中在该区间的索引列表，此列表可以直接应用在numpy.ndarray类型数据中得到相应的时间序列数据
+ `get_time`：pass
+ `get_ampl`：pass
+ `get_time_bound`：pass
+ `get_delta_time`：pass
+ `integrate`：指定区间和基线进行积分，积分方法可以选择梯形积分法，或者矩形积分法
+ `max_ampl`：区间内幅值的极大值
+ `min_ampl`：同上
+ `trigger`：指定区间和阈值，进行触发判选
+ `pedestal`：指定区间，计算基线$ped = \frac{\int_a^{b}f(x)dx}{b-a}$，积分的计算方法和上面计算积分同样，分为矩形积分法和梯形积分法

## SinglePhotonSpectrum

在经过上面WaveForm积分循环操作后，应该会得到一个记录`File|Q|ped|......`这几列数据的csv文件，我们暂时叫做Spe数据文件，SinglePhotonSpectrum类就是初步处理这个文件的类。该类可以通过两种方式初始化，其一是使用pd.DataFrame类型数据初始化，另外一种是读取csv文件。

此类的结构比较简单，主要是对Spe数据的初步处理，后续处理包括绘制Histogram， 拟合以及计算后脉冲处理均在其他类中实现。类的成员变量有四个`self.pd_data（以pandas数据类型记录Spe数据文件）`,`self.max（Q极大值，对于确定Histo边界有用）`,`self.min（Q极小值）`,`self.num（数据总量）`

WaveForm类的成员函数

+ `get_info`：获取大部分的成员变量，返回字典类型数据
+ `get_pandas_data`：返回pandas类型的Spe数据
+ `get_charge`：返回所有电荷Q的numpy列表
+ `proportion`：输入一个电荷阈值，得到高于该阈值和低于该阈值的两部分事例数，用于寻找信号数据，判断是否在单光子状态

## SpeHist

这个类主要是生成单光电子谱，并谱进行拟合，不过目前python的scipy对于全局拟合（较为复杂的函数模型）存在问题，对于单高斯拟合效果较好。此类的初始化需要几个参数：

1. 电荷的numpy列表，可以使用上面SinglePhotonSpectrum类的get_charge方法获取
2. bins， 可以有默认和自定义两种形式，默认则会使用电荷numpy列表的极值作为bins的边沿。自定义则需要自己设定
3. scale数值，作为可选的参数，默认值为1，但是为了更好的拟合，可以使用scale将单光电子谱进行等比例放大。

SpeHist类的成员变量有下面几个`self.edge1`,`self.edge2（这两个分别是bins的最小边界和最大边界）`，`self.bin_num（bins的数量）`,`self.hist_content（使用np.hist后得到每个bin的content）`,`self.scatter_x`,`self.scatter_y（hist转化为散点图，用于拟合）`

SpeHist的成员函数

+ `get_scatter`：获取散点数据
+ `get_hist`：获取content和bins的数据
+ `get_info`：获取简单的成员变量，包括bins的上下边界值，bins的数量，以及`scale`
+ `model_gauss`：`model_fun`这种形式的皆为静态函数，是相应的函数模型
+ `fit_spe`：核心函数，利用样本的散点进行拟合，主要可以拟合高斯或者全局拟合两种预设拟合方式，不过全局拟合curve_fit表现不是很好，可以尝试使用root进行拟合。返回值为包含拟合参数和协方差的一个元组

## AfterPulse

AfterPulse类是寻找，记录，保存后脉冲数据的类，其初始化也需要SinglePhotonSpectrum对Spe数据进行初步的处理，使用proportion方法筛选出具有信号的pandas数据传入AfterPulse对其进行初始化。AfterPulse初始化还需要几个参数：①`ap_trigger`后脉冲触发判选阈值，只有超过该阈值才会对相应的区域进行积分。②`ap_window`对后脉冲积分时的积分窗口值。③`ap_region`后脉冲区域，一般是信号后到整个波形时间末尾。④`ped_flag`对后脉冲积分时是否减去基线

AfterPulse的成员变量和初始化过程中的形参基本一致，不再赘述

AfterPulse的成员函数

+ `search_after_pulse`：静态函数。在后脉冲区域寻找后脉冲信号，需要输入相应的波形文件，以及后脉冲触发阈、后脉冲区域、积分窗口、基线flag参数。得到time列表和ampl列表，列表长度为单个波函数中后脉冲的个数。数据形式为`[time1, time2, time3], [amp1, amp2, amp3]`
+ `zip_data`：静态函数，主要是将上面的函数寻找得到time和ampl数据进行整合，以及添加上文件名称数据。处理后的数据形式`[[file1, time1, amp1], [file1, time2, amp2], [file1, time3, amp3]]`。并且这种形式的数据容易写入pandas中
+ `loop_all`：利用上面的两个函数对成员变量中存储的`self.pd_data`所有信号数据寻找后脉冲，并保存成csv文件内容有三列`File|Time|Q`

