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

def imprimirMatriz(matriz):
  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
      print(matriz[i][j], end=" ")
    print()

# Devuelve la matriz sin las columnas en las que haya un nan
def getCleanMatix(matriz):
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


def getSimple(matriz, cleanmatriz):
  n_persona = 2
  sim = []
  n_pos = 0
  max = len(matriz[0])
  for persona in matriz:
    for item in persona:
      if (isnan(item)):
        sim = np.array(getCoefPear(cleanmatriz[matriz.index(persona)], cleanmatriz))
        print(sim)
        VecinosSim = sim[np.argsort(sim)]
        print(VecinosSim)
        VecinosSim = VecinosSim[len(VecinosSim) - n_persona:]
        VecinosSim = VecinosSim[::-1]
        for valor in VecinosSim:
          print(np.where( sim == valor)[0][0])
        #sim = sim[:-len(sim) - n_persona]
        # for i in range(len(sim)):
    #   pos += 1
    # pos = 0

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
  # imprimirMatriz(matrizNormalizada)

  f.close()
  cleanMatriz = getCleanMatix(matrizNormalizada)
  numPersona = int(input("Introduce con cuantas personas quieres comparar: "))
  if (numPersona > (len(matrizNormalizada) - 1)): #-1 no vale puesto que puede haber de un usuario que no ha valorado ese item
    print ("El numero de personas es mayor que el numero de personas que hay en la matriz")
    exit()
  personRelation = getCoefPear(cleanMatriz[0], cleanMatriz) # Habria que pasarle por una funcion
  #Ponemos los valores de mayor a menor de tal manera que los primeros elementos son los que mas se parecen
  personRelationOrdened = sorted(personRelation, reverse=True)
  acumulator = 0
  for i in range(numPersona):
    acumulador += personRelationOrdened[i] #Tengo que ver como coger el valor de esa persona. / personRelationOrdened[i] 










  # persona = int(input("Introduce la persona"))
  # pos = 0
  # for persona in CleanMatriz:
  #   # print("\nPersona -> ", persona, " ", matriz[pos])
  #   # print("Lista Coeficiente ", getCoefPear(persona, CleanMatriz))
  #   # print("Lista Coseno ", getDisCos(persona, CleanMatriz))
  #   # print("Lista Euclidea ", getDisEuc(persona, CleanMatriz))
  #   pos += 1
  # print('Simple ', getSimple(matrizNormalizada, CleanMatriz))

main()
# 5.0 3.0 4.0 4.0 -