import pandas as pd
import numpy as np

#Cria dataframe com soma total de casos globais
casos = pd.read_csv('casos.csv')
casos.rename(columns={'Country/Region':'País'}, inplace=True)
casosSoma = np.sum(casos.iloc[ : , 4 : casos.shape[1]])
casosSoma.index = pd.DatetimeIndex(casosSoma.index)
#print(casosGraph.tail())

#Cria dataframe com soma total de mortes globais
mortes = pd.read_csv('mortes.csv')
mortes.rename(columns={'Country/Region':'País'}, inplace=True)
mortesSoma = np.sum(mortes.iloc[ : , 4 : mortes.shape[1]])
mortesSoma.index = pd.DatetimeIndex(mortesSoma.index)
#print(mortesGraph.tail())

#Cria dataframe com soma total de recuperados globais
recuperados = pd.read_csv('recuperados.csv')
recuperados.rename(columns={'Country/Region':'País'}, inplace=True)
recuperadosSoma = np.sum(recuperados.iloc[ : , 4 : recuperados.shape[1]])
recuperadosSoma.index = pd.DatetimeIndex(recuperadosSoma.index)
#print(recuperadosGraph.tail())

#Soma global dos casos ativos
ativosSoma = casosSoma - (recuperadosSoma+mortesSoma)
#print(ativosSoma.tail())

#Dataframe cmo todos os casos globais
dfTotal = pd.concat([casosSoma, ativosSoma, recuperadosSoma, mortesSoma], axis=1)
dfTotal.columns = (['casos','ativos','recuperados','mortes'])
#print(somaTotal.plot())

#Separando os dados por país
casos.pop('Lat')
casos.pop('Long')
casos.pop('Province/State')
mortes.pop('Lat')
mortes.pop('Long')
mortes.pop('Province/State')
recuperados.pop('Lat')
recuperados.pop('Long')
recuperados.pop('Province/State')

dfPaísTotal = casos.groupby(['País']).sum().reset_index()
dfPaísMortes = mortes.groupby(['País']).sum().reset_index()
dfPaísRecuperados = recuperados.groupby(['País']).sum().reset_index()

#Criando dataframe de casos ativos por país
dfPaísAtivos = pd.concat([dfPaísMortes, dfPaísRecuperados])
dfPaísAtivos = dfPaísAtivos.groupby(['País']).sum().reset_index()
dfPaísAtivos = pd.concat([dfPaísTotal, dfPaísAtivos]).reset_index()
dfPaísAtivos.pop('index').reset_index()
dfPaísAtivos = dfPaísAtivos.groupby(['País']).diff(-1)
dfPaísAtivos.dropna(inplace=True)
coluna_paises = dfPaísTotal['País']
dfPaísAtivos.insert(0,'País',coluna_paises)
dfPaísAtivos.reset_index()

#Juntando todos em um único dataframe principal
dfPaísTotal.insert(1,'Tipo','Total')
dfPaísMortes.insert(1,'Tipo','Mortes')
dfPaísRecuperados.insert(1,'Tipo','Recuperados')
dfPaísAtivos.insert(1,'Tipo','Ativos')

dataframe = pd.concat([dfPaísTotal, dfPaísMortes, dfPaísRecuperados, dfPaísAtivos])
dataframe = dataframe.groupby(['País', 'Tipo']).sum()

#dataframe = dataframe.T
#Brasil = dataframe.loc['Brazil',0]


#Exportar .csv
dataframe.to_csv(r'nosso_dataframe.csv',index=False)