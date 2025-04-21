from utlis.querys import queryhive
from utlis.getData import *
from collections import Counter,defaultdict


def getCountryChartData():
    country_mapping = {
        '中国香港': 'Hong Kong',
        '印度': 'India',
        '英国': 'United Kingdom',
        '新西兰': 'New Zealand',
        '意大利': 'Italy',
        '中国台湾': 'Taiwan',
        '西班牙': 'Spain',
        '法国': 'France',
        '加拿大': 'Canada',
        '马来西亚': 'Malaysia',
        '澳大利亚': 'Australia',
        '韩国': 'South Korea',
        '爱尔兰': 'Ireland',
        '捷克': 'Czech Republic',
        '俄罗斯': 'Russia',
        '越南': 'Vietnam',
        '中国大陆': 'China',
        '日本': 'Japan',
        '美国': 'United States',
        '德国': 'Germany',
        '泰国': 'Thailand',
        '巴基斯坦': 'Pakistan',
        'Unknown': 'Unknown',
        '瑞士': 'Switzerland',
        '匈牙利': 'Hungary',
        '新加坡': 'Singapore',
        '阿联酋': 'United Arab Emirates',
        '巴哈马': 'Bahamas',
        '南非': 'South Africa',
        '芬兰': 'Finland',
        '黎巴嫩': 'Lebanon'
    }

    countryTotalTicket = list(getcountryTotalTicket())

    dataList = []
    for item in countryTotalTicket:
        english_name = country_mapping.get(item[0], item[0])  # Fallback to original if not found
        dataList.append({'name': english_name, 'value': item[1]})
    return dataList
def getcountryRateData():
    countryRateData = list(getcountryMeanRate())
    countryName = []
    countryRate = []
    for item in countryRateData:
        countryName.append(item[0])
        countryRate.append(round(item[1],2) if item[1] else 0)

    return countryName, countryRate

def getcountryMeanLengthData():
    lengthCountryName = []
    lengthCountryData = []
    for item in getcountryMeanLength():
        lengthCountryName.append(item[0])
        lengthCountryData.append(round(item[1],2) if item[1] else 0)

    return lengthCountryName, lengthCountryData

def getCountryName():
    topMovieData = list(getcountryTopMovie())
    countryName = []
    for item in topMovieData:
        countryName.append(item[0])
    return list(set(countryName))
def getcountryTopMovieData(defaultCountry):
    topMovieData = list(getcountryTopMovie())
    topMoiveName = []
    topMovieTicket = []
    for item in topMovieData:
        if item[0] == defaultCountry:
            topMoiveName.append(item[1])
            topMovieTicket.append(item[2])

    return topMoiveName, topMovieTicket
