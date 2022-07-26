# -*- coding: utf-8 -*-
"""algoritmos_geneticos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1z-NVosVlfLOjd-Yuphg0Lmgj-T9W2uWi

# **LISTA DE EXERCÍCIOS 2**

Aluno: Leonardo Cechella Velho

# **Exercício 1**

Com base no algoritmo desenvolvido em sala de aula, realize uma alteração onde o usuário deverá informar uma quantidade de itens que ele queira cadastrar, depois ele deverá cadastrar esses itens (peso e valor) e também informar a capacidade máxima da mochila. (pts: 0.5).
"""

import numpy as np 
import pandas as pd
import random as rd 
from random import randint 
import matplotlib.pyplot as plt
from IPython.display import clear_output

n = int(input("Defina o número de itens da loja: "))
clear_output()
numero_itens = []
pesos = []
valores = []

for i in range(n):
  numero_itens.append(i+1)
  peso = int(input("Defina o peso do item " + str(i+1) + ": "))
  pesos.append(peso)
  valor = int(input("Defina o valor do item " + str(i+1) + ": "))
  valores.append(valor)

clear_output()

numero_itens = np.array(numero_itens)
pesos = np.array(pesos)
valores = np.array(valores)
max_peso_mochila = int(input("Defina o peso máximo que a mochila pode carregar: "))

print(numero_itens)
print(pesos)
print(valores)

print('Item.    Peso(Kg)     Valor ($)')
for i in range(numero_itens.shape[0]):
    print('{0}        {1}        {2}\n'.format(numero_itens[i], pesos[i], valores[i]))

solucao_por_populacao = 8
tamanho_populacao = (solucao_por_populacao, numero_itens.shape[0])
print('Tamanho da População = {}'.format(tamanho_populacao))
print('Número de individuos (solução) = {}'.format(tamanho_populacao[0]))
print('Número itens (genes) = {}'.format(tamanho_populacao[1]))

populacao_inicial = np.random.randint(2, size = tamanho_populacao)
populacao_inicial = populacao_inicial.astype(int)
n_geracoes = 300 
print('População Inicial: \n{}'.format(populacao_inicial))

def cal_fitness(peso, valor, populacao, max_peso_mochila):
    fitness = np.empty(populacao.shape[0])
    for i in range(populacao.shape[0]):
        S1 = np.sum(populacao[i] * valor)
        S2 = np.sum(populacao[i] * peso) 
        if S2 <= max_peso_mochila:
           fitness[i] = S1
        else : 
           fitness[i] = 0
    return fitness.astype(int)

def selecao_roleta(fitness, numero_pais, populacao):
  max_fitness = sum(fitness)
  probabilidades = fitness/max_fitness 
  selecionados = populacao[np.random.choice(len(populacao),
                                            size=numero_pais,
                                            p=probabilidades)]
  return selecionados

def crossover(pais, numero_filhos):
    filhos = np.empty((numero_filhos, pais.shape[1]))
    ponto_crossover = int(pais.shape[1]/2)
    for k in range(numero_filhos):
      pai_1_idx = k%pais.shape[0]
      pai_2_idx = (k+1)%pais.shape[0]
      filhos[k, 0:ponto_crossover] = pais[pai_1_idx, 0:ponto_crossover]
      filhos[k, ponto_crossover:] = pais[pai_2_idx, ponto_crossover:]
    return filhos

def mutacao(filhos):
    mutacoes = np.empty((filhos.shape))
    for i in range(mutacoes.shape[0]):
        posicao_gene = randint(0,filhos.shape[1]-1)
        if mutacoes[i,posicao_gene] == 0 :
            mutacoes[i,posicao_gene] = 1
        else :
            mutacoes[i,posicao_gene] = 0
    return mutacoes

def rodar_AG(pesos, valores, populacao, tamanho_populacao, n_geracoes, max_peso_mochila):
    parametros, historico_fitness = [], []
    numero_pais = int(tamanho_populacao[0]/2)
    numero_filhos = tamanho_populacao[0] - numero_pais
    fitness = []
    print('Número de pais {} e Número de filhos {}'.format(numero_pais,numero_filhos))
    for i in range(n_geracoes): 
        fitness = cal_fitness(pesos, valores, populacao, max_peso_mochila)
        historico_fitness.append(fitness)
        pais = selecao_roleta(fitness, numero_pais, populacao)
        filhos = crossover(pais, numero_filhos)
        filhos_mutados = mutacao(filhos)
        populacao[0:pais.shape[0], :] = pais 
        populacao[pais.shape[0]:, :] = filhos_mutados
    print('Última Geração: \n{}\n'.format(populacao))
    fitness_ultima_geracao = cal_fitness(pesos, valores, populacao, max_peso_mochila)
    print('Fitness Última Geração: \n{}\n'.format(fitness_ultima_geracao))
    max_fitness = np.where(fitness_ultima_geracao == np.max(fitness_ultima_geracao))
    parametros.append(populacao[max_fitness[0][0],:])
    return parametros, historico_fitness

