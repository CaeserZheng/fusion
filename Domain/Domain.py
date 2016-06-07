# -.- coding:utf-8 -.-

from qiniu import Auth
import requests,json

HOST='fusion.qiniuapi.com'
PATH="/v2/domains"


class Domain():
    def __init__(self,ak,sk):
        if not (ak or sk):
            raise ValueError("Please input ak and sk!!")

        self.op=Auth(ak,sk)


    def GetDomainList(self,marker=None,limit=None,domainPrefix=None,sourceType=None,sourceQiniuBucket=None):
        query = ""
        if marker is not None:
            query = "&marker=" + marker
        if limit is not None:
            query = query + "&limit=" + limit
        if domainPrefix is not None:
            query = query + "&domainPrefix=" + domainPrefix
        if sourceType is not None:
            query = query + "&sourceType=" + sourceType
            if sourceQiniuBucket is not None:
                query = query + "&sourceQiniuBucket" + sourceQiniuBucket
            else:
                raise ValueError("sourceQiniuBucket invalue!!")

        query = query[1:]
        if len(query) == 0:
            url = "http://" + HOST + PATH
        else:
            url = "http://" + HOST + PATH + "?" +query

        url=url.replace(' ','%20')
        token=self.op.token_of_request(url)
        token="QBox " + token
        header={'Authorization':str(token)}
        #print header
        re=requests.get(url,headers = header)
        '''
        try:
            re=requests.get(url,headers = header)
            if re.status_code == 200:
                domain={}
                res = re.text
                res = json.loads(res)
                domainInfos = res["domainInfos"][0]
            else:
                print re.status_code,re.headers

        except:
            print(re)
        '''
        #print re.headers
        print re.status_code
        print re.text

        return re.headers,re.status_code,re.text






