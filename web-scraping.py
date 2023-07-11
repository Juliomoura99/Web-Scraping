import requests		# GET
from bs4 import BeautifulSoup	#Para a leitura/tradução do HTML 
import re
import pandas as pd	#Para o dataframe
import math


url = 'https://www.kabum.com.br/busca/cadeiras'

headers = {  }  #User agent - só colocar no google e copiar aqui.

site = requests.request('GET', url)
soup = BeautifulSoup(site.content, 'html.parser')	#Entende o conteudo da pagina HTML 

qtd_Itens = soup.find('div',id='listingCount').get_text().strip()

index = qtd_Itens.find(' ') # Achar espaço em branco na frase ' 6835 produtos'

qtd = qtd_Itens[:index]

ultima_pagina = math.ceil(int(qtd)/20)	#Chegar na ultima pagina

dic_produtos = {'marca':[], 'preco':[]}

for i in range(1, ultima_pagina+1):
    url_pag = f'https://www.kabum.com.br/busca/cadeiras?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    site = requests.request('GET', url_pag)
    soup = BeautifulSoup(site.content, 'html.parser')
    produtos = soup.find_all('div', class_=re.compile('productCard'))

    for produto in produtos:
        marca = produto.find('span', class_=re.compile('nameCard')).get_text().strip()
        preco = produto.find('span', class_=re.compile('priceCard')).get_text().strip()

        print(marca,preco)

        dic_produtos['marca'].append(marca)
        dic_produtos['preco'].append(preco)
    print(url_pag)


df = pd.DataFrame(dic_produtos)
df.to_csv(r" [PATH] \preco_cadeira.csv", encoding="utf-8", sep=";") # colocar o caminho \ nome do arquivo que será criado



        


