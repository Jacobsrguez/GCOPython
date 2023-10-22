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

import numpy as np
from numpy.linalg import norm
from math import dist
from math import isnan
import sys

# Importamos las librerías necesarias
def imprimirMatriz(matriz):
  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
      if isinstance(matriz[i][j], str):
        print(matriz[i][j], end="")
      else:
        print(f"{matriz[i][j]:.{3}f}", end=" ")
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


def getSimple(matriz, cleanmatriz, tipo, numeroVecinos):
  print(tipo)
  if (tipo == 'p'):
    funcion = getCoefPear
  elif (tipo == 'e'):
    funcion = getDisEuc
  elif (tipo == 'c'):
    funcion = getDisCos
  else:
    print("Funcion no creada")
    sys.exit(1)
  if numeroVecinos >= len(matriz):
    print("El numero de veciones debe de ser extrictamente menor que el total de ellos")
  elif numeroVecinos <= 0:
    print("El numero de vecinos debe de ser mayor que cero") 
  sim = []
  posVecinos = []
  posItem = 0
  postPersona = 0
  valorNumerador = 0.0
  valorDenominador = 0.0
  valorAprox = 0.0
  for persona in matriz:
    if hasNan(persona):
      sim = np.array(funcion(cleanmatriz[matriz.index(persona)], cleanmatriz))
      VecinosSim = sim[np.argsort(sim)]
      VecinosSim = VecinosSim[len(VecinosSim) - numeroVecinos:]
      VecinosSim = VecinosSim[::-1]
      for valor in VecinosSim:
        tmpPosVecino = (np.where( sim == valor)[0][0])
        if (tmpPosVecino >= postPersona):
          tmpPosVecino += 1
        posVecinos.append(tmpPosVecino)
      posVecinos = posVecinos[:len(VecinosSim)]
      for item in persona:
        if (isnan(item)):
    #     #VecinosSim = [valor for valor in VecinosSim if valor > 0.0]
          for iterador in range(len(posVecinos)):
            if not (isnan(matriz[posVecinos[iterador]][posItem])): 
              #print(matriz[posVecinos[iterador]], " con similitud ", VecinosSim[iterador])
              #print (matriz[posVecinos[iterador]][posItem] , "*", VecinosSim[iterador] , " entre ", abs(VecinosSim[iterador]))
              valorNumerador += (matriz[posVecinos[iterador]][posItem] * VecinosSim[iterador])
              valorDenominador += abs(VecinosSim[iterador])
          valorAprox = round(valorNumerador / valorDenominador, 3)
          #print("Valor creado para la posicion ", valorAprox)
          matriz[postPersona][posItem] = valorAprox
          valorAprox = 0.0
        #print("Valor estimado para la persona ", persona, " en la posicion ", posItem, " es ", valorAprox)
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

if __name__ == "__main__":
  argumentos = sys.argv
  matriz = []
  matrizNormalizada = []
  if argumentos[1] == "--help":
    print("Intrucciones a seguir: python SistemaRecomendador.py fichero modoEuristica numeroVecinos modoPrediccion")
    print("fichero -> Coloque el nombre del fichero finalizando en .txt")
    print("modoEuristica -> Coloque [p]earson | [c]oseno | [e]uclidea")
    print("numeroVecinos -> Coloque el numero de vecinos que desea elegir")
    print ("\t\tten en cuenta que debe ser menor que el numero total")
    print("modoEuristica -> Coloque [s]imple | [m]edia")
    print("Ej: python SistemaRecomendador.py in.txt p 5 s")
  if (len(argumentos) != 4):
    print("Coloque --help para conocer el funcionamiento")
    sys.exit(1)
  file = argumentos[1]
  f = open(file, "r")
  line = f.readline()
  valorMinimo = float(line)
  line = f.readline()
  valorMaximo = float(line)
  for line in f.readlines():
    # Creamos una lista con number, este es de tipo floar, number sale del line.split. El valor sale normalizado si no esta vacio
    fila = [(float(number) - valorMinimo) / (valorMaximo - valorMinimo) if number != '-' else float('NaN') for number in line.split()]
    # La matriz normal guarda el valor de la linea tal cual se lee, es de tipo str
    matriz.append(line)
    # Esta matriz tiene los valores normalizado de tipo float
    matrizNormalizada.append(fila)
  f.close()
  CleanMatriz = getCleanMatix(matrizNormalizada)
  #persona = int(input("Introduce la persona"))
  # for persona in CleanMatriz:
    # print("\nPersona -> ", persona, " ", matriz[pos])
    # print("Lista Coeficiente ", getCoefPear(persona, CleanMatriz))
    # print("Lista Coseno ", getDisCos(persona, CleanMatriz))
    # print("Lista Euclidea ", getDisEuc(persona, CleanMatriz))
  imprimirMatriz(matriz)
  imprimirMatriz(matrizNormalizada)
  imprimirMatriz(desnormalizar_array(getSimple(matrizNormalizada, CleanMatriz, argumentos[2], int(argumentos[3])), valorMinimo, valorMaximo))