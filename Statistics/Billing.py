#-.- coding:utf-8 -.-

import Traffic
import excel

SAVEPATH="/Users/caeser/Codes/python2/Fusion/Statistics/data/"

class QNBilling():
    def __init__(self):
        self.traffic = Traffic.QNTraffic()

    def MonthAveragePerByUid(self,uid,startTime,endTime,domain=None,savefile=False):
        '''
        根据UID提供月平均计费值
        :param uid:
        :param startTime:
        :param endTime:
        :return:sum、bandwidth
        '''
        if domain is not None:
            data = self.traffic.GetBandwidthByUid(uid,startTime,endTime,domain=domain)
        else:
            data = self.traffic.GetBandwidthByUid(uid,startTime,endTime)

        if data[0] == 2002:
            timestamp_5mins = data[1]
            bandwidth_5mins = data[2]
            timestamp_day_max = data[3]
            bandwidth_day_max = data[4]


        value = {}
        for (type,bandwidth) in bandwidth_day_max.items():
            avg =(sum(bandwidth)/len(bandwidth_day_max))
            value[type] = avg
        if savefile:
            filename = SAVEPATH + str(uid) + "_" + str(startTime) + "_" + str(endTime) + ".xls"

            fs = excel.DoExcel()
            fs.WriteExcel(filename,timestamp_5mins,bandwidth_5mins,timestamp_day_max,bandwidth_day_max,value,2)
            return filename

        return value

    def Month95PerByUid(self,uid,startTime,endTime,domain=None,savefile=False):
        '''
        月95计费
        :param uid: 用户ID
        :param startTime:开始时间 YYYY-MM-DD
        :param endTime: 结束时间 YYYY-MM-DD
        :param domain: 域名
        :return: value={type:[bandwidth,time]}
        '''

        if domain is not None:
            data = self.traffic.GetBandwidthByUid(uid,startTime,endTime,domain=domain)
        else:
            data = self.traffic.GetBandwidthByUid(uid,startTime,endTime)

        if data[0] == 2002:
            timestamp_5mins = data[1]
            bandwidth_5mins = data[2]
            timestamp_day_max = data[3]
            bandwidth_day_max = data[4]

        #print bandwidth_5mins
        value = {}
        for (type,band) in bandwidth_5mins.items():
            res = []
            if len(band) > 0:
                bandwidth = sorted(band)
                tag = int(len(bandwidth)*0.95)
                res.append(bandwidth[tag])
                res.append(timestamp_5mins[band.index(bandwidth[tag])])
                value[type] = res

        if savefile:
            filename = SAVEPATH + str(uid) + "_" + str(startTime) + "_" + str(endTime) + ".xls"

            fs = excel.DoExcel()
            fs.WriteExcel(filename,timestamp_5mins,bandwidth_5mins,timestamp_day_max,bandwidth_day_max,value,1)
            return filename

        return value

    def Day95PerByUid(self):
        pass


    def SumTraffic(self,uid,startTime,endTime,domain=None,savefile=False,):
        '''
        月95计费
        :param uid: 用户ID
        :param startTime:开始时间 YYYY-MM-DD
        :param endTime: 结束时间 YYYY-MM-DD
        :param domain: 域名
        :return:
        '''

        if domain is not None:
            data = self.traffic.GetTrafficByUid(uid,startTime,endTime,domain=domain)
        else:
            data = self.traffic.GetTrafficByUid(uid,startTime,endTime)

        if data[0] == 2002:
            timestamp_5mins = data[1]
            traffics_5mins = data[2]
            timestamp_day = data[3]
            traffics_day = data[4]
        #print bandwidth_5mins
        sum_traffic_day = {}
        for (type,traffic) in traffics_5mins.items():
            if len(traffic) > 0:
                t = 0
                for i in traffic:
                    t += i

            sum_traffic_day[type] = t

        if savefile:
            filename = SAVEPATH + str(uid) + "_" + str(startTime) + "_" + str(endTime) + ".xls"

            fs = excel.DoExcel()
            fs.WriteExcelForTraffic(filename,timestamp_5mins,traffics_5mins,timestamp_day,traffics_day,sum_traffic_day)
            return filename

        return sum_traffic_day