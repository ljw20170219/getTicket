#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :WebRequest.py
@说明    :
@时间    :2020/05/11 22:49:09
'''

import urllib3
import re
import json

class WebRequest():
    '''
    @description: 获取火车站点与其对应的代号
    @param {type}
    @return:
    '''
    def downloadStationsCode(self):
        filepath = 'E:/File/MyEnv/PythonProgram/Spider/getTicket/station.json'
        stationCodeUrl = 'https://kyfw.12306.cn/otn/resources/' \
        'js/framework/station_name.js?station_version=1.9142'

        stationsCode = {}

        # 发出网页请求
        http = urllib3.PoolManager()
        req = http.request('GET', stationCodeUrl)

        # 格式整理/信息提取
        stationCodeData = str(req.data, encoding='utf-8')
        stationCodeDataFilter = re.findall(u'([\u4e00-\u9fa5]+\|[a-zA-Z]{0,30})',stationCodeData)

        # 对火车站代号进行格式化，以代号为键，以站点为值
        for x in stationCodeDataFilter:
            stationsCode[x.split('|')[1]] = x.split('|')[0]

            os.remove(filepath)
            with open(filepath,'w', encoding='utf-8') as s:
                s.write(json.dumps(stationsCode))

    '''
    @description: 获取所有列车信息
    @param {type}
    @return:
    '''
    def getTodayTrainList(self, from_station, to_station, date):
        url = 'https://kyfw.12306.cn/otn/leftTicket/query'

        # 经测试，headers中的User-Agent和Cookies是必须要的，否则不能获取到数据
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36 Edg/81.0.416.68',
            'Cookie': "JSESSIONID=3B7F39302BA35A93D72724191B4E23C3; BIGipServerotn=2229797130.24610.0000; RAIL_EXPIRATION=1589187364309; RAIL_DEVICEID=MzMYDvW1Us_kunpobOvIsC8S3TwRASCALF0BiWt_RWeUjw8gCBUnnNhPEW26t8zSZa4wr1Jq1Page7CpW1uSM1yYvbH9j7lw5cuJvlaFohgNYEu0-oVkUYU6ZALZhFVTA82duorJjTW8nTpgL_IkgYS4v9mXuwMY; BIGipServerpassport=820510986.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; _jc_save_toDate=2020-05-08; _jc_save_wfdc_flag=dc; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_fromDate=2020-05-08"
        }

        # 设置get的参数
        fields = {
            'leftTicketDTO.train_date': date,
            'leftTicketDTO.from_station':from_station,
            'leftTicketDTO.to_station':to_station,
            'purpose_codes':'ADULT'
        }

        # 发出网页请求
        http = urllib3.PoolManager()
        req = http.request('GET', url, headers=headers, fields=fields)
        req = json.loads(str(req.data,'utf-8-sig'))
        available_trains = req['data']['result']
        station_map = req['data']['map']
        return available_trains, station_map

# getTodayStationList('2020-05-12', 'BJP', 'SHH')
