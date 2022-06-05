import datetime
import json
import os
import random
import re
import threading
import time
#from io import StringIO
import execjs
import pytz
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from lxml import etree

import wenjuanxing

# 输出时间
__js_engine = execjs.compile(wenjuanxing.JSCODE)
# cktool md5 MD5: ceb3b8327189ff82d4c99a6c47d7acc7
div_tag1 = []
div_tag2 = []
# 企业微信推送
corpid = 'wwc5cf4219baacc89e'
agentid = '1000004'
corpsecret = '5yCu77gkY9iyDSJLrK9e3GjPyNhk6OqMsqV6Iv_oSyQ'
# pushusr = 'Bimozhiyan'  # 企业微信推送用户,默认'@all'为应用全体用户

data_am = r'个人数据'

data_pm = '个人数据'

data = {
    'submitdata': '1$1}2$}3$}4$山西省太原市万柏林区千峰街道博学东路太原理工大学虎峪校区[112.521114,37.859621]}5$}6$2}7$1!|}8$1}9$1}10$3}11$(跳过)^(跳过)^(跳过)^(跳过)^(跳过)}12$3}13$-3}14$2}15$(跳过)^(跳过)^(跳过)^(跳过)^(跳过)^(跳过)}16$1'
}
# 日志中写入 现在时间
tz = pytz.timezone('Asia/Shanghai')

