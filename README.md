# Gestion del Conocimiento de las organizaciones
## Sistemas de recomendación. Métodos de filtrado colaborativo
### Dependencias
Numpy: pip install numpy
### Autores:
* Hector Rodríguez Alonso (alu0101365107)
* Jacob Santana Rodríguez (alu0101330426)  

### Introducción
En la práctica se nos propone implementar un sistema de recomendación siguiendo el método de filtrado colaborativo. 

Para ello, hicimos una aplicación por línea de comandos que recibe las entradas siguiendo el estilo POSIX. Dicha aplicacion hace lo siguiente:

* Lee y guarda de un archivo, la matriz con los datos de los items y usuarios.
* La matriz de utilidad con la predicción de los elementos faltantes en la matriz original.  
* La similaridad entre cada usuario y sus vecinos de acuerdo a la métrica elegida.
* Los vecinos seleccionados en el proceso de predicción.
* El cálculo de cada predicción de la matriz de utilidad en base a los vecinos seleccionados.  

### Decisiones
* Valores negativos en el Coeficiente de Pearson no se toman en cuenta, se eliminan.
* Valores en ítems vecinos con alta similitud que no hayan sido valorados, no se toman en cuenta, se pasa al siguiente vecino.
* Valores en ítems los cuales hayan sido generados por el algoritmo, no se toman en cuenta para siguientes predicciones, se tratan como no evaluados.
* Debido a lo comentado anteriormente, si el usuario ingresa 3 vecinos y alguno no ha valorado, se emplearán los que esten valorados aunque la predicción se realice con menos vecinos de los dados por el usuario.

### Explicación del código
* functions.py Fichero que contiene diferentes funciones "adicionales" que desarrollamos para lograr tener un codigo mas estructurado y legible.

* SistemasRecomendador.py En este fichero se encuentran las funciones mas primordiales del programa, y donde esta escrito el propio programa.

Empezaré explicando el *functions.py*

> `show_matriz(matriz)`: Se encarga de mostrar una matriz con los valores pasados por parametros
> `get_clean_matrix(matriz)`: Se le pasa una matriz la cual recorre y devuelve sin los valores nulos(nan)  
> `has_nan(list)`: Recorre la lista y devuevle true en caso de que haya un valor nulo  
> `desnormalize_array(array, min_value, max_value)`: Se encarga de desnormalizar la matriz que se le pasa  
> `get_media_person(matriz)`: Calcula las media de cada persona de la matriz

Estas son las funciones que se encuentran en functions.py ahora vamos a nombrar las que se encontrara en *SistemaRecomendador.py*

> `get_sim_pearson(person, matrix)`: Calcula el coeficinete de una persona con sus vecinos, hacemos uso de la librería numpy para el cálculo  
> `get_sim_dis_coseno(person, matrix)`: Calcula la distancia coceno de el usuario respecto a sus vecinos y tambien se apoya en la libreria numpy  
> `get_dis_euc(person, matriz)`: Calcula la distancia euristica de la persona respecto a sus vecinos.
> `get_predicction(matrix, clean_matrix, type_sim , number_neighbors, type_pred)`: Se encarga de calcular la prediccion dependiendo ya sea simple o con el calculo de la media, en funcion de lo que contenga type_def.

El programa recibe las entradas siguiendo el método POSIX y empleando la librería *argparse* y *sys*, basándonos en el siguiente [ejemplo](https://nullprogram.com/blog/2020/08/01/). Obteniendo el siguiente resultado:
>$ python ../SistemaRecomendador.py --help  
> usage: SistemaRecomendador.py [-h] [--f F] [--ms MS] [--n N] [--mp MP]  
>options:  
>&emsp;-h, --help  show this help message and exit  
>&emsp;--f F       Nombre del fichero de lectura  
>&emsp;--ms MS     Metodo similitud [p]earson | [c]oseno | [e]uclidea        
>&emsp;--n N       Numero de vecinos  
>&emsp;--mp MP     Metodo prediccion [s]imple | [m]edia  

### Ejemplos de uso

Estos son algunos ejemplo para ejecutar el programa, siguiendo nuestro esquema de argumentos:
>$ python SistemaRecomendador.py --f utility-matrix-5-10-1.txt --ms c --n 3 --mp s  

&emsp; Resultado: [matrix-5-10](/results/m5-10/c_3_s_utility-matrix-5-10-1.txt)

>$ python SistemaRecomendador.py --f utility-matrix-25-100-4.txt --ms p --n 3 --mp m  

&emsp; Resultado: [matrix-25-100](/results/m25-100/p_3_m_utility-matrix-25-100-4.txt)

>$ python SistemaRecomendador.py --f utility-matrix-50-250-2.txt --ms e --n 3 --mp m  

&emsp; Resultado: [matrix-50-250](/results/m50-250/e_3_m_utility-matrix-50-250-2.txt)