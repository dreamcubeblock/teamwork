"""web框架的职责专门负责处理动态资源请求"""
import time
import json
import logging
import pymysql
import random

# index.html展示
def index(body):
    # 状态信息
    status = "200 OK"
    # 响应头信息
    response_header = [("Server", "PWS/1.1")]
    # 1. 打开指定模板文件，读取模板文件中的数据
    with open("./static/index.html", "r", encoding="utf-8") as file:
        file_data = file.read()

    # 这里返回的是元组
    return status, response_header, file_data


# 处理没有找到的动态资源
def not_found():
    # 状态信息
    status = "404 Not Found"
    # 响应头信息
    response_header = [("Server", "PWS/1.1")]
    # web框架处理后的数据
    data = "not found"

    # 这里返回的是元组
    return status, response_header, data


# 封装一个执行crud的函数
def execut_crud_sql(sql, data):
    # 连接mysql的服务端
    conc = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='28853379',
        database='group6',
        charset='utf8'
    )
    status_code = []  # status_code=0(successed status_code=1(failed)
    # 3.创建游标对象
    cur = conc.cursor()

    try:

        # 4.编写增加 数据的流程 SQL 语句
        # 5.使用游标对象 执行 SQL 语句
        cur.execute(sql, data)
        # 6.提交操作
        conc.commit()
    except Exception as e:
        print('操作失败:', e)
        status_code.append(str(e))
        # 回滚数据
        conc.rollback()
    finally:

        # 关闭游标
        cur.close()

        # 关闭连接
        conc.close()
        return status_code


# reg注册(插入)
def reg(body):
    conc = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='28853379',
        database='group6',
        charset='utf8'
    )
    status_code = []  # status_code=0(successed status_code=1(failed)
    cur = conc.cursor()
    try:
        sql = 'insert into user(username,passwd,plan) values(%s,%s,%s);'
        cur.execute(sql, body)
        conc.commit()

        sql = "select id from group6.user where username='" + body[0] + "';"
        cur.execute(sql)
        result = cur.fetchall()
        userid = result[0][0]

        sql = "create table user_" + str(userid) + "(wordid int,status int default 0);"
        cur.execute(sql)
        conc.commit()


        sql = "insert into user_" + str(userid) + "(wordid)" + " select wordid from word order by rand();"
        cur.execute(sql)
        conc.commit()

    except Exception as e:
        print('操作失败:', e)
        status_code.append(str(e))
        conc.rollback()
    finally:
        cur.close()
        conc.close()
    if status_code:
        data = {"ret": 1, "msg": status_code[0]}
    else:
        data = {"ret": 0}
    json_str = json.dumps(data, ensure_ascii=False)
    # 状态信息
    status = "200 OK"
    # 响应头信息
    response_header = [
        ("Server", "PWS/1.1"),
        # 指定编码格式，因为没有模板文件，可以通过响应头指定编码格式
        ("Content-Type", "text/html;charset=utf-8")
    ]
    return status, response_header, json_str


# login(select)
def login(body):
    # 2.链接mysql的服务端
    conc = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='28853379',
        database='group6',
        charset='utf8'
    )

    # 3.创建游标对象
    cur = conc.cursor()
    data_list = []
    try:
        # 4.编写 查询orders表的 所有数据 SQL
        sql = "select passwd from user where username='"+str(body[0])+"';"
        # 5.使用 游标对象 执行 SQL
        cur.execute(sql)

        # 6.获取查询的所有结果 fetchall()==>元祖
        result = cur.fetchall()

        # 7.将数据 转换成 [{},{}]
        if len(result):
            if body[1] == result[0][0]:
                data_list.append({
                    "ret": 0,
                    "userid": body[0],
                })
            else:
                data_list.append({
                    "ret": 1,
                    "msg": "用户名或密码错误"
                })
        else:
            data_list.append({
                "ret": 1,
                "msg": "用户名或密码错误"
            })

    # 若数据库执行失败，获取失败信息存入data_list
    except Exception as e:
        print('操作失败:', e)
        data_list.append({
            "ret": 1,
            "msg": str(e)
        })
        # 回滚数据
        conc.rollback()
    finally:
        # 关闭游标对象
        cur.close()
        # 关闭连接
        conc.close()

    # 把列表转成json字符串数据
    # ensure_ascii=False 表示在控制台能够显示中文
    json_str = json.dumps(data_list, ensure_ascii=False)

    # 状态信息
    status = "200 OK"
    # 响应头信息
    response_header = [
        ("Server", "PWS/1.1"),
        # 指定编码格式，因为没有模板文件，可以通过响应头指定编码格式
        ("Content-Type", "text/html;charset=utf-8")
    ]
    return status, response_header, json_str

