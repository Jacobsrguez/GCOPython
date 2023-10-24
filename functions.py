import numpy as np
from numpy.linalg import norm
from math import dist
from math import isnan
import sys

# Muestra una matriz pasado por parametro
def show_matriz(matriz):
  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
      if isinstance(matriz[i][j], str):
        print(matriz[i][j], end="")
      else:
        print(f"{matriz[i][j]:.{3}f}", end=" ")
    print()

# Devuelve una matriz sin los valores nulos
def get_clean_matrix(matriz):
  empty_position = set()
  valid_colums = []
  good_value = []
  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
      if isnan(matriz[i][j]):
        empty_position.add(j)

  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
      if not (j in empty_position):
        good_value.append(matriz[i][j])
    valid_colums.append(good_value)
    good_value = []
  return valid_colums

# Comprueba si tiene valores nulos
def has_nan(list):
  for valor in list:
    if isnan(valor):
      return True
  return False

# Desnormaliza la matriz 
def desnormalize_array(array, min_value, max_value):
  denormalize = []
  for list in array:
    denormalize_list = [(value * (max_value - min_value)) + min_value for value in list]
    denormalize.append(denormalize_list)
  return denormalize

# Calcula la media de las persona
def get_media_person(matriz):
  temp_value = 0.0
  nan_num = 0
  media = []
  for person in matriz:
    for item in person:
      if not (isnan(item)):
        temp_value += item
      else:
        nan_num += 1
    media.append(round(temp_value / (len(person) - nan_num), 3))
    temp_value = 0.0
    nan_num = 0
  return media