parametros, historico_fitness = rodar_AG(pesos,
                                         valores,
                                         populacao_inicial,
                                         tamanho_populacao,
                                         n_geracoes,
                                         max_peso_mochila)
print('Os parametros otimizados para as entradas fornecidas são: \n{}'.format(parametros))

itens_selecionados = numero_itens * parametros 
print('\n Itens selecionados que maximizarão a mochila sem quebrá-la:')
for i in range(itens_selecionados.shape[1]):
  if itens_selecionados[0][i] != 0:
      print('{}\n'.format(itens_selecionados[0][i]))

fitness_medio = [np.mean(fitness) for fitness in historico_fitness]
fitness_max = [np.max(fitness) for fitness in historico_fitness]
plt.plot(list(range(n_geracoes)), fitness_medio, label = 'Fitness Médio')
plt.plot(list(range(n_geracoes)), fitness_max, label = 'Fitness Máximo')
plt.legend()
plt.title('Fitness ao decorrer das gerações')
plt.xlabel('Geração')
plt.ylabel('Fitness')
plt.show()
print(np.asarray(historico_fitness).shape)

"""# **Exercício 2**

Com base no algoritmo desenvolvido na atividade anterior, realize uma alteração no crossover do código, você deverá implementar um crossover de múltiplos pontos (2 pontos, fica a seu critério definir as posições dos pontos) e apresente um comparativo (gráficos de geração x fitness) do código original (crossover de ponto único) e sua solução de crossover de múltiplos pontos. (pts: 1)
Obs: O Comparativo deve ser realizado com os mesmos itens, capacidade da mochila, tamanho da população, inicialização... 

"""

import numpy as np 
import pandas as pd
import random as rd 
from random import randint 
import matplotlib.pyplot as plt
from IPython.display import clear_output

n = int(input("Defina o número de itens da loja: "))
clear_output()
numero_itens = []
pesos = []
valores = []

for i in range(n):
  numero_itens.append(i+1)
  peso = int(input("Defina o peso do item " + str(i+1) + ": "))
  pesos.append(peso)
  valor = int(input("Defina o valor do item " + str(i+1) + ": "))
  valores.append(valor)

clear_output()

numero_itens = np.array(numero_itens)
pesos = np.array(pesos)
valores = np.array(valores)
max_peso_mochila = int(input("Defina o peso máximo que a mochila pode carregar: "))

print(numero_itens)
print(pesos)
print(valores)

print('Item.    Peso(Kg)     Valor ($)')
for i in range(numero_itens.shape[0]):
    print('{0}        {1}        {2}\n'.format(numero_itens[i], pesos[i], valores[i]))

solucao_por_populacao = 8
tamanho_populacao = (solucao_por_populacao, numero_itens.shape[0])
print('Tamanho da População = {}'.format(tamanho_populacao))
print('Número de individuos (solução) = {}'.format(tamanho_populacao[0]))
print('Número itens (genes) = {}'.format(tamanho_populacao[1]))

populacao_inicial = np.random.randint(2, size = tamanho_populacao)
populacao_inicial = populacao_inicial.astype(int)
n_geracoes = 300 
print('População Inicial: \n{}'.format(populacao_inicial))

def cal_fitness(peso, valor, populacao, max_peso_mochila):
    fitness = np.empty(populacao.shape[0])
    for i in range(populacao.shape[0]):
        S1 = np.sum(populacao[i] * valor)
        S2 = np.sum(populacao[i] * peso) 
        if S2 <= max_peso_mochila:
           fitness[i] = S1
        else : 
           fitness[i] = 0
    return fitness.astype(int)

def selecao_roleta(fitness, numero_pais, populacao):
  max_fitness = sum(fitness)
  probabilidades = fitness/max_fitness 
  selecionados = populacao[np.random.choice(len(populacao),
                                            size=numero_pais,
                                            p=probabilidades)]
  return selecionados

def crossover(pais, numero_filhos):
    filhos =np.empty((numero_filhos, pais.shape[1]))
    ponto_crossover = int(pais.shape[1]/2)
    for k in range(numero_filhos):
      pai_1_idx = k%pais.shape[0]
      pai_2_idx = (k+1)%pais.shape[0]
      filhos[k, 0:ponto_crossover] = pais[pai_1_idx, 0:ponto_crossover]
      filhos[k, ponto_crossover:] = pais[pai_2_idx, ponto_crossover:]
    return filhos

def multi_point_crossover(pais, numero_filhos):
  for i in range(2):
    filhos = crossover(pais, numero_filhos)
  return filhos;

