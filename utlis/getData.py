from utlis.querys import queryhive

def getMovieData():
    return queryhive('SELECT * FROM default.moviedata', params=[], type='select')


def getmovieTagCount():
    return queryhive('SELECT * FROM default.movieTagCount', params=[], type='select')

def getticketTopMovie():
    return queryhive('SELECT * FROM default.ticketTopMovie', params=[], type='select')

def gettypeTopMovie():
    return queryhive('SELECT * FROM default.typeTopMovie', params=[], type='select')

def getcountryCount():
    return queryhive('SELECT * FROM default.countryCount', params=[], type='select')



def getrateCount():
    return queryhive('SELECT * FROM default.rateCount', params=[], type='select')

#####################################
def gettypeCountRate():
    return queryhive('SELECT * FROM default.typeCountRate', params=[], type='select')
def getavgTypeLen():
    return queryhive('SELECT * FROM default.avgTypeLen', params=[], type='select')
def getperTypeTickets():
    return queryhive('SELECT * FROM default.perTypeTickets', params=[], type='select')

def getmeanTypeRate():
    return queryhive('SELECT * FROM default.meanTypeRate', params=[], type='select')



###################################
def getcountryMeanRate():
    return queryhive('SELECT * FROM default.countryMeanRate', params=[], type='select')

def getcountryMeanLength():
    return queryhive('SELECT * FROM default.countryMeanLength', params=[], type='select')

def getcountryTotalTicket():
    return queryhive('SELECT * FROM default.countryTotalTicket', params=[], type='select')
def getcountryTopMovie():
    return queryhive('SELECT * FROM default.countryTopMovie', params=[], type='select')

###########################

def getyearMeanRate():
    return queryhive('SELECT * FROM default.yearMeanRate', params=[], type='select')

def getyearMovie():
    return queryhive('SELECT * FROM default.yearMovie', params=[], type='select')

def getyearTotalTicket():
    return queryhive('SELECT * FROM default.yearTotalTicket', params=[], type='select')

def getyearTopMovie():
    return queryhive('SELECT * FROM default.yearTopMovie', params=[], type='select')