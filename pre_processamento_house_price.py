# -*- coding: utf-8 -*-
"""pre-processamento_house_price.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BTlGNyZm8E0tkLhLUsD_k5tlbqwCYSEh

Neste desafio vamos passar por todo o processo de pré-processamento e criação de um modelo de aprendizado de máquina no famoso conjunto de dados “House Price”, que é usado em competições de Machine Learning. Neste dataset você pode encontrar mais 70 atributos sobre casas e seus respectivos preços.

**Objetivo:** É seu trabalho como engenheiro da computação prever o preço de venda de cada casa, ou seja, criar um modelo para isso.

**Itens que você deve cumprir**:

***PARTE 1 ***

*   Detectar possíveis itens faltantes
*   Caso houver, substituir os valores nulos pela média (selecionar pelo menos um atributo. Ex:LotFrontage. )
*   Detectar atributos categóricos (pelo menos 2 atributos, Ex:Street,LotConfig)
*   Utilizar Ordinal Encoding e One hot encoding para transformar os atributos em “números”
*   Verificar possíveis outlier em um atributo (apenas plotar o gráfico) 
*   Selecionar ao menos 10 atributos e aplicar ao modelo de regressão (dado pelo professor) e verificar a acurácia

**Importando as principais bibliotecas**
"""

import pandas as pd #biblioteca utilizada para o tratamento de dados via dataframes 
import numpy as np #biblioteca utilizada para o tratamento de valores numéricos (vetores e matrizes)
import matplotlib.pyplot as plt #biblioteca utilizada para construir os gráficos
import seaborn as sns #biblioteca utilizada para construir os gráficos
from sklearn.linear_model import LogisticRegression # biblioteca para regressão logística 
from sklearn.decomposition import PCA #biblioteca para PCA
from sklearn.feature_selection import RFE #biblioteca para aplicação RFE
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression #importa o modelo de regressão linear univariada
from sklearn.metrics import r2_score #método para o cálculo do R2 (coeficiente de determinação)

"""**Obtendos os dados utilizano google files**"""

from google.colab import files  #biblioteca utilizada para carregar os dados para o google colab
uploaded = files.upload()

"""**Ler o arquivo CSV para um data frame** -> utilizar o read_csv"""

nome_do_arquivo="Dataset_H.csv" 
dataframe = pd.read_csv(nome_do_arquivo, sep=',') #carrega o CSV para um dataframe

"""***Apresentar uma "exemplo" do dataframe (5 instâncias) ***

"""

dataframe.head()

"""***Apresentar as informações sobre as instâncais do dataset, como : N-Entradas, N-Atributos e Tipos ***"""

dataframe.info()

"""**Verificar o somatório de dados nullos em cada atributo**"""

dataframe.isnull().sum()

"""**Calcular média para substituir nos valores nulos**"""

mean_lotFrontage = dataframe['LotFrontage'].mean()

mean_lotFrontage

"""***Preencher os dados nulos com a média ***"""

dataframe['LotFrontage'].fillna(mean_lotFrontage, inplace=True)

dataframe['LotFrontage']

"""**Verificar o somatório de dados nulos em cada atributo**"""

dataframe.isnull().sum()

"""***Verificar possíveis outliers ***"""

ax = sns.boxplot(data=dataframe['LotFrontage'])

"""***Analisar as variáveis e definir um método para trasnformar o dado categórico ***-> comando dummies para One Hot Encoding ou labelencoder para OrdinalEncoder"""

one_hot = pd.get_dummies(dataframe[['Street', 'LotConfig']])

dataframe = dataframe.join(one_hot)

dataframe.head()

"""***Escolher 10 variáveis de entrada e a variável preço como saída***


dica:

 'SalePrice','LotFrontage','OverallQual','TotalBsmtSF', '1stFlrSF','2ndFlrSF','GarageCars','GarageArea','YearBuilt','Grvl','Pave','LotConfig_encoded'


"""

x = dataframe[['LotFrontage','OverallQual','TotalBsmtSF', '1stFlrSF','2ndFlrSF','GarageCars','GarageArea','YearBuilt','Grvl','Pave']]

y = dataframe[['SalePrice']]



"""**Aplicar ao modelo de regressão (dado pelo professor) e verificar a acurácia**"""

#Realiza a construção do modelo de regressão
reg= LinearRegression()
#x_Reshaped=x.reshape((-1, 1)) #coloca os dados no formato 2D
regressao= reg.fit(x,y) # encontra os coeficientes (realiza a regressão)

#realiza a previsão
previsao=reg.predict(x)

#parâmetros encontrados
print('Y = {}X {}'.format(reg.coef_,reg.intercept_))

R_2 = r2_score(y, previsao)  #realiza o cálculo do R2

print("Coeficiente de Determinação (R2):", R_2)

plt.figure(figsize=(10, 10), dpi=100)
plt.scatter(x.index[1:200], y[1:200],  color='gray') #realiza o plot do gráfico de dispersão
plt.scatter(x.index[1:200], previsao[1:200],  color='blue') #realiza o plot do gráfico de dispersão
plt.show()