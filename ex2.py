from datetime import date

def getIdade(dataNascimento):
    atual = date.today()
    age = atual.year - dataNascimento.year - ((atual.month, atual.day) < (dataNascimento.month, dataNascimento.day)) 
  
    return age 

def ShowIdade():
    dia = int(input('Qual o dia: '))
    mes = int(input('Qual o mes: '))
    ano = int(input('Qual o ano: '))

    print("A sua idade é: ")

    print(getIdade(date(ano, mes, dia)), "years")


def multiplos():
    p = int(input('Entre o valor de P: '))
    n = int(input('Entre o valor de N: '))

    if n >= 0 and p <= 0 :
        print("Os valores tem d ser positivios")
        return


    print('Multuplos de ', p)
    i = 0
    while i <= n :
        b =  p * i
        print('M%d: %d'% (i, b))
        i += 1
        
matzA = [
    [10,2,4,9],
    [-8,6,7,10]
]

matzB = [
    [50,30,4],
    [10,7,8],
    [5,6,7],
    [12,9,14],
]

def makeQuadrada(matzA, maxDim):
    while len(matzA) < maxDim:
        
        if len(matzA) < maxDim:
            print('matriz n é quadrada (linha)')
         
            #Isto é para testar linhas da matriz
           # se uma linha é de dimençao inferior a dimençao global,  a matriz sera ajustada
          
            addLinhas = maxDim - len(matzA)
            #print(len(matzA))
            print('add linhas+: ' ,addLinhas)
            matzA.append([0,0,0,0])
        else:
            print('matriz é quadrada (linha)')
            
    while  len(matzA[0]) < maxDim: 
        if len(matzA[0]) < maxDim:
            print('matriz n é quadrada (coluna)')
            '''
            Isto é para testar colunas da matriz
            se uma colunas é de dimençao inferior a dimençao global,  a matriz sera ajustada
            '''
            addColunas = maxDim - len(matzA[0])
            #print(len(matzA[0]))
            #print('add coluna +: ' ,addColunas)
            #print('range(mat): ', range(len(matzA[0])))
            for i in range(len(matzA[0])+1):
                matzA[i].extend([0])
        else:
            print('matriz é quadrada (coluna)')

    return matzA
    

def somaMatriz(matzA, matzB):
    # Para saber a dimensao das colunas, len([0]), dimencao da primeira linha
    # e para as linhas  len([])
    maxDimArr = [] # dimencoes dos arrays
    maxDimArr.append(len(matzA))
    maxDimArr.append(len(matzA[0]))
    maxDimArr.append(len(matzB))
    maxDimArr.append(len(matzB[0]))
    maxDim = max(maxDimArr)

    print('maxDIm: ', maxDimArr)
    print('MatA: ', makeQuadrada(matzA, maxDim))
    A = makeQuadrada(matzA, maxDim)
    print('MatB: ', makeQuadrada(matzB, maxDim))
    B = makeQuadrada(matzB, maxDim)

    # C = A + B
    
        
'''
    for i in range(len(matzA)) : 
        for j in range(len(matzA[i])) : 
            print(matzA[i][j], end=" ")
            
        print() 
''' 
    

def main():
    # ShowIdade()
    # multiplos()
    #print(matzA)
    #print(matzB)
    print('=======================')
    somaMatriz(matzA, matzB)
    
if __name__ == "__main__":
    main()