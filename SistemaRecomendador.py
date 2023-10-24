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
import functions
import argparse

# Calcula el coeficiente de pearson
def get_sim_pearson(person, matrix):
  list_pearson = []
  for list in matrix:
    if person != list:
      coef_pearson = np.corrcoef(person, list)
      list_pearson.append(coef_pearson[0][1])
  return list_pearson

# Calcula la distancia coceno
def get_sim_dis_coseno(person, matrix):
  tmp_list_cos = []
  for list in matrix:
    if person != list:
      result = np.dot(person, list) / (norm(person) * norm(list))
      tmp_list_cos.append(1- result) #Cuanto menor es el valor, MAS se parecen esas personas
  return tmp_list_cos

# Calcula la distancia euclidea
def get_dis_euc(person, matriz):
  tmp_list_euc = []
  for list in matriz:
    if person != list:
      tmp_list_euc.append(1.0 / (1.0 + dist(person, list)))
  return tmp_list_euc

# Calcula la prediccion
def get_predicction(matrix, clean_matrix, type_sim , number_neighbors, type_pred):
  similarity = []
  pos_neighbors = [] #Lista con la posicion de los vecinos en la matriz
  pos_person = 0
  numerator = 0.0
  denominator = 0.0
  predicction = 0.0
  copy_matrix = matrix
  result_string = ""
  result_string_similarity = ""
  if (type_sim == 'p'):
    function_sim = get_sim_pearson
  elif (type_sim == 'e'):
    function_sim = get_dis_euc
  elif (type_sim == 'c'):
    function_sim = get_sim_dis_coseno

  if (type_pred == "m"):
    media = functions.get_media_person(copy_matrix)

  for person in copy_matrix:
    if functions.has_nan(person):
      similarity = np.array(function_sim(clean_matrix[copy_matrix.index(person)], clean_matrix))
      result_string_similarity += "Persona {} tiene la siguiente similitud {}\n".format(pos_person, similarity)
      neighbors_similitary = similarity[np.argsort(similarity)]
      neighbors_similitary = [value for value in neighbors_similitary if value >= 0.0]
      if type_sim != "e":
        neighbors_similitary = neighbors_similitary[::-1]
      neighbors_similitary = neighbors_similitary[:number_neighbors]
      for value in neighbors_similitary:
        tmp_pos_neighbor = (np.where( similarity == value)[0][0])
        if (tmp_pos_neighbor >= pos_person):
          tmp_pos_neighbor += 1
        pos_neighbors.append(tmp_pos_neighbor)
      result_string_similarity += "Vecinos validos {} \n".format(pos_neighbors)
      pos_neighbors = pos_neighbors[:len(neighbors_similitary)]
      pos_nan = np.where(np.isnan(np.array(person)))[0]
      for iterator in range(len(pos_nan)):
        for iterator_neighbor in range(len(pos_neighbors)):
          if not (isnan(copy_matrix[pos_neighbors[iterator_neighbor]][pos_nan[iterator]])):
            if (type_pred == "s"):
              numerator += (copy_matrix[pos_neighbors[iterator_neighbor]][pos_nan[iterator]] * neighbors_similitary[iterator_neighbor])
              denominator += abs(neighbors_similitary[iterator_neighbor])
            elif (type_pred == "m"):
              numerator += (neighbors_similitary[iterator_neighbor] * (copy_matrix[pos_neighbors[iterator_neighbor]][pos_nan[iterator]] - media[pos_neighbors[iterator_neighbor]]))
              denominator += abs(neighbors_similitary[iterator_neighbor])
            else:
              print("Tipo de prediccion no implementada\nUse --help")
              sys.out(1)
        if (denominator == 0.0):
          predicction = 0.0
        else:
          predicction = round(numerator / denominator, 3)
        if (predicction < 0.0):
          predicction = 0.0
        if (type_pred == "m"):
          predicction += media[pos_person]
        result_string += "Persona {} e item {} prediccion {} con vecinos {} y sim {}\n".format(pos_person, pos_nan[iterator], round(predicction, 3), pos_neighbors, neighbors_similitary)
        matrix[pos_person][pos_nan[iterator]] = round(predicction, 3)
        predicction = 0.0
        numerator = 0.0
        denominator = 0.0
    pos_neighbors = []
    pos_person += 1
  return matrix, result_string, result_string_similarity

#### Programa principal ####
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--f', type=str, help='Nombre del fichero de lectura')
  parser.add_argument('--ms', type=str, help='Metodo similitud [p]earson | [c]oseno | [e]uclidea')
  parser.add_argument('--n', type=int, help="Numero de vecinos")
  parser.add_argument('--mp', type=str, help="Metodo prediccion [s]imple | [m]edia")
  args = parser.parse_args(sys.argv[1:])

  if not args.ms in ['p', 'e', 'c']:
    print("Tipo de similitud no creado\nUse --help para obtener mas informacion")
    sys.exit(1)
  if not args.mp in ['s', 'm']:
    print("Tipo de prediccion no creado\nUse --help para obtener mas informacion")
    sys.exit(1)

  matrix = []
  normalize_matrix = []
  f = open(args.f, "r")
  line = f.readline()
  value_min = float(line)
  line = f.readline()
  value_max = float(line)
  for line in f.readlines():
    # Creamos una lista con number, este es de tipo floar, number sale del line.split. El valor sale normalizado si no esta vacio
    fila = [(float(number) - value_min) / (value_max - value_min) if number != '-' else float('NaN') for number in line.split()]
    # La matriz normal guarda el valor de la linea tal cual se lee, es de tipo str
    matrix.append(line)
    # Esta matriz tiene los valores normalizado de tipo float
    normalize_matrix.append(fila)
  f.close()
  if int(args.n) >= len(matrix):
    print("El numero de vecinos debe de ser extrictamente menor que el total de ellos")
  elif int(args.n) <= 0:
    print("El numero de vecinos debe de ser mayor que cero") 
  
  normalize_utility_matrix, result_string, result_string_similarity = get_predicction(normalize_matrix, functions.get_clean_matrix(normalize_matrix), args.ms, args.n, args.mp)
  utility_matrix = functions.desnormalize_array(normalize_utility_matrix, value_min, value_max)
  result_file = open(args.ms + "_" + str(args.n) + "_" + args.mp + "_" + args.f, "w")
  result_file.write("-- Matriz entrante --\n")
  for person in matrix:
   result_file.write(person)
  result_file.write("\n\n" + result_string + "\n\n")
  result_file.write("-- Similitud entre personas--\n" + result_string_similarity + "\n\n")
  result_file.write("-- Matriz de utilidad --\n")
  for i in range(len(utility_matrix)):
   for j in range(len(utility_matrix[i])):
     texto = "{:.3f} ".format(utility_matrix[i][j])
     result_file.write(texto)
   result_file.write("\n")
  result_file.close()