
# -*- coding: utf-8 -*-
import urllib.request
import xml.etree.ElementTree
import sys
import unicodedata
import datetime
import os as sistema
import sys
import colorama
from colorama import Fore as F
import requests as r
sistema.system('cls' if sistema.name == 'nt' else 'reset')
index = r"""
 ____                       _ _         _   _ ____  
/ ___|  ___  ___ _   _ _ __(_) |_ _   _| | | |  _ \ 
\___ \ / _ \/ __| | | | '__| | __| | | | | | | |_) |
 ___) |  __/ (__| |_| | |  | | |_| |_| | |_| |  __/ 
|____/ \___|\___|\__,_|_|  |_|\__|\__, |\___/|_|    
                                  |___/   
Criado por Joas Antonio dos Santos Barbosa
"""
print(index)

TEMPO = {'ec':'Encoberto com Chuvas Isoladas',
         'ci':'Chuvas Isoladas',
         'c':'Chuva',
         'in':'Instável',
         'pp':'Possibilidade de Pancadas de Chuva',
         'cm':'Chuva pela Manhã',
         'cn':'Chuva à Noite',
         'pt':'Pancadas de Chuva à Tarde',
         'pm':'Pancadas de Chuva pela Manhã',
         'np':'Nublado e Pancadas de Chuva',
         'pc':'Pancadas de Chuva',
         'pn':'Parcialmente Nublado',
         'cv':'Chuvisco',
         'ch':'Chuvoso',
         't':'Tempestade',
         'ps':'Predomínio de Sol',
         'e':'Encoberto',
         'n':'Nublado',
         'cl':'Céu Claro',
         'nv':'Nevoeiro',
         'g':'Geada',
         'ne':'Neve',
         'nd':'Não Definido',
         'pnt':'Pancadas de Chuva à Noite',
         'psc':'Possibilidade de Chuva',
         'pcm':'Possibilidade de Chuva pela Manhã',
         'pct':'Possibilidade de Chuva à Tarde',
         'pcn':'Possibilidade de Chuva à Noite',
         'npt':'Nublado com Pancadas à Tarde',
         'npn':'Nublado com Pancadas à Noite',
         'ncn':'Nublado com Possibilidade de Chuva à Noite',
         'nct':'Nublado com Possibilidade de Chuva à Tarde',
         'ncm':'Nublado com Possibilidade de Chuva pela Manhã',
         'npm':'Nublado com Pancadas de Chuva pela Manhã',
         'npp':'Nublado com Possibilidade de Chuva',
         'vn':'Variação de Nebulosidade',
         'ct':'Chuva à Tarde',
         'ppn':'Possibilidade de Pancadas de Chuva à Noite',
         'ppt':'Possibilidade de Pancadas de Chuva à Tarde',
         'ppm':'Possibilidade de Pancadas de Chuva pela Manhã'}

def getxmlcodes(args):
    # Busca do código das cidades
    codigos = []
    for query in args:
        with urllib.request.urlopen('http://servicos.cptec.inpe.br/XML/listaCidades?city={0}'.format(query)) as url:
            content = url.read().decode('iso-8859-1')

        root = xml.etree.ElementTree.fromstring(content)
        codigos.extend([ elem.text for elem in root.findall('./cidade/id') ])

    if len(codigos) == 0:
        raise ValueError("Não foi encontrado nenhuma Cidade")

    return codigos

def main():
    if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
        print('Modo de uso: {0} "CIDADE[1]" "CIDADE[2]" ... "CIDADE[N]"\nO uso de aspas (") é obrigatório'\
               .format(sys.argv[0]))
        print('Exemplo: {0} "São Paulo"'.format(sys.argv[0]))
        print('Digite o nome do estado ou cidade')
        sys.exit(1)

    # Formatar entrada, remover acentos e substituir espaço por %20
    args = [ unicodedata.normalize('NFKD', elem).encode('ascii', 'ignore').decode('ascii').lower().replace(' ', '%20')
             for elem in sys.argv[1:] ]

    # Obter XML das cidades
    for codes in getxmlcodes(args):
        with urllib.request.urlopen('http://servicos.cptec.inpe.br/XML/cidade/{0}/previsao.xml'.format(codes)) as url:
            content = url.read().decode('iso-8859-1')

        # Filtrar os dados
        root = xml.etree.ElementTree.fromstring(content)
        dias = [ elem.text for elem in root.findall('previsao/dia') ]
        dias = [ datetime.datetime.strptime(elem, '%Y-%m-%d').strftime('%d/%m/%Y') for elem in dias ]
        clima = [elem.text for elem in root.findall('previsao/tempo') ]
        temperaturas = [ (ma, mi) for ma, mi in zip([elem.text for elem in root.findall('previsao/maxima') ],
                                                       [elem.text for elem in root.findall('previsao/minima') ]) ]

        iuv = [ elem.text for elem in root.findall('previsao/iuv') ]

        # Imprimir resultado
        print('\n\nPrevisão do tempo para {0} - {1}:'.format(root[0].text, root[1].text))
        print('(Atualizado em {0})\n'.format(datetime.datetime.strptime(root[2].text, '%Y-%m-%d').strftime('%d/%m/%Y')))

        for i in range(len(dias)):
            print('Dia {0}:'.format(dias[i]))
            print('Clima: {0}'.format(TEMPO[clima[i]]))
            print('Temperatura máxima: {0} °C'.format(temperaturas[i][0]))
            print('Temperatura mínima: {0} °C'.format(temperaturas[i][1]))
            print('Índice UV: {0}'.format(iuv[i]))
            print()



if __name__ == '__main__':
    main()
