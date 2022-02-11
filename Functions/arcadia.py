
# AB#55
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
import os
from itertools import compress
import shutil
from urllib.request import Request, urlopen
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo
#funções:
#retorna uma lista pra preenchimento da coluna de códigos

#retorna os links obtidos na base principal

def getLinksBase(path, filename):
    links_base = []
    path = path + filename
    try:
        dfbase = pd.read_csv(path)
        links_base=(dfbase['link'].tolist())
    except:
        pass
    return links_base
#retorna os links que ainda nao foram lidos
def getNewLinks(links_base, links):
    track =[i in links_base for i in links] 
    new_links_bool = [not bool for bool in track] 
    new_links=(list(compress(links,new_links_bool)))
    return new_links

def arcadia2(path):
    try:
        print('[arcadia][arcadia2][start]')
        pathbase = path.rsplit('//', 1)[0]+'//baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '//arcadia_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://www.arcadiafund.org.uk/articles-case-studies?sort-by=&programme=&focus-area=&content-type=news').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        for card in soup.find_all('div', class_ = 'card'):
            link = card.find('a')['href']
            links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                titulo = page_soup.find('h2', class_ = 'uk-margin-large-bottom').text
                titulos.append(titulo)
                texto = ''
                for p in page_soup.find_all('p'):
                    texto+=p.text
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'arcadia_')
            df.to_csv(path+filename, index=False)
        else:
            print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, './/'+dia)
        print('[arcadia][arcadia2][end]')
        
    except Exception as e:
        print(e)
        print('Erro em arcadia2')

#arcadia2(os.getcwd())

def arcadia3(path):
    try:
        print('[arcadia][arcadia3][start]')
        titulos = []
        textos = []
        link = 'https://www.arcadiafund.org.uk/how-we-operate'
        dia = datetime.today().strftime('%y%m%d')
        filename = '//arcadia_03.csv'
        page = requests.get(link).content.decode('UTF-8')
        soup = BeautifulSoup(page, 'lxml')
        titulo = clean(soup.find('h1').text)
        titulos.append(titulo)
        texto = clean(soup.find('section', class_='section uk-background-white').get_text())
        textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['arcadia']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = [link]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'arcadia_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
        print('[arcadia][arcadia3][end]')
    
    except Exception as e:
        print(e)
        print('Erro em arcadia3')

#arcadia3(os.getcwd())

def arcadia4(path, keywords = '(latin american region|brazil)'):
    #funções de auxilio:
    try:
        print('[arcadia][arcadia4][start]')
        #inicializacao das listas
        codes = []
        hasBrazil = []
        greater2020 = []
        dia = datetime.today().strftime("%y%m%d") #setando o dia
        df = pd.read_csv('https://www.arcadiafund.org.uk/uploads/Arcadia-grants-360Giving-29-September-2020.csv', encoding = 'cp1252') #captura do link que gera o csv
        df = df.drop(['Identifier', 'Currency', 'Term (Months)', 'Term (Years)', 
        'Recipient Org:Identifier', 'Recipient Org:Name', 'Grant Programme:Title', 'Grant Programme:Subtitle', 'Recipient Org:Charity Number',  
        'Funding Org:Identifier', 'Award Date', 'Status'], axis = 1) #informaões irrelevantes
        df['atualizacao'] = [dia]*len(df.index)
        df = df.rename(columns = {'Title': 'prj_titulo', 'Description': 'opo_texto', 'Recipient Org:Web Address': 'link', 'Amount Awarded': 'prj_valor', 'Funding Org:Name': 'prj_instituicao'}) #mudando os nomes
        for i in range(0,len(df.index)): #buscando pelo tipo nos textos  
            if(findall(keywords, df['opo_texto'][i].lower())): #buscando pelas keywords no texto
                hasBrazil.append('Y')
            else:
                hasBrazil.append('N')
        greater2020 = df['Award Year'] >= 2020 #filtrando anos maiores que 2020
        df['prj_brazil'] = hasBrazil
        path = path + '''//arcadia_04.csv'''
        df = df[greater2020]
        codes = getCodList(dia, len(df.index), '_4_', 'arcadia_')
        df['codigo'] = codes
        df = df.drop(columns = ['Award Year', 'opo_texto'])
        df.to_csv(path,index=False,sep=",")
        print('[arcadia][arcadia4][end]')

    except Exception as e:
        print(e)
        print('Erro em arcadia 4')
        
#arcadia4(os.getcwd())
