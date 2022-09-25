# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 09:48:46 2022

@author: User
"""

def tratamento_por_ano(boletins):
   boletins2016 = boletins.where(boletins['Ano Fato'] == 2016).dropna()
   boletins2017 = boletins.where(boletins['Ano Fato'] == 2017).dropna()
   boletins2018 = boletins.where(boletins['Ano Fato'] == 2018).dropna()
   boletins2019 = boletins.where(boletins['Ano Fato'] == 2019).dropna()
   boletins2020 = boletins.where(boletins['Ano Fato'] == 2020).dropna()
   boletins2021 = boletins.where(boletins['Ano Fato'] == 2021).dropna() 
   boletins2022 = boletins.where(boletins['Ano Fato'] == 2022).dropna() 

   crime_bairro_2016 = pd.pivot_table(boletins2016, values= ['Qtde Ocorrências'],index=['bairro_geobr'],aggfunc=np.sum,fill_value=0)
   crime_bairro_2017 = pd.pivot_table(boletins2017, values= ['Qtde Ocorrências'],index=['bairro_geobr'],aggfunc=np.sum,fill_value=0)
   crime_bairro_2018 = pd.pivot_table(boletins2018, values= ['Qtde Ocorrências'],index=['bairro_geobr'],aggfunc=np.sum,fill_value=0)
   crime_bairro_2019 = pd.pivot_table(boletins2019, values= ['Qtde Ocorrências'],index=['bairro_geobr'],aggfunc=np.sum,fill_value=0)
   crime_bairro_2020 = pd.pivot_table(boletins2020, values= ['Qtde Ocorrências'],index=['bairro_geobr'],aggfunc=np.sum,fill_value=0)
   crime_bairro_2021 = pd.pivot_table(boletins2021, values= ['Qtde Ocorrências'],index=['bairro_geobr'],aggfunc=np.sum,fill_value=0)
   crime_bairro_2022 = pd.pivot_table(boletins2022, values= ['Qtde Ocorrências'],index=['bairro_geobr'],aggfunc=np.sum,fill_value=0)
   
   geoloc2016 = bairros_geobr.merge(crime_bairro_2016, left_on ="name_neighborhood",right_on = 'bairro_geobr', how="left")
   geoloc2017 = bairros_geobr.merge(crime_bairro_2017, left_on ="name_neighborhood",right_on = 'bairro_geobr', how="left")
   geoloc2018 = bairros_geobr.merge(crime_bairro_2018, left_on ="name_neighborhood",right_on = 'bairro_geobr', how="left")
   geoloc2019 = bairros_geobr.merge(crime_bairro_2019, left_on ="name_neighborhood",right_on = 'bairro_geobr', how="left")
   geoloc2020 = bairros_geobr.merge(crime_bairro_2020, left_on ="name_neighborhood",right_on = 'bairro_geobr', how="left")
   geoloc2021 = bairros_geobr.merge(crime_bairro_2021, left_on ="name_neighborhood",right_on = 'bairro_geobr', how="left")
   geoloc2022 = bairros_geobr.merge(crime_bairro_2022, left_on ="name_neighborhood",right_on = 'bairro_geobr', how="left")
    
   geoloc2016['Qtde Ocorrências'] = np.log10(geoloc2016['Qtde Ocorrências']).fillna(0)
   geoloc2017['Qtde Ocorrências'] = np.log10(geoloc2017['Qtde Ocorrências']).fillna(0)
   geoloc2018['Qtde Ocorrências'] = np.log10(geoloc2018['Qtde Ocorrências']).fillna(0)
   geoloc2019['Qtde Ocorrências'] = np.log10(geoloc2019['Qtde Ocorrências']).fillna(0)
   geoloc2020['Qtde Ocorrências'] = np.log10(geoloc2020['Qtde Ocorrências']).fillna(0)
   geoloc2021['Qtde Ocorrências'] = np.log10(geoloc2021['Qtde Ocorrências']).fillna(0)
   geoloc2022['Qtde Ocorrências'] = np.log10(geoloc2022['Qtde Ocorrências']).fillna(0)
   
    
   return geoloc2016,geoloc2017,geoloc2018,geoloc2019,geoloc2020,geoloc2021,geoloc2022

def plotagens_anuais(geoloc):
    plt.rcParams.update({"font.size": 5})

    fig, ax = plt.subplots(figsize=(4, 4), dpi=1000)

    geoloc.plot(
        column='Qtde Ocorrências',
        cmap='Reds',
        legend=True,
        edgecolor="#FEBF57",
        linewidth = 0.35,
        legend_kwds={
            "label": "$log_{10}$(Quantidade de Ocorrências)",
            "orientation": "vertical",
            "shrink": 0.6,
        },
        ax=ax,
    )

    ax.set_title("Boletins de Ocorrência de Crimes Noturnos em Vias Públicas de Juiz de Fora")
    ax.axis("off")
    return

import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import geobr
import warnings
warnings.filterwarnings("ignore") 

#Mapa de Juiz de Fora
#https://github.com/ipeaGIT/geobr

bairro = geobr.read_neighborhood(year=2010)
bairros_geobr = bairro.loc[bairro["code_muni"]==3136702]
bairros_geobr["name_neighborhood"] = bairros_geobr["name_neighborhood"].str.upper().str.strip()
bairros_geobr = bairros_geobr[['name_neighborhood','geometry' ]].drop_duplicates()

#------------------------------------------------------------#

#De-para de bairros geobr e pm
#O detalhamento da base da PM é maior que o Geobr, portanto usamos o de-para da prefeitura de Juiz de Fora para alocar
#mais bairros do detalhamento dentro de regiões maiores.

#https://www.pjf.mg.gov.br/institucional/cidade/mapas/mapa_central.php

de_para_geobr_pm = pd.read_excel(r"D:\Usuarios\Dell\Documents\1. Faculdade\1. TCC\de_para_bairros.xlsx")  #Alterar path
de_para_geobr_pm['bairro_geobr'] = de_para_geobr_pm['bairro_geobr'] .str.upper().str.strip()
de_para_geobr_pm['bairro_pm'] = de_para_geobr_pm['bairro_pm'] .str.upper().str.strip()

#------------------------------------------------------------#

#Tratando string
#Removendo acentuação
de_para_geobr_pm['bairro_pm'] = de_para_geobr_pm['bairro_pm'].str.replace('Á', 'A').str.replace('É', 'E').str.replace('Ã', 'A').str.replace('Â', 'A').str.replace('Ú', 'U').str.replace('Ô', 'O').str.replace('Ó', 'O').str.replace('Ê', 'E').str.replace('Í', 'I').str.replace('Ç', 'C').str.replace('Ñ', 'N')
de_para_geobr_pm['bairro_geobr'] = de_para_geobr_pm['bairro_geobr'].str.replace('Á', 'A').str.replace('É', 'E').str.replace('Ã', 'A').str.replace('Â', 'A').str.replace('Ú', 'U').str.replace('Ô', 'O').str.replace('Ó', 'O').str.replace('Ê', 'E').str.replace('Í', 'I').str.replace('Ç', 'C')

#------------------------------------------------------------#

#Padronizando bairros
#Padronizando bairros do de-para da prefeitura
de_para_geobr_pm['bairro_geobr'] = de_para_geobr_pm['bairro_geobr'].str.replace('VILA OZANAN', 'OZANAN').str.replace('SANTO ANTONIO', 'SANTO ANTONIO DO PARAIBUNA').str.replace('LOURDES', 'NOSSA SENHORA DE LOURDES').str.replace('JOQUEI CLUBE', 'JOCKEY CLUB')

#Tratando bairros do Geobr para bater com a base da PM
bairros_geobr["name_neighborhood"] = bairros_geobr["name_neighborhood"].str.replace('Á', 'A').str.replace('É', 'E').str.replace('Ã', 'A').str.replace('Â', 'A').str.replace('Ú', 'U').str.replace('Ô', 'O').str.replace('Ó', 'O').str.replace('Ê', 'E').str.replace('Í', 'I').str.replace('Ç', 'C').str.replace("GRAMBERY","GRANBERY").str.replace("JOCKEY CLUB","JOQUEI CLUB").str.replace("CRUZEIRO DE SANTO ANTONIO","CRUZEIRO SANTO ANTONIO DO PARAIBUNA").str.replace("SANTA RITA DE CASSIA","SANTA RITA").str.replace("GRANJAS BETHANIA","GRANJAS BETANIA").str.replace("JARDIM PAINEIRAS","PAINEIRAS").str.replace("JARDIM SANTA HELENA","SANTA HELENA").str.replace("VILA FURTADO DE MENEZES","FURTADO DE MENEZES")

#------------------------------------------------------------#

#Criando um só dataframe para os dados da PM

path = r"D:\Usuarios\Dell\Documents\1. Faculdade\1. TCC\LAI_pm"                 #Alterar path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, 
                     index_col=None, 
                     header=0,
                     sep=';',
                     encoding='latin-1',
                     parse_dates=['Data Fato'],
                     error_bad_lines=False)
    li.append(df)

boletins = pd.concat(li, axis=0, ignore_index=True)

#Mais tratamento de bairros na base da PM
boletins["Bairro"] = boletins["Bairro"].str.replace("VALE DO YUNG","YUNG").str.replace("SAO LUCAS 2","SAO LUCAS").str.replace("SAO DAMIAO II","SAO DAMIAO").str.replace('Ç', 'C').str.replace('RECANTO DA MATA 2', 'RECANTO DA MATA').str.replace('OLAVO COSTA', 'VILA OLAVO COSTA').str.replace('RESIDENCIAL PORTAL DA TORRE', 'PORTAL DA TORRE').str.replace("AMAZONAS","AMAZONIA").str.replace("ARCO IRIS","ARCO-IRIS").str.replace('JOQUEI CLUBE','JOQUEI CLUB').str.replace('JUSCELINO KUBITSCHEK','JUSCELINO KUBITSCHECK').str.replace('JARDIM BOM CLIMA','JARDIM BONCLIMA').str.replace('NOSSA SENHORA DE LOURDES','LOURDES').str.replace('JARDIM ABC','PARQUE ABC')
boletins['hora'] = boletins['Horário Fato'].str.slice(stop=2).astype(int)
boletins['diurno/noturno'] =  np.where((boletins['hora'] > 6)&(boletins['hora'] < 17),'diurno','noturno')
#boletins_indexado = np.where((boletins['diurno/noturno']=='noturno') & (boletins['Descrição Grupo Local Imediato']=='VIA DE ACESSO'))
boletins_indexado = boletins[(boletins['diurno/noturno']=='noturno') & (boletins['Descrição Grupo Local Imediato']=='VIA DE ACESSO')]
pivot_test = pd.pivot_table(boletins_indexado,values=['Qtde Ocorrências'],index=['Bairro'],columns=['Ano Fato'],aggfunc=np.sum,fill_value=0,margins=True)


#Merge da base da PM com o de-para da prefeitura para agrupar os bairros detalhados da PM em regiões maiores do geobr
boletins_indexado_merged = boletins_indexado.merge(de_para_geobr_pm, left_on="Bairro", right_on='bairro_pm',how='left')
boletins_indexado_merged['bairro_geobr'] = boletins_indexado_merged['bairro_geobr'].fillna(boletins_indexado_merged["Bairro"])
pivot_test2 = pd.pivot_table(boletins_indexado_merged,values=['Qtde Ocorrências'],index=['Bairro'],columns=['Ano Fato'],aggfunc=np.sum,fill_value=0,margins=True)





# #------------------------------------------------------------#


geoloc2016,geoloc2017,geoloc2018,geoloc2019,geoloc2020,geoloc2021,geoloc2022 = tratamento_por_ano(boletins_indexado_merged)



# # #Criando a tabela dinâmica com o total de ocorrências por bairro
tot_crimes_bairro = pd.pivot_table(boletins_indexado_merged, values= ['Qtde Ocorrências'],index=['bairro_geobr'],aggfunc=np.sum,fill_value=0)


# # # #Mapa de Ocorrencias
crimes_geolocalizados_1 = boletins_indexado_merged.merge(bairros_geobr, right_on ="name_neighborhood",left_on = 'bairro_geobr', how="left")
crimes_geolocalizados = tot_crimes_bairro.merge(bairros_geobr, right_on ="name_neighborhood",left_on = 'bairro_geobr', how="left")



# #Colocando as ocorrências em escala logarítmica
crimes_geolocalizados['Qtde Ocorrências'] = crimes_geolocalizados['Qtde Ocorrências'].fillna(10)
crimes_geolocalizados['Qtde Ocorrências'] = np.log10(crimes_geolocalizados['Qtde Ocorrências'])


# plotagens_anuais(geoloc2016)
# plotagens_anuais(geoloc2017)
# plotagens_anuais(geoloc2018)
# plotagens_anuais(geoloc2019)
# plotagens_anuais(geoloc2020)
# plotagens_anuais(geoloc2021)
# plotagens_anuais(geoloc2022)

# Plotagem do mapa

from geopandas import GeoDataFrame

crimes_geolocalizados = GeoDataFrame(crimes_geolocalizados)

plt.rcParams.update({"font.size": 5})

fig, ax = plt.subplots(figsize=(4, 4), dpi=1000)

crimes_geolocalizados.plot(
    column='Qtde Ocorrências',
    cmap='Reds',
    legend=True,
    edgecolor="#FEBF57",
    linewidth = 0.35,
    legend_kwds={
        "label": "$log_{10}$(Quantidade de Ocorrências)",
        "orientation": "vertical",
        "shrink": 0.6,
    },
    ax=ax,
)

ax.set_title("Boletins de Ocorrência de Crimes Noturnos em Vias Públicas de Juiz de Fora - 2016/2022")
ax.axis("off")


# #--------------------------------------------------------------------------#



# #--------------------------------------------------------------------------#



crimes_geolocalizados_1.to_excel(r'D:\Usuarios\Dell\Documents\1. Faculdade\1. TCC\crimes_geolocalizados_databse.xlsx')          #Alterar path para salvar base
# boletins_indexado.to_excel(r'D:\Usuarios\Dell\Documents\1. Faculdade\1. TCC\noturno_via.xlsx')            