c_time = datetime.datetime.now(tz)
nowtime = str(datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")).replace('-', '/')
new_time = str(time.mktime(time.strptime(nowtime, '%Y/%m/%d %H:%M:%S')) + int(2) * 60)[:10]

# sio = StringIO('      疫情签到日志\n')
# sio.seek(0, 2)  # 将读写位置移动到结尾
# sio.write("===" + nowtime + "===\n")


class WXPusher:
    def __init__(self, usr=None, desp=None):
        self.base_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
        self.req_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='
        self.corpid = corpid  # 填写企业ID
        self.corpsecret = corpsecret  # 应用Secret
        self.agentid = int(agentid)  # 填写应用ID，是个整型常数,就是应用AgentId
        if usr is None:
            usr = '@all'
        self.usr = usr
        self.msg = desp

    def get_access_token(self):
        urls = self.base_url + 'corpid=' + self.corpid + '&corpsecret=' + self.corpsecret
        resp = requests.get(urls).json()
        access_token = resp['access_token']
        return access_token

    def send_message(self):
        data = self.get_message()
        req_urls = self.req_url + self.get_access_token()
        res = requests.post(url=req_urls, data=data)
        print(res.text)

    def get_message(self):
        data = {
            "touser": self.usr,
            "toparty": "@all",
            "totag": "@all",
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": self.msg
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        data = json.dumps(data)
        return data


# 全局变量
def get_geturl():
    # 获取含参网站
    url = "https://tyutgs.wjx.cn/user/qlist.aspx?u=%E6%89%8B%E6%9C%BA%E7%94%A8%E6%88%B7tivliw38j0y8djcff6vstq&userSystem=1&systemId=55677040"
    payload = {}
    headers = {
        'Host': 'tyutgs.wjx.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"',
        'sec-ch-ua-mobile': '?0',
        'Referer': 'https://tyutgs.wjx.cn/user/loginForm.aspx?user_token=RzCs8KPQb4VEfycFVJ8OMztE5FTgJGXpBj0M1NsuatiZzuullOcE2qNhFz1gNCLMf2Rz0IoQ2%2b%2fQvHgDWQRylqbGCNwf9At747llgCvdCidNf%2fEPUf6k4g%3d%3d&returnUrl=%2fuser%2fqlist.aspx%3fu%3d%25e6%2589%258b%25e6%259c%25ba%25e7%2594%25a8%25e6%2588%25b7tivliw38j0y8djcff6vstq%26userSystem%3d1%26systemId%3d55677040 ',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        # 'Cookie': cook_value
        # 'Hm_lvt_21be24c80829bd7a683b2c536fcf520b=1612156172; acw_tc=2f624a4b16285696992693771e56b920fd5f5b71ea8944
        # 49a9cd707ff56f0a; .ASPXANONYMOUS=vjAb_DHE1wEkAAAANDY5NmMyZTYtM2U1Ny00NDVmLWJlZmMtNWYzNjQwZTQ3NTlinmxYqoPfbWpYC2LotPXoRtdUKS41; yksuserinfo_e2369e3a6980baa283793081acb7b3ae_1_55677040_ext={"40000":["26"]}; yksuserinfo_e2369e3a6980baa283793081acb7b3ae_1_55677040=3BqzmdV9BvRT5+2iH7VZgJm+oTXI+aD7xTOt7YWu1MVwR+XA0u9eOwpT8teV2glNwlVpPhaNiK8wnPgXHqbT4ABwnrL/WjePBaDecofcNwvn9XpwlG4AGxDQEql8Ub7eYA708RsB4izmCmF2Nhjlvyfr97WxWS/Jjki+ye5xUJe/BaE/lLjL2ZFZ52lXCFoqadoYadxe8ljQTBBdBVYO01rPq8vvQURSkG9TAXKSbHRoCqZ6P3+cIqtVXdxHehKoZrrdHMzVgPgrIc7Lc5EnWiUSSlTN5ClWvjfnJoVwpGvD438WMi4m0NOu5sd8GxNk8KlqiqFU6bskpLSC2VMQ7eAxN4jE8EFMIGsggU6a1h8rr4TNxWnDrnn2xxjGUPNcM3JY3fjLP+2zwMc5+/YuMsepK76NrScHrK6y2HhndLuo9TRMan+K6UwMm8UlKLRlqNB/L/fQcgyU25xLw7ySdA==; SERVERID=3f9180de4977a2b2031e23b89d53baa6|1628569755|1628569699; .ASPXANONYMOUS=l5dj2TLE1wEkAAAAZjczOWI0ZDAtMGY3Ny00YTA5LWI5MWQtMjdmMzM5M2RlMGI2uqc--Uzyng3PBKG2YZj_HUtm5Fk1; SERVERID=3f9180de4977a2b2031e23b89d53baa6|1628697053|1628697053; yksuserinfo_e2369e3a6980baa283793081acb7b3ae_1_55677040=3BqzmdV9BvRT5+2iH7VZgJm+oTXI+aD7xTOt7YWu1MVwR+XA0u9eOwpT8teV2glNwlVpPhaNiK8wnPgXHqbT4ABwnrL/WjePBaDecofcNwvn9XpwlG4AGxDQEql8Ub7eYA708RsB4izmCmF2Nhjlvyfr97WxWS/Jjki+ye5xUJe/BaE/lLjL2ZFZ52lXCFoqadoYadxe8ljQTBBdBVYO01rPq8vvQURSkG9TAXKSbHRoCqZ6P3+cIqtVXdxHehKoZrrdHMzVgPgrIc7Lc5EnWiUSSlTN5ClWvjfnJoVwpGvD438WMi4m0NOu5sd8GxNk8KlqiqFU6bskpLSC2VMQ7eAxN4jE8EFMIGsggU6a1h8rr4TNxWnDrnn2xxjGUPNcM3JY3fjLP+2zwMc5+/YuMsepK76NrScHrK6y2HhndLuo9TRMan+K6UwMm8UlKLRlqNB/L/fQcgyU25xLw7ySdA==; yksuserinfo_e2369e3a6980baa283793081acb7b3ae_1_55677040_ext={"40000":["26"]}'
    }

    response = requests.request("GET", url, headers=headers, data=payload, cookies=cook_value)

    r = response.text
    # print(response.text)
    selector = etree.HTML(r)
    post_urls = selector.xpath('//*[@id="ulQs"]/dl/a/@href')  # print(response.text)
    selector = etree.HTML(r)
    # post_urls = selector.xpath('//*[@id="UserAttr"]')
    titles = selector.xpath('//*[@id="ulQs"]/dl/a/span/text()')
    name_list = selector.xpath('//*[@id="UserAttr"]/text()')[0]
    name = name_list.split()[0]
    p_urls = []
    # ts=[]
    des = f'{name}你好,\n'
    for post_url, title in zip(post_urls, titles):
        #print(post_url,title)
        b_url = 'https://tyutgs.wjx.cn' + str(post_url)
        p_urls.append([b_url, title])
        print(post_url, title)
        if '下午' in title:
            des += check_time(b_url, data, title)
        elif '上午' in title:
            des += check_time(b_url, data, title)
        # p_urls.append(title)
        else:
            des += f'\n执行了其他时间的问卷<{title}>，请检查云函数!'
        # ts.append(p_urls)
        #print(p_urls)
        # check_time(b_url, data_am)
    return des+'\n本次由体温打卡系统为您提供服务'


def get_fill_content(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
    r1 = requests.get(url, headers=headers)
    setCookie = r1.headers['Set-Cookie']
    #CookieText = re.findall(r'SERVERID=.*;', setCookie)[0]
    # print(r1.text, CookieText)
    return r1.text, setCookie


# 从页面中获取'curid','rn','jqnonce','starttime',同时构造ktimes用作提交调查问卷
def get_submit_query(content):
    global activityId
    content = content.replace(' ', '')
    title_name = re.search(r'《(.+?)》', content).group(
        1)
    try:
        shortid = re.search(r'shortid=(.+?)"', content).group(1)
    except:
        shortid = re.search(r"shortAid='(.+?)'", content).group(1)
    activityId = re.search(r'activityId=(.+?);', content).group(1)
    activityId = int(activityId) ^ 2130030173  # 有一个位运算符^   activityId=activityId^ 2130030173
    # (activityId)
    rn = re.search(r'\d{9,10}\.\d{8}', content).group()
    jqnonce = re.search(r'.{8}-.{4}-.{4}-.{4}-.{12}', content).group()
    ktimes = random.randint(60, 65)
    starttime = nowtime  # re.search('starttime="(.+?)";', content).group(1)
    relts = re.search('relts="(.+?)";', content).group(1)
    relsign = re.search(r'relsign="(.+?)";', content).group(1)
    mst = re.search(r'maxSurveyTime=(.+?);', content).group(1)
    jqparm_1 = rn[:rn.find('.')]
    jqparm_2 = starttime
    jqpram = __get_jqparam(jqparm_1, jqparm_2, activityId)
    d = 1984474479 ^ 2130030173
    # print(__get_jqparam('1898723791.23666634', '2022/1/16 13:14:11', d))
    # print(get_jqsign(ktimes, '369dbd8d-2c64-42e2-a4ec-325752f8db77'))
    relusername = re.search(r'relusername="(.+?)";', content).group(1)
    relrealname = re.search(r'relrealname="(.+?)";', content).group(1)
    relext = re.search(r'relext="(.+?)";', content).group(1)
    reldept = re.search(r'reldept="(.+?)";', content).group(1)
    return shortid, activityId, rn, jqnonce, ktimes, starttime, relts, relsign, mst, jqpram, title_name, relext, reldept, relrealname, relusername


def __get_jqparam(random, time, activityId):
    return __js_engine.call('getcanshu', random, time, activityId)
    # return __js_engine.call('jamieDe', random, time, curid)


# 通过ktimes,jqnonce构造jqsign
def get_jqsign(ktimes, jqnonce):
    result = []
    b = ktimes % 10
    if b == 0:
        b = 1
    for char in list(jqnonce):
        f = ord(char) ^ b
        result.append(chr(f))
    return ''.join(result)


def get_vdate():
    url = "https://tyutgs.wjx.cn/user/loginForm.aspx?user_token=C986fzY4Y8ANeie91V0XkpP4XeBHzWYe/A64fzr7fkPiRZf2kIaSoofLYyFRUMEBCGxP3CW6GDLy/A3R4/HM5lqgV6aXXLFDBvloBYX/fRxlBJtMmtTdTA==&returnUrl=/user/qlist.aspx?user_token=C986fzY4Y8ANeie91V0XkpP4XeBHzWYe%2fA64fzr7fkPiRZf2kIaSoofLYyFRUMEBCGxP3CW6GDLy%2fA3R4%2fHM5lqgV6aXXLFDBvloBYX%2ffRxlBJtMmtTdTA%3d%3d%26manager=0"
    # payload={}
    # headers = {
    #     'Cookie': '.ASPXANONYMOUS=ZULSox8o1wEkAAAANTg3ZmY1ZTQtN2Y1ZC00ZmZiLTg5ZTQtYWI5YWE4Njc4ODY0WJGAPNEe99o48zpz3-BwEjxSyhM1; acw_tc=2f624a4716120650672832369e6b8d485fe2856daea55b6c33b7a1556288a4; SERVERID=3f9180de4977a2b2031e23b89d53baa6|1612065095|1612065009'
    # }
    response = requests.request("GET", url)  # headers=headers, data=payload, allow_redirects=False
    prin = response.text
    html = etree.HTML(response.text)
    __VIEWSTATE = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
    __VIEWSTATEGENERATOR = html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
    __EVENTVALIDATION = html.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
    return __VIEWSTATEGENERATOR, __EVENTVALIDATION, __VIEWSTATE, response.cookies


def get_cookie(loginid, pwd):
    post_url = "https://tyutgs.wjx.cn/user/loginForm.aspx?user_token=RzCs8KPQb4VEfycFVJ8OMztE5FTgJGXpBj0M1NsuatiZzuullOcE2qNhFz1gNCLMf2Rz0IoQ2%2b%2fQvHgDWQRylqbGCNwf9At747llgCvdCidNf%2fEPUf6k4g%3d%3d&returnUrl=%2fuser%2fqlist.aspx%3fu%3d%25e6%2589%258b%25e6%259c%25ba%25e7%2594%25a8%25e6%2588%25b7tivliw38j0y8djcff6vstq%26userSystem%3d1%26systemId%3d55677040"
    __VIEWSTATEGENERATOR, __EVENTVALIDATION, __VIEWSTATE, cookies = get_vdate()
    payload = {
        '_EVENTTARGET': 'btnSubmit',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
        '__EVENTVALIDATION': __EVENTVALIDATION,
        'hideIsPhone': '',
        'hfQueryCond': '',
        'hfQuery': f'10000|{loginid}〒30000|{pwd}',
        'hfPwd': '2',
        'phoneVal': '',
        'txtVerifyCode_1': '',
        'checkCode': '',
        'hidPhone': '',
        'password': '',
        'name': '',
    }
    headers = {
        'Host': 'tyutgs.wjx.cn',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        # 'Cookie': cook_value,#'.ASPXANONYMOUS=Ni__qR4f1wEkAAAAZDdkNDAwMTYtNWI5Ni00ZjAxLTk3MzgtNGMyYjFhNWRiYWVlb71BdKV7ofCzMp9ZueOEtpqI7ds1; UM_distinctid=176f47b1addf5-029d8ad041c9e9-7d677965-1fa400-176f47b1ade201; CNZZDATA4478442=cnzz_eid%3D1092683263-1610415618-https%253A%252F%252Ftyutgs.wjx.cn%252F%26ntime%3D1611193232; acw_tc=2f624a5216120606611694400e3c63cc1f4bb6e5a489de19f8016ac340f09a; yksuserinfo_e2369e3a6980baa283793081acb7b3ae_1_55677040_ext={"40000":["26"]}; ssxmod_itna=eqUOGIqIxfxROADz1KRx0IxiKDQSxKPj=4oKjwdD/4pDnqD=GFDK40oEgqDCSmljhr5zeF=CRD5z8rjTLpN1G22fvV9Yx0aDbqGk3RRT4GGUxBYDQxAYDGDDPRD84Dr6xYPG0DiKGRDlIHXxDaRxi36xGaZx0OgcKN61KDRp5D0PqHDQKDucK1C=Os84D13iyDqnKD92oDs2GL1nIpXKk5KUROVZ5wD0Fs6xibzEoDUDnxLjh37=I4duw4lW4NtQ4P=WRK7G2NaBi5tWexo12g1DDWqnhPEz2K4D; ssxmod_itna2=eqUOGIqIxfxROADz1KRx0IxiKDQSxKPj=4oKjqG9W5SfDBwO0x7PpwU8+O447D6GMF6QxwWTHhwQbFeurvdaFu2x7q3FkucjSWjxLTDBYFvq2OHUrMI0fyPI8OX2MYwBGx7kIOd8kKk5jjom+U+hIWihkULG1KniQ3bx7DwRvGE++YGT79iiqHT=KHL0ihR6qZWxpInA=83nsD6IOVCRbVhIlGSrp96TGz=aKxRqNy0BbbtdhCPLpMMvID4EpCKa7nO7NgFyA/82ZjFdK4TYvB4nG7TEMbN1Zt+MENb7Hln8kjI=wt9OYis2fKMTsCAGgMsKR85BGBqC5w=FLNi284fs5CbOCoHQhalYtn8XS5WQhmlYkmHVMDTWx1fw6fGc3IlLxObYtTxfEmfbYGeGPlI1ew+fbzi7Z2xeD35iikBaM2POhxtnYtii+AYpOQOgpO8QSYxz+xSDfOSb4ekOcT448+mvFbAz3EObNPlFy1mz4hKnY0=UkmdO+k+fvoQUDhs/Oh06ipe0Su7yppoQ+au0xxwYMs7/FDxuGwk8wkFaxfDDw=G2BKjmPQGhIjD5UTjAqznoW0YK0qHXqzHq1Hq7kk3Z++lh+BKsrfwM+orD5ZUxXGt6hQYacnxfVaZGIl2Wknftc3zMkvfAPWeKivEvpF4u5nP6sZ8DVGuDDjKDekNsGD=0yaDab5eFo+LPqS2Nj1X27jdr09jxdpL61U9KYDD=; yksuserinfo_e2369e3a6980baa283793081acb7b3ae_1_55677040=3BqzmdV9BvRT5+2iH7VZgJm+oTXI+aD7xTOt7YWu1MVwR+XA0u9eOwpT8teV2glNwlVpPhaNiK8wnPgXHqbT4ABwnrL/WjePBaDecofcNwvn9XpwlG4AGxDQEql8Ub7eYA708RsB4izmCmF2Nhjlvyfr97WxWS/Jjki+ye5xUJe/BaE/lLjL2ZFZ52lXCFoqadoYadxe8ljQTBBdBVYO01rPq8vvQURSOBSnJPC0bxgnVDVSwxniTaqhQVc+4QqoMbBncgAJLwgRDNJIZhcPDgfXWfUQV3RJ35E1hzWKSvdhAsewivCxE983s6vhPOLbJnDk7jeM1+iso+e8yJMyrHKU113aZPQenkS0d53bG9coj4VGf5azC9lbqfEkGKOFz7f8LwXJuI1Og+Zv3WijGmeplwwzuWfnkSLM4gC75pGwM9LmstzL8hEkM/bnPTsAG2mMAyjXuxJXGkC7yNzZGw==; SERVERID=119945d15c384f33654d4a5e74800f98|1612061307|1612060661; .ASPXANONYMOUS=ZULSox8o1wEkAAAANTg3ZmY1ZTQtN2Y1ZC00ZmZiLTg5ZTQtYWI5YWE4Njc4ODY0WJGAPNEe99o48zpz3-BwEjxSyhM1; SERVERID=3f9180de4977a2b2031e23b89d53baa6|1612084374|1612084374',
        'Referer': 'https://tyutgs.wjx.cn/user/loginForm.aspx?user_token=C986fzY4Y8ANeie91V0XkpP4XeBHzWYe%2fA64fzr7fkPiRZf2kIaSoofLYyFRUMEBCGxP3CW6GDLy%2fA3R4%2fHM5lqgV6aXXLFDBvloBYX%2ffRxlBJtMmtTdTA%3d%3d&returnUrl=%2fuser%2fqlist.aspx%3fuser_token%3dC986fzY4Y8ANeie91V0XkpP4XeBHzWYe%252fA64fzr7fkPiRZf2kIaSoofLYyFRUMEBCGxP3CW6GDLy%252fA3R4%252fHM5lqgV6aXXLFDBvloBYX%252ffRxlBJtMmtTdTA%253d%253d%26manager%3d0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response_r = requests.request("POST", post_url, headers=headers, data=payload, allow_redirects=False)
    b = response_r.cookies
    cook_value = ''
    for x in b:
        cook_value += x.name + '=' + x.value + ';'
    cook_value_1 = cook_value[:len(cook_value) - 1]
    # print(cook_value_1)
    return cook_value_1, b


def check_time(b_url, payload, title):
    '''
    此函数只是用于检测填写问卷时间是否在设置时间内
    :param b_url:
    :param payload:
    :return:
    '''
    r = requests.get(b_url).text
    # post_cc(b_url, payload)

    if '您只能在' in r:
        return f'\n执行了其他时间的问卷<{title}>，请检查云函数'
    elif '无法显示网页' in r:
        return '暂无问卷，进入了错误页面'
    else:
        return post_cc(b_url, payload)


def post_cc(b_url, payload):
    url = b_url
    # print(url)
    fill_content, cookies = get_fill_content(url)
    shortid, curid, rn, jqnonce, ktimes, starttime, relts, relsign, mst, jqpram, title_name, relext, reldept, relrealname, relusername = get_submit_query(
        fill_content)
    jqsign = get_jqsign(ktimes, jqnonce)
    jqsign1 = get_jqsign(84, '0e98efcb-c610-4a2d-b484-bf55999e55a7')
    # sio.write('{}\n'.format(relrealname))
    # print(jqsign)
    ser_time = int(time.time()) + 1
    time_stamp = '{}{}'.format(int(new_time), random.randint(100, 200))
    # print(time_stamp)
    params = {
        'shortid': shortid,
        # 'curID': curid,
        'submittype': '1',
        't': time_stamp,
        'starttime': starttime,
        'ktimes': ktimes,
        'rn': rn,
        'relts': relts,
        'relusername': relusername,
        'relsign': relsign,
        'relrealname': relrealname,
        'reldept': reldept,
        'relext': relext,
        'hmt': '1',
        'jqpram': jqpram,
        'hlv': '1',
        'vpsiu': '1',
        # 'source': 'directphone',
        'sd': 'http://tyutgs.wjx.cn/',
        'mst': mst,
        'jqnonce': jqnonce,
        'jqsign': jqsign,

    }
    # b_url = url
    # response = requests.request("GET", b_url, headers='') /etc/sillyGirl/node-onebot  /etc/sillyGirl/node-onebot/etc/sillyGirl/node-onebotpm2 start "node main 2440405521"
    # b = response.cookies
    # cook_value = ''
    # for x in b:
    #     cook_value += x.name + '=' + x.value + ';'
    # cook_value = cook_value[:len(cook_value) - 1]
    # cook_value, b = get_cookie()
    # print(cook_value)
    post_url = 'https://tyutgs.wjx.cn/joinnew/processjq.ashx'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '728',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': cook_value,
        # '.ASPXANONYMOUS=vjAb_DHE1wEkAAAANDY5NmMyZTYtM2U1Ny00NDVmLWJlZmMtNWYzNjQwZTQ3NTlinmxYqoPfbWpYC2LotPXoRtdUKS41; UM_distinctid=17b2ebf181112d-0760a7b8a4da14-7868796f-1fa400-17b2ebf18121b3; Hm_lvt_21be24c80829bd7a683b2c536fcf520b=1629251582,1629252896; acw_tc=2f624a6716293438761012374e19d9aa2b211b4d14bfde237f5b2748e5a46c; yksuserinfo_e2369e3a6980baa283793081acb7b3ae_1_55677040_ext={"40000":["26"]}; yksuserinfo_e2369e3a6980baa283793081acb7b3ae_1_55677040=3BqzmdV9BvRT5+2iH7VZgJm+oTXI+aD7xTOt7YWu1MVwR+XA0u9eOwpT8teV2glNwlVpPhaNiK8wnPgXHqbT4ABwnrL/WjePBaDecofcNwvn9XpwlG4AGxDQEql8Ub7eYA708RsB4izmCmF2Nhjlvyfr97WxWS/Jjki+ye5xUJe/BaE/lLjL2ZFZ52lXCFoqadoYadxe8ljQTBBdBVYO01rPq8vvQURSkG9TAXKSbHRoCqZ6P3+cIqtVXdxHehKoZrrdHMzVgPgrIc7Lc5EnWiUSSlTN5ClWvjfnJoVwpGsHRBqCqw7eo5jLD+rAybg0xC0dLKURksUvxwB5b1ivvlobVRaaWX+2se+FhotxhG/MXOF8TQwpUK18MppKEeBURbekV6BLCdrl7sqkTXmDk0uRfUTyrtlI8MlFOUFihPlt60bGoSy+6l0/j9p4ZrbayHNPBWhiVIliC2S7yo2urg==; jac126755197=84827734; CNZZDATA4478442=cnzz_eid%3D227611899-1628574664-https%253A%252F%252Ftyutgs.wjx.cn%252F%26ntime%3D1629341801; SERVERID=6142ed0ee68ecc71fb491c53c82ec4a0|1629344100|1629343876; .ASPXANONYMOUS=l5dj2TLE1wEkAAAAZjczOWI0ZDAtMGY3Ny00YTA5LWI5MWQtMjdmMzM5M2RlMGI2uqc--Uzyng3PBKG2YZj_HUtm5Fk1',
        'Host': 'tyutgs.wjx.cn',
        'Origin': 'https://tyutgs.wjx.cn',
        'Pragma': 'no-cache',
        'Referer': url,
        # 'https://tyutgs.wjx.cn/vj/Y2Fe96w.aspx?relusername=2020510759&relrealname=x%2fsBS53CHW0%3d&relts=1629344086&relsign=4a50a1d20df18a9c6c01e5f77a19c6f1f6f73bf7&appid=&access_token=&user_token=C986fzY4Y8ANeie91V0XkpP4XeBHzWYe%2fA64fzr7fkPiRZf2kIaSoofLYyFRUMEBCGxP3CW6GDLy%2fA3R4%2fHM5lqgV6aXXLFDBvloBYX%2ffRxlBJtMmtTdTA%3d%3d&relDept=009%e7%9f%bf%e4%b8%9a%e5%b7%a5%e7%a8%8b%e5%ad%a6%e9%99%a2%5b%e5%90%ab%e9%87%8d%e7%82%b9%e5%ae%9e%e9%aa%8c%e5%ae%a4%5d&relExt=%e5%88%98%e4%b8%9c%e5%a8%9c%7c%e5%9c%b0%e8%b4%a8%e8%b5%84%e6%ba%90%e4%b8%8e%e5%9c%b0%e8%b4%a8%e5%b7%a5%e7%a8%8b&nbk=1',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"',
        'sec-ch-ua-mobile': '?1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 Edg/92.0.902.73'
    }
    # payload = json.dumps(payload)
    # payload = "submitdata=1%242%7D2%241%7D3%24(%E8%B7%B3%E8%BF%87)%7D4%24(%E8%B7%B3%E8%BF%87)%7D5%24%E5%B1%B1%E8%A5%BF%E7%9C%81%E5%A4%AA%E5%8E%9F%E5%B8%82%E4%B8%87%E6%9F%8F%E6%9E%97%E5%8C%BA%E4%B8%8B%E5%85%83%E8%A1%97%E9%81%93%E5%A4%AA%E5%8E%9F%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6-%E5%AD%A6%E7%94%9F%E5%85%AC%E5%AF%93%E5%8D%81%E6%A5%BC%E8%A5%BF%E5%8C%BA%E5%A4%AA%E5%8E%9F%E7%90%86%E5%B7%A5%E5%A4%A7%E5%AD%A6%E8%99%8E%E5%B3%AA%E6%A0%A1%E5%8C%BA%5B112.52134%2C37.8519%5D%7D6%242%7D7%243%7D8%241!(%E7%A9%BA)%7C(%E7%A9%BA)%7D9%241%7D10%241%7D11%24-3%7D12%24(%E8%B7%B3%E8%BF%87)%5E(%E8%B7%B3%E8%BF%87)%5E(%E8%B7%B3%E8%BF%87)%5E(%E8%B7%B3%E8%BF%87)%5E(%E8%B7%B3%E8%BF%87)%7D13%24-3%7D14%24-3%7D15%24-3%7D16%24(%E8%B7%B3%E8%BF%87)%5E(%E8%B7%B3%E8%BF%87)%5E(%E8%B7%B3%E8%BF%87)%5E(%E8%B7%B3%E8%BF%87)%5E(%E8%B7%B3%E8%BF%87)%5E(%E8%B7%B3%E8%BF%87)%7D17%24%7D18%241"
    r = requests.post(url=post_url, headers=headers, data=payload, params=params, cookies=cook_value)
    r_t = r.text
    if '10' in r_t:
        c = '成功'
    elif '2' in r_t:
        c = '失败'
    else:
        c = r_t
    # 通过测试返回数据中表示成功与否的关键数据（’10‘or '22s'）在开头,所以只需要提取返回数据中前两位元素
    # print(r.text[0:2])
    #sio.write('\n' + title_name + '\n结果：' + c)
    return '\n' + title_name + '\n结果：' + c



def get_arg(logid, pwd):
    url = "https://tyutgs.wjx.cn/user/loginForm.aspx?user_token=RzCs8KPQb4VEfycFVJ8OMztE5FTgJGXpBj0M1NsuatiZzuullOcE2qNhFz1gNCLMf2Rz0IoQ2%2b%2fQvHgDWQRylqbGCNwf9At747llgCvdCidNf%2fEPUf6k4g%3d%3d&returnUrl=%2fuser%2fqlist.aspx%3fu%3d%25E6%2589%258B%25E6%259C%25BA%25E7%2594%25A8%25E6%2588%25B7tivliw38j0y8djcff6vstq%26userSystem%3d1%26systemId%3d55677040"
    payload = f'__EVENTTARGET=btnSubmit&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUKMTg4NzM3MzkzMA9kFgICAQ9kFgpmDw8WAh4EVGV4dAUq5aSq5Y6f55CG5bel5aSn5a2m56CU56m255Sf6Zmi55ar5oOF5bmz5Y%2BwZGQCAQ8PFgIfAGVkZAIDDxYCHglpbm5lcmh0bWwF3gE8aW5wdXQgcGxhY2Vob2xkZXI9J%2BWtpuWPty%2Fouqvku73or4Hlj7cnIHR5cGU9J3RleHQnIGlkPSdyZWdpc3Rlci11c2VyLW5hbWUnIHF2YWx1ZT0nMTAwMDAnIC8%2BPGlucHV0IHBsYWNlaG9sZGVyPSfouqvku73or4HlkI7lha3kvY0nIGlkPSdyZWdpc3Rlci11c2VyLXBhc3N3b3JkJyB0eXBlPSdwYXNzd29yZCcgcXZhbHVlPSczMDAwMCcgdmFsdWU9JycgYXV0b2NvbXBsZXRlPSdvZmYnLz5kAg0PZBYCAgEPFgIeBGhyZWYFhgVodHRwczovL2dyYXBoLnFxLmNvbS9vYXV0aDIuMC9hdXRob3JpemU%2FcmVzcG9uc2VfdHlwZT1jb2RlJmNsaWVudF9pZD0yMDQwNTkmc3RhdGU9c29qdW1wJnJlZGlyZWN0X3VyaT1odHRwcyUzYSUyZiUyZnd3dy53anguY24lMmZodG1sJTJmZ2V0cXFjb2RlLmh0bWwlM2ZyZWRpcmVjdF91cmklM2RodHRwcyUyNTNhJTI1MmYlMjUyZnR5dXRncy53anguY24lMjUyZnVzZXIlMjUyZmxvZ2luRm9ybS5hc3B4JTI1M2Z1c2VyX3Rva2VuJTI1M2RSekNzOEtQUWI0VkVmeWNGVko4T016dEU1RlRnSkdYcEJqME0xTnN1YXRpWnp1dWxsT2NFMnFOaEZ6MWdOQ0xNZjJSejBJb1EyJTI1MjUyYiUyNTI1MmZRdkhnRFdRUnlscWJHQ053ZjlBdDc0N2xsZ0N2ZENpZE5mJTI1MjUyZkVQVWY2azRnJTI1MjUzZCUyNTI1M2QlMjUyNnJldHVyblVybCUyNTNkJTI1MjUyZnVzZXIlMjUyNTJmcWxpc3QuYXNweCUyNTI1M2Z1JTI1MjUzZCUyNTI1MjVFNiUyNTI1MjU4OSUyNTI1MjU4QiUyNTI1MjVFNiUyNTI1MjU5QyUyNTI1MjVCQSUyNTI1MjVFNyUyNTI1MjU5NCUyNTI1MjVBOCUyNTI1MjVFNiUyNTI1MjU4OCUyNTI1MjVCN3RpdmxpdzM4ajB5OGRqY2ZmNnZzdHElMjUyNTI2dXNlclN5c3RlbSUyNTI1M2QxJTI1MjUyNnN5c3RlbUlkJTI1MjUzZDU1Njc3MDQwZAIODxYCHgdWaXNpYmxlaGRkaMklT6noC%2FU98XVvT%2FNuA9CGeFU%3D&__VIEWSTATEGENERATOR=EA405E62&__EVENTVALIDATION=%2FwEdAAw6iXTH43vTfL3YUkJcmzlrWp7kJr8w5TjvJ3MvPivpl3A8TJAPbjHFWGrvGl0ymTWwPPHhxrLpFiCSBTl5p%2FIo4ls5DrSML6E8mK%2BtEG%2B8PTzmltaUM7aEAN%2Bg9cP%2Fm11lBZ36GORgpLgB%2BoY9A1iDjFzsHdJS7HeWg%2BRQwMeVRIt98DInGDOYrSCgiLhQTAUvLwj5k69AZNJxFQi3USBJ7ixyIk7cehzrzFMW1kZASJ%2BEqQ45iRU%2BNJmG7S9yuEEnMQBW61RkdUwnnI4eD%2BQOfBqioQ%3D%3D&hideIsPhone=&hfQueryCond=&hfQuery=10000%7C{logid}%E3%80%9230000%7C{pwd}&hfPwd=2&phoneVal=&txtVerifyCode_1=&checkCode=&hidPhone=&password=&name='
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '1974',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'tyutgs.wjx.cn',
        'Origin': 'https://tyutgs.wjx.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://tyutgs.wjx.cn/user/loginForm.aspx?user_token=RzCs8KPQb4VEfycFVJ8OMztE5FTgJGXpBj0M1NsuatiZzuullOcE2qNhFz1gNCLMf2Rz0IoQ2%2b%2fQvHgDWQRylqbGCNwf9At747llgCvdCidNf%2fEPUf6k4g%3d%3d&returnUrl=%2fuser%2fqlist.aspx%3fu%3d%25E6%2589%258B%25E6%259C%25BA%25E7%2594%25A8%25E6%2588%25B7tivliw38j0y8djcff6vstq%26userSystem%3d1%26systemId%3d55677040',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    res = etree.HTML(response.text)
    UserAttr = res.xpath('//*[@id="UserAttr"]')[0]
    print(UserAttr.text)
    return response.cookies, UserAttr.text


def total(loginId, pwd, pushusr):
    global a
    a = '        疫情签到日志\n' + "===" + nowtime + "===\n"
    global cook_value
    cook_value, UserAttr = get_arg(loginId, pwd)
    des = get_geturl()
    #desp = sio.getvalue()
    # sio.close()
    desp = a + des
    desp = desp.replace('\n\n', '\n')
    print(desp)
    push = WXPusher(pushusr, desp)
    push.send_message()



def main():
    import lining
    lining.ning()
    if os.path.exists('./config.txt'):
        configs = open('./config.txt', 'r', encoding='utf-8').read().replace(' ', '')
        username_list = configs.split('\n')
        b = []
        for i in username_list:
            b.append(i.split(','))
        for i in b:
            loginId = i[0]
            pwd = i[1]
            pushusr = i[2]
            # total(loginId, pwd)
            # print('执行完成')
            my_threading = threading.Thread(target=total, args=(loginId, pwd, pushusr))
            my_threading.start()
    else:
        raise '请新建一个config.txt文件！'


main()

# if __name__ == "__main__":
#     print("⏲ 请输入定时时间（默认每天6:05、12:05）")
#     #minute = input("\tminute: ") or 5
#     scheduler = BlockingScheduler(timezone='Asia/Shanghai')
#     scheduler.add_job(main, 'cron', hour='6,12', minute='5')  # args=['20212091', 'Wenjing916'],  这里使用的是个人账号
#     print('⏰ 已启动定时程序，每天 6,12点%02d 为您打卡' % (int(5)))
#     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
#     os.system('cls')  # TODO 这里我加入了一个清空命令
#     try:
#         scheduler.start()
#     except (KeyboardInterrupt, SystemExit):
#         pass
