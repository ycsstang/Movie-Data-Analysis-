from utlis.querys import queryhive
from utlis.getData import *
from collections import Counter,defaultdict


def getTypeData():
    typeData = [x[0] for x in list(getavgTypeLen())]
    return list(set(typeData))
def getChartOneDataByType(defaultType):
    perTypeDataTicket = list(getperTypeTickets())

    typeTopName = []
    typeTopTicket = []
    for item in perTypeDataTicket:
        if item[0] == defaultType:
            typeTopName.append(item[1])
            typeTopTicket.append(item[2])
    return typeTopName, typeTopTicket

def getRateCountByType(defaultType):
    typeRateCountData = list(gettypeCountRate())
    typeRateData = []
    typeRateDataCount = []
    for item in typeRateCountData:
        if item[0] == defaultType:
            typeRateData.append(item[1])
            typeRateDataCount.append(item[2])
    # 初始化分组字典
    grouped_data = defaultdict(int)

    # 将数据分组并累加计数
    for rate, count in zip(typeRateData, typeRateDataCount):
        # 计算所属区间
        group_index = rate // 10 * 10
        if rate == 100:  # 处理100分的特殊情况
            group_index = 90
        group_key = f"{group_index}-{group_index + 9}"
        if group_index == 90:  # 90-100区间
            group_key = "90-100"
        grouped_data[group_key] += count

    # 转换为有序列表
    sorted_groups = sorted(grouped_data.items(), key=lambda x: int(x[0].split('-')[0]))
    rating_ranges = [item[0] for item in sorted_groups]
    count_totals = [item[1] for item in sorted_groups]
    return rating_ranges, count_totals

def getAvgLengthData():
    avgLengthData = list(getavgTypeLen())
    typeName = []
    typeLength = []
    for item in avgLengthData:
        typeName.append(item[0])
        typeLength.append(round(item[1],2))
    return typeName, typeLength