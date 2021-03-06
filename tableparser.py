#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

class TableParser():
	
	def __init__(self, name):
		self.name = name
		
	def parse_file(self, filename):
		soup = BeautifulSoup(open(filename), 'lxml')
		table = soup.find_all('table')[3] # Grab the right table
		return self.parse_table(table)
			
	def parse_table(self, table):
		if ("LCI" in self.name) or ("LCA" in self.name):
			names = ["tipo", "nome", "vencimento", "taxa", "indexador", "equiv", "ir", "minimo", "rating", "agencia", "liquidez", "aplicar"]
		else:
			names = ["tipo", "nome", "vencimento", "taxa", "indexador", "ir", "minimo", "rating", "agencia", "liquidez", "aplicar"]
		new_table = pd.DataFrame(columns=names, index = [0]) # I know the size
		
		row_marker = 0
		for row in table.find_all('tr'):	
			column_marker = 0
			columns = row.find_all('td')			
			if len(columns) != 0:
				new_table.at[row_marker] = [self.name] + [column.get_text() for column in columns]
				row_marker += 1
		
		new_table['taxa'] = new_table.taxa.str.replace(",", ".")
		new_table['taxa'] = new_table.taxa.str.replace(" %", "").astype(float)/100.0
		new_table['taxa'] = new_table.taxa.astype(str).str.replace(".", ",")
		
		new_table['indexador'] = new_table.indexador.str.replace(u"IPC-A", u"IPCA")
		new_table['indexador'] = new_table.indexador.str.replace(u"Pré", u"prefixado")
		
		new_table['ir'] = new_table.ir.str.replace("Isento", "0")
		new_table['ir'] = new_table.ir.str.replace(",", ".")
		new_table['ir'] = new_table.ir.str.replace(" ", "")
		new_table['ir'] = new_table.ir.str.replace("%", "").astype(float)/100.0
		new_table['ir'] = new_table.ir.astype(str).str.replace(".", ",")
		
		new_table['minimo'] = new_table.minimo.str.replace(".", "")
				
		if new_table['vencimento'][0].isdigit():
			new_table['vencimento'] = datetime.today() + pd.to_timedelta(new_table['vencimento'].astype(int), unit='D')
			new_table['vencimento'] = new_table['vencimento'].dt.strftime('%d/%m/%Y')
		
		new_table = new_table.drop('agencia', 1)
		new_table = new_table.drop('aplicar', 1)		
		if ("LCI" in self.name) or ("LCA" in self.name):
			new_table = new_table.drop('equiv', 1)
				
		return new_table

if __name__ == "__main__":
	filename = "CDB.htm"
	name = 'CDB'
	table = TableParser(name)
	print table.parse_file(filename)
