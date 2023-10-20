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

# Importamos las librerías necesarias
def imprimirMatriz(matriz):
  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
      print(matriz[i][j], end=" ")
    print()

def getCleanMatix(matriz):
###Inicio funcion de limpieza de valores nulo
  # Creamos variables, matriz con las columnas validas, no tiene las columnas que tiene los valores vacios
  columnas_validas = []
  # Array con las posiciones donde hay vacio, en las columnas
  posVacio = []
  # Array para guardar los valores de cada fila
  valoresBuenos = []
  # Leemos la matriz normalizada
  for fila in matriz:
    # Sacamos de cada fila, el valor y nos quedamos con la posicion del valor
    for pos, valor in enumerate(fila):
      # Si es mayor que el valorMaximo => es un vacio, nos quedamos con la posicion
      if (isnan(valor)):
        posVacio.append(pos)
      # Hay que mejorar esto, peruano, ya que si el array de posiciones Vacia esta a 0, perdemos la primera fila, por eso esta el else
      if (len(posVacio) != 0):
        for valorPosVacio in posVacio:
          if valorPosVacio != pos:
            valoresBuenos.append(valor)
      else:
        valoresBuenos.append(valor)
    columnas_validas.append(valoresBuenos)
    valoresBuenos = []
  return columnas_validas

def getCoefPear(persona, matriz):
  ### Inicio funcion de matriz CofPearson
  #Hacemos el coeficiente de Pearson de la PersonaA con el resto
  lista_corr = []
  for lista in matriz:
    coef_corr = np.corrcoef(persona, lista)
    lista_corr.append(coef_corr[0][1])
  return lista_corr

def getDisCos(persona, matriz):
  ###Inicio funcion DistanciaCoseno
  tmp_lista_cos = []
  for lista in matriz:
    result = np.dot(persona, lista) / (norm(persona) * norm(lista))
    tmp_lista_cos.append(1- result) #Cuanto menor es el valor, MAS se parecen esas personas
  return tmp_lista_cos

def getDisEuc(persona, matriz):
  ### Inicio funcion DistanciEuclidea
  tmp_lista_euc = []
  for lista in matriz:
    tmp_lista_euc.append(dist(persona, lista))
  return tmp_lista_euc
  # ### Final funcion DistanciEuclidea


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

  
  imprimirMatriz(matriz)
  imprimirMatriz(matrizNormalizada)

  f.close()
  CleanMatriz = getCleanMatix(matrizNormalizada)
  persona = int(input("Introduce la persona"))
  MatrizPersona = CleanMatriz[persona]
  CleanMatriz.remove(CleanMatriz[persona])
  print("\nLista Coeficiente ", getCoefPear(MatrizPersona, CleanMatriz))
  print("\nLista Coseno ", getDisCos(MatrizPersona, CleanMatriz))
  print("\nLista Euclidea ", getDisEuc(MatrizPersona, CleanMatriz))
  
main()

# 5.0 3.0 4.0 4.0 -