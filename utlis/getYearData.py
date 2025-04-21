from utlis.querys import queryhive
from utlis.getData import *
from collections import Counter,defaultdict


def merge_year_data(yearRateList, yearRate, yearMovieName, yearMovieCount):
    """
    清洗并合并评分数据和电影数量数据，自动处理None值和年份对齐

    参数:
        yearRateList: 评分数据的年份列表（可能含None）
        yearRate: 对应的评分列表
        yearMovieName: 电影数量的年份列表（可能含None）
        yearMovieCount: 对应的电影数量列表

    返回:
        merged_years: 合并后的有效年份列表（按数字顺序排序）
        merged_rates: 对应年份的评分列表（无None）
        merged_counts: 对应年份的电影数量列表（无None）
    """

    # 第一步：清洗数据，移除None年份和对应值
    def clean_data(years, values):
        return [(y, v) for y, v in zip(years, values)
                if y is not None and v is not None]

    # 清洗评分数据
    cleaned_rates = clean_data(yearRateList, yearRate)
    # 清洗电影数量数据
    cleaned_counts = clean_data(yearMovieName, yearMovieCount)

    # 第二步：转换为字典（年份作为键）
    rate_dict = dict(cleaned_rates)
    count_dict = dict(cleaned_counts)

    # 第三步：获取所有有效年份并排序
    all_years = sorted(
        set(rate_dict.keys()).union(set(count_dict.keys())),
        key=lambda x: int(x)
    )
    # 第四步：合并数据（只保留两个数据集都有的年份）
    merged_years = []
    merged_rates = []
    merged_counts = []

    for year in all_years:
        if year in rate_dict and year in count_dict:
            merged_years.append(year)
            merged_rates.append(rate_dict[year])
            merged_counts.append(count_dict[year])

    return merged_years, merged_rates, merged_counts


def getYearData():
    data = list(getyearTopMovie())
    yearList = []
    for item in data:
        yearList.append(str(item[0]))
    yearList = list(set(yearList))
    yearList.sort(reverse=True)
    return yearList

def getTopMovieData(defaultYear):
    data = list(getyearTopMovie())

    topMovieName = []
    topMovieTicket = []
    for item in data:
        if str(item[0]) == defaultYear:
            topMovieName.append(item[1])
            topMovieTicket.append(item[2])
    return topMovieName,topMovieTicket

def getyearMovieData():
    data = list(getyearMovie())

    yearMovieName = []
    yearMovieCount = []
    for item in data:
        yearMovieName.append(item[0])
        yearMovieCount.append(item[1])

    return yearMovieName,yearMovieCount
def getyearMeanRateData():
    data = list(getyearMeanRate())
    yearRateList = []
    yearRate = []
    for item in data:
        yearRateList.append(item[0])
        yearRate.append(item[1])

    return yearRateList,yearRate

def getyearTotalTicketData():
    data = list(getyearTotalTicket())
    yeatTotalList = []
    yearTotalTicket = []
    for item in data:
        if item[0]:
            yeatTotalList.append(item[0])
            yearTotalTicket.append(item[1])
    sortData = []
    for item in zip(yeatTotalList,yearTotalTicket):
        sortData.append(item)
    yeatTotalList = []
    yearTotalTicket = []
    sortData.sort(key=lambda x: x[0],reverse=True)
    for item in sortData:
        yeatTotalList.append(item[0])
        yearTotalTicket.append(item[1])

    return yeatTotalList,yearTotalTicket
