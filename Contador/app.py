import time

def contador_infinito():
    contador = 0
    while True:
        print(contador, end="\r")
        time.sleep(1)  # Pausa de 1 segundo
        contador += 1

# Chamada do contador infinito
contador_infinito()