# get_qu
def get_qu(body):
    conc = pymysql.Connect(host='127.0.0.1', port=3306, user='root', password='28853379', database='group6', charset='utf8')
    cur = conc.cursor()
    try:
        sql = "select id from group6.user where username='" + body[0] + "';"
        cur.execute(sql)
        result = cur.fetchall()
        userid = result[0][0]

        sql = "SELECT plan FROM user WHERE id = "+str(userid)+";"
        cur.execute(sql)
        plan = cur.fetchall()[0][0]

        sql = "select wordid,english,chinese from group6.word where wordid in(select wordid from group6.user_" + str(userid) + " where status='0') limit "+str(plan)+";"
        cur.execute(sql)
        result = cur.fetchall()

        data_list = []
        for each in result:
            sql = " select  chinese  from  group6.word where wordid!=" + "'" + str(each[1]) + "'" + " order by rand() limit 3;"
            cnAns = cur.fetchall()
            cnAns_list = [cnAns[0][0], cnAns[1][0], cnAns[2][0], each[2]]
            random.shuffle(cnAns_list)
            data_list.append({
                "cn": each[2],
                "en": each[1],
                "cnAns": [cnAns_list[0], cnAns_list[1], cnAns_list[2], cnAns_list[3]]
            })

    except Exception as e:
        print('操作失败:', e)
        data_list = []
        data_list.append({
            "ret": 1,
            "msg": str(e)
        })
        # 回滚数据
        conc.rollback()
    finally:
        # 关闭游标对象
        cur.close()
        # 关闭连接
        conc.close()

    # 状态信息
    status = "200 OK"
    # 响应头信息
    response_header = [
        ("Server", "PWS/1.1"),
        # 指定编码格式，因为没有模板文件，可以通过响应头指定编码格式
        ("Content-Type", "text/html;charset=utf-8")
    ]
    return status, response_header, str(data_list)

# change_plan
def change_plan(body):
    conc = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='28853379',
        database='group6',
        charset='utf8'
    )
    status_code = []  # status_code=0(successed status_code=1(failed)
    cur = conc.cursor()
    try:
        sql = "select id from group6.user where username='" + body[0] + "';"
        cur.execute(sql)
        result = cur.fetchall()
        userid = result[0][0]

        sql ="update user set plan = "+ str(body[1]) +" where id = "+ str(userid) +";"
        cur.execute(sql)
        conc.commit()

    except Exception as e:
        print('操作失败:', e)
        status_code.append(str(e))
        conc.rollback()
    finally:
        cur.close()
        conc.close()
    if status_code:
        data = {"ret": 1, "msg": status_code[0]}
    else:
        data = {"ret": 0}
    json_str = json.dumps(data, ensure_ascii=False)
    # 状态信息
    status = "200 OK"
    # 响应头信息
    response_header = [
        ("Server", "PWS/1.1"),
        # 指定编码格式，因为没有模板文件，可以通过响应头指定编码格式
        ("Content-Type", "text/html;charset=utf-8")
    ]
    return status, response_header, json_str


def done(body):
    conc = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='28853379',
        database='group6',
        charset='utf8'
    )
    status_code = []  # status_code=0(successed status_code=1(failed)
    cur = conc.cursor()
    try:
        sql = "select id from group6.user where username='" + body[0] + "';"
        cur.execute(sql)
        result = cur.fetchall()
        userid = result[0][0]

        sql = "SELECT plan FROM user WHERE id = " + str(userid) + ";"
        cur.execute(sql)
        plan = cur.fetchall()[0][0]

        sql = "update user_"+ str(userid) +" set status = 1 where status = 0 limit "+ str(plan) +";"
        cur.execute(sql)
        conc.commit()


    except Exception as e:
        print('操作失败:', e)
        status_code.append(str(e))
        conc.rollback()
    finally:
        cur.close()
        conc.close()
    if status_code:
        data = {"ret": 1, "msg": status_code[0]}
    else:
        data = {"ret": 0}
    json_str = json.dumps(data, ensure_ascii=False)
    # 状态信息
    status = "200 OK"
    # 响应头信息
    response_header = [
        ("Server", "PWS/1.1"),
        # 指定编码格式，因为没有模板文件，可以通过响应头指定编码格式
        ("Content-Type", "text/html;charset=utf-8")
    ]
    return status, response_header, json_str


