
from pyhive import hive

conn = hive.connect(host='node1',port=10000,username = 'root')
cursor = conn.cursor()



def queryhive(sql,params,type = 'no_select'):
    params = tuple(params)
    cursor.execute(sql,params)

    if type != 'no_select':
        data_list = cursor.fetchall()
        conn.commit()
        return data_list
    else:
        conn.commit()
        return '数据库语句执行成功'
#
# data = queryhive('SELECT * FROM moviedata', params=[], type='select')
# print(data[0])
