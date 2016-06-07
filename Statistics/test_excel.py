#-.- coding:utf-8 -.-
from Statistics import excel

time=["2016-05-01 00:00:05","2016-05-01 00:00:01"]
band=[11,22]
ex = excel.DoExcel()
print ex.day_count(time,band)
ss = ex.WriteExcel("test.xls",bw_timestamp=time,bandwidth=band)
if ss:
    print "done"


