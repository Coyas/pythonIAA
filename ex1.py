import random

def number_pnp(n,p):
    while n >= 0 and n >= p and p > 0 :
        print(p)
        p = p + p

def aleatorio(n):
    print(random.randint(0,n))

def List_of_random(n):
    Lista = []
    inc = 0
    while inc <= n:
        Lista.append(random.randint(0,n))
        inc +=  1

   # print(Lista)
    return Lista

def menor_numero(Lista):
    print(min(Lista))

def maior_numero(Lista):
    print(max(Lista))

def pares(Lista):
    #print(max(Lista))
    pares = []
    for n in Lista:
        if n % 2 == 0:
            pares.append(n)
    print(pares)

def impars(Lista):
    #print(max(Lista))
    impars = []
    for n in Lista:
        if n % 2 != 0:
            impars.append(n)
    print(impars)

def max_div_comun(n, p):
    while(p != 0):
        resto = n % p
        n = p
        p = resto

    print(n)



def main():
    n = int(input("Entre N:"))
    p = int(input("Entre P:"))

    print('Um numero aleatorio usando N como seed')
    aleatorio(n)
    print('contagem de P em P até N')
    number_pnp(n,p)
    print('Uma Lista de Numeros areatorios tendo N como limite')
    a = List_of_random(n)
    print(a)
    print('menor numero na lista de numeros')
    menor_numero(a)      
    print('maior numero na lista de numeros')
    maior_numero(a)     
    print('todos os numero pares na lista de numeros')   
    pares(a)        
    print('todos os numero impares na lista de numeros')   
    impars(a)
    print('maximo divisor comun n & p')
    max_div_comun(n, p)
        
    
if __name__ == "__main__":
    main()