# importando biblioteca
from pandas_datareader import data as web
from matplotlib import pyplot as plt
from datetime import date as dt
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
import os
from joblib import parallel
from joblib import delayed
#define options
options = Options()
options.add_argument('--headless')

#ABRE NAVEGADOR
navegator = webdriver.Chrome(ChromeDriverManager().install(), options= options)
navegator.get('https://finance.yahoo.com/trending-tickers')

sleep(3)
t_body = navegator.find_element_by_tag_name('tbody')

ancoras = t_body.find_elements_by_tag_name('a')

lista_CodBolsas = []

for ancora in ancoras:
    lista_CodBolsas.append(ancora.text)
    
#sempre que passar o filter tem que transformar em lista pois ele retorna um interavel não uma lista

lista_CodBolsas = list(filter(None, lista_CodBolsas))

navegator.quit()

data_inicio = '01/01/2021' 
data_final = dt.today()
os.chdir('C:\\Users\\mathe\\Documents\\codigos_python\\projeto_cotaçao\\plots')
# pegando cotação

def plota_bolsas(nome_bolsa):
    cotacao = web.DataReader(nome_bolsa, data_source = 'yahoo', start = data_inicio, end = data_final)
    #imprime cotaçao
    fig = cotacao["Adj Close"].plot(figsize= (15,15))
    plt.plot()
    plt.title(nome_bolsa,fontdict={'fontsize': 50})
    plt.xlabel('Data',fontdict={'fontsize': 20})
    plt.ylabel('Faturamento',{'fontsize': 20})
    plt.savefig(f'{os.getcwd()}\\{nome_bolsa}.pdf', format = 'pdf', dpi = 300, transparent = True, bbox_inches = 'tight')
    #plt.savefig(f'C:\Users\mathe\Documents\codigos_python\projeto_cotaçao\plots\Faturamento {nome_bolsa} de {data_inicio} ate {data_final}.png')
    plt.close()
    
    

resultado = parallel(n_jobs = 2)(delayed(plota_bolsas)(nome_bolsa) for nome_bolsa in lista_CodBolsas)

#fazendo um teste