from utlis.querys import queryhive
from utlis.getData import *
from collections import Counter

###电影标签统计###
def tagData():
    movieTagList = list(getmovieTagCount())
    tagChartData = []
    for tag in movieTagList:
        tagChartData.append({
            'name':tag[0],
            'value':tag[1]
        })
    return tagChartData

##前10电影信息##
def ticketTopData():
    ticketTopData = list(getticketTopMovie())
    topName = [x[1] for x in ticketTopData]
    topRate = [x[6] for x in ticketTopData]
    topAllTicket = [x[12] for x in ticketTopData]
    topType = [x[2] for x in ticketTopData]
    topTime = [x[5] for x in ticketTopData]

    return topName, topRate, topAllTicket,topType,topTime,zip(topName, topType, topAllTicket, topTime)

##评分分布##
def rateCount():
    rateCount_list = list(getrateCount())
    sum = 0
    for rate in rateCount_list:
        sum += rate[1]
    rateCountData = [
        {
            'name':x[0],
            'value':round(x[1] / sum,2) * 100
        }
        for x in rateCount_list
    ]
    return rateCountData

##国家电影数量分布##
def countryCount():
    countryCount_list = list(getcountryCount())
    countryCount_list.sort(key = lambda x: x[1], reverse=True)
    count = Counter()

    for country in countryCount_list[:11]:
        count[country[0].strip()] += country[1]
    countryName = list(count.keys())
    countrycont = list(count.values())
    return countryName, countrycont

##种类票房##
def perTypeTicket():
    perTypeTicketData = list(getperTypeTickets())
    # print(perTypeTicketData)

def perTypeTopMovie():
    perTypeTopMovieData = list(gettypeTopMovie())
    sortedMovieData = sorted(perTypeTopMovieData, key=lambda x: x[2], reverse=True)
    sortedMovieData = sortedMovieData[:10]
    tagName = []
    firstWeek = []
    total = []
    for movie in sortedMovieData:
        tagName.append(movie[0])
        firstWeek.append(movie[1])
        total.append(movie[2])
    return (tagName,firstWeek,total)
