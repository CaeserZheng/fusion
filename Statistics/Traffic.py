#-.- coding:utf-8 -.-

import json
import re

import requests

from Statistics import excel

api="http://api.qiniu.com/v1/user/top"
SAVEPATH="/Users/caeser/Codes/python2/Fusion/Statistics/data/"
class QNTraffic():
    def __init__(self):
        pass

    #http post 'http://api.qiniu.com/v1/user/top' uid:=1378266334 from=2016-05-01 to=2016-05-09
    def GetBandwidthByUid(self,uid,startTime,endTime,savefile=False,domain=None):
        '''
        通过uid获取一段时间内的用户带宽情况，粒度五分钟
        :param uid:用户uid
        :param startTime:开始时间 YYYY-MM-DD
        :param endTime:结束时间 YYYY-MM-DD
        :param savefile:结果保存目标文件
        :param domain:获取某个域名的数据
        :return:timestamp_5mins dick五分钟时间戳,bandwidth_5mins五分钟带宽,timestamp_day_max日时间戳,bandwidth_day_max日峰值
        2001 返回文件
        2002 返回数据
        '''
        #请求表单
        form={"uid":uid,"from":startTime,"to":endTime}
        re = requests.post(api,form)

        #print re.status_code,re.content,re.headers
        if re.status_code == 200:
            data =re.text

            data=json.loads(data)
            timestamp_5mins = data["time"]      #时间戳
            bandwidth_5mins = self._analizy_band(data,domain)
            #print bandwidth_5mins
            #计算日峰值
            rs = self._getMaxPerDay(timestamp_5mins,bandwidth_5mins)
            timestamp_day_max = rs[0]
            bandwidth_day_max = rs[1]
            if savefile:
                fs = excel.DoExcel()
                filename = SAVEPATH + str(uid) + "_" + str(startTime) + "_" + str(endTime) + ".xls"
                print filename
                rs = fs.WriteExcel(filename,timestamp_5mins,bandwidth_5mins,timestamp_day_max,bandwidth_day_max)
                if rs:
                    return 2001,filename
            else:
                return  2002,timestamp_5mins,bandwidth_5mins,timestamp_day_max,bandwidth_day_max
        else:
            return re.status_code,re.headers,re.content

    def GetTrafficByUid(self,uid,startTime,endTime,savefile=False,domain=None):
        '''
        通过UID获取用户流量
        :param uid:
        :param startTime: YYYY-MM-DD
        :param endTime: YYYY-MM-DD
        :param savefile:结果保存目标文件
        :param domain:获取某个域名的数据
        :return:状态码,时间戳\t流量大小单位B
        '''
        st=startTime.replace(" ","%20")
        et=endTime.replace(" ","%20")
        if domain is not None:
            data = self.GetBandwidthByUid(uid,st,et,domain)
        else:
            data = self.GetBandwidthByUid(uid,st,et)

        status = data[0]
        if status == 2002:
            timestamp_5mins=data[1]
            bandwidth_5mins=data[2]
            timestamp_day=data[3]
            traffics_5mins = {}
            traffics_day = {}

            #计算5mins单位流量
            #print "bandwidth_5mins==>"+str(bandwidth_5mins)
            for (type,bandwidth) in bandwidth_5mins.items():
                traffic = []
                if len(bandwidth) > 0:
                    for i in bandwidth:
                        traffic.append(i*300/8)
                    traffics_5mins[type]=traffic
            #计算天单位流量
            for (type,tra) in traffics_5mins.items():
                traffic = []
                i = 0
                while i < len(tra) - 287:
                    traffic.append(sum(tra[i:i+287]))
                    i+=288
                traffics_day[type]=traffic


            if savefile:
                fs = excel.DoExcel()
                filename = SAVEPATH + str(uid) + "_" + str(startTime) + "_" + str(endTime) + ".xls"
                #print filename
                rs = fs.WriteExcelForTraffic(filename,timestamp_5mins,traffics_5mins,timestamp_day,traffics_day)
                if rs:
                    return 2001,filename
            else:
                return  2002,timestamp_5mins,traffics_5mins,timestamp_day,traffics_day
        else:
            return data

    def GetBandwidthDiffDomainByUID(self,uid,startTime,endTime,savefile=False):
        '''
        根据UID获取各个域名的带宽信息
        :param uid:
        :param startTime:
        :param endTime:
        :param savefile:
        :return:
        '''

        form={"uid":uid,"from":startTime,"to":endTime}
        re = requests.post(api,form)

        #print re.status_code,re.content,re.headers
        if re.status_code == 200:
            data =re.text

            data=json.loads(data)
            timestamp_5mins = data["time"]      #时间戳
            bandwidth_5mins = self._analizy_band(data)
            if data["httpCN"]:
                for dict in data["httpCN"]:
                    pass

        pass

    def GetDomainByUID(self,UID):
        '''
        获取域名列表
        :param UID:
        :return:域名列表
        '''
        pass


    #def GetBandwidthByDomain(self,uid,domain,startTime,endTime):
    def _getMaxPerDay(self,timestamp_5mins,bandwidth_5mins):
        '''
        计算每天的峰值
        :param timestamp_5mins: 时间戳
        :param bandwidth_5mins:     带宽数据
        :return:
        '''
        dayStamp = []      #获取天数
        bandwidth_day_max = {}         #按照协议分类
        timestamp_day_max = {}

        i = 0
        while i < len(timestamp_5mins)-287:
                dayStamp.append(re.split("T",timestamp_5mins[i])[0])
                i+=288

        for (type,bandw) in bandwidth_5mins.items():
            maxOfday = []      #每日峰值
            timestamp = []
            if len(bandw) > 0:
                j = 0
                while j < len(bandw)-287:
                    va = max(bandw[j:j+287])
                    maxOfday.append(va)
                    timestamp.append(timestamp_5mins[bandw.index(va)])
                    j+=288
                timestamp_day_max[type] = timestamp
                bandwidth_day_max[type] = maxOfday

        return timestamp_day_max,bandwidth_day_max

    def _analizy_band(self,data,domain=None):
        '''
        过滤流量
        :param data:流量数据
        :param domain: 域名
        :return:bandwidth_5mins: dict={协议:list[带宽]}
        '''
        httpCN_band = []
        httpOV_band = []
        httpsCN_band = []
        httpsOV_band = []
        timestamp_5mins = data["time"]      #时间戳
        if domain is not None:
            if data["httpCN"]:
                for dict in data["httpCN"]:    #以域名来统计数值
                    if dict["domain"] == domain:
                        httpCN_band = dict["value"]

            if data["httpOV"]:
                for dict in data["httpOV"]:    #以域名来统计数值
                    if dict["domain"] == domain:
                        httpOV_band = dict["value"]

            if data["httpsCN"]:
                for dict in data["httpsCN"]:    #以域名来统计数值
                    if dict["domain"] == domain:
                        httpsCN_band = dict["value"]

            if data["httpsOV"]:
                for dict in data["httpsOV"]:    #以域名来统计数值
                    if dict["domain"] == domain:
                        httpsOV_band = dict["value"]
        else:
            for i in range(0,len(timestamp_5mins)):
                v1=v2=v3=v4=0
                if data["httpCN"]:
                    for dict in data["httpCN"]:    #以域名来统计数值
                        v1 = v1 + dict["value"][i]
                    httpCN_band.append(v1)
                if data["httpOV"]:
                    for dict in data["httpOV"]:    #以域名来统计数值
                        v2 = v2 + dict["value"][i]
                    httpOV_band.append(v2)

                if data["httpsCN"]:
                    for dict in data["httpsCN"]:    #以域名来统计数值
                        v3 = v3 + dict["value"][i]
                    httpsCN_band.append(v3)
                if data["httpsOV"]:
                    for dict in data["httpsOV"]:    #以域名来统计数值
                        v4 = v4 + dict["value"][i]
                    httpsOV_band.append(v4)


        bandwidth_5mins={"httpCN_band":httpCN_band,"httpOV_band":httpOV_band,"httpsCN_band":httpsCN_band,"httpsOV_band":httpsOV_band}
        return bandwidth_5mins





