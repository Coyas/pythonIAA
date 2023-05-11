"""
O algoritmo de ordenação por seleção, ou selection sort, é um algoritmo simples de 
ordenação que divide a lista em duas partes: uma parte ordenada e outra parte não ordenada.
 O algoritmo procura o menor (ou maior) elemento na parte não ordenada e o coloca na posição 
 correta na parte ordenada. Esse processo é repetido até que toda a lista esteja ordenada.

Aqui está uma explicação passo a passo do algoritmo de selection sort:

1. Inicialmente, consideramos toda a lista como a parte não ordenada.

2. Para cada iteração do algoritmo, encontramos o menor (ou maior) elemento na parte não ordenada.

3. Percorremos a parte não ordenada para encontrar o menor (ou maior) elemento.

4. Trocamos o menor (ou maior) elemento encontrado com o primeiro elemento da parte não ordenada.

5. Agora, o primeiro elemento da lista está na posição correta, tornando-se parte da parte ordenada.

Repetimos os passos 2 a 5 para a parte não ordenada restante, até que toda a lista esteja ordenada.

O selection sort tem uma complexidade de tempo de O(n^2), onde 'n' é o número de elementos a serem ordenados.
 Isso ocorre porque em cada iteração ele percorre a parte não ordenada para encontrar o menor (ou maior) elemento,
   resultando em uma comparação adicional para cada elemento.

Embora o selection sort não seja tão eficiente quanto outros algoritmos de ordenação, como o merge sort ou o quick 
sort, ele é fácil de implementar e pode ser útil para ordenar pequenos conjuntos de dados ou quando o uso de memória 
é uma preocupação.

Em resumo, o selection sort é um algoritmo de ordenação que seleciona o menor (ou maior) elemento da parte não ordenada 
e o coloca na posição correta na parte ordenada. Esse processo é repetido até que toda a lista esteja ordenada.
"""

def SelectionSort(array):
    
    for i in range(len(array)):
        menor_elemento = i
        for j in range(i+1, len(array)):
            if array[menor_elemento] > array[j]:
                menor_elemento = j
        
       
        # array[i] = array[menor_elemento] # isso nao funciona
        # array[menor_elemento] = array[i] # porque vai substituir o valor original de maneira errada
        
        array[i], array[menor_elemento] = array[menor_elemento], array[i]
        

    return array


def main():
    print('SelectionSort Algoritmo')
    print("Array Inicial: ")
    array1 = [1,5,9,7,88,6,3,4,7,9,3,4,7,88,9,6,33,5,852,65,85,66,87,0]
    print(array1)
    print("Array Ordanado por SelectionSort: ")
    print(SelectionSort(array1))

if __name__ == "__main__":
    main()