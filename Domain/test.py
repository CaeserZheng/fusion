#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : test.py
@Time    : 2019/8/2 15:18
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""
from Domain.Domain import DomainManager

ak = 'Tc3iKoKxu76LJCDF72fuDVbbF1FywfpMkAlyzBQ0'
sk = 'pCYt6gXcEVv7lxC71uqXyXvG-7F7YpkL7sJVI0Bj'


accessKey = 'Rp-xCNSXMcymNzvOoRO6hEJj8wwRfaGs5HbXiLvi'
secretKey = '8wsdGD4chIHIckLT21A7vbXV29JVMpQlG7q3Enpk'

dm = DomainManager(accessKey,secretKey)
print(dm.GetDomainList())
