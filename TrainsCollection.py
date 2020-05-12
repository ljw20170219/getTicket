'''
@Date: 2020-05-08 11:57:53
@LastEditTime: 2020-05-11 21:50:50
@Description: 格式化网页请求的信息
'''
import prettytable as pt
import json
from WebRequest import WebRequest
import os
import re

class TrainsCollection:
    def formatData(self, available_trains, station_map):
        ToorFrom = '\|预订\|\w*\|' \
            '(?P<列车>[A-Z][0-9]{1,5})\|' \
            '(?P<始>[A-Z]{3})\|' \
            '(?P<终>[A-Z]{3})\|' \
            '[A-Z]{3}\|' \
            '[A-Z]{3}\|' \
            '(?P<起始时间>\d{2}:\d{2})\|' \
            '(?P<到站时间>\d{2}:\d{2})\|' \
            '(?P<全时长>\d{2}:\d{2})\|'

        seatTpye = '\|\d\|\d\|\|(?P<高级软卧4>\d{0,2})?\|\|' \
            '(?P<软卧一等卧5>\w{0,2})?\|'\
            '(?P<软座8>\w{0,2})?\|' \
            '(?P<其他11>\w{0,2})?\|' \
            '(?P<无座10>\w{0,2})?\|' \
            '(?P<动卧6>\w{0,2})?\|' \
            '(?P<硬卧二等座7>\w{0,2})?\|' \
            '(?P<硬座9>\w{0,2})?\|' \
            '(?P<二等座包座3>\w{0,2})?\|' \
            '(?P<一等座2>\w{0,2})?\|' \
            '(?P<商务座1>\w{0,2})?\|\|'

        tb = pt.PrettyTable()
        tb.set_style(pt.MSWORD_FRIENDLY)
        tb.field_names = ['列车','车站','时间','历时',
                        '商务座','一等座','二等座',
                        '高级软卧','软卧一等卧','动卧',
                        '硬卧二等座','软座','硬座',
                        '无座','其他'
        ]

        self.TableFormat(available_trains, ToorFrom, seatTpye, tb)

    def TableFormat(self,available_trains, ToorFrom, seatTpye, tb):
        for x in available_trains:
            ToorFromData = re.search(ToorFrom, x) # 列车起始到站时间
            seatTypeData = re.search(seatTpye, x) # 乘坐类型
            if ToorFromData and seatTypeData:
                tff = {
                    'line' : ToorFromData.group('列车'),
                    'starAndend':[ToorFromData.group('始'), ToorFromData.group('终')],
                    'from' : ToorFromData.group('始'),
                    'to' : ToorFromData.group('终'),
                    'startTime' : ToorFromData.group('起始时间'),
                    'endTime' : ToorFromData.group('到站时间'),
                    'allTime' : ToorFromData.group('全时长')
                }

                stf = {
                    '商务座' : seatTypeData.group('商务座1'),
                    '一等座' : seatTypeData.group('一等座2'),
                    '二等座' : seatTypeData.group('二等座包座3'),
                    '高级软卧' : seatTypeData.group('高级软卧4'),
                    '软卧一等卧' : seatTypeData.group('软卧一等卧5'),
                    '动卧' : seatTypeData.group('动卧6'),
                    '硬卧二等座' : seatTypeData.group('硬卧二等座7'),
                    '软座' : seatTypeData.group('软座8'),
                    '硬座' : seatTypeData.group('硬座9'),
                    '无座' : seatTypeData.group('无座10'),
                    '其他' : seatTypeData.group('其他11'),
                }
                tb.add_row([
                    tff['line'],
                    # tff['from'] +"->"+ tff['to'],
                    # self.getStationsCode([tff['from'], tff['to']], code='code')[0] +"->"+ self.getStationsCode([tff['from'], tff['to']], code='code')[1],
                    self.getStationsCode([tff['from'], tff['to']], code='code')[tff['from']] +"--"+
                    self.getStationsCode([tff['from'], tff['to']], code='code')[tff['to']],
                    tff['startTime'] +"--"+ tff['endTime'],
                    tff['allTime'],
                    stf['商务座'],
                    stf['一等座'],
                    stf['二等座'],
                    stf['高级软卧'],
                    stf['软卧一等卧'],
                    stf['动卧'],
                    stf['硬卧二等座'],
                    stf['软座'],
                    stf['硬座'],
                    stf['无座'],
                    stf['其他']
                ])
        print(tb)

    '''
    @description: 查询:站点-->代号/代号-->站点
    @param stationArr {list} 站点/代码的键值对 例如：['ICW', 'MBN'] or ['成都东', '麻城北']
    @paran code 默认为空值，当stationArr为['成都东', '麻城北']这种以汉字为key时，根据汉字反查站点代号；而当code='code'时，则是根据代号查找站点
    @return:
    '''
    def getStationsCode(self, stationArr:list,code=None):
        #  判断station.json是否存在
        stationsCodePath = 'E:/File/MyEnv/PythonProgram/Spider/getTicket/station.json'
        # 判断station.json文件是否存在
        if os.path.exists(stationsCodePath) == False:
            self.wr.downloadStationsCode()

        with open(stationsCodePath, 'r', encoding='utf-8') as s:
            # 因为输入的是汉字，需要钭原station.json进行键值对换
            ordic = dict(json.load(s))
            if code == 'code':
                return {stationArr[0]:ordic[stationArr[0]], stationArr[1]:ordic[stationArr[1]]}
            else:
                newdic =dict(zip(ordic.values(), ordic.keys()))
                return {stationArr[0]:newdic[stationArr[0]],stationArr[1]:newdic[stationArr[1]]}

    def getFormatData(self, from_station, to_station, date):
        # 获取站点代号
        stationCode = self.getStationsCode([from_station, to_station])
        wr = WebRequest()
        trainList = wr.getTodayTrainList(stationCode[from_station], stationCode[to_station], date)
        return self.formatData(trainList[0], trainList[1])
