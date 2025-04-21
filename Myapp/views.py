import json

import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from Myapp.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from utlis.querys import *
from utlis.getData import *
from utlis.getIndexChartData import *
from utlis.getTypeChartData import *
from utlis.getCountryChartData import *
from utlis.getYearData import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    username = request.session['username']
    UserInfo = User.objects.get(username=username)
    tagChartData = tagData()
    topName, topRate, topAllTicket,topType,topTime,zipData = ticketTopData()
    maxTicket = topAllTicket[0]
    maxTicketMovie = topName[0]
    maxTicketMoiveType = topType[0]
    rateCountData = rateCount()
    countryName, countrycont = countryCount()
    perTypeTicketData = perTypeTicket()
    tagName,firstWeek,total = perTypeTopMovie()
    return render(request,'index.html', {
        'userInfo': UserInfo,
        'tagChartData':tagChartData,
        'topName':topName,
        'topRate':topRate,
        'topAllTicket':topAllTicket,
        'topType':topType,
        'topTime':topTime,
        'zipData':zipData,
        'rateCountData':rateCountData,
        'countryName':countryName,
        'countryCount':countrycont,
        'tagName':tagName,
        'firstWeek':firstWeek,
        'total':total,
        'maxTicket':maxTicket,
        'maxTicketMovie':maxTicketMovie,
        'maxTicketMoiveType':maxTicketMoiveType,
    })


def catChart(request):
    username = request.session['username']
    UserInfo = User.objects.get(username=username)
    typeData = getTypeData()
    defaultType = request.GET.get('typeName') or '剧情'
    typeTopName, typeTopTicket = getChartOneDataByType(defaultType)
    typeName, typeLength = getAvgLengthData()
    rating_ranges, count_totals = getRateCountByType(defaultType)
    return render(request, 'catChart.html', {
        'userInfo': UserInfo,
        'typeData':typeData,
        'defaultType':defaultType,
        'typeTopName':typeTopName,
        'typeTopTicket':typeTopTicket,
        'rating_ranges':rating_ranges,
        'count_totals':count_totals,
        'typeName':typeName,
        'typeLength':typeLength,

    })

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {})

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # 验证字段非空
        if not username or not password:
            message = '用户信息不可为空'
            messages.error(request, message)
            return redirect('/myApp/login', )

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if password == user.password:
                request.session['username'] = user.username
                return redirect('/myApp/index')
            else:
                messages.error(request,'密码错误')
                return redirect('/myApp/login', )
        else:
            messages.error(request, '用户名不存在')
            return redirect('/myApp/login')

def register(request):
    if request.method == "GET":
        return render(request, 'register.html', {})
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        checkPwd = request.POST['checkPwd']
        accept_terms = request.POST.get('accept_terms')  # 是否接受协议

        # 验证用户名是否已存在
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户已存在')
            return redirect('/myApp/register')

        # 验证协议是否勾选
        if not accept_terms:
            messages.error(request, '请接受协议和隐私政策')
            return redirect('/myApp/register')

        # 验证字段非空
        if not username or not password or not checkPwd:
            message = '用户信息不可为空'
            messages.error(request, message)
            return redirect('/myApp/register',)

        if password != checkPwd:
            message = '两次输入密码不一致，请检查'
            messages.error(request, message)
            return redirect('/myApp/register',)

        # 创建用户
        try:
            user = User.objects.create(username=username, password=password)
            messages.success(request, '注册成功！')
            return redirect('/myApp/login')
        except Exception as e:
            messages.error(request, f'注册失败: {str(e)}')
            return redirect('/myApp/register')

def logOut(request):
    request.session['username'] = ''
    return redirect('/myApp/login')


def countryChart(request):
    username = request.session['username']
    UserInfo = User.objects.get(username=username)
    countryTicketData = getCountryChartData()
    countryName, countryRate = getcountryRateData()
    lengthCountryName, lengthCountryData = getcountryMeanLengthData()

    topCountryName = getCountryName()
    defaultCountry = request.GET.get('countryName') or '中国大陆'

    topMoiveName, topMovieTicket = getcountryTopMovieData(defaultCountry)
    return render(request, 'countryChart.html', {
        'userInfo': UserInfo,
        'countryTicketData': json.dumps(countryTicketData),  # 转换为JSON字符串
        'countryName': countryName,
        'countryRate': countryRate,
        'lengthCountryName': lengthCountryName,
        'lengthCountryData': lengthCountryData,
        'topCountryName': topCountryName,
        'defaultCountry': defaultCountry,
        'topMoiveName':topMoiveName,
        'topMovieTicket':topMovieTicket,
    })

def timeChart(request):
    username = request.session['username']
    UserInfo = User.objects.get(username=username)
    topYearList = getYearData()
    defultYear = request.GET.get('yearName') or '2018'
    topMovieName, topMovieTicket = getTopMovieData(defultYear)
    yearMovieName,yearMovieCount = getyearMovieData()
    yearRateList,yearRate = getyearMeanRateData()
    yeatTotalList,yearTotalTicket = getyearTotalTicketData()

    merged_years, merged_rates, merged_counts = merge_year_data(
        yearRateList, yearRate,
        yearMovieName, yearMovieCount
    )

    return render(request, 'timeChart.html', {
        'userInfo': UserInfo,
        'topYearList':topYearList,
        'defultYear':defultYear,
        'topMovieName':topMovieName,
        'topMovieTicket':topMovieTicket,
        'yearMovieName':yearMovieName,
        'yearMovieCount':yearMovieCount,
        'yearRateList':yearRateList,
        'yearRate':yearRate,
        'yeatTotalList':yeatTotalList,
        'yearTotalTicket':yearTotalTicket,
        'merged_years':merged_years,
        'merged_rates':merged_rates,
        'merged_counts':merged_counts,

    })

def ticketChart(request):
    return render(request, 'ticketChart.html', {})


def totalMovies(request):
    username = request.session['username']
    UserInfo = User.objects.get(username=username)
    movieData = list(getMovieData())
    # 获取搜索参数
    search_query = request.GET.get('q', '').lower()
    def contains(value,query):
        if value is None or value == '':
            return False
        else:
            return query.lower() in str(value).lower()
    # 如果有搜索词，过滤数据
    if search_query:
        filtered_data = [
            item for item in movieData
            if (contains(item[1], search_query) or  # 名称
                contains(item[2], search_query) or  # 国家
                contains(item[5], search_query) or  # 演员
                contains(item[6], search_query))  # 导演
        ]
    else:
        filtered_data = movieData
    page = request.GET.get('page', 1)
    paginator = Paginator(filtered_data, 6)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    movieData = page_obj.object_list
    return render(request,'totalMovie.html',{
        'userInfo':UserInfo,
        'movieData':movieData,
        'page':page,
        'page_obj':page_obj,
        'search_query':search_query,

    })