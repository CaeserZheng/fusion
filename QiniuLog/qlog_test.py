#-.- coding=utf-8 -.-

import Qlog

domain="qncdn.gionee.com"
date="2016-04-01"

if __name__ == "__main__":
    log=Qlog.Logs()

   
    res=log.get_log_url(domain,date)
    count=0
    for url in res:
        count += 1
        print str(count) + ":" + url