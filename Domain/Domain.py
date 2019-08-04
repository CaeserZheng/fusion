# -.- coding:utf-8 -.-

from qiniu import Auth
import requests, json

HOST = 'fusion.qiniuapi.com'
PATH = "/v2/domains"

_filter_feild =  set([
    'name',
    'sourceType',
    'sourceType',
    'sourceURLScheme',
    'sourceDomain',
    'sourceHost',
    'sourceIPs'
])

def filters(d,k,v):
    if d[k] == v:
        return d
    else:
        return None


class DomainManager():
    def __init__(self, ak, sk):
        if not (ak or sk):
            raise ValueError("Please input ak and sk!!")

        self.op = Auth(ak, sk)

    def GetDomainListV2(self, marker=None, limit=None):
        query = ""
        if marker is not None:
            query = "&marker=" + marker
        if limit is not None:
            query = query + "&limit=" + limit
        query = query[1:]
        if len(query) == 0:
            url = "http://" + HOST + PATH
        else:
            url = "http://" + HOST + PATH + "?" + query

        url = url.replace(' ', '%20')
        token = self.op.token_of_request(url)
        token = "QBox " + token
        header = {'Authorization': str(token)}
        # print header
        re = requests.get(url, headers=header)
        # print re.headers
        print(re.status_code)
        print(re.text)

        return re.headers, re.status_code, re.text

    def GetDomains(self):
        '''
                marker=None,limit=None,domainPrefix=None,sourceType=None,sourceQiniuBucket=None
                :param kwargs:
                :return:
                '''
        url = "http://" + HOST + PATH
        url = url.replace(' ', '%20')

        token = self.op.token_of_request(url)
        header = {'Authorization': 'QBox %s' % token}
        # print header
        try:
            re = requests.get(url, headers=header)
            info = {'code': re.status_code, 'message': re.headers}
            body = re.text
        except (requests.HTTPError,requests.ConnectionError) as e:
            info = {'code': 0, 'message': e.message()}
            body = None

        return info, body

    def GetDomainList(self, **kwargs):
        '''
        :param kwargs: 过滤条件
        :return:
        '''
        url = "http://" + HOST + PATH
        url = url.replace(' ', '%20')

        token = self.op.token_of_request(url)
        header = {'Authorization': 'QBox %s' % token}
        # print header
        try:
            re = requests.get(url, headers=header)
            body = json.loads(re.text)
            domainInfos = body['domainInfos']
            domian_list = []
            if kwargs:
                for d in domainInfos:
                    for k,v in kwargs.items():
                        d = filters(d,k,v)
                    if d:
                        domian_list.append(d['name'])
            else:
                for d in domainInfos:
                    domian_list.append(d['name'])
            info = {'code': re.status_code, 'message': re.headers}
            return info,domian_list
        except (requests.HTTPError, requests.ConnectionError) as e:
            info = {'code': 0, 'message': e.message()}
            body = None
            return info, body


if __name__ == '__main__':
    ak = ''
    sk = ''

    accessKey = ''
    secretKey = ''

    dm = DomainManager(accessKey, secretKey)
    #print(dm.GetDomains())
    res = dm.GetDomainList(sourceHost='txbind.91shequn.cn')
    for i in res[1]:
        print(i)


