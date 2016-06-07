#-.- coding=utf-8 -.-

from qiniu import Auth
from qiniu import BucketManager
import re


#填写ak,sk
access_key="<You Access Key>"
secrek_ley="<You Secrek Key>"

#填写bucket，默认命名qiniulog
bucket="qiniulog"

#填写下载域名
bucket_domain="7xsfp2.com2.z0.glb.qiniucdn.com"

class Logs():
    def __init__(self):
        #初始化Auth状态
        self.au=Auth(access_key, secrek_ley)
        self.bucket=BucketManager(self.au)

    def time_format(self,date):
        '''
        校验日期格式
        :param date:
        :return:
        '''
        # domain_YYYY-MM-DD.gz
        # prefix=domain_YYYY-MM-DD
        # 正则校验日期格式
        reg=re.compile('[0-9]{4}-(0|1)[0-9]{1}-[0-3]{1}[0-9]{1}')
        if reg.match(date):
            return str(date)
        else:
            return False


    def log_list(self,prefix):
        '''
        根据前缀查询日志列表
        :param prefix: 查询前缀
        :return:返回查询结果
        '''
        res = self.bucket.list(bucket,prefix=prefix)
        return res


    def get_log_url(self,domain,date):
        '''
        生成日志下载链接
        :param domain: 需要下载日志的域名
        :param date: 时间：YYYY-MM-DD
        :return:返回日志下载链接，有效期3600
        '''

        #生成查询前缀
        if  domain is None :
            raise ValueError("Please Import Doamin!!!")

        prefix=""
        if self.time_format(str(date)):
            prefix = domain + "_" + date
        else:
            raise ValueError("Date Format：YYYY-MM-DD")

        #生成日志下载url
        urls=[]
        try:
            res = self.log_list(prefix)
            items=res[0]["items"]
            for item in items:
                key = item["key"]
                base_url = 'http://%s/%s' % (bucket_domain, key)
                private_url = self.au.private_download_url(base_url,3600)
                urls.append(private_url)
            return urls
        except:
            print "ERROR:"+res