def mutacao(filhos):
    mutacoes = np.empty((filhos.shape))
    for i in range(mutacoes.shape[0]):
        posicao_gene = randint(0,filhos.shape[1]-1)
        if mutacoes[i,posicao_gene] == 0 :
            mutacoes[i,posicao_gene] = 1
        else :
            mutacoes[i,posicao_gene] = 0
    return mutacoes

def rodar_AG(pesos, valores, populacao, tamanho_populacao, n_geracoes, max_peso_mochila):
    parametros, historico_fitness = [], []
    numero_pais = int(tamanho_populacao[0]/2)
    numero_filhos = tamanho_populacao[0] - numero_pais
    fitness = []
    print('Número de pais {} e Número de filhos {}'.format(numero_pais,numero_filhos))
    for i in range(n_geracoes): 
        fitness = cal_fitness(pesos, valores, populacao, max_peso_mochila)
        historico_fitness.append(fitness)
        pais = selecao_roleta(fitness, numero_pais, populacao)
        filhos = multi_point_crossover(pais, numero_filhos)
        filhos_mutados = mutacao(filhos)
        populacao[0:pais.shape[0], :] = pais 
        populacao[pais.shape[0]:, :] = filhos_mutados
    print('Última Geração: \n{}\n'.format(populacao))
    fitness_ultima_geracao = cal_fitness(pesos, valores, populacao, max_peso_mochila)
    print('Fitness Última Geração: \n{}\n'.format(fitness_ultima_geracao))
    max_fitness = np.where(fitness_ultima_geracao == np.max(fitness_ultima_geracao))
    parametros.append(populacao[max_fitness[0][0],:])
    return parametros, historico_fitness

parametros, historico_fitness = rodar_AG(pesos,
                                         valores,
                                         populacao_inicial,
                                         tamanho_populacao,
                                         n_geracoes,
                                         max_peso_mochila)
print('Os parametros otimizados para as entradas fornecidas são: \n{}'.format(parametros))

itens_selecionados = numero_itens * parametros 
print('\n Itens selecionados que maximizarão a mochila sem quebrá-la:')
for i in range(itens_selecionados.shape[1]):
  if itens_selecionados[0][i] != 0:
      print('{}\n'.format(itens_selecionados[0][i]))

fitness_medio = [np.mean(fitness) for fitness in historico_fitness]
fitness_max = [np.max(fitness) for fitness in historico_fitness]
plt.plot(list(range(n_geracoes)), fitness_medio, label = 'Fitness Médio')
plt.plot(list(range(n_geracoes)), fitness_max, label = 'Fitness Máximo')
plt.legend()
plt.title('Fitness ao decorrer das gerações')
plt.xlabel('Geração')
plt.ylabel('Fitness')
plt.show()
print(np.asarray(historico_fitness).shape)

"""# **Exercício 3**

Dado o dataset (heart.csv) onde possui informações de pessoas que tiveram ataques cardíacos. Utilize uma rede neural artificial para criar um modelo inteligente que consiga realizar a predição. (pts:1.5)  
Você está livre para escolher melhor estrutura para rede neural (número de camadas, número de neurônios, funções de ativação). 
Obs: Você deve encontrar apresentar um modelo com no MINIMO 70% de acurácia e precisão.

"""

import pandas as pd
dataset = pd.read_csv("heart.csv")

dataset.head()

dataset.info()

dataset.describe()

x_entrada = dataset[['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']]
y_saida = dataset['target']

x_entrada

y_saida

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x_entrada, y_saida, test_size = 0.25, random_state = 0)

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

tamanho_entrada = x_entrada.shape[1]

import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping

model = Sequential()
model.add(Dense(40, input_shape=[x_entrada.shape[1]], activation='relu'))

model.add(Dense(40, activation='relu'))
model.add(Dense(40, activation='relu'))

model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

history = model.fit(x_train, y_train,
                    epochs=200,
                    batch_size=35,
                    verbose=1,
                    validation_split=0.2,
                    callbacks=[EarlyStopping(monitor='val_loss', patience=5)])

import matplotlib.pyplot as plt
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['loss', 'val_loss'])
plt.title('Loss')
plt.xlabel('Epoch')

y_pred = model.predict(x_test)

y_pred_bin = [ ( 1 if elem > 0.5 else 0) for elem in y_pred ]

from sklearn.metrics import classification_report
print(classification_report(y_test,y_pred_bin))

import seaborn as sns
from sklearn.metrics import confusion_matrix
import numpy as np

cf_matrix = confusion_matrix(y_test, y_pred_bin)
sns.heatmap(cf_matrix/np.sum(cf_matrix), annot=True, fmt='.2%', cmap='Blues')