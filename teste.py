#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tableparser import TableParser

headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'}

url_login = "https://portal.easynvest.com.br/autenticacao/login"

payload = {
    "Conta": raw_input('Conta: '),
    "AssinaturaEletronica": raw_input('Senha: ')
}

url_data = {
	"CDB": "https://portal.easynvest.com.br/rendafixa/cdb/",
	"LCI": "https://portal.easynvest.com.br/rendafixa/lci/",
	"LCA": "https://portal.easynvest.com.br/rendafixa/lca/",
	"LC": "https://portal.easynvest.com.br/rendafixa/lc/",
	"Debentures": "https://portal.easynvest.com.br/rendafixa/debentures/"	

}


s = requests.session()
s.headers.update(headers)
req1 = s.post(url_login, data=payload)
print req1.status_code, req1.url

frames = []

for key, value in url_data.iteritems():
	time.sleep(5)
	req2 = s.get(value)
	print req2.status_code, req2.url
	with open(key + '.htm', 'wb') as f:
		f.write(req2.content)	
	table = TableParser(key)
	frames = frames + [table.parse_file(key + '.htm')]
result = pd.concat(frames)

result.to_csv('valores.csv', index=False, header=False, encoding='utf-8')
		
