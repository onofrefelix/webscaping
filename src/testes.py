from random import randint

def gera6numeros(qte=10,menorvalor=125,maiorvalor=155):

    total = 0
    apostas = list()
    while total<qte:

        aposta = [randint(1, 48) for i in range(6)]
        apostaset = set(aposta)
        if len(apostaset) == 6 and menorvalor < sum(aposta) < maiorvalor:
            aposta2 = aposta.sort()
            apostas.append(aposta)
            total = len(apostas)

    return apostas

a = gera6numeros()

print(a)