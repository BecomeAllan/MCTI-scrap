
#------ Importação das bibliotecas --------
 
from bs4 import BeautifulSoup as bs
import requests as rq
import re
import csv
import pandas as pd
from IPython.core.display import display
from datetime import datetime
import os
 
#--------------------------------------------

dado = []
url = 'https://www.iadb.org/pt/sala-de-imprensa'
teste = rq.get(url)

soup = bs(teste.text, 'html.parser')

teste2 = soup.find('div', class_='group-content')


# Projetos
def iadb4(path): # A entrada é o caminho do arquivo que vai ser definido no arquivo ppfcentral.py

  try:
    print('[iadb4][projetos][start]')
    pages = [] # variavel que conta as paginas
    
    dados = [] # variavel que quarda os dados extraidos de cada pagina
    
    for i in range(3): # total de paginas que o codigo vai percorrer
        url = 'https://www.iadb.org/en/projects-search?country=BR&sector=&status=&query=&page=' + str(i) # Implementa o range nas url
        pages.append(url)
        
    
    
    for item in pages: # for para rodar as paginas 
        page = rq.get(item)
        soup = bs(page.text, 'html.parser')


        even = soup.find_all('tr', class_=re.compile("even")) # tag de extração de uma linha da tabela


        odd = soup.find_all('tr', class_=re.compile("odd")) # tag de extração de uma linha da tabela

        for teste in odd: # for para repetir a variavel odd varias vezes 
          id = teste.find('td').text #busca o codigo
          
          i = id
          
          odd1 = [] # total de paginas que o codigo vai percorrer 

          site = 'https://www.iadb.org/pt/project/' + i # Implementa o range nas url
          odd1.append(site) 

          for x in odd1: # for para rodar as paginas 
            y = rq.get(x)
            sopa = bs(y.text, 'html.parser')

            odd = sopa.find('div', class_=re.compile("group-left")) # tag de extração de uma linha da tabela
            for x in odd:
              cabecario = x.find_previous_sibling('p', class_="project-description")
          
          pais = teste.find('td').next_sibling.next_sibling.text #busca o pais
          setor = teste.find('td').next_sibling.next_sibling.next_sibling.next_sibling.text #busca o setor
          prj_titulo = teste.find('td').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text #busca o titulo do projeto
          prj_valor = teste.find('td').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text #busca o financeiro do projeto
          status = teste.find('td').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text #busca o status do projeto
          data = teste.find('td').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text #busca a data do projeto

          dados.append(dict(zip(['ID','Pais', 'Setor', 'prj_titulo', 'prj_valor', 'Status', 'Data', 'Descrição'], # transforma os dados em uma tabela
                                [id,pais,setor,prj_titulo,prj_valor,status,data,cabecario])))
          
        
          

        #-----------------------------
        


    
        for teste1 in even: # for para repetir a variavel even varias vezes

          id = teste1.find('td').text #busca o codigo

          i = id
          
          linha1 = [] # total de paginas que o codigo vai percorrer 

          site = 'https://www.iadb.org/pt/project/' + i # Implementa o range nas url
          linha1.append(site) 

          for x in linha1: # for para rodar as paginas 
            y = rq.get(x)
            sop = bs(y.text, 'html.parser')

            linha2 = sop.find('div', class_=re.compile("group-left")) # tag de extração de uma linha da tabela
            for x in linha2:
              cabecario = x.find_previous_sibling('p', class_="project-description")


          pais = teste1.find('td').next_sibling.next_sibling.text #busca o pais
          # setor = teste1.find('td').next_sibling.next_sibling.next_sibling.next_sibling.text #busca o setor
          titulo = teste1.find('td').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text #busca o titulo do projeto
          financeiro = teste1.find('td').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text #busca o financeiro do projeto
          # status = teste1.find('td').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text #busca o status do projeto
          # data = teste1.find('td').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text #busca a data do projeto
          
          
          #--------------------------
    
          dados.append(dict(zip(['Pais', 'link', 'prj_titulo', 'prj_valor'], # transforma os dados em uma tabela
                                [pais,site,titulo,financeiro])))

        # cria um dataFrame 
    df = pd.DataFrame(dados,columns=['Pais', 'link', 'prj_titulo', 'prj_valor'])   # organiza as colunas

    for index, row in df.iterrows(): # confere se comtém brasil ou não
        if row['Pais'] == "Brazil":
          df.loc[index,'prj_brazil'] =  "Y"
        else:
          df.loc[index,'prj_brazil'] = "N"

    cod = []
    dia = datetime.today().strftime('%y%m%d')
    for i in range(0,len(site)):
          cod.append('iadb_'+dia+'_04_'+str("{0:0=3d}".format(i)))



    path = path+'''/iadb_12.csv'''
    df.to_csv(path,index=False,sep=",")
    print('[iadb4][projetos][end]')
  except:
    print('Erro na função')