def more_qu(body):
    conc = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='28853379',
        database='group6',
        charset='utf8'
    )
    cur = conc.cursor()
    try:
        sql = "select id from group6.user where username='" + body[0] + "';"
        cur.execute(sql)
        result = cur.fetchall()
        userid = result[0][0]

        sql = "select wordid,english,chinese from group6.word where wordid in(select wordid from group6.user_" + str(userid) + " where status='0') limit "+str(body[1])+";"
        cur.execute(sql)
        result = cur.fetchall()

        data_list = []
        for each in result:
            sql = " select  chinese  from  group6.word where wordid!=" + "'" + str(each[0]) + "'" + " order by rand() limit 3;"



            cnAns = cur.fetchall()
            cnAns_list = [cnAns[0][0], cnAns[1][0], cnAns[2][0], each[2]]
            random.shuffle(cnAns_list)
            data_list.append({
                "cn": each[2],
                "en": each[1],
                "cnAns": [cnAns_list[0], cnAns_list[1], cnAns_list[2], cnAns_list[3]]
            })

    except Exception as e:
        print('操作失败:', e)
        data_list = []
        data_list.append({
            "ret": 1,
            "msg": str(e)
        })
        # 回滚数据
        conc.rollback()
    finally:
        # 关闭游标对象
        cur.close()
        # 关闭连接
        conc.close()

    # 状态信息
    status = "200 OK"
    # 响应头信息
    response_header = [
        ("Server", "PWS/1.1"),
        # 指定编码格式，因为没有模板文件，可以通过响应头指定编码格式
        ("Content-Type", "text/html;charset=utf-8")
    ]
    return status, response_header, str(data_list)


def more_qu_done(body):
    conc = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='28853379',
        database='group6',
        charset='utf8'
    )
    status_code = []  # status_code=0(successed status_code=1(failed)
    cur = conc.cursor()
    try:
        sql = "select id from group6.user where username='" + body[0] + "';"
        cur.execute(sql)
        result = cur.fetchall()
        userid = result[0][0]

        sql = "update user_"+ str(userid) +" set status = 1 where status = 0 limit "+ str(body[1]) +";"
        cur.execute(sql)
        conc.commit()


    except Exception as e:
        print('操作失败:', e)
        status_code.append(str(e))
        conc.rollback()
    finally:
        cur.close()
        conc.close()
    if status_code:
        data = {"ret": 1, "msg": status_code[0]}
    else:
        data = {"ret": 0}
    json_str = json.dumps(data, ensure_ascii=False)
    # 状态信息
    status = "200 OK"
    # 响应头信息
    response_header = [
        ("Server", "PWS/1.1"),
        # 指定编码格式，因为没有模板文件，可以通过响应头指定编码格式
        ("Content-Type", "text/html;charset=utf-8")
    ]
    return status, response_header, json_str


# 路由列表
route_list = [

    ('/index.html', index), # 主页 GET

    ('/api/reg.html', reg), # 注册 POST
                            # 请求：username password plan
                            # 响应："ret":0

    ('/api/login.html', login), # 登录 POST
                                # 请求：username password
                                # 响应："ret": 0 "username":用户名

    ('/api/get_qu.html', get_qu),   # 获取今日单词 POST
                                    # 请求：username
                                    # 响应: [{
                                    #         'cn': 'vt.刺；刺痛',
                                    #         'en': 'sting',
                                    #         'cnAns': [
                                    #                   'vt.刺；刺痛',
                                    #                   'n.耙子',
                                    #                   'prep.除…之外',
                                    #                   'pron.我们的'
                                    #                   ]
                                    #       },{...}
                                    #       ]

    ('/api/change_plan.html', change_plan),  # 改变计划 POST
                                            # 请求：username plan
                                            # 响应："ret":0

    ('/api/done.html', done),   # 完成每日计划确认 POST
                                # 请求：username
                                # 响应："ret": 0

    ('/api/more_qu.html', more_qu)  # 获取计划外单词 POST
                                    # 请求：username qnum
                                    # 响应: 格式同get_qu

    ('/api/more_qu_done.html', more_qu_done)    # 计划外单词完成确认 POST
                                                # 请求：username qnum
                                                # 响应: "ret": 0
]


# 处理动态资源请求f
def handle_request(env):
    # 获取动态的请求资源路径
    request_path = env["request_path"]
    print("动态资源请求的地址:", request_path)
    body = env.get('body')
    # 遍历路由列表，匹配请求的url
    for path, func in route_list:
        if request_path == path:
            # 找到了指定路由，执行对应的处理函数
            result = func(body)
            return result
    else:
        # 没有动态资源数据, 返回404状态信息
        result = not_found()
        logging.error("没有设置相关的路由信息:" + request_path)
        # 把处理后的结果返回给web服务器使用，让web服务器拼接响应报文时使用
        return result
