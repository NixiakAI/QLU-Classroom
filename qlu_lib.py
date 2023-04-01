import requests
import json
import time
import pytz
import datetime
import random
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4706.0 Safari/537.36 Edg/98.0.1084.0",
    "Referer": "http://yuyue.lib.qlu.edu.cn"
}

# 获取东八区日期
def get_time(addday=0):
    tz = pytz.timezone("Asia/Shanghai")  # 东八区
    time_now = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone("Asia/Shanghai"))
    time_now=time_now+datetime.timedelta(days=addday)
    dt=time_now.strftime("%Y-%m-%d")
    hm=time_now.strftime("%H:%M")
    return [dt,hm]

def is_available(count_list):
    if count_list[0] == 0:
        return False
    for count in count_list:
        #print(count,type(count))
        if count==None:
            return False
    if count_list[0]==count_list[1]:
        return False
    return True


def query(time):
    url = "http://yuyue.lib.qlu.edu.cn/api.php/areas/1"
    response = requests.request("GET", url)
    a = response.cookies.items()
    b = ";".join('='.join(tup) for tup in a)

    # 楼层区域 信息
    total_url = "http://yuyue.lib.qlu.edu.cn/api.php/areas/0/date/%s" % time[0]
    
    # 或许在图书馆崩了的时候有所帮助
    try:
        # 需要session
        headers["Cookie"] = b
        total_info=requests.get(total_url,headers=headers,timeout=0.8)
    except:
        return [{'area_name': "当前响应过慢，不予访问，减少图书馆压力"}], [{'area_name': "当前响应过慢，不予访问，减少图书馆压力"}],''

    # 判断是否访问成功
    if total_info.status_code != 200:
        print(total_info.status_code, '图书馆已崩')
        return [{'area_name':"当前不可用。。"}], [{'area_name':"当前不可用。。"}]

    total_info=total_info.json()
    av_seat_list=[] #  记录每个区域空座信息，便于按楼层输出
    un_seat_list=[] #  记录每个区域非空座信息，便于按楼层输出
    for cd_area in total_info['data']['list']['childArea']:
        #cd_area['name'], ['TotalCount'], ['UnavailableSpace'], ['id'], ['parentId'] 
        # 排除大楼层（无用信息）
        if cd_area['parentId']>1: 
            # is_available其实可以不要了,因为已经排除 None 了 
            if is_available([cd_area['TotalCount'],cd_area['UnavailableSpace']]): #证明这里有座位
                available_num=int(cd_area['TotalCount'])-int(cd_area['UnavailableSpace'])
                av_seat_list.append({'area_id':"%02d"%cd_area['id'],'area_name':cd_area['name'].ljust(30),'available_num':available_num})
            else:
                un_seat_list.append({'area_id':"%02d"%cd_area['id'],'area_name':cd_area['name'],'available_num':0})

    # 按楼层排序
    name_sort=lambda x: x['area_name']
    av_seat_list.sort(key=name_sort)
    un_seat_list.sort(key=name_sort)

    # print('*'*30,'\n以下区域有座：\n','-'*30)
    floor_now=av_seat_list[0]['area_name'][0:1]

# 以下用于控制台打印座位信息
    # for f in av_seat_list:
    #     if floor_now!=f['area_name'][0:1]:
    #         print('-'*30)
    #         floor_now=f['area_name'][0:1]
        # print('{:>2d} : {} 剩余空座数:{}'.format(f['area_id'],f['area_name'],f['available_num']))
    

    # print('*'*30,'\n以下区域无座：\n','-'*30)
    # floor_now=un_seat_list[0]['area_name'][0:1]
    #
    # for f in un_seat_list:
    #     if floor_now!=f['area_name'][0:1]:
    #         print('-'*30)
    #         floor_now=f['area_name'][0:1]
    #     print('{:>2d} : {} '.format(f['area_id'],f['area_name']))
    
    return av_seat_list,un_seat_list,"剩余空座："


def nowtime():
    # 报个时
    dt,hm=get_time()
    #print('当前日期:',dt,'\n当前时间:',hm)
    return dt,hm

