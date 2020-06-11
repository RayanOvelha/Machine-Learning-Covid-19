import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

df = pd.read_csv('dados-abertos.csv')

#Limpeza e preparo dos dados para o KNN
df.pop('id')
df.pop('Data')
df.pop('Data Cadastro')
df.pop('UF')
df.pop('RA')
df.rename(columns={'Estado de Saúde':'Estado'}, inplace=True)
df.drop(df[df.Estado == 'Não Informado'].index, inplace=True)
df.drop(df[df.Estado == 'Grave'].index, inplace=True)
df.drop(df[df.Estado == 'Leve'].index, inplace=True)
df.drop(df[df.Estado == 'Moderado'].index, inplace=True)
df.reset_index()

df = df.apply(lambda x: x.replace('Sim',True))
df = df.apply(lambda x: x.replace('Não',False))
df = df.apply(lambda x: x.replace('Masculino',1)) #Sexo Masculino = 1
df = df.apply(lambda x: x.replace('Feminino',0)) #Sexo Feminino = 0
df = df.apply(lambda x: x.replace('<= 19 anos',19))# <= 19 anos = 19
df = df.apply(lambda x: x.replace('20 a 29 anos',20))# 20 a 29 anos = 20
df = df.apply(lambda x: x.replace('30 a 39 anos',30))# 30 a 39 anos = 30
df = df.apply(lambda x: x.replace('40 a 49 anos',40))# 40 a 49 anos = 40
df = df.apply(lambda x: x.replace('50 a 59 anos',50))# 50 a 59 anos = 50
df = df.apply(lambda x: x.replace('>= 60 anos',60))# >= 60 anos = 60
df = df.fillna(False)
df.reset_index(drop=True, inplace=True)
doencas = ['Pneumopatia','Nefropatia','Doença Hematológica','Distúrbios Metabólicos','Imunopressão','Obesidade','Outros','Cardiovasculopatia']
df[doencas] = df[doencas].astype(bool)

#Separando uma parte dos dados para teste do KNN
teste = df.loc[((df.shape[0])-950):((df.shape[0])-850)]
teste.to_csv(r'teste.csv',index=False)
df = df.drop(df.index[((df.shape[0])-950):((df.shape[0])-850)])
teste.reset_index(drop=True, inplace=True)

#Treinando KNN
entrada = ['Sexo','Faixa Etária','Pneumopatia','Nefropatia','Doença Hematológica','Distúrbios Metabólicos','Imunopressão','Obesidade','Outros','Cardiovasculopatia']
saída = ['Estado']
x_df = df[entrada].to_numpy()
y_df = df[saída].to_numpy()
x_teste = teste[entrada].to_numpy()
y_teste = teste[saída].to_numpy()

knn = KNeighborsClassifier(n_neighbors=3,weights='distance')
knn.fit(x_df, y_df.ravel())
output = knn.predict(x_teste)

#print(knn.predict([x_teste[0]]))
#print(y_teste[0])

correct = 0.0
for i in range(len(output)):
    if y_teste[i][0] == output[i]:
        correct += 1
        
acertos = correct/len(output)
print(acertos)