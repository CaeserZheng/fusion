#-.- coding:utf-8 -.-



from Statistics import Traffic
from Statistics import Billing

tr = Traffic.QNTraffic()
bl = Billing.QNBilling()


uid="1380267848"


st="2016-05-01"
et="2016-06-01"
print bl.Month95PerByUid(uid,st,et,savefile=True)

#print rs
#va = bl.SumTraffic(uid,st,et)
#print va


#小影


'''
uid="1378266334"
st="2016-05-01"
et="2016-05-09"
domian="qn.v2.xiaoying.tv"
file="/Users/caeser/test.txt"
rs = tr.GetBandwidthByUid(uid,st,et,savefile=file,domain=domian)
print rs
'''
'''
status = rs[0]
time= rs[1]
band= rs[2]
if status == 200:
    for i in range(0,len(time)):
        print time[i]+ "\t" + str(band[i])
'''
'''
#百田
uid="1380662347"
st="2016-04-01"
et="2016-05-01"
bl=Billing.QNBilling()

tr=Traffic.QNTraffic()

#print tr.GetBandwidthByUid(uid,st,et)


rs=bl.AveragePerMonthByUid(uid,st,et)

print "统计类型：月平均"
print "统计时间：From:"+st+"\t\tTo="+et
print "月平均值："+str(rs)
print "月平均值："+str(rs/(1000*1000))+"Mbps"
'''
'''
'''

