"""
O algoritmo de ordenação por inserção, ou insertion sort, é um algoritmo simples e 
eficiente para ordenar um conjunto de elementos. Ele percorre a lista de elementos a serem ordenados, 
um por um, e insere cada elemento em sua posição correta na parte já ordenada da lista.

O processo do insertion sort pode ser explicado passo a passo da seguinte maneira:

1. Inicialmente, consideramos o primeiro elemento da lista como a parte ordenada, pois não há elementos
 anteriores para comparar.

2. Em seguida, percorremos a lista a partir do segundo elemento até o último. Para cada elemento atual, fazemos o seguinte:

a. Comparamos o elemento atual com os elementos anteriores na parte ordenada da lista.

b. Enquanto o elemento atual for menor do que o elemento anterior, movemos o elemento anterior para a
 próxima posição e continuamos a comparação com o próximo elemento anterior.

c. Quando encontramos a posição correta para o elemento atual, inserimos o elemento naquela posição.

3. Repetimos o passo 2 para cada elemento subsequente até percorrer toda a lista.

4. Após a iteração final, todos os elementos estarão em suas posições corretas, e a lista estará ordenada.

O insertion sort tem uma complexidade de tempo no pior caso de O(n^2), onde 'n' é o número de elementos a 
serem ordenados. No entanto, ele pode ser eficiente para conjuntos de dados pequenos ou quase ordenados, pois a 
inserção de cada elemento na parte ordenada requer um número limitado de comparações e movimentos.

Em resumo, o insertion sort é um algoritmo de ordenação que percorre a lista de elementos e insere cada elemento 
em sua posição correta na parte já ordenada da lista. Ele é simples de implementar, eficiente para pequenos conjuntos 
de dados e tem uma complexidade de tempo de pior caso de O(n^2).
"""

def InsertionSort(array):
    
    for i in range(1, len(array)):
        #print(array[i])
        key = array[i] # gaurda o segundo elemento numa chave (key)
        j = i - 1 # atribui ao J o valor de i -1, ou seja o primeiro elemento do array
        #print("J",array[j])

        while j >= 0 and array[j] > key: # enquanto o j é maior q zero e houver um elemnto no array que é maior que o da chave
            array[j + 1] = array[j]
            j -= 1
            #pass
        
        array[j + 1] = key

    return array

def main():
    print('InsertionSort Algoritmo')
    print("Array Inicial: ")
    array1 = [1,5,9,7,88,6,3,4,7,9,3,4,7,88,9,6,33,5,852,65,85,66,87,0]
    print(array1)
    print("Array Ordanado por InsertionSort: ")
    print(InsertionSort(array1))

if __name__ == "__main__":
    main()