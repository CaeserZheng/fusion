#-.- coding:utf-8 -.-

import xlwt
import xlrd
import re
from Statistics import Billing

class DoExcel():

    def __init__(self):
        pass


    def get_excel(self):
        try:
            fs = xlwt.Workbook()
            return fs
        except Exception,e:
            print str(e)


    def WriteExcel(self,filename,timestamp_5mins,bandwidth_5mins,timestamp_day,bandwidth_day,count=None,count_type=None):

        '''
        excel写入
        :param file:excel名称
        :param timestamp: list 五分钟带宽时间戳
        :param bandwidth: dict 带宽
        :param timestamp2: dict 以天为单位的时间戳
        :param data2: dict 每天的峰值
        :return:返回excel文件路径
        '''
        #print filename,timestamp1,data1,timestamp2,data2

        try:
            fs = self.get_excel()
            for (type,data) in bandwidth_5mins.items():
                print "type===>" + type + str(data)
                if len(data) != 0:
                    #写入五分钟带宽|流量
                    sheel = fs.add_sheet(type+"_5mins")
                    for row in range(0,len(timestamp_5mins)):
                        sheel.write(row,0,str(timestamp_5mins[row]))
                        sheel.write(row,1,str(data[row]))

                    #写入日峰值

                    daystamp = timestamp_day[type]
                    data = bandwidth_day[type]
                    print "日峰值==>"+str(type)+"==>"+str(data)
                    sheel = fs.add_sheet(type+"_days")
                    for row in range(0,len(data)):
                        timestamp = re.split("T",daystamp[row])
                        d1 = timestamp[0]
                        d2 = timestamp[1]
                        sheel.write(row,0,str(d1))
                        sheel.write(row,1,str(d2))
                        sheel.write(row,2,str(data[row]))

                    #写入计费方式
                    if count is not None:
                        if count_type == 1: #95值统计
                            sheel = fs.add_sheet(type+"_95_month")
                        if count_type == 2: #月平均值统计
                            sheel = fs.add_sheet(type+"_Ave_month")
                        if count_type == 3: #流量计费
                            sheel = fs.add_sheet(type+"_sum_month")
                        band = count[type][0]
                        time = count[type][1]
                        sheel.write(0,0,str(band))
                        sheel.write(0,1,str(time))

            fs.save(filename)
            return True
        except Exception,e:
            print str(e)
            return False

    def WriteExcelForTraffic(self,filename,timestamp_5mins,traffic_5mins,timestamp_day,traffic_day,count=None):

        '''
        excel写入
        :param file:excel名称
        :param timestamp: list 五分钟带宽时间戳
        :param bandwidth: dict 带宽
        :param timestamp2: dict 以天为单位的时间戳
        :param data2: dict 每天的峰值
        :return:返回excel文件路径
        '''
        #print filename,timestamp1,data1,timestamp2,data2

        try:
            fs = self.get_excel()
            for (type,data) in traffic_5mins.items():
                print "type===>" + type + str(data)
                if len(data) != 0:
                    #写入五分钟带宽|流量
                    sheel = fs.add_sheet(type+"_5mins")
                    for row in range(0,len(timestamp_5mins)):
                        sheel.write(row,0,str(timestamp_5mins[row]))
                        sheel.write(row,1,str(data[row]))

                    #写入日峰值

                    daystamp = timestamp_day[type]
                    data = traffic_day[type]
                    sheel = fs.add_sheet(type+"_days")
                    #print "len==>" + str(len(data))
                    for row in range(0,len(data)):
                        print "1"
                        timestamp = re.split("T",daystamp[row])
                        print "2"
                        sheel.write(row,0,str(timestamp[0]))
                        sheel.write(row,1,str(data[row]))


                    #写入计费方式
                    #print "count==>"+str(count)
                    if count is not None:
                        sheel = fs.add_sheet(type+"_sum_month")
                        all_traffic = count[type]
                        sheel.write(0,0,str(all_traffic))

            fs.save(filename)
            return True
        except Exception,e:
            print str(e)
            return False





