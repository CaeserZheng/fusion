__author__ = 'caeser'
import json

from Domain import Domain

ak="ipQVw8XQQvMtvV1-QS9BNNdSpVWG4cQdo13IkR4Q"
sk="wnOkR88DWJOrJNODq8TdzZIPlu6iuzljgp1Shsls"
'''
accessKey = '16rc8D6zdNP-Q0fTHD5od5wnhxZcn1QreZyKOzYD'
secretKey = 'fUdQnpAraDR8wq0i3GpBGMg0f6vXg3hEYTwrY-ed'
'''
'''
#meitu
ak="IUJ_2mB_Xlw8aw3cW_OiLCQN2GLPcdLbs_Wo1aYq"
sk="RZ1gRsE4bQJpeJT41tdBITEPdmjX9wVCsvp01py5"
'''
d = Domain.Domain(ak,sk)

res = d.GetDomainList()
res = json.loads(res[2])

domainInfos = res["domainInfos"]
for domain in domainInfos:
    #print domain
    #domainInfos = res["domainInfos"][0]
    print domain["name"]+"\t"+domain["cname"]+"\t"+domain["platform"]+"\t"+domain['sourceType']+"\t"+domain["sourceDomain"]+"\t"+domain['sourceCname']






