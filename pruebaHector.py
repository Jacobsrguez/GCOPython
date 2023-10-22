"""
El software debe proporcionar como salida lo siguiente: 
  - La matriz de utilidad con la predicción de los elementos faltantes en la matriz original.
  - La similaridad entre cada usuario y sus vecinos de acuerdo a la métrica elegida.
  - Los vecinos seleccionados en el proceso de predicción.
  - El cálculo de cada predicción de la matriz de utilidad en base a los vecinos seleccionados.

Como resultado de esta práctica debes entregar lo siguiente:
  - Enlace a repositorio GitHub público con el código fuente del sistema recomendador implementado. Incluye en el README.md del repositorio:
  - Instrucciones de instalación de dependencias, despliegue, etc. del software creado.
  - Descripción del código desarrollado.
  - Ejemplo de uso.
  - Un informe en PDF describiendo el análisis realizado en varios ejemplos y las conclusiones extraídas.
"""
# Importamos las librerías necesarias
import numpy as np
from numpy.linalg import norm
from math import dist
from math import isnan


### Funciones
def imprimirMatriz(matriz):
  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
      print(matriz[i][j], end=" ")
    print()

def getCleanMatix(matriz):
###Inicio funcion de limpieza de valores nulo
  # Creamos variables, matriz con las columnas validas, no tiene las columnas que tiene los valores vacios
  posVacio = set()
  columnas_validas = []
  valoresBueno = []
  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
      if isnan(matriz[i][j]):
        posVacio.add(j)

  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
      if not (j in posVacio):
        valoresBueno.append(matriz[i][j])
    columnas_validas.append(valoresBueno)
    valoresBueno = []
  return columnas_validas

def getCoefPear(persona, matriz):
  ### Inicio funcion de matriz CofPearson
  #Hacemos el coeficiente de Pearson de la PersonaA con el resto
  lista_corr = []
  for lista in matriz:
    if persona != lista:
      coef_corr = np.corrcoef(persona, lista)
      lista_corr.append(coef_corr[0][1])
  return lista_corr

def getDisCos(persona, matriz):
  ###Inicio funcion DistanciaCoseno
  tmp_lista_cos = []
  for lista in matriz:
    if persona != lista:
      result = np.dot(persona, lista) / (norm(persona) * norm(lista))
      tmp_lista_cos.append(1- result) #Cuanto menor es el valor, MAS se parecen esas personas
  return tmp_lista_cos

def getDisEuc(persona, matriz):
  ### Inicio funcion DistanciEuclidea
  tmp_lista_euc = []
  for lista in matriz:
    if persona != lista:
      tmp_lista_euc.append(dist(persona, lista))
  return tmp_lista_euc
  # ### Final funcion DistanciEuclidea


def hasNan(lista):
  for valor in lista:
    if isnan(valor):
      return True
  return False


def getSimple(matriz, cleanmatriz):
  n_persona = 4
  sim = []
  posVecinos = []
  posItem = 0
  postPersona = 0
  valorNumerador = 0.0
  valorDenominador = 0.0
  result = 0.0
  # Recorremos las filas de la matriz
  for persona in matriz:
    # Si esa persona tiene un nan pues vamos a rellenarlo
    if hasNan(persona):
      # Obtenemos la lista de coeficiente de Pearson
      sim = np.array(getCoefPear(cleanmatriz[matriz.index(persona)], cleanmatriz))
      # Ordenamos la lista de coeficiente de Pearson
      VecinosSim = sim[np.argsort(sim)]
      VecinosSim = VecinosSim[len(VecinosSim) - n_persona:]
      VecinosSim = VecinosSim[::-1]
      # Recorremos la lista de coeficiente de Pearson
      for valor in VecinosSim:
        # Buscamos los valores de la diagonal
        tmpPosVecino = (np.where( sim == valor)[0][0])
        if (tmpPosVecino >= postPersona):
          # Anadimos un valor mas a las posiciones de los vecinos para que no se pise con la persona
          tmpPosVecino += 1
        # Metemos el valor en la lista de posiciones de los vecinos
        posVecinos.append(tmpPosVecino)
      # Dejamos el vector del mismo tamano que el de los vecinos
      posVecinos = posVecinos[:len(VecinosSim)]
      print(matriz.index(persona), "Sus vecinos son:", posVecinos, VecinosSim)
      for item in persona:
        if (isnan(item)):
          print ("", postPersona)
          print(matriz[postPersona][posItem])
          print("--------------------")
          print(postPersona)
          #valorNumerador += (matriz[postPersona][posItem] * VecinosSim[posVecinos.index(postPersona)])
          #valorDenominador += abs(VecinosSim[posVecinos.index(postPersona)])
          #result = round(valorNumerador / valorDenominador, 3)
          #matriz[postPersona][posItem] = result
          result = 0.0
          posItem += 1
      posItem = 0
    posVecinos = []
    postPersona += 1
  return matriz

def desnormalizar_array(array, valor_minimo, valor_maximo):
  desnormalizado = []

  for lista in array:
      desnormalizada_lista = [(valor * (valor_maximo - valor_minimo)) + valor_minimo for valor in lista]
      desnormalizado.append(desnormalizada_lista)

  return desnormalizado

def main():
  file = "in.txt"
  f = open(file, "r")
  line = f.readline()
  valorMinimo = float(line)
  line = f.readline()
  valorMaximo = float(line)
  matriz = []
  matrizNormalizada = []
  lines = f.readlines()
  serachValue = 0
  for line in lines:
    # Creamos una lista con number, este es de tipo floar, number sale del line.split. El valor sale normalizado si no esta vacio
    fila = [(float(number) - valorMinimo) / (valorMaximo - valorMinimo) if number != '-' else float('NaN') for number in line.split()]
    # La matriz normal guarda el valor de la linea tal cual se lee, es de tipo str
    matriz.append(line)
    # Esta matriz tiene los valores normalizado de tipo float
    matrizNormalizada.append(fila)

  f.close()
  # imprimirMatriz(desnormalizar_array(getSimple(matrizNormalizada, CleanMatriz), valorMinimo, valorMaximo))
  ejercicio = getSimple(matrizNormalizada, getCleanMatix(matrizNormalizada))


## Inicio del programa principal
main()