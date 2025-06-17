"""
O algoritmo de ordenação por bolha, ou bubble sort, é um algoritmo simples e eficiente para ordenar 
uma lista de elementos. Ele compara repetidamente pares de elementos adjacentes e os troca se estiverem
 na ordem errada. Esse processo é repetido até que a lista esteja totalmente ordenada.

Aqui está uma explicação passo a passo do algoritmo de bubble sort:

1. Inicialmente, consideramos toda a lista como não ordenada.

2. Percorremos a lista, comparando elementos adjacentes.

3. Se um elemento for maior (ou menor, dependendo da ordem desejada) que o elemento adjacente, 
eles são trocados de posição.

4. O maior (ou menor) elemento "borbulha" para o final da lista.

5. Repetimos os passos 2 a 4 até que não ocorram mais trocas durante uma passagem completa pela lista.

6. A lista está totalmente ordenada quando não houver mais trocas durante uma passagem completa.

O nome "bubble sort" vem da ideia de que os elementos maiores (ou menores) vão "borbulhando" para o final
 da lista à medida que as trocas são feitas.

O bubble sort tem uma complexidade de tempo de O(n^2), onde 'n' é o número de elementos a serem ordenados. 
Isso ocorre porque em cada iteração ele percorre a lista e faz comparações e trocas. No pior caso, onde a lista 
está inversamente ordenada, o bubble sort requer um número quadrático de comparações e trocas.

Apesar de sua simplicidade, o bubble sort não é tão eficiente quanto outros algoritmos de ordenação, como o merge 
sort ou o quick sort. No entanto, pode ser útil em casos de listas pequenas ou quando a lista já está parcialmente ordenada.

Em resumo, o bubble sort é um algoritmo de ordenação que compara pares de elementos adjacentes e os troca se estiverem 
na ordem errada. Ele repete esse processo até que a lista esteja totalmente ordenada.
"""

def BubbleSort(array):
    
    for i in range(len(array)):
        
        for j in range(i+1, len(array) - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j+1] = array[j+1], array[j]
        

    return array


def main():
    print('SelectionSort Algoritmo')
    print("Array Inicial: ")
    array1 = [1,5,9,7,88,6,3,4,7,9,3,4,7,88,9,6,33,5,852,65,85,66,87,0]
    print(array1)
    print("Array Ordanado por SelectionSort: ")
    print(BubbleSort(array1))

if __name__ == "__main__":
